"""Demo模式 - 无API Key也能体验完整流程"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

# 颜色主题（用于生成彩色占位图）
COLOR_THEMES = {
    "热血冒险": ["#FF6B35", "#FF4444", "#FFD700", "#FF8C00"],
    "恋爱日常": ["#FFB6C1", "#FF69B4", "#FFC0CB", "#FF1493"],
    "悬疑推理": ["#4A4A4A", "#2F4F4F", "#708090", "#363636"],
    "奇幻魔法": ["#9370DB", "#7B68EE", "#6A5ACD", "#8A2BE2"],
    "科幻未来": ["#00CED1", "#00BFFF", "#1E90FF", "#4169E1"],
    "恐怖惊悚": ["#2C2C2C", "#8B0000", "#4A0E0E", "#1C1C1C"],
    "搞笑日常": ["#FFD700", "#FF6347", "#32CD32", "#FF8C00"],
    "古风仙侠": ["#DEB887", "#D2691E", "#8B4513", "#F4A460"],
}

# 预设的场景占位文字
SCENE_LABELS = [
    "城市街道", "教室", "森林", "海边", "天空", "废墟",
    "图书馆", "战场", "山巅", "地下室", "神殿", "星空",
]

EMOTION_OVERLAYS = {
    "紧张": ("#FF0000", 30),
    "温馨": ("#FFD700", 20),
    "搞笑": ("#00FF00", 15),
    "悲伤": ("#0000FF", 25),
    "愤怒": ("#FF4500", 30),
    "惊讶": ("#FFFF00", 20),
    "恐怖": ("#800000", 35),
    "浪漫": ("#FF69B4", 20),
}

def generate_demo_panel(panel_index: int, scene_description: str = "",
                        emotion: str = "", genre: str = "热血冒险",
                        width: int = 512, height: int = 512) -> Image.Image:
    """生成Demo占位画面"""
    colors = COLOR_THEMES.get(genre, COLOR_THEMES["热血冒险"])
    base_color = colors[panel_index % len(colors)]
    
    # 基础渐变背景
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    # 渐变效果
    r1, g1, b1 = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
    for y in range(height):
        factor = y / height
        r = int(r1 * (1 - factor * 0.5))
        g = int(g1 * (1 - factor * 0.5))
        b = int(b1 * (1 - factor * 0.5))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 添加情绪色调
    if emotion in EMOTION_OVERLAYS:
        overlay_color, alpha = EMOTION_OVERLAYS[emotion]
        overlay = Image.new("RGB", (width, height), overlay_color)
        img = Image.blend(img, overlay, alpha / 100)
        draw = ImageDraw.Draw(img)
    
    # 装饰性元素 - 简单几何图案
    _draw_decorations(draw, width, height, panel_index)
    
    # 场景文字
    font = _get_demo_font(24)
    small_font = _get_demo_font(16)
    
    # DEMO 标记
    demo_font = _get_demo_font(36)
    draw.text((width // 2, height // 3), "DEMO", font=demo_font,
              fill="#FFFFFF88", anchor="mm")
    
    # 分镜编号
    draw.text((width // 2, height // 2 - 20), f"分镜 {panel_index}",
              font=font, fill="white", anchor="mm")
    
    # 场景描述（截断）
    if scene_description:
        desc = scene_description[:20] + ("..." if len(scene_description) > 20 else "")
        draw.text((width // 2, height // 2 + 20), desc,
                  font=small_font, fill="#FFFFFFCC", anchor="mm")
    
    # 情绪标签
    if emotion:
        draw.text((width // 2, height - 40), f"[{emotion}]",
                  font=small_font, fill="#FFFFFFAA", anchor="mm")
    
    return img

def generate_demo_character_sheet(character_name: str, description: str,
                                   genre: str = "热血冒险") -> Image.Image:
    """生成Demo角色参考图"""
    colors = COLOR_THEMES.get(genre, COLOR_THEMES["热血冒险"])
    base_color = colors[hash(character_name) % len(colors)]
    
    width, height = 512, 512
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    # 渐变背景
    r1, g1, b1 = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
    for y in range(height):
        factor = y / height
        r = int(r1 * (0.7 + factor * 0.3))
        g = int(g1 * (0.7 + factor * 0.3))
        b = int(b1 * (0.7 + factor * 0.3))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 人物轮廓（简笔画风格）
    cx, cy = width // 2, height // 2 + 30
    # 头
    draw.ellipse([cx - 40, cy - 120, cx + 40, cy - 40], outline="white", width=3)
    # 身体
    draw.line([(cx, cy - 40), (cx, cy + 60)], fill="white", width=3)
    # 手臂
    draw.line([(cx - 50, cy - 10), (cx + 50, cy - 10)], fill="white", width=3)
    # 腿
    draw.line([(cx, cy + 60), (cx - 30, cy + 120)], fill="white", width=3)
    draw.line([(cx, cy + 60), (cx + 30, cy + 120)], fill="white", width=3)
    
    # 名字
    font = _get_demo_font(28)
    small_font = _get_demo_font(14)
    draw.text((width // 2, 40), character_name, font=font, fill="white", anchor="mm")
    draw.text((width // 2, 70), "角色参考图 (Demo)", font=small_font, fill="#FFFFFFAA", anchor="mm")
    
    # 描述
    if description:
        lines = _demo_wrap_text(description, small_font, width - 40)
        for i, line in enumerate(lines[:3]):
            draw.text((width // 2, height - 60 + i * 18), line,
                      font=small_font, fill="#FFFFFFBB", anchor="mm")
    
    return img

def generate_demo_cover(title: str, genre: str = "热血冒险") -> Image.Image:
    """生成Demo封面"""
    colors = COLOR_THEMES.get(genre, COLOR_THEMES["热血冒险"])
    
    width, height = 1200, 1600
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    # 深色渐变
    c1, c2 = colors[0], colors[1]
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    for y in range(height):
        f = y / height
        r = int(r1 + (r2 - r1) * f)
        g = int(g1 + (g2 - g1) * f)
        b = int(b1 + (b2 - b1) * f)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 装饰
    _draw_decorations(draw, width, height, hash(title) % 10)
    
    # 标题
    title_font = _get_demo_font(56)
    sub_font = _get_demo_font(24)
    
    draw.text((width // 2 + 3, height // 3 + 3), title, font=title_font,
              fill="#00000066", anchor="mm")
    draw.text((width // 2, height // 3), title, font=title_font,
              fill="white", anchor="mm")
    
    draw.text((width // 2, height // 3 + 70), "AI漫剧自动生成器 DEMO",
              font=sub_font, fill="#FFFFFFAA", anchor="mm")
    
    return img

def _draw_decorations(draw, w, h, seed):
    """绘制装饰性几何图案"""
    rng = random.Random(seed)
    for _ in range(8):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        size = rng.randint(20, 80)
        alpha = rng.randint(20, 50)
        shape = rng.choice(["circle", "rect", "line"])
        if shape == "circle":
            draw.ellipse([x, y, x + size, y + size], outline="#FFFFFF33", width=2)
        elif shape == "rect":
            draw.rectangle([x, y, x + size, y + size // 2], outline="#FFFFFF22", width=1)
        else:
            draw.line([(x, y), (x + size, y + size)], fill="#FFFFFF22", width=1)

def _get_demo_font(size: int) -> ImageFont.FreeTypeFont:
    """获取Demo模式字体"""
    font_candidates = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:\\Windows\\Fonts\\msyh.ttc",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()

def _demo_wrap_text(text: str, font, max_width: int) -> list:
    """文字换行"""
    lines = []
    current = ""
    for char in text:
        test = current + char
        try:
            w = font.getbbox(test)[2] - font.getbbox(test)[0]
        except Exception:
            w = len(test) * 14
        if w > max_width and current:
            lines.append(current)
            current = char
        else:
            current = test
    if current:
        lines.append(current)
    return lines or [text]
