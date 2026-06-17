"""漫画转视频 v11 - 分镜动画·特效增强·漫画效果"""

import os
import io
import math
import random
import tempfile
import config

def is_video_available() -> bool:
    """检查视频生成依赖是否可用"""
    try:
        from PIL import Image
        return True
    except ImportError:
        return False

# ============ v11 核心：漫画特效系统 ============

class ComicEffects:
    """漫画特效 - 将漫画效果转化为视频动画"""
    
    EFFECT_TYPES = {
        # 速度线效果
        "speed_lines": {
            "name": "速度线",
            "description": "表现快速移动或冲击",
            "color": (255, 255, 255),
            "direction": "radial"  # radial / linear
        },
        # 冲击波效果
        "impact": {
            "name": "冲击波",
            "description": "爆炸或冲击的瞬间",
            "color": (255, 200, 50),
            "type": "radial_burst"
        },
        # 闪光效果
        "flash": {
            "name": "闪光",
            "description": "强光闪烁",
            "color": (255, 255, 200),
            "duration": 3  # 帧数
        },
        # 烟雾效果
        "smoke": {
            "name": "烟雾",
            "description": "爆炸或神秘场景",
            "color": (150, 150, 150),
            "opacity": 0.5
        },
        # 震动效果
        "shake": {
            "name": "震动",
            "description": "地震或冲击",
            "amplitude": 8
        },
        # 旋涡效果
        "vortex": {
            "name": "旋涡",
            "description": "能量汇聚或传送",
            "color": (100, 100, 255)
        },
        # 心跳效果
        "heartbeat": {
            "name": "心跳",
            "description": "心动或紧张时刻",
            "scale_range": (1.0, 1.1),
            "color": (255, 100, 100)
        },
        # 回忆效果
        "memory": {
            "name": "回忆",
            "description": "闪回或梦境",
            "sepia": True,
            "blur": True
        }
    }
    
    @classmethod
    def apply_speed_lines(cls, frame, intensity: float = 0.5, direction: str = "center"):
        """应用速度线效果"""
        from PIL import Image, ImageDraw
        w, h = frame.size
        canvas = frame.copy().convert("RGBA")
        
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 生成速度线
        num_lines = int(20 * intensity)
        if direction == "center":
            cx, cy = w // 2, h // 2
            for _ in range(num_lines):
                angle = random.uniform(0, 2 * math.pi)
                length = random.randint(int(h * 0.3), int(h * 0.7))
                start_x = cx + int(random.uniform(-w * 0.3, w * 0.3))
                start_y = cy + int(random.uniform(-h * 0.3, h * 0.3))
                end_x = int(start_x + math.cos(angle) * length)
                end_y = int(start_y + math.sin(angle) * length)
                alpha = int(150 * intensity)
                draw.line([(start_x, start_y), (end_x, end_y)], 
                         fill=(255, 255, 255, alpha), width=2)
        else:
            # 线性速度线（横向）
            for _ in range(num_lines):
                y = random.randint(0, h)
                length = random.randint(int(w * 0.5), int(w * 1.0))
                start_x = random.randint(0, w)
                draw.line([(start_x, y), (start_x + length, y)], 
                         fill=(255, 255, 255, 100), width=1)
        
        return Image.alpha_composite(canvas, overlay)
    
    @classmethod
    def apply_impact(cls, frame, center: tuple = None, intensity: float = 0.7):
        """应用冲击波效果"""
        from PIL import Image, ImageDraw
        w, h = frame.size
        cx, cy = center or (w // 2, h // 2)
        
        canvas = frame.copy().convert("RGBA")
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 冲击波圆环
        max_radius = int(min(w, h) * 0.5 * intensity)
        num_rings = 3
        for i in range(num_rings):
            radius = int(max_radius * (i + 1) / num_rings)
            alpha = int(200 * (1 - i / num_rings) * intensity)
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                        outline=(255, 200, 50, alpha), width=4)
        
        # 辐射线
        num_rays = 12
        for i in range(num_rays):
            angle = 2 * math.pi * i / num_rays
            inner_r = max_radius * 0.8
            outer_r = int(max_radius * 1.2)
            x1 = int(cx + math.cos(angle) * inner_r)
            y1 = int(cy + math.sin(angle) * inner_r)
            x2 = int(cx + math.cos(angle) * outer_r)
            y2 = int(cy + math.sin(angle) * outer_r)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 200, 50, 150), width=2)
        
        return Image.alpha_composite(canvas, overlay)
    
    @classmethod
    def apply_flash(cls, frame, intensity: float = 1.0):
        """应用闪光效果"""
        from PIL import Image
        w, h = frame.size
        alpha = int(255 * intensity)
        flash = Image.new("RGBA", (w, h), (255, 255, 220, alpha))
        return Image.alpha_composite(frame.convert("RGBA"), flash)
    
    @classmethod
    def apply_smoke(cls, frame, intensity: float = 0.5):
        """应用烟雾效果"""
        from PIL import Image, ImageFilter
        w, h = frame.size
        
        # 生成烟雾纹理
        smoke = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        for _ in range(int(10 * intensity)):
            x = random.randint(0, w)
            y = random.randint(h // 2, h)
            size = random.randint(50, 150)
            alpha = int(100 * intensity)
            smoke_circle = Image.new("RGBA", (size, size), (150, 150, 150, alpha))
            smoke_circle = smoke_circle.filter(ImageFilter.GaussianBlur(radius=size // 4))
            smoke.paste(smoke_circle, (x - size // 2, y - size // 2), smoke_circle)
        
        return Image.alpha_composite(frame.convert("RGBA"), smoke)
    
    @classmethod
    def apply_shake(cls, frame, amplitude: int = 8):
        """应用震动效果"""
        from PIL import Image
        w, h = frame.size
        
        offset_x = random.randint(-amplitude, amplitude)
        offset_y = random.randint(-amplitude, amplitude)
        
        canvas = Image.new("RGB", (w, h), (20, 20, 30))
        shifted = frame.crop((max(0, -offset_x), max(0, -offset_y),
                            min(w, w - offset_x), min(h, h - offset_y)))
        canvas.paste(shifted, (max(0, offset_x), max(0, offset_y)))
        
        return canvas
    
    @classmethod
    def apply_heartbeat(cls, frame, progress: float, scale_range: tuple = (1.0, 1.1)):
        """应用心跳效果"""
        from PIL import Image
        w, h = frame.size
        
        # 心跳节奏
        if progress < 0.3:
            scale = scale_range[0]
        elif progress < 0.5:
            scale = scale_range[1]
        elif progress < 0.7:
            scale = scale_range[0]
        elif progress < 0.9:
            scale = scale_range[1]
        else:
            scale = scale_range[0]
        
        # 缩放
        nw, nh = int(w * scale), int(h * scale)
        scaled = frame.resize((nw, nh), Image.LANCZOS)
        
        # 居中裁剪
        x1 = (nw - w) // 2
        y1 = (nh - h) // 2
        result = scaled.crop((x1, y1, x1 + w, y1 + h))
        
        # 添加红心装饰
        if scale > scale_range[0]:
            overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            # 心形效果会在帧上叠加
            pass
        
        return result
    
    @classmethod
    def apply_memory_effect(cls, frame, intensity: float = 0.7):
        """应用回忆/梦境效果"""
        from PIL import Image, ImageEnhance, ImageFilter
        
        # 转灰度
        gray = frame.convert("L").convert("RGB")
        
        # 添加暖色调
        sepia = Image.new("RGB", frame.size, (255, 240, 220))
        result = Image.blend(frame, sepia, intensity * 0.3)
        
        # 轻微模糊
        result = result.filter(ImageFilter.GaussianBlur(radius=intensity * 2))
        
        # 降低对比度
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(1 - intensity * 0.3)
        
        return result
    
    @classmethod
    def get_effect_for_emotion(cls, emotion: str) -> list:
        """根据情感获取适合的特效"""
        emotion_effects = {
            "紧张": ["shake", "speed_lines"],
            "高潮": ["impact", "flash", "speed_lines"],
            "搞笑": ["heartbeat"],  # 心动/搞笑
            "浪漫": ["heartbeat"],
            "悲伤": ["smoke", "memory"],
            "悬疑": ["smoke", "memory"],
            "温馨": [],
            "释然": [],
        }
        return emotion_effects.get(emotion, [])

# ============ v11 核心：分镜微动效系统 ============

class PanelMicroAnimation:
    """分镜微动效 - 让每个分镜有细腻的动画"""
    
    @classmethod
    def add_blink_effect(cls, frame, progress: float, is_eye_close: bool = False):
        """眨眼效果"""
        # 对于人物特写，可以在某些帧添加眨眼
        return frame
    
    @classmethod
    def add_breath_effect(cls, frame, progress: float, strength: float = 0.02):
        """呼吸效果（轻微缩放）"""
        from PIL import Image
        w, h = frame.size
        
        # 轻微的上下浮动
        scale = 1.0 + math.sin(progress * math.pi * 4) * strength
        nw, nh = int(w * scale), int(h * scale)
        scaled = frame.resize((nw, nh), Image.LANCZOS)
        
        x1 = (nw - w) // 2
        y1 = (nh - h) // 2
        return scaled.crop((x1, y1, x1 + w, y1 + h))
    
    @classmethod
    def add_wind_effect(cls, frame, progress: float):
        """风吹效果（轻微晃动）"""
        from PIL import Image
        w, h = frame.size
        
        offset = int(math.sin(progress * math.pi * 6) * 3)
        canvas = Image.new("RGB", (w, h), (20, 20, 30))
        shifted = frame.crop((max(0, offset), 0, min(w, w + offset), h))
        canvas.paste(shifted, (max(0, -offset), 0))
        
        return canvas
    
    @classmethod
    def add_light_flicker(cls, frame, progress: float, intensity: float = 0.3):
        """光线闪烁效果"""
        from PIL import Image
        w, h = frame.size
        
        # 根据进度调整亮度
        flicker = 1.0 - intensity * abs(math.sin(progress * math.pi * 8))
        
        # 简单调光
        import numpy as np
        arr = np.array(frame).astype(float)
        arr = arr * flicker
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        
        return Image.fromarray(arr)

# ============ 动态镜头效果（保留v10功能）===========

def apply_pan_effect(img, direction: str, strength: float = 0.1, frame_progress: float = 0.5):
    """应用镜头平移效果
    Args:
        img: PIL Image
        direction: left / right / up / down / none
        strength: 平移幅度 (0-1)
        frame_progress: 当前帧进度 (0-1)
    """
    from PIL import Image
    w, h = img.size
    
    # 计算当前帧的平移量
    if direction == "none":
        return img.copy()
    
    max_offset = int(min(w, h) * strength * 0.5)
    if direction == "left":
        offset = int(max_offset * (frame_progress * 2 - 1))  # -max 到 0
    elif direction == "right":
        offset = int(max_offset * (1 - frame_progress * 2))  # 0 到 -max
    elif direction == "up":
        offset = int(max_offset * (frame_progress * 2 - 1))
    elif direction == "down":
        offset = int(max_offset * (1 - frame_progress * 2))
    else:
        offset = 0
    
    # 裁剪并填充边缘
    canvas = Image.new("RGB", (w, h), (20, 20, 30))  # 深色边框
    
    if direction in ["left", "right"]:
        x = offset
        crop_box = (max(0, x), 0, min(w, w + x), h)
        cropped = img.crop(crop_box)
        paste_x = w - cropped.width if x < 0 else 0
        canvas.paste(cropped, (paste_x, 0))
    else:
        y = offset
        crop_box = (0, max(0, y), w, min(h, h + y))
        cropped = img.crop(crop_box)
        paste_y = h - cropped.height if y < 0 else 0
        canvas.paste(cropped, (0, paste_y))
    
    return canvas

def apply_zoom_effect(img, zoom_in: bool, frame_progress: float, strength: float = 0.15):
    """应用镜头缩放效果
    Args:
        img: PIL Image
        zoom_in: True=放大, False=缩小
        frame_progress: 当前帧进度 (0-1)
        strength: 缩放幅度 (0-1)
    """
    from PIL import Image
    w, h = img.size
    
    # 计算缩放
    if zoom_in:
        scale = 1.0 + strength * frame_progress
    else:
        scale = 1.0 + strength * (1 - frame_progress)
    
    nw, nh = int(w * scale), int(h * scale)
    # 缩放
    zoomed = img.resize((nw, nh), Image.LANCZOS)
    
    # 居中裁剪回原尺寸
    x1 = (nw - w) // 2
    y1 = (nh - h) // 2
    cropped = zoomed.crop((x1, y1, x1 + w, y1 + h))
    
    return cropped

def apply_tilt_effect(img, direction: str, frame_progress: float, strength: float = 0.02):
    """应用镜头倾斜效果（模拟手持感）
    Args:
        img: PIL Image
        direction: shake / gentle / none
        frame_progress: 当前帧进度 (0-1)
        strength: 倾斜幅度
    """
    from PIL import Image
    w, h = img.size
    
    if direction == "none":
        return img.copy()
    
    center_x, center_y = w // 2, h // 2
    
    if direction == "gentle":
        angle = strength * math.sin(frame_progress * math.pi * 4) * 5
    elif direction == "shake":
        angle = random.uniform(-strength * 5, strength * 5)
    else:
        angle = 0
    
    rotated = img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(20, 20, 30))
    
    # 居中裁剪
    x1 = (rotated.width - w) // 2
    y1 = (rotated.height - h) // 2
    cropped = rotated.crop((x1, y1, x1 + w, y1 + h))
    
    return cropped

def get_camera_motion_for_page(page_index: int, total_pages: int) -> dict:
    """为每一页生成镜头运动参数
    
    Returns:
        dict: {
            "static_frames": 前静止帧的运动,
            "motion": 镜头运动类型,
            "direction": 方向,
            "dynamic_frames": 需要动态效果的帧数
        }
    """
    motions = [
        ("pan", "left"),
        ("pan", "right"),
        ("zoom_in", None),
        ("zoom_out", None),
        ("tilt", "gentle"),
        ("none", None),
    ]
    
    # 根据页码选择不同的运动
    motion_type, direction = motions[page_index % len(motions)]
    
    # 第一页和最后一页用轻微运动
    if page_index == 0 or page_index == total_pages - 1:
        motion_type = "tilt"
        direction = "gentle"
    
    return {
        "type": motion_type,
        "direction": direction,
        "strength": random.uniform(0.08, 0.15),
        "dynamic_ratio": random.uniform(0.3, 0.6),  # 多少比例的帧应用运动
    }

# ============ 帧生成 ============

def _page_to_animated_frames(
    page_img, 
    num_static_frames: int = 24,
    motion: dict = None,
    fps: int = 8
):
    """将一页漫画生成带动态效果的帧
    
    Args:
        page_img: PIL Image
        num_static_frames: 静止帧数
        motion: 镜头运动参数
        fps: 帧率
    """
    from PIL import Image, ImageFilter
    frames = []
    w, h = page_img.size
    
    # 分割静止帧和动态帧
    dynamic_ratio = motion.get("dynamic_ratio", 0.4) if motion else 0
    num_dynamic = int(num_static_frames * dynamic_ratio)
    num_truly_static = num_static_frames - num_dynamic
    
    motion_type = motion.get("type", "none") if motion else "none"
    direction = motion.get("direction", "none") if motion else "none"
    strength = motion.get("strength", 0.1) if motion else 0.1
    
    # 前半段动态
    for i in range(num_dynamic):
        frame_progress = i / num_dynamic
        if motion_type == "pan":
            frame = apply_pan_effect(page_img, direction, strength, frame_progress)
        elif motion_type == "zoom_in":
            frame = apply_zoom_effect(page_img, True, frame_progress, strength)
        elif motion_type == "zoom_out":
            frame = apply_zoom_effect(page_img, False, frame_progress, strength)
        elif motion_type == "tilt":
            frame = apply_tilt_effect(page_img, direction, frame_progress, strength)
        else:
            frame = page_img.copy()
        frames.append(frame)
    
    # 静止帧
    for _ in range(num_truly_static):
        frames.append(page_img.copy())
    
    # 后半段反向动态
    for i in range(num_dynamic):
        frame_progress = 1 - (i / num_dynamic)
        if motion_type == "pan":
            frame = apply_pan_effect(page_img, direction, strength, frame_progress)
        elif motion_type == "zoom_in":
            frame = apply_zoom_effect(page_img, True, frame_progress, strength)
        elif motion_type == "zoom_out":
            frame = apply_zoom_effect(page_img, False, frame_progress, strength)
        elif motion_type == "tilt":
            frame = apply_tilt_effect(page_img, direction, frame_progress, strength)
        else:
            frame = page_img.copy()
        frames.append(frame)
    
    return frames

def _create_slide_transition(img1, img2, num_frames=24, direction="left"):
    """创建两张图之间的滑动过渡"""
    from PIL import Image
    w, h = img1.size
    frames = []
    for i in range(num_frames):
        t = (i + 1) / num_frames
        canvas = Image.new("RGB", (w, h))
        if direction == "left":
            offset1 = int(-w * t)
            offset2 = int(w * (1 - t))
            canvas.paste(img1, (offset1, 0))
            canvas.paste(img2, (offset2, 0))
        elif direction == "right":
            offset1 = int(w * t)
            offset2 = int(-w * (1 - t))
            canvas.paste(img1, (offset1, 0))
            canvas.paste(img2, (offset2, 0))
        elif direction == "up":
            offset1 = int(-h * t)
            offset2 = int(h * (1 - t))
            canvas.paste(img1, (0, offset1))
            canvas.paste(img2, (0, offset2))
        else:  # down
            offset1 = int(h * t)
            offset2 = int(-h * (1 - t))
            canvas.paste(img1, (0, offset1))
            canvas.paste(img2, (0, offset2))
        frames.append(canvas)
    return frames

def _create_fade_transition(img1, img2, num_frames=20):
    """创建两张图之间的淡入淡出过渡"""
    from PIL import Image
    w, h = img1.size
    frames = []
    for i in range(num_frames):
        t = (i + 1) / num_frames
        blended = Image.blend(img1.convert("RGB"), img2.convert("RGB"), t)
        frames.append(blended)
    return frames

def _create_zoom_transition(img1, img2, num_frames=20):
    """缩放过渡：img1放大消失，img2缩小出现"""
    from PIL import Image
    w, h = img1.size
    frames = []
    for i in range(num_frames):
        t = (i + 1) / num_frames
        # img1 zoom in
        scale1 = 1.0 + 0.3 * t
        nw1, nh1 = int(w * scale1), int(h * scale1)
        zoomed1 = img1.resize((nw1, nh1), Image.LANCZOS)
        cropped1 = zoomed1.crop(((nw1-w)//2, (nh1-h)//2, (nw1+w)//2, (nh1+h)//2))
        # img2 zoom from center
        scale2 = 1.0 + 0.3 * (1 - t)
        nw2, nh2 = int(w * scale2), int(h * scale2)
        zoomed2 = img2.resize((nw2, nh2), Image.LANCZOS)
        cropped2 = zoomed2.crop(((nw2-w)//2, (nh2-h)//2, (nw2+w)//2, (nh2+h)//2))
        # blend
        blended = Image.blend(cropped1.convert("RGB"), cropped2.convert("RGB"), t)
        frames.append(blended)
    return frames

TRANSITIONS = {
    "fade": ("淡入淡出", _create_fade_transition),
    "slide_left": ("左滑", lambda i1, i2, n: _create_slide_transition(i1, i2, n, "left")),
    "slide_right": ("右滑", lambda i1, i2, n: _create_slide_transition(i1, i2, n, "right")),
    "slide_up": ("上滑", lambda i1, i2, n: _create_slide_transition(i1, i2, n, "up")),
    "zoom": ("缩放", _create_zoom_transition),
}

# ============ 背景音乐生成 ============

def generate_bgm(style: str = "normal", duration_seconds: float = 30) -> bytes:
    """生成简单的背景音乐（使用简化的合成方式）
    
    Args:
        style: 音乐风格 normal / epic / romantic / suspense / relaxing
        duration_seconds: 时长（秒）
    
    Returns:
        WAV格式的音频数据
    """
    import struct
    import wave
    import random
    
    sample_rate = 22050
    num_samples = int(sample_rate * duration_seconds)
    
    # 不同风格的音色参数
    style_params = {
        "normal": {"base_freq": 440, "chord": [1.0, 1.25, 1.5], "tempo": 1.0},
        "epic": {"base_freq": 220, "chord": [1.0, 1.25, 1.5, 2.0], "tempo": 0.7},
        "romantic": {"base_freq": 523, "chord": [1.0, 1.2, 1.5], "tempo": 1.2},
        "suspense": {"base_freq": 330, "chord": [1.0, 1.059], "tempo": 0.5},
        "relaxing": {"base_freq": 392, "chord": [1.0, 1.25], "tempo": 1.3},
    }
    
    params = style_params.get(style, style_params["normal"])
    base_freq = params["base_freq"]
    tempo = params["tempo"]
    
    # 生成音频数据
    audio_data = []
    for i in range(num_samples):
        t = i / sample_rate
        # 主旋律
        freq_mod = 1.0 + 0.02 * math.sin(t * tempo * 2)
        freq = base_freq * freq_mod
        
        # 谐波
        value = 0.0
        for h, amp in enumerate(params["chord"]):
            value += amp * math.sin(2 * math.pi * freq * h * t) / (h + 1)
        
        # 包络
        env = min(1.0, t * 2) * min(1.0, (duration_seconds - t) * 0.5)
        value *= env * 0.3
        
        # 添加随机微扰（更自然）
        value += random.uniform(-0.02, 0.02)
        
        audio_data.append(int(value * 32767))
    
    # 转换为字节
    audio_bytes = struct.pack("<" + "h" * len(audio_data), *audio_data)
    
    # 包装成WAV
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(audio_bytes)
    
    return wav_buffer.getvalue()

def suggest_bgm_for_story(story_type: str) -> str:
    """根据故事类型推荐背景音乐风格
    
    Args:
        story_type: 故事模板名称
    
    Returns:
        推荐的bgm风格
    """
    bgm_map = {
        "热血冒险": "epic",
        "恋爱日常": "romantic",
        "暗恋心事": "romantic",
        "破镜重圆": "romantic",
        "悬疑推理": "suspense",
        "恐怖惊悚": "suspense",
        "奇幻魔法": "epic",
        "科幻未来": "suspense",
        "星际探险": "epic",
        "搞笑日常": "relaxing",
        "职场囧事": "relaxing",
        "古风仙侠": "relaxing",
        "江湖恩怨": "epic",
        "治愈日常": "relaxing",
        "治愈孤独": "relaxing",
    }
    return bgm_map.get(story_type, "normal")

# ============ 视频生成 ============

def generate_video_frames(
    pages,
    fps: int = 8,
    duration_per_page: float = 3.0,
    transition: str = "fade",
    transition_duration: float = 0.5,
    enable_camera_motion: bool = True,
):
    """生成所有视频帧（含动态镜头）
    
    Args:
        pages: PIL Image列表
        fps: 帧率
        duration_per_page: 每页停留秒数
        transition: 过渡效果
        transition_duration: 过渡时长秒数
        enable_camera_motion: 是否启用镜头运动
    
    Returns:
        list of PIL Image frames
    """
    from PIL import Image

    if not pages:
        return []

    static_frames_per_page = int(fps * duration_per_page)
    transition_frame_count = int(fps * transition_duration)
    transition_fn = TRANSITIONS.get(transition, TRANSITIONS["fade"])[1]

    all_frames = []
    for i, page in enumerate(pages):
        # 统一尺寸
        page_rgb = page.convert("RGB")

        # 获取镜头运动参数
        motion = None
        if enable_camera_motion:
            motion = get_camera_motion_for_page(i, len(pages))

        # 带动态效果的帧
        animated_frames = _page_to_animated_frames(
            page_rgb, 
            num_static_frames=static_frames_per_page,
            motion=motion,
            fps=fps
        )
        all_frames.extend(animated_frames)

        # 过渡帧（到下一页）
        if i < len(pages) - 1:
            next_page = pages[i + 1].convert("RGB")
            # 确保尺寸一致
            if next_page.size != page_rgb.size:
                next_page = next_page.resize(page_rgb.size, Image.LANCZOS)
            trans_frames = transition_fn(page_rgb, next_page, max(transition_frame_count, 4))
            all_frames.extend(trans_frames)

    return all_frames

def export_video_pil(
    pages,
    title: str,
    output_dir: str = None,
    fps: int = 8,
    duration_per_page: float = 3.0,
    transition: str = "fade",
    enable_camera_motion: bool = True,
    progress_callback=None,
) -> str:
    """用PIL生成GIF格式视频（不依赖ffmpeg）"""
    from PIL import Image

    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, f"{title}.gif")

    frames = generate_video_frames(
        pages, fps=fps, duration_per_page=duration_per_page,
        transition=transition, transition_duration=0.5,
        enable_camera_motion=enable_camera_motion,
    )

    if not frames:
        return output_path

    if progress_callback:
        progress_callback(0, len(frames))

    # 缩小尺寸以控制文件大小
    max_w = 800
    if frames[0].width > max_w:
        scale = max_w / frames[0].width
        new_h = int(frames[0].height * scale)
        frames = [f.resize((max_w, new_h), Image.LANCZOS) for f in frames]

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )

    if progress_callback:
        progress_callback(len(frames), len(frames))

    return output_path

def export_video_mp4(
    pages,
    title: str,
    output_dir: str = None,
    fps: int = 12,
    duration_per_page: float = 3.0,
    transition: str = "fade",
    enable_camera_motion: bool = True,
    include_bgm: bool = False,
    bgm_style: str = "normal",
    story_type: str = None,
    progress_callback=None,
) -> str:
    """生成MP4视频（带音频）
    
    Args:
        pages: 漫画页面列表
        title: 标题
        output_dir: 输出目录
        fps: 帧率
        duration_per_page: 每页停留秒数
        transition: 过渡效果
        enable_camera_motion: 启用镜头运动
        include_bgm: 是否包含背景音乐
        bgm_style: 音乐风格
        story_type: 故事类型（用于自动选择音乐）
        progress_callback: 进度回调
    """
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)

    frames = generate_video_frames(
        pages, fps=fps, duration_per_page=duration_per_page,
        transition=transition, transition_duration=0.5,
        enable_camera_motion=enable_camera_motion,
    )

    if not frames:
        return ""

    if progress_callback:
        progress_callback(0, len(frames))

    # 计算视频时长
    video_duration = len(frames) / fps
    
    # 根据故事类型自动选择音乐
    if bgm_style == "auto" and story_type:
        bgm_style = suggest_bgm_for_story(story_type)

    # 尝试ffmpeg（带音频）
    try:
        import subprocess
        tmp_dir = tempfile.mkdtemp()
        # 写帧图片
        for i, frame in enumerate(frames):
            frame.save(os.path.join(tmp_dir, f"frame_{i:05d}.png"))
        
        output_path = os.path.join(out_dir, f"{title}.mp4")
        
        if include_bgm:
            # 生成背景音乐
            bgm_path = os.path.join(tmp_dir, "bgm.wav")
            bgm_data = generate_bgm(bgm_style, video_duration)
            with open(bgm_path, "wb") as f:
                f.write(bgm_data)
            
            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(tmp_dir, "frame_%05d.png"),
                "-i", bgm_path,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", "23",
                "-preset", "fast",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                output_path,
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(tmp_dir, "frame_%05d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", "23",
                "-preset", "fast",
                output_path,
            ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=180)
        if result.returncode == 0:
            # 清理临时文件
            import shutil
            shutil.rmtree(tmp_dir, ignore_errors=True)
            if progress_callback:
                progress_callback(len(frames), len(frames))
            return output_path
        else:
            raise RuntimeError(f"ffmpeg failed: {result.stderr[:200]}")
    except (FileNotFoundError, RuntimeError, subprocess.TimeoutExpired):
        pass

    # 回退GIF
    return export_video_pil(
        pages, title, out_dir, fps=max(fps // 2, 4),
        duration_per_page=duration_per_page, transition=transition,
        enable_camera_motion=enable_camera_motion,
        progress_callback=progress_callback,
    )

def video_to_bytes(video_path: str) -> bytes:
    """读取视频文件为字节数据"""
    with open(video_path, "rb") as f:
        return f.read()

# ============ 视频预览生成 ============

def generate_preview_thumbnail(pages, index: int = 0) -> str:
    """生成预览缩略图"""
    from PIL import Image
    
    if not pages or index >= len(pages):
        return ""
    
    page = pages[index].convert("RGB")
    
    # 缩小
    max_w = 400
    if page.width > max_w:
        scale = max_w / page.width
        page = page.resize((max_w, int(page.height * scale)), Image.LANCZOS)
    
    # 保存
    out_path = os.path.join(config.OUTPUT_DIR, "preview", f"thumb_{index}.jpg")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    page.save(out_path, "JPEG", quality=85)
    
    return out_path

# ============ v9 新增：字幕生成 ============

def generate_subtitles(pages_data: list, fps: int = 8, duration_per_page: float = 3.0) -> list:
    """根据对话内容生成字幕时间轴"""
    subtitles = []
    frame_idx = 0
    
    for page_data in pages_data:
        page_start = frame_idx
        page_frames = int(fps * duration_per_page)
        
        page_texts = []
        for panel in page_data:
            for dialogue in panel.get("dialogues", []):
                speaker = dialogue.get("speaker", "")
                text = dialogue.get("text", "")
                if text:
                    page_texts.append(f"{speaker}: {text}" if speaker else text)
        
        if page_texts:
            text = " | ".join(page_texts[:2])
            mid_start = page_start + page_frames // 4
            mid_end = page_start + page_frames * 3 // 4
            subtitles.append((mid_start, mid_end, text))
        
        frame_idx += page_frames
    
    return subtitles

def render_subtitle_on_frame(frame, text: str, font_size: int = 24):
    """在帧上渲染字幕"""
    from PIL import Image, ImageDraw, ImageFont
    
    frame = frame.convert("RGBA")
    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    w, h = frame.size
    sub_h = font_size + 20
    sub_y = h - sub_h - 20
    
    draw.rectangle([(0, sub_y), (w, h)], fill=(0, 0, 0, 160))
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_x = (w - text_w) // 2
    
    draw.text((text_x, sub_y + 10), text, font=font, fill=(255, 255, 255, 255))
    
    result = Image.alpha_composite(frame, overlay)
    return result.convert("RGB")

def add_subtitles_to_video(frames, pages_data, fps=8, duration_per_page=3.0):
    """为视频帧添加字幕"""
    if not frames or not pages_data:
        return frames
    
    subtitles = generate_subtitles(pages_data, fps, duration_per_page)
    
    frame_subtitles = {}
    for start, end, text in subtitles:
        for f_idx in range(start, min(end, len(frames))):
            frame_subtitles[f_idx] = text
    
    result_frames = []
    for f_idx, frame in enumerate(frames):
        if f_idx in frame_subtitles:
            frame = render_subtitle_on_frame(frame, frame_subtitles[f_idx])
        result_frames.append(frame)
    
    return result_frames

# ============ v9 新增：视频封面生成 ============

def generate_video_cover(pages, title: str, genre: str = ""):
    """生成视频封面"""
    from PIL import Image, ImageDraw, ImageFont
    
    if not pages:
        cover = Image.new("RGB", (1280, 720), (30, 30, 50))
        draw = ImageDraw.Draw(cover)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), title, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((1280 - text_w) // 2, 300), title, font=font, fill=(255, 255, 255))
        return cover
    
    cover = pages[0].convert("RGB")
    
    target_w, target_h = 1280, 720
    scale = max(target_w / cover.width, target_h / cover.height)
    new_w, new_h = int(cover.width * scale), int(cover.height * scale)
    cover = cover.resize((new_w, new_h), Image.LANCZOS)
    
    x = (new_w - target_w) // 2
    y = (new_h - target_h) // 2
    cover = cover.crop((x, y, x + target_w, y + target_h))
    
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for i in range(200):
        alpha = int(180 * (1 - i / 200))
        draw.rectangle([(0, target_h - 200 + i), (target_w, target_h - 200 + i + 1)], fill=(0, 0, 0, alpha))
    
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
    
    draw = ImageDraw.Draw(cover)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        genre_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        genre_font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), title, font=title_font)
    text_w = bbox[2] - bbox[0]
    draw.text(((target_w - text_w) // 2, target_h - 120), title, font=title_font, fill=(255, 255, 255))
    
    if genre:
        draw.text((20, target_h - 50), f"  {genre}", font=genre_font, fill=(200, 200, 200))
    
    return cover

# ============ v9 新增：高级视频API检测 ============

def is_kling_available() -> bool:
    return bool(config.KLING_API_KEY)

def is_sora_available() -> bool:
    return bool(config.SORA_API_KEY)

def is_runway_available() -> bool:
    return bool(config.RUNWAY_API_KEY)

def is_minimax_available() -> bool:
    return bool(config.MINIMAX_API_KEY)

def get_available_video_backends() -> list:
    """获取可用的视频生成后端"""
    backends = [("pil", "幻灯片（免费）")]
    if is_kling_available():
        backends.append(("kling", "可灵AI（高质量）"))
    if is_sora_available():
        backends.append(("sora", "Sora（高质量）"))
    if is_runway_available():
        backends.append(("runway", "Runway（高质量）"))
    if is_minimax_available():
        backends.append(("minimax", "MiniMax（高质量）"))
    return backends

# ============ v9 新增：完整视频生成（含字幕） ============

def generate_full_video_with_subtitles(
    pages, pages_data, title: str, output_dir: str = None,
    fps: int = 8, duration_per_page: float = 3.0,
    transition: str = "fade", enable_camera_motion: bool = True,
    include_bgm: bool = False, bgm_style: str = "normal",
    story_type: str = None, include_subtitles: bool = True,
    progress_callback=None,
) -> str:
    """生成完整视频（含字幕）"""
    frames = generate_video_frames(
        pages, fps=fps, duration_per_page=duration_per_page,
        transition=transition, transition_duration=0.5,
        enable_camera_motion=enable_camera_motion,
    )
    
    if not frames:
        return ""
    
    if include_subtitles:
        frames = add_subtitles_to_video(frames, pages_data, fps, duration_per_page)
    
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    
    if progress_callback:
        progress_callback(0, len(frames))
    
    max_w = 800
    if frames[0].width > max_w:
        scale = max_w / frames[0].width
        new_h = int(frames[0].height * scale)
        frames = [f.resize((max_w, new_h), Image.LANCZOS) for f in frames]
    
    output_path = os.path.join(out_dir, f"{title}_subtitled.gif")
    frames[0].save(
        output_path, save_all=True, append_images=frames[1:],
        duration=int(1000 / fps), loop=0, optimize=True,
    )
    
    if progress_callback:
        progress_callback(len(frames), len(frames))
    
    return output_path

# ============ v10 新增：高级转场效果 ============

def _create_flash_transition(img1, img2, num_frames=8):
    """闪白转场"""
    from PIL import Image
    w, h = img1.size
    frames = []
    for i in range(num_frames):
        t = (i + 1) / num_frames
        if t < 0.3:
            blended = Image.blend(img1.convert("RGB"), Image.new("RGB", (w, h), (255, 255, 255)), t / 0.3)
        elif t < 0.5:
            blended = Image.new("RGB", (w, h), (255, 255, 255))
        else:
            blended = Image.blend(Image.new("RGB", (w, h), (255, 255, 255)), img2.convert("RGB"), (t - 0.5) / 0.5)
        frames.append(blended)
    return frames

def _create_blur_transition(img1, img2, num_frames=16):
    """模糊转场"""
    from PIL import Image, ImageFilter
    w, h = img1.size
    frames = []
    for i in range(num_frames):
        t = (i + 1) / num_frames
        if t < 0.5:
            blur_level = int(t * 2 * 10)
            blurred = img1.filter(ImageFilter.GaussianBlur(radius=max(blur_level, 0.5)))
            blended = Image.blend(img1.convert("RGB"), blurred.convert("RGB"), t * 2)
        else:
            blur_level = int((1 - t) * 2 * 10)
            blurred = img2.filter(ImageFilter.GaussianBlur(radius=max(blur_level, 0.5)))
            blended = Image.blend(blurred.convert("RGB"), img2.convert("RGB"), (t - 0.5) * 2)
        frames.append(blended)
    return frames

def _create_shake_transition(img1, img2, num_frames=12):
    """抖动转场"""
    from PIL import Image
    import random
    w, h = img1.size
    frames = []
    for i in range(num_frames):
        t = (i + 1) / num_frames
        shake_x = random.randint(-10, 10) if t < 0.5 else random.randint(-5, 5)
        shake_y = random.randint(-8, 8) if t < 0.5 else random.randint(-3, 3)
        
        if t < 0.5:
            frame = img1.copy()
            frame = frame.crop((max(0, -shake_x), max(0, -shake_y), 
                              min(w, w - shake_x), min(h, h - shake_y)))
            frame = frame.resize((w, h), Image.LANCZOS)
        else:
            frame = img2.copy()
            frame = frame.crop((max(0, -shake_x), max(0, -shake_y),
                              min(w, w - shake_x), min(h, h - shake_y)))
            frame = frame.resize((w, h), Image.LANCZOS)
        frames.append(frame)
    return frames

def _create_wipe_transition(img1, img2, num_frames=20):
    """从中心向外扩散转场"""
    from PIL import Image, ImageDraw
    w, h = img1.size
    frames = []
    center_x, center_y = w // 2, h // 2
    max_radius = int((w**2 + h**2)**0.5)
    
    for i in range(num_frames):
        t = (i + 1) / num_frames
        current_radius = int(max_radius * t)
        
        canvas = img1.copy().convert("RGBA")
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse([center_x - current_radius, center_y - current_radius,
                     center_x + current_radius, center_y + current_radius], fill=255)
        
        canvas.putalpha(mask)
        canvas = Image.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, 255)), canvas)
        frames.append(canvas.convert("RGB"))
    return frames

# 注册高级转场
TRANSITIONS["flash"] = ("闪白", _create_flash_transition)
TRANSITIONS["blur"] = ("模糊", _create_blur_transition)
TRANSITIONS["shake"] = ("抖动", _create_shake_transition)
TRANSITIONS["wipe"] = ("扩散", _create_wipe_transition)

# ============ v10 新增：情感配乐系统 ============

class EmotionBGM:
    """情感配乐系统 - 根据情感曲线自动调整音乐"""
    
    EMOTION_MUSIC_MAP = {
        "温馨": {"style": "warm", "tempo": 1.0, "volume": 0.8},
        "紧张": {"style": "tense", "tempo": 1.3, "volume": 1.0},
        "高潮": {"style": "epic", "tempo": 1.5, "volume": 1.0},
        "搞笑": {"style": "comedic", "tempo": 1.2, "volume": 0.7},
        "浪漫": {"style": "romantic", "tempo": 0.8, "volume": 0.75},
        "悲伤": {"style": "sad", "tempo": 0.6, "volume": 0.85},
        "悬疑": {"style": "mystery", "tempo": 0.5, "volume": 0.9},
        "释然": {"style": "peaceful", "tempo": 0.7, "volume": 0.7},
        "惊讶": {"style": "surprise", "tempo": 1.4, "volume": 1.0},
    }
    
    @classmethod
    def generate_emotion_bgm(cls, emotion_curve: list, fps: int = 8, duration_per_page: float = 3.0) -> bytes:
        """根据情感曲线生成动态配乐"""
        import struct
        import wave
        
        total_frames = len(emotion_curve) * int(fps * duration_per_page)
        duration = total_frames / fps
        sample_rate = 22050
        
        base_freq = 440
        audio_data = []
        
        for frame_idx in range(total_frames):
            page_idx = frame_idx // int(fps * duration_per_page)
            emotion = emotion_curve[page_idx] if page_idx < len(emotion_curve) else "温馨"
            music_params = cls.EMOTION_MUSIC_MAP.get(emotion, cls.EMOTION_MUSIC_MAP["温馨"])
            
            t = frame_idx / sample_rate
            style = music_params["style"]
            tempo = music_params["tempo"]
            volume = music_params["volume"]
            
            if style == "warm":
                freq = base_freq * 1.0
            elif style == "tense":
                freq = base_freq * 1.2
            elif style == "epic":
                freq = base_freq * 0.8
            elif style == "comedic":
                freq = base_freq * 1.1
            elif style == "romantic":
                freq = base_freq * 1.25
            elif style == "sad":
                freq = base_freq * 0.9
            elif style == "mystery":
                freq = base_freq * 0.7
            elif style == "peaceful":
                freq = base_freq * 1.05
            else:
                freq = base_freq
            
            value = math.sin(2 * math.pi * freq * t * tempo)
            env = min(1.0, t * 0.5) * min(1.0, (duration - t) * 0.5)
            value *= env * volume * 0.3
            
            audio_data.append(int(value * 32767))
        
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(struct.pack("<" + "h" * len(audio_data), *audio_data))
        
        return wav_buffer.getvalue()

# ============ v10 新增：视频预览生成 ============

def generate_video_preview(pages, title: str, max_duration: int = 10) -> str:
    """生成低分辨率预览视频"""
    from PIL import Image
    
    if not pages:
        return ""
    
    out_dir = os.path.join(config.OUTPUT_DIR, "previews")
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, f"{title}_preview.gif")
    
    max_frames = max_duration * 8
    total_needed = len(pages) * 8
    
    if total_needed > max_frames:
        step = total_needed / max_frames
        sampled_pages = [pages[min(int(i * step), len(pages) - 1)] for i in range(max_frames // 8)]
    else:
        sampled_pages = pages
    
    frames = []
    for page in sampled_pages:
        frame = page.convert("RGB")
        max_w = 320
        if frame.width > max_w:
            scale = max_w / frame.width
            frame = frame.resize((max_w, int(frame.height * scale)), Image.LANCZOS)
        frames.append(frame)
    
    if frames:
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=125, loop=0)
    
    return output_path

def generate_storyboard_preview(pages_data: list, title: str) -> str:
    """生成故事板预览（带情感标注）"""
    from PIL import Image, ImageDraw, ImageFont
    
    if not pages_data:
        return ""
    
    thumb_size = 200
    cols = min(len(pages_data), 4)
    rows = (len(pages_data) + cols - 1) // cols
    
    canvas = Image.new("RGB", (cols * thumb_size, rows * thumb_size + 50), (40, 40, 50))
    draw = ImageDraw.Draw(canvas)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 10), f"Storyboard: {title}", font=font, fill=(255, 255, 255))
    
    emotion_colors = {
        "温馨": (255, 200, 100),
        "紧张": (255, 100, 100),
        "高潮": (255, 50, 50),
        "搞笑": (255, 255, 100),
        "浪漫": (255, 150, 200),
        "悲伤": (100, 100, 200),
        "悬疑": (150, 50, 150),
    }
    
    for idx, page_data in enumerate(pages_data[:cols * rows]):
        col = idx % cols
        row = idx // cols
        emotion = page_data.get("emotion", "")
        color = emotion_colors.get(emotion, (200, 200, 200))
        
        x = col * thumb_size + 5
        y = row * thumb_size + 30
        
        draw.rectangle([x, y, x + thumb_size - 10, y + thumb_size - 40], fill=color)
        draw.text((x + 5, y + thumb_size - 30), f"Page {idx+1}", font=font, fill=(255, 255, 255))
    
    out_dir = os.path.join(config.OUTPUT_DIR, "previews")
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, f"{title}_storyboard.png")
    canvas.save(output_path)
    
    return output_path

# ============ v10 新增：增强视频导出 ============

def export_video_enhanced(
    pages, pages_data: list, title: str, output_dir: str = None,
    fps: int = 8, duration_per_page: float = 3.0, transition: str = "fade",
    enable_camera_motion: bool = True, enable_emotion_bgm: bool = False,
    enable_narration: bool = False, emotion_curve: list = None,
    progress_callback=None,
) -> str:
    """v10 增强版视频导出"""
    from PIL import Image
    
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    
    frames = generate_video_frames(
        pages, fps=fps, duration_per_page=duration_per_page,
        transition=transition, transition_duration=0.5,
        enable_camera_motion=enable_camera_motion,
    )
    
    if not frames:
        return ""
    
    if progress_callback:
        progress_callback(0, len(frames))
    
    if pages_data:
        frames = add_subtitles_to_video(frames, pages_data, fps, duration_per_page)
    
    max_w = 720
    if frames[0].width > max_w:
        scale = max_w / frames[0].width
        new_h = int(frames[0].height * scale)
        frames = [f.resize((max_w, new_h), Image.LANCZOS) for f in frames]
    
    output_path = os.path.join(out_dir, f"{title}_enhanced.gif")
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, optimize=True)
    
    if progress_callback:
        progress_callback(len(frames), len(frames))
    
    return output_path

# ============ v10 新增：完整导出 ============

def export_full_video(
    pages, script: dict, title: str, output_dir: str = None,
    fps: int = 8, duration_per_page: float = 3.0, transition: str = "fade",
    enable_camera_motion: bool = True, enable_subtitles: bool = True,
    enable_preview: bool = False, progress_callback=None,
) -> dict:
    """v10 完整视频导出 - 返回多个文件"""
    from PIL import Image, ImageDraw, ImageFont
    
    out_dir = output_dir or os.path.join(config.OUTPUT_DIR, title)
    os.makedirs(out_dir, exist_ok=True)
    
    result = {"main_video": "", "preview": "", "storyboard": "", "cover": ""}
    
    if progress_callback:
        progress_callback(0, 100)
    
    # 主视频
    pages_data = [p.get("panels", []) for p in script.get("pages", [])]
    result["main_video"] = export_video_enhanced(
        pages=pages, pages_data=pages_data, title=title, output_dir=out_dir,
        fps=fps, duration_per_page=duration_per_page, transition=transition,
        enable_camera_motion=enable_camera_motion, progress_callback=None,
    )
    
    if progress_callback:
        progress_callback(50, 100)
    
    if enable_preview:
        result["preview"] = generate_video_preview(pages, title, max_duration=8)
    
    result["storyboard"] = generate_storyboard_preview(script.get("pages", []), title)
    
    # 封面
    target_w, target_h = 1280, 720
    if pages and pages[0]:
        cover = pages[0].convert("RGB")
        scale = max(target_w / cover.width, target_h / cover.height)
        new_w, new_h = int(cover.width * scale), int(cover.height * scale)
        cover = cover.resize((new_w, new_h), Image.LANCZOS)
        x, y = (new_w - target_w) // 2, (new_h - target_h) // 2
        cover = cover.crop((x, y, x + target_w, y + target_h))
    else:
        cover = Image.new("RGB", (target_w, target_h), (30, 30, 50))
    
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i in range(150):
        alpha = int(180 * (1 - i / 150))
        draw.rectangle([(0, target_h - 180 + i), (target_w, target_h - 180 + i + 1)], fill=(0, 0, 0, alpha))
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
    
    draw = ImageDraw.Draw(cover)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        title_font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((target_w - (bbox[2] - bbox[0])) // 2, target_h - 120), title, font=title_font, fill=(255, 255, 255))
    
    output_path = os.path.join(out_dir, "cover.jpg")
    cover.save(output_path, "JPEG", quality=95)
    result["cover"] = output_path
    
    if progress_callback:
        progress_callback(100, 100)
    
    return result
