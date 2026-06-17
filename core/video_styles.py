# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 视频风格增强
更多风格选项和预设模板
"""

from typing import Dict, List
from dataclasses import dataclass


# ============ 视频风格数据 ============

VIDEO_STYLES = {
    "动漫风": {
        "icon": "🎌",
        "prompt": "anime style, vibrant colors, dynamic camera, cel-shading, Japanese animation",
        "speed": 1.0,
        "transitions": ["硬切", "淡入淡出", "闪烁"],
        "bpm_range": (80, 140),
        "suitable_genres": ["冒险", "校园", "热血"],
    },
    "真人影视": {
        "icon": "🎬",
        "prompt": "cinematic style, depth of field, film grain, professional lighting, 24fps feel",
        "speed": 0.8,
        "transitions": ["叠化", "淡入淡出", "划变"],
        "bpm_range": (60, 120),
        "suitable_genres": ["都市", "悬疑", "爱情"],
    },
    "水墨动画": {
        "icon": "🎨",
        "prompt": "Chinese ink wash animation, flowing brushstrokes, traditional aesthetic, ethereal",
        "speed": 0.6,
        "transitions": ["墨晕", "淡入", "飞白"],
        "bpm_range": (40, 80),
        "suitable_genres": ["古风", "修仙", "武侠"],
    },
    "赛博朋克": {
        "icon": "🌆",
        "prompt": "cyberpunk neon, glitch effects, holographic overlays, dark atmosphere, rain",
        "speed": 1.2,
        "transitions": ["故障", "闪烁", "数据流"],
        "bpm_range": (120, 160),
        "suitable_genres": ["科幻", "末世", "赛博"],
    },
    "像素复古": {
        "icon": "👾",
        "prompt": "pixel art animation, 16-bit retro game style, nostalgic, chiptune feel",
        "speed": 1.0,
        "transitions": ["像素化", "扫描线", "闪烁"],
        "bpm_range": (100, 150),
        "suitable_genres": ["游戏", "日常", "搞笑"],
    },
    "水彩绘本": {
        "icon": "🖌️",
        "prompt": "watercolor illustration animation, soft edges, dreamlike, pastel palette, gentle",
        "speed": 0.5,
        "transitions": ["水晕", "色散", "柔化"],
        "bpm_range": (40, 80),
        "suitable_genres": ["治愈", "童话", "暖心"],
    },
    "3D渲染": {
        "icon": "💎",
        "prompt": "3D rendered animation, realistic lighting, volumetric effects, high detail",
        "speed": 0.9,
        "transitions": ["旋转", "缩放", "环绕"],
        "bpm_range": (80, 130),
        "suitable_genres": ["奇幻", "科幻", "动作"],
    },
    "纸片人风": {
        "icon": "📋",
        "prompt": "paper cutout animation, flat design, layered parallax, craft style",
        "speed": 0.7,
        "transitions": ["翻转", "层叠", "弹跳"],
        "bpm_range": (70, 110),
        "suitable_genres": ["搞笑", "日常", "创意"],
    },
}

# 视频模板
VIDEO_TEMPLATES = {
    "抖音竖屏": {
        "aspect_ratio": "9:16",
        "resolution": "1080x1920",
        "duration": "15-60秒",
        "fps": 30,
        "tip": "竖屏短视频，适合快速吸引注意",
    },
    "B站横屏": {
        "aspect_ratio": "16:9",
        "resolution": "1920x1080",
        "duration": "3-15分钟",
        "fps": 24,
        "tip": "横屏长视频，适合完整叙事",
    },
    "小红书方屏": {
        "aspect_ratio": "1:1",
        "resolution": "1080x1080",
        "duration": "15-60秒",
        "fps": 30,
        "tip": "方形视频，适合图文结合展示",
    },
    "电影宽幅": {
        "aspect_ratio": "2.35:1",
        "resolution": "2560x1080",
        "duration": "5-30分钟",
        "fps": 24,
        "tip": "电影宽银幕比例，沉浸感强",
    },
}


class VideoStyleManager:
    """视频风格管理器"""

    def __init__(self):
        pass

    def get_all_styles(self) -> Dict:
        return VIDEO_STYLES

    def get_style(self, name: str) -> Dict:
        return VIDEO_STYLES.get(name, {})

    def get_style_prompt(self, name: str) -> str:
        style = self.get_style(name)
        return style.get("prompt", "")

    def get_suitable_styles(self, genre: str) -> List[Dict]:
        results = []
        for name, data in VIDEO_STYLES.items():
            if genre in data.get("suitable_genres", []):
                results.append({"name": name, **data})
        return results

    def get_templates(self) -> Dict:
        return VIDEO_TEMPLATES

    def get_template(self, name: str) -> Dict:
        return VIDEO_TEMPLATES.get(name, {})


def render_video_styles_page():
    """渲染视频风格页面"""
    import streamlit as st

    mgr = VideoStyleManager()

    st.header("🎬 视频风格")
    st.caption("更多风格选项，打造独特视觉体验")

    tab1, tab2, tab3 = st.tabs(["🎨 风格库", "📐 视频模板", "🔍 风格推荐"])

    with tab1:
        for name, data in mgr.get_all_styles().items():
            with st.expander(f"{data['icon']} {name}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**提示词**: `{data['prompt'][:80]}...`")
                    st.write(f"**推荐速度**: {data['speed']}x")
                    st.write(f"**转场效果**: {', '.join(data['transitions'])}")
                with c2:
                    st.write(f"**适合题材**: {', '.join(data['suitable_genres'])}")
                    st.write(f"**音乐BPM**: {data['bpm_range'][0]}-{data['bpm_range'][1]}")
                if st.button(f"使用此风格", key=f"use_vstyle_{name}", use_container_width=True):
                    st.toast(f"已选择风格: {name}")

    with tab2:
        for name, data in mgr.get_templates().items():
            with st.expander(f"📐 {name}"):
                st.write(f"**比例**: {data['aspect_ratio']}")
                st.write(f"**分辨率**: {data['resolution']}")
                st.write(f"**时长**: {data['duration']}")
                st.write(f"**帧率**: {data['fps']}fps")
                st.caption(f"💡 {data['tip']}")

    with tab3:
        genre = st.selectbox("选择你的题材", ["冒险", "校园", "热血", "都市", "悬疑", "爱情", "古风", "修仙", "科幻", "治愈", "搞笑"])
        suitable = mgr.get_suitable_styles(genre)
        if suitable:
            for s in suitable:
                st.success(f"{s['icon']} **{s['name']}** — 推荐用于{genre}题材")
        else:
            st.info("暂无特别推荐，可自由选择风格")
