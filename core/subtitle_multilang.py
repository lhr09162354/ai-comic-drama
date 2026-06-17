"""
AI Comic Drama Generator v15 - 多语言字幕模块
支持15种语言的字幕生成和翻译
"""

import streamlit as st
import json
from typing import List, Dict, Optional
from datetime import datetime
import hashlib

class MultiLanguageSubtitle:
    """多语言字幕引擎"""
    
    SUPPORTED_LANGUAGES = {
        "zh-CN": {"name": "简体中文", "native": "简体中文", "tts_voice": "zh-CN-Female", "rtl": False},
        "zh-TW": {"name": "繁體中文", "native": "繁體中文", "tts_voice": "zh-TW-Female", "rtl": False},
        "en": {"name": "英语", "native": "English", "tts_voice": "en-US-Female", "rtl": False},
        "ja": {"name": "日语", "native": "日本語", "tts_voice": "ja-JP-Female", "rtl": False},
        "ko": {"name": "韩语", "native": "한국어", "tts_voice": "ko-KR-Female", "rtl": False},
        "es": {"name": "西班牙语", "native": "Español", "tts_voice": "es-ES-Female", "rtl": False},
        "fr": {"name": "法语", "native": "Français", "tts_voice": "fr-FR-Female", "rtl": False},
        "de": {"name": "德语", "native": "Deutsch", "tts_voice": "de-DE-Female", "rtl": False},
        "pt": {"name": "葡萄牙语", "native": "Português", "tts_voice": "pt-BR-Female", "rtl": False},
        "ru": {"name": "俄语", "native": "Русский", "tts_voice": "ru-RU-Female", "rtl": True},
        "ar": {"name": "阿拉伯语", "native": "العربية", "tts_voice": "ar-SA-Female", "rtl": True},
        "hi": {"name": "印地语", "native": "हिन्दी", "tts_voice": "hi-IN-Female", "rtl": False},
        "vi": {"name": "越南语", "native": "Tiếng Việt", "tts_voice": "vi-VN-Female", "rtl": False},
        "th": {"name": "泰语", "native": "ไทย", "tts_voice": "th-TH-Female", "rtl": False},
        "id": {"name": "印尼语", "native": "Bahasa Indonesia", "tts_voice": "id-ID-Female", "rtl": False},
    }
    
    def __init__(self):
        self.cache = {}  # 翻译缓存
    
    def translate_text(
        self,
        text: str,
        source_lang: str = "zh-CN",
        target_lang: str = "en",
        use_cache: bool = True
    ) -> str:
        """
        翻译文本
        
        Args:
            text: 源文本
            source_lang: 源语言
            target_lang: 目标语言
            use_cache: 是否使用缓存
        
        Returns:
            翻译后的文本
        """
        if source_lang == target_lang:
            return text
        
        # 检查缓存
        if use_cache:
            cache_key = self._get_cache_key(text, source_lang, target_lang)
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        # 模拟翻译（实际应用中调用翻译API）
        translated = self._mock_translate(text, source_lang, target_lang)
        
        # 缓存结果
        if use_cache:
            self.cache[cache_key] = translated
        
        return translated
    
    def _mock_translate(self, text: str, source: str, target: str) -> str:
        """模拟翻译（实际应用中替换为真实翻译API）"""
        # 这里返回原文本，实际使用需要接入翻译API（如Google Translate、DeepL等）
        return text
    
    def batch_translate(
        self,
        texts: List[str],
        source_lang: str = "zh-CN",
        target_lang: str = "en"
    ) -> List[str]:
        """批量翻译"""
        return [
            self.translate_text(text, source_lang, target_lang)
            for text in texts
        ]
    
    def _get_cache_key(self, text: str, source: str, target: str) -> str:
        """生成缓存键"""
        return hashlib.md5(f"{text}_{source}_{target}".encode()).hexdigest()

class SubtitleGenerator:
    """字幕生成器"""
    
    def __init__(self):
        self.multi_lang = MultiLanguageSubtitle()
    
    def generate_subtitles(
        self,
        dialogues: List[Dict],
        language: str = "zh-CN",
        style: Dict = None
    ) -> List[Dict]:
        """
        生成字幕数据
        
        Args:
            dialogues: 对话列表 [{start, end, text, speaker}]
            language: 字幕语言
            style: 字幕样式配置
        
        Returns:
            字幕数据列表
        """
        if style is None:
            style = self._get_default_style(language)
        
        subtitles = []
        
        for i, dialogue in enumerate(dialogues):
            # 翻译文本
            text = dialogue.get("text", "")
            if language != "zh-CN":
                text = self.multi_lang.translate_text(text, "zh-CN", language)
            
            # 处理文本长度（自动换行）
            wrapped_text = self._wrap_text(text, style.get("max_chars_per_line", 20))
            
            subtitle = {
                "id": i,
                "start": dialogue.get("start", 0),
                "end": dialogue.get("end", 3),
                "text": text,
                "wrapped_text": wrapped_text,
                "speaker": dialogue.get("speaker", ""),
                "style": style,
                "language": language,
            }
            
            subtitles.append(subtitle)
        
        return subtitles
    
    def _wrap_text(self, text: str, max_chars: int = 20) -> str:
        """文本自动换行"""
        if len(text) <= max_chars:
            return text
        
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)
    
    def _get_default_style(self, language: str) -> Dict:
        """获取默认字幕样式"""
        is_rtl = self.multi_lang.SUPPORTED_LANGUAGES.get(language, {}).get("rtl", False)
        
        return {
            "font_family": "Noto Sans SC" if language.startswith("zh") else "Noto Sans",
            "font_size": 32,
            "color": "#FFFFFF",
            "outline_color": "#000000",
            "outline_width": 2,
            "background_color": "rgba(0, 0, 0, 0.5)",
            "position": "bottom",
            "margin_bottom": 60,
            "rtl": is_rtl,
            "text_align": "center" if not is_rtl else "center",
        }
    
    def export_srt(self, subtitles: List[Dict]) -> str:
        """导出SRT格式字幕"""
        srt_content = []
        
        for i, sub in enumerate(subtitles, 1):
            start = self._format_srt_time(sub["start"])
            end = self._format_srt_time(sub["end"])
            
            srt_content.append(f"{i}")
            srt_content.append(f"{start} --> {end}")
            srt_content.append(sub["wrapped_text"])
            srt_content.append("")
        
        return "\n".join(srt_content)
    
    def export_ass(self, subtitles: List[Dict]) -> str:
        """导出ASS格式字幕（支持更多样式）"""
        ass_header = """[Script Info]
Title: AI Comic Drama
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},28,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
""".format(font="Noto Sans SC")
        
        events = ["\n[Events]", "Format: Layer, Start, End, Style, Text"]
        
        for sub in subtitles:
            start = self._format_ass_time(sub["start"])
            end = self._format_ass_time(sub["end"])
            text = sub["wrapped_text"].replace("\n", "\\N")
            
            events.append(f"Dialogue: 0,{start},{end},Default,{text}")
        
        return ass_header + "\n".join(events)
    
    def _format_srt_time(self, seconds: float) -> str:
        """格式化SRT时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _format_ass_time(self, seconds: float) -> str:
        """格式化ASS时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centisecs = int((seconds % 1) * 100)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

class SubtitleRenderer:
    """字幕渲染器"""
    
    def __init__(self):
        self.subtitle_generator = SubtitleGenerator()
    
    def render_subtitle_overlay(
        self,
        frame: "Image.Image",
        subtitle: Dict,
        device: str = "mobile"
    ) -> "Image.Image":
        """
        在帧上渲染字幕
        
        Args:
            frame: 原始帧图像
            subtitle: 字幕数据
            device: 设备类型 (mobile/tablet/desktop)
        
        Returns:
            带字幕的图像
        """
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建可绘制对象
        img = frame.copy()
        draw = ImageDraw.Draw(img)
        
        style = subtitle.get("style", {})
        
        # 根据设备调整字号
        base_size = style.get("font_size", 32)
        if device == "mobile":
            size = int(base_size * 0.75)
        elif device == "tablet":
            size = int(base_size * 0.9)
        else:
            size = base_size
        
        # 加载字体
        try:
            font = ImageFont.truetype("NotoSansSC-Regular.ttf", size)
        except:
            font = ImageFont.load_default()
        
        # 计算字幕位置
        text = subtitle.get("wrapped_text", "")
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 位置设置
        margin_bottom = style.get("margin_bottom", 60)
        x = (img.width - text_width) // 2
        y = img.height - text_height - margin_bottom
        
        # 绘制背景
        padding = 10
        bg_box = [
            x - padding, y - padding,
            x + text_width + padding, y + text_height + padding
        ]
        bg_color = style.get("background_color", "rgba(0, 0, 0, 0.5)")
        draw.rectangle(bg_box, fill=self._parse_color(bg_color))
        
        # 绘制描边
        outline_color = style.get("outline_color", "#000000")
        outline_width = style.get("outline_width", 2)
        
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # 绘制主文字
        main_color = style.get("color", "#FFFFFF")
        draw.text((x, y), text, font=font, fill=self._parse_color(main_color))
        
        return img
    
    def _parse_color(self, color_str: str) -> tuple:
        """解析颜色字符串"""
        if color_str.startswith("rgba"):
            # rgba(r, g, b, a)
            import re
            match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", color_str)
            if match:
                return tuple(int(x) for x in match.groups())
        elif color_str.startswith("#"):
            # #RRGGBB
            hex_color = color_str[1:]
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        
        return (255, 255, 255)  # 默认白色
    
    def render_batch_subtitles(
        self,
        frames: List["Image.Image"],
        subtitles: List[Dict],
        device: str = "mobile"
    ) -> List["Image.Image"]:
        """批量渲染字幕"""
        rendered = []
        
        for i, frame in enumerate(frames):
            # 找到对应时间的字幕
            frame_time = i / 24  # 假设24fps
            
            current_subtitle = None
            for sub in subtitles:
                if sub["start"] <= frame_time <= sub["end"]:
                    current_subtitle = sub
                    break
            
            if current_subtitle:
                frame = self.render_subtitle_overlay(frame, current_subtitle, device)
            
            rendered.append(frame)
        
        return rendered

class TTSMultilang:
    """多语言TTS配音"""
    
    VOICE_MAP = {
        "zh-CN": {
            "female": "zh-CN-XiaoxiaoNeural",
            "male": "zh-CN-YunxiNeural",
        },
        "zh-TW": {
            "female": "zh-TW-HsiaoChenNeural",
            "male": "zh-TW-YunJheNeural",
        },
        "en": {
            "female": "en-US-JennyNeural",
            "male": "en-US-GuyNeural",
        },
        "ja": {
            "female": "ja-JP-NanamiNeural",
            "male": "ja-JP-KeitaNeural",
        },
        "ko": {
            "female": "ko-KR-SunhiNeural",
            "male": "ko-KR-InJoonNeural",
        },
        "es": {
            "female": "es-ES-ElviraNeural",
            "male": "es-ES-AlvaroNeural",
        },
        "fr": {
            "female": "fr-FR-DeniseNeural",
            "male": "fr-FR-HenriNeural",
        },
        "de": {
            "female": "de-DE-KatjaNeural",
            "male": "de-DE-ConradNeural",
        },
    }
    
    def __init__(self):
        self.cache = {}
    
    def get_voice_id(self, language: str, gender: str = "female") -> str:
        """获取语音ID"""
        lang_voices = self.VOICE_MAP.get(language, self.VOICE_MAP["en"])
        return lang_voices.get(gender, lang_voices["female"])
    
    def generate_speech(
        self,
        text: str,
        language: str = "zh-CN",
        gender: str = "female",
        speed: float = 1.0,
        pitch: float = 1.0
    ) -> bytes:
        """
        生成语音
        
        Args:
            text: 文本内容
            language: 语言
            gender: 性别
            speed: 语速 (0.5-2.0)
            pitch: 音调 (0.5-2.0)
        
        Returns:
            音频数据（bytes）
        """
        voice_id = self.get_voice_id(language, gender)
        
        # 模拟TTS（实际应用中调用Azure TTS或其他TTS API）
        # 这里返回空字节，实际使用需要接入真实API
        return b""

class SubtitleManager:
    """字幕管理器"""
    
    def __init__(self):
        self.multi_lang = MultiLanguageSubtitle()
        self.generator = SubtitleGenerator()
        self.renderer = SubtitleRenderer()
        self.tts = TTSMultilang()
        self.project_subtitles = {}
    
    def create_project_subtitles(
        self,
        project_id: str,
        dialogues: List[Dict],
        languages: List[str],
        default_lang: str = "zh-CN"
    ) -> Dict[str, List[Dict]]:
        """
        为项目创建多语言字幕
        
        Args:
            project_id: 项目ID
            dialogues: 对话列表
            languages: 目标语言列表
            default_lang: 默认语言
        
        Returns:
            {语言: 字幕数据列表}
        """
        all_subtitles = {}
        
        for lang in languages:
            subtitles = self.generator.generate_subtitles(
                dialogues,
                language=lang
            )
            all_subtitles[lang] = subtitles
        
        # 存储到项目
        self.project_subtitles[project_id] = {
            "languages": all_subtitles,
            "default": default_lang,
            "created_at": datetime.now().isoformat(),
        }
        
        return all_subtitles
    
    def export_subtitles(
        self,
        project_id: str,
        language: str,
        format: str = "srt"
    ) -> str:
        """导出字幕文件"""
        if project_id not in self.project_subtitles:
            return ""
        
        subtitles = self.project_subtitles[project_id]["languages"].get(language, [])
        
        if format == "srt":
            return self.generator.export_srt(subtitles)
        elif format == "ass":
            return self.generator.export_ass(subtitles)
        
        return ""

def render_subtitle_settings_ui():
    """渲染字幕设置UI"""
    st.subheader("📝 多语言字幕设置")
    
    # 语言选择
    lang_options = MultiLanguageSubtitle.SUPPORTED_LANGUAGES
    lang_choice = st.selectbox(
        "选择字幕语言",
        options=list(lang_options.keys()),
        format_func=lambda x: f"{lang_options[x]['native']} ({lang_options[x]['name']})"
    )
    
    # 字幕预览
    st.info(f"**当前语言:** {lang_options[lang_choice]['name']}")
    
    # 多语言同时生成
    with st.expander("🌐 同时生成多种语言"):
        all_langs = st.multiselect(
            "选择要生成的语种",
            options=list(lang_options.keys()),
            default=["zh-CN", "en", "ja"],
            format_func=lambda x: lang_options[x]["native"]
        )
        
        st.write(f"将生成 {len(all_langs)} 种语言字幕")
    
    # 字幕样式
    with st.expander("🎨 字幕样式"):
        col1, col2 = st.columns(2)
        
        with col1:
            font_size = st.slider("字体大小", 16, 48, 32)
            outline_width = st.slider("描边宽度", 0, 5, 2)
        
        with col2:
            bg_opacity = st.slider("背景透明度", 0, 100, 50)
            margin_bottom = st.slider("底部边距", 20, 100, 60)
    
    # TTS配音设置
    with st.expander("🎙️ TTS配音设置"):
        use_tts = st.checkbox("启用语音配音")
        
        if use_tts:
            voice_gender = st.radio("配音音色", ["female", "male"], format_func=lambda x: "女声" if x == "female" else "男声")
            speech_speed = st.slider("语速", 0.5, 2.0, 1.0)
            speech_pitch = st.slider("音调", 0.5, 2.0, 1.0)
    
    # 导出格式
    export_format = st.selectbox(
        "导出格式",
        options=["srt", "ass", "vtt"],
        format_func=lambda x: {"srt": "SRT（通用）", "ass": "ASS（高级）", "vtt": "VTT（Web）"}[x]
    )
    
    return {
        "language": lang_choice,
        "languages": all_langs if 'all_langs' in dir() else ["zh-CN", "en", "ja"],
        "font_size": font_size if 'font_size' in dir() else 32,
        "outline_width": outline_width if 'outline_width' in dir() else 2,
        "bg_opacity": bg_opacity if 'bg_opacity' in dir() else 50,
        "margin_bottom": margin_bottom if 'margin_bottom' in dir() else 60,
        "use_tts": use_tts if 'use_tts' in dir() else False,
        "voice_gender": voice_gender if 'voice_gender' in dir() else "female",
        "speech_speed": speech_speed if 'speech_speed' in dir() else 1.0,
        "export_format": export_format,
    }
