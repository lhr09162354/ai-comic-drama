"""角色参考图管理 - 生成并缓存角色设定图，提升画面一致性"""

import os
import hashlib
import json
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import config

# 角色设定图prompt模板
CHARACTER_SHEET_PROMPT = """Character reference sheet, {style_prompt}.
Full body front view of a character: {description}.
Clean white background, multiple views: front view, 3/4 view, side view.
Character design sheet, consistent appearance, detailed features.
No text, no watermark, professional character reference illustration."""

# 角色特写prompt（用于对话场景）
CHARACTER_PORTRAIT_PROMPT = """{style_prompt}.
Close-up portrait of {name}: {description}.
{emotion} expression, detailed face, consistent with character design.
Clean composition, professional manga illustration."""

# 角色全身prompt
CHARACTER_FULLBODY_PROMPT = """{style_prompt}.
Full body view of {name}: {description}.
{pose} pose, {emotion} expression, dynamic stance.
Consistent with character design, professional manga illustration."""

def _get_cache_dir(project_name: str) -> str:
    """获取角色参考图缓存目录"""
    cache_dir = os.path.join(config.OUTPUT_DIR, project_name, "characters")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def _get_character_hash(name: str, description: str) -> str:
    """根据角色信息生成唯一hash，用于缓存判断"""
    content = f"{name}:{description}"
    return hashlib.md5(content.encode()).hexdigest()[:12]

def _load_character_cache(cache_dir: str) -> dict:
    """加载角色缓存索引"""
    index_path = os.path.join(cache_dir, "_index.json")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_character_cache(cache_dir: str, cache: dict):
    """保存角色缓存索引"""
    index_path = os.path.join(cache_dir, "_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def generate_character_sheet(character: dict, style_key: str, project_name: str,
                             force_regenerate: bool = False) -> dict:
    """
    为角色生成参考设定图，返回 {name, sheet_path, hash}
    支持缓存，相同描述不会重复生成
    """
    name = character["name"]
    description = character["visual_description"]
    style_prompt = config.STYLE_PROMPTS.get(style_key, config.STYLE_PROMPTS["manga"])
    
    cache_dir = _get_cache_dir(project_name)
    cache = _load_character_cache(cache_dir)
    char_hash = _get_character_hash(name, description)
    
    # 检查缓存
    if not force_regenerate and name in cache and cache[name].get("hash") == char_hash:
        sheet_path = cache[name].get("sheet_path")
        if sheet_path and os.path.exists(sheet_path):
            return cache[name]
    
    # 生成角色设定图
    prompt = CHARACTER_SHEET_PROMPT.format(
        style_prompt=style_prompt,
        description=description
    )
    
    sheet_path = _call_image_api(prompt, name, cache_dir, suffix="sheet")
    
    result = {
        "name": name,
        "sheet_path": sheet_path,
        "hash": char_hash,
        "visual_description": description,
    }
    
    # 更新缓存
    cache[name] = result
    _save_character_cache(cache_dir, cache)
    
    return result

def build_consistent_prompt(panel: dict, characters: list, character_sheets: dict,
                            style_key: str = "manga") -> str:
    """
    构建带角色一致性信息的生图prompt
    character_sheets: {name: {sheet_path, visual_description, ...}}
    """
    style_prompt = config.STYLE_PROMPTS.get(style_key, config.STYLE_PROMPTS["manga"])
    
    parts = [style_prompt + ","]
    
    # 镜头角度
    camera = panel.get("camera_angle", "")
    camera_map = {
        "特写": "extreme close-up shot",
        "近景": "close-up shot",
        "中景": "medium shot",
        "远景": "wide shot",
        "俯视": "high angle shot looking down",
        "仰视": "low angle shot looking up",
        "鸟瞰": "bird's eye view",
        "过肩": "over-the-shoulder shot",
    }
    if camera in camera_map:
        parts.append(camera_map[camera] + ",")
    elif camera:
        parts.append(camera + " shot,")
    
    # 角色描述（带一致性标记）
    chars_in_scene = panel.get("characters_in_scene", [])
    for char_name in chars_in_scene:
        sheet_info = character_sheets.get(char_name)
        if sheet_info:
            parts.append(f"character '{char_name}': {sheet_info['visual_description']},")
        else:
            # 从剧本角色列表查找
            for c in characters:
                if c["name"] == char_name:
                    parts.append(f"character '{char_name}': {c['visual_description']},")
                    break
    
    # 场景描述
    parts.append(panel.get("scene_description", "") + ",")
    
    # 情绪氛围
    emotion = panel.get("emotion", "")
    emotion_map = {
        "紧张": "tense atmosphere, dramatic lighting",
        "温馨": "warm atmosphere, soft lighting, cozy mood",
        "搞笑": "comedic atmosphere, exaggerated expressions, funny",
        "悲伤": "melancholic atmosphere, dim lighting, somber mood",
        "愤怒": "intense atmosphere, harsh lighting, fierce",
        "惊讶": "surprised atmosphere, dynamic composition",
        "恐怖": "horror atmosphere, dark shadows, eerie lighting",
        "浪漫": "romantic atmosphere, soft glow, dreamy",
    }
    if emotion in emotion_map:
        parts.append(emotion_map[emotion] + ",")
    
    # 质量标记
    parts.append("high quality, detailed, masterpiece, best quality")
    
    # 负面提示
    negative = "bad anatomy, deformed, blurry, low quality, watermark, text, signature"
    
    prompt = " ".join(p for p in parts if p)
    return prompt.strip(), negative

def _call_image_api(prompt: str, name: str, output_dir: str, suffix: str = "img") -> str:
    """调用图像API生成图片"""
    if config.IMAGE_BACKEND == "dalle":
        api_key = config.DALLE_API_KEY or config.LLM_API_KEY
        client = OpenAI(api_key=api_key, base_url=config.LLM_BASE_URL)
        response = client.images.generate(
            model=config.DALLE_MODEL,
            prompt=prompt,
            size=config.DALLE_SIZE,
            quality=config.DALLE_QUALITY,
            n=1,
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url, timeout=60).content
        image = Image.open(io.BytesIO(img_data))
        
    elif config.IMAGE_BACKEND == "siliconflow":
        api_key = config.SILICONFLOW_API_KEY
        if not api_key:
            raise ValueError("请设置 SILICONFLOW_API_KEY")
        response = requests.post(
            "https://api.siliconflow.cn/v1/images/generations",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": config.SILICONFLOW_MODEL,
                "prompt": prompt,
                "image_size": "1024x1024",
                "num_inference_steps": 25,
            },
            timeout=120,
        )
        if response.status_code != 200:
            raise RuntimeError(f"SiliconFlow API 错误: {response.text}")
        data = response.json()
        image_url = data["images"][0]["url"]
        img_data = requests.get(image_url, timeout=60).content
        image = Image.open(io.BytesIO(img_data))
        
    elif config.IMAGE_BACKEND == "stability":
        api_key = config.STABILITY_API_KEY
        if not api_key:
            raise ValueError("请设置 STABILITY_API_KEY")
        import base64
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            json={
                "text_prompts": [{"text": prompt, "weight": 1}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
            timeout=120,
        )
        if response.status_code != 200:
            raise RuntimeError(f"Stability API 错误: {response.text}")
        data = response.json()
        img_bytes = base64.b64decode(data["artifacts"][0]["base64"])
        image = Image.open(io.BytesIO(img_bytes))
    else:
        raise ValueError(f"不支持的图像后端: {config.IMAGE_BACKEND}")
    
    # 安全文件名
    safe_name = "".join(c for c in name if c.isalnum() or c in "_-") or "unnamed"
    path = os.path.join(output_dir, f"{safe_name}_{suffix}.png")
    image.save(path, "PNG")
    return path

def generate_all_character_sheets(characters: list, style_key: str,
                                   project_name: str) -> dict:
    """为所有角色批量生成参考设定图，返回 {name: sheet_info}"""
    sheets = {}
    for char in characters:
        try:
            sheet = generate_character_sheet(char, style_key, project_name)
            sheets[char["name"]] = sheet
        except Exception as e:
            # 单个角色生成失败不影响其他
            sheets[char["name"]] = {
                "name": char["name"],
                "sheet_path": None,
                "hash": "",
                "visual_description": char["visual_description"],
                "error": str(e),
            }
    return sheets
