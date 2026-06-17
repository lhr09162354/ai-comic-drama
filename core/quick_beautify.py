# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 一键美化
自动优化作品封面和标题
"""

import re
from typing import Dict, Optional, List


# ============ 标题美化数据 ============

TITLE_PATTERNS = {
    "甜宠": {
        "prefixes": ["甜度爆表", "满级甜宠", "超甜预警", "心动满分"],
        "templates": [
            "{prefix}《{title}》",
            "《{prefix}{title}》",
            "{title}·{prefix}",
        ],
        "emoji": ["💕", "💗", "🍬", "🍓", "🌸"],
    },
    "悬疑": {
        "prefixes": ["谜案追踪", "暗夜迷局", "真相倒计时", "不可说的秘密"],
        "templates": [
            "{prefix}《{title}》",
            "《{title}》—{prefix}",
            "{title}|{prefix}",
        ],
        "emoji": ["🔍", "🌑", "🔑", "⚠️", "🎭"],
    },
    "热血": {
        "prefixes": ["燃爆全场", "巅峰之路", "逆风翻盘", "破晓之战"],
        "templates": [
            "{prefix}《{title}》",
            "《{prefix}{title}》",
            "{title}·{prefix}",
        ],
        "emoji": ["⚔️", "🔥", "💪", "⚡", "🏆"],
    },
    "科幻": {
        "prefixes": ["星际纪元", "量子迷途", "未来序章", "赛博觉醒"],
        "templates": [
            "{prefix}《{title}》",
            "《{title}》—{prefix}",
            "{title}|{prefix}",
        ],
        "emoji": ["🚀", "🌌", "🤖", "💫", "🔭"],
    },
    "日常": {
        "prefixes": ["温馨记录", "日常小确幸", "生活万岁", "人间值得"],
        "templates": [
            "{prefix}《{title}》",
            "《{title}》·{prefix}",
            "{title}—{prefix}",
        ],
        "emoji": ["☀️", "☕", "📖", "🌻", "🐱"],
    },
    "古风": {
        "prefixes": ["风华录", "千秋梦", "锦绣章", "山河志"],
        "templates": [
            "《{prefix}·{title}》",
            "{title}·{prefix}",
            "《{title}》{prefix}",
        ],
        "emoji": ["🏯", "📜", "🎋", "🪷", "🗡️"],
    },
}

# 封面配色方案
COVER_COLOR_SCHEMES = {
    "甜宠": {
        "primary": "#FF6B9D",
        "secondary": "#C44569",
        "bg_gradient": ["#FFF0F5", "#FFE4E1"],
        "text_color": "#8B2252",
    },
    "悬疑": {
        "primary": "#2C3E50",
        "secondary": "#E74C3C",
        "bg_gradient": ["#1A1A2E", "#16213E"],
        "text_color": "#FFFFFF",
    },
    "热血": {
        "primary": "#E74C3C",
        "secondary": "#F39C12",
        "bg_gradient": ["#FF6B6B", "#FFE66D"],
        "text_color": "#FFFFFF",
    },
    "科幻": {
        "primary": "#00D4FF",
        "secondary": "#7B2FF7",
        "bg_gradient": ["#0C0C1D", "#1A1A3E"],
        "text_color": "#00D4FF",
    },
    "日常": {
        "primary": "#F8B500",
        "secondary": "#FF6B6B",
        "bg_gradient": ["#FFF8E7", "#FFE4B5"],
        "text_color": "#8B6914",
    },
    "古风": {
        "primary": "#C0392B",
        "secondary": "#D4AC0D",
        "bg_gradient": ["#FDF5E6", "#FAEBD7"],
        "text_color": "#8B0000",
    },
}


class QuickBeautify:
    """一键美化"""

    def __init__(self):
        pass

    def beautify_title(self, title: str, genre: str = "甜宠") -> Dict:
        """美化标题"""
        pattern = TITLE_PATTERNS.get(genre, TITLE_PATTERNS["日常"])
        import random

        prefix = random.choice(pattern["prefixes"])
        template = random.choice(pattern["templates"])
        emoji = random.choice(pattern["emoji"])

        beautified = template.format(prefix=prefix, title=title)

        # 生成多个候选
        candidates = []
        for tmpl in pattern["templates"][:3]:
            for pref in pattern["prefixes"][:2]:
                candidates.append(tmpl.format(prefix=pref, title=title))

        return {
            "original": title,
            "beautified": f"{emoji} {beautified}",
            "candidates": candidates,
            "genre": genre,
            "emoji_options": pattern["emoji"],
        }

    def get_cover_scheme(self, genre: str = "甜宠") -> Dict:
        """获取封面配色方案"""
        return COVER_COLOR_SCHEMES.get(genre, COVER_COLOR_SCHEMES["日常"])

    def auto_detect_genre(self, title: str, description: str = "") -> str:
        """自动检测题材类型"""
        text = (title + " " + description).lower()
        genre_keywords = {
            "甜宠": ["甜", "爱", "恋", "宠", "糖", "婚", "蜜"],
            "悬疑": ["谜", "案", "杀", "暗", "密", "诡", "凶"],
            "热血": ["战", "斗", "拳", "胜", "燃", "冠", "热血"],
            "科幻": ["星", "宇", "未来", "机甲", "AI", "赛博"],
            "古风": ["宫", "帝", "妃", "朝", "古", "剑", "侠"],
            "日常": ["日", "生活", "咖啡", "猫", "花", "饭"],
        }
        best_genre = "日常"
        best_score = 0
        for genre, keywords in genre_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_genre = genre
        return best_genre

    def generate_cover_prompt(self, title: str, genre: str = None, description: str = "") -> str:
        """生成封面图提示词"""
        if not genre:
            genre = self.auto_detect_genre(title, description)
        scheme = self.get_cover_scheme(genre)

        return (
            f"Professional comic book cover, {genre} style, "
            f"title '{title}', "
            f"color scheme: primary {scheme['primary']}, secondary {scheme['secondary']}, "
            f"background gradient from {scheme['bg_gradient'][0]} to {scheme['bg_gradient'][1]}, "
            f"high quality, detailed, eye-catching design"
        )


def render_quick_beautify_page():
    """渲染一键美化页面"""
    import streamlit as st

    beautify = QuickBeautify()

    st.header("✨ 一键美化")
    st.caption("自动优化作品封面和标题，让作品更吸引眼球")

    tab1, tab2, tab3 = st.tabs(["🏷️ 标题美化", "🎨 封面配色", "🤖 智能检测"])

    with tab1:
        st.subheader("标题美化")
        title = st.text_input("输入原始标题", value="", key="beautify_title")
        genre = st.selectbox("选择题材", list(TITLE_PATTERNS.keys()), key="beautify_genre")

        if st.button("✨ 一键美化标题", type="primary", use_container_width=True):
            if title:
                result = beautify.beautify_title(title, genre)
                st.success(f"美化结果: {result['beautified']}")
                st.write("**候选标题:**")
                for i, candidate in enumerate(result["candidates"], 1):
                    st.write(f"{i}. {candidate}")
            else:
                st.warning("请先输入标题")

    with tab2:
        st.subheader("封面配色方案")
        cover_genre = st.selectbox("选择题材风格", list(COVER_COLOR_SCHEMES.keys()), key="cover_genre")
        scheme = beautify.get_cover_scheme(cover_genre)
        st.json(scheme)
        st.write(f"主色: `{scheme['primary']}` | 辅色: `{scheme['secondary']}`")
        st.write(f"背景渐变: `{scheme['bg_gradient'][0]}` → `{scheme['bg_gradient'][1]}`")
        st.write(f"文字色: `{scheme['text_color']}`")

    with tab3:
        st.subheader("智能题材检测")
        detect_title = st.text_input("输入标题", key="detect_title")
        detect_desc = st.text_input("输入简介(可选)", key="detect_desc")

        if st.button("🔍 自动检测", use_container_width=True):
            if detect_title:
                detected = beautify.auto_detect_genre(detect_title, detect_desc)
                st.success(f"检测到的题材: **{detected}**")

                # 同时美化
                result = beautify.beautify_title(detect_title, detected)
                st.info(f"建议标题: {result['beautified']}")
            else:
                st.warning("请输入标题")
