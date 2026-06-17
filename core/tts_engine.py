"""TTS语音配音引擎 - 支持OpenAI TTS和edge-tts"""

import os
import io
import json
import tempfile
import config

def _get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_BASE_URL)

def is_tts_available() -> bool:
    """检查TTS是否可用"""
    if config.LLM_API_KEY:
        return True
    try:
        import edge_tts
        return True
    except ImportError:
        return False

# ============ OpenAI TTS ============

OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# 角色默认音色映射
DEFAULT_VOICE_MAP = {
    "主角": "alloy", "男主角": "echo", "女主角": "nova",
    "侦探": "onyx", "助手": "alloy", "伙伴": "fable",
    "宿敌": "onyx", "师尊": "onyx", "修仙者": "echo",
    "旁白": "shimmer", "narrator": "shimmer",
}

def tts_openai(text: str, voice: str = "alloy", speed: float = 1.0) -> bytes:
    """用OpenAI TTS生成语音，返回mp3字节数据"""
    client = _get_openai_client()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        speed=speed,
    )
    return response.content

# ============ edge-tts (免费) ============

EDGE_TTS_VOICES = {
    "中文女": "zh-CN-XiaoxiaoNeural",
    "中文男": "zh-CN-YunxiNeural",
    "中文温柔女": "zh-CN-XiaoyiNeural",
    "中文沉稳男": "zh-CN-YunjianNeural",
    "日文女": "ja-JP-NanamiNeural",
    "日文男": "ja-JP-KeitaNeural",
    "英文女": "en-US-JennyNeural",
    "英文男": "en-US-GuyNeural",
}

DEFAULT_EDGE_VOICE_MAP = {
    "主角": "中文男", "男主角": "中文男", "女主角": "中文女",
    "侦探": "中文沉稳男", "伙伴": "中文男", "宿敌": "中文沉稳男",
    "旁白": "中文温柔女",
}

async def _edge_tts_generate(text: str, voice_name: str = "中文女") -> bytes:
    """用edge-tts生成语音"""
    import edge_tts
    voice_id = EDGE_TTS_VOICES.get(voice_name, "zh-CN-XiaoxiaoNeural")
    communicate = edge_tts.Communicate(text, voice_id)
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    buf.seek(0)
    return buf.getvalue()

def tts_edge(text: str, voice_name: str = "中文女") -> bytes:
    """edge-tts同步包装"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return loop.run_in_executor(pool, _run_edge_sync, text, voice_name).result()
    except RuntimeError:
        pass
    return asyncio.run(_edge_tts_generate(text, voice_name))

def _run_edge_sync(text, voice_name):
    import asyncio
    return asyncio.run(_edge_tts_generate(text, voice_name))

# ============ 统一接口 ============

def generate_dialogue_audio(
    dialogue: dict,
    character_name: str = "",
    use_edge_tts: bool = False,
    voice_override: str = "",
) -> bytes:
    """为单条对话生成语音"""
    text = dialogue.get("text", "")
    speaker = dialogue.get("speaker", character_name)
    if not text.strip():
        return b""

    if use_edge_tts or not config.LLM_API_KEY:
        voice = voice_override or DEFAULT_EDGE_VOICE_MAP.get(speaker, "中文女")
        return tts_edge(text, voice)
    else:
        voice = voice_override or DEFAULT_VOICE_MAP.get(speaker, "alloy")
        return tts_openai(text, voice)

def generate_page_audio(
    page_data: list,
    character_colors: dict = None,
    use_edge_tts: bool = False,
    progress_callback=None,
) -> list:
    """为一页的所有对话生成语音，返回 [{speaker, text, audio_bytes}]"""
    results = []
    total_dialogues = sum(len(p.get("dialogues", [])) for p in page_data)
    count = 0
    for panel in page_data:
        for dialogue in panel.get("dialogues", []):
            try:
                audio = generate_dialogue_audio(
                    dialogue,
                    use_edge_tts=use_edge_tts,
                )
                results.append({
                    "speaker": dialogue.get("speaker", ""),
                    "text": dialogue.get("text", ""),
                    "audio": audio,
                })
            except Exception as e:
                results.append({
                    "speaker": dialogue.get("speaker", ""),
                    "text": dialogue.get("text", ""),
                    "audio": b"",
                    "error": str(e),
                })
            count += 1
            if progress_callback:
                progress_callback(count, total_dialogues)
    return results

def combine_audio_files(audio_chunks: list, output_path: str, format: str = "mp3") -> str:
    """合并多个音频片段为一个文件"""
    try:
        from pydub import AudioSegment
        combined = AudioSegment.empty()
        for chunk in audio_chunks:
            if chunk:
                seg = AudioSegment.from_mp3(io.BytesIO(chunk))
                combined += seg + AudioSegment.silent(duration=500)  # 间隔0.5秒
        combined.export(output_path, format=format)
        return output_path
    except ImportError:
        # fallback: 直接拼接mp3字节
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in audio_chunks:
                if chunk:
                    f.write(chunk)
        return output_path

def generate_full_audio(
    pages_data: list,
    title: str,
    use_edge_tts: bool = False,
    progress_callback=None,
) -> str:
    """为整部漫画生成完整配音，返回音频文件路径"""
    output_dir = os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{title}_dubbing.mp3")

    all_audio = []
    total_panels = sum(len(p) for p in pages_data)
    count = 0
    for pi, page in enumerate(pages_data):
        for panel in page:
            for dialogue in panel.get("dialogues", []):
                try:
                    audio = generate_dialogue_audio(dialogue, use_edge_tts=use_edge_tts)
                    if audio:
                        all_audio.append(audio)
                except Exception:
                    pass
                count += 1
                if progress_callback:
                    progress_callback(count, total_panels)

    if all_audio:
        combine_audio_files(all_audio, output_path)
    return output_path
