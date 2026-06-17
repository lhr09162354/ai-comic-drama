# -*- coding: utf-8 -*-
"""
AI漫剧自动生成器 v34 - 配置管理
全面优化升级：模块合并、体验优化、新功能增加、性能提升
"""

import os
from pathlib import Path

# 项目基础路径
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
STATIC_DIR = BASE_DIR / "static"

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DALLE_API_KEY = os.getenv("DALLE_API_KEY", OPENAI_API_KEY)

# 版本信息
VERSION = "v36"
VERSION_DESC = "关系图谱·节奏控制·运镜建议"

# ============ 语言与模板配置 ============

DEFAULT_LANGUAGE = "zh-CN"

SUPPORTED_LANGUAGES = {
    "zh-CN": "简体中文", "zh-TW": "繁體中文", "en": "English",
    "ja": "日本語", "ko": "한국어", "fr": "Français",
    "de": "Deutsch", "es": "Español", "pt": "Português",
    "ru": "Русский", "ar": "العربية", "hi": "हिन्दी",
    "th": "ไทย", "vi": "Tiếng Việt", "id": "Bahasa Indonesia",
}

STORY_TEMPLATES = {
    "romance": {"theme": "💕 甜宠恋爱", "desc": "霸道总裁爱上我，甜蜜日常撒糖不停", "style": "甜蜜温馨"},
    "adventure": {"theme": "⚔️ 热血冒险", "desc": "少年踏上征途，一路披荆斩棘", "style": "热血激昂"},
    "mystery": {"theme": "🔍 悬疑推理", "desc": "层层迷雾中的真相，抽丝剥茧", "style": "紧张刺激"},
    "fantasy": {"theme": "🌟 奇幻修仙", "desc": "修仙问道，探索无限可能", "style": "神秘绚丽"},
    "comedy": {"theme": "😄 搞笑日常", "desc": "轻松搞笑的日常生活", "style": "轻松幽默"},
    "scifi": {"theme": "🚀 科幻未来", "desc": "星际探索，未来世界冒险", "style": "科技感"},
    "campus": {"theme": "🎒 校园青春", "desc": "热血校园，青春无悔", "style": "青春活力"},
    "workplace": {"theme": "💼 职场逆袭", "desc": "小人物大逆袭，职场风云", "style": "现实主义"},
    "historical": {"theme": "🏯 古风宫斗", "desc": "宫廷权谋，步步为营", "style": "古典雅致"},
    "horror": {"theme": "👻 恐怖惊悚", "desc": "深夜怪谈，让人背脊发凉", "style": "阴森恐怖"},
    "sports": {"theme": "⚽ 竞技热血", "desc": "赛场上的荣耀与汗水", "style": "热血拼搏"},
    "healing": {"theme": "🌸 治愈暖心", "desc": "温暖治愈的小确幸", "style": "温馨治愈"},
}

ART_STYLES = {
    "manga": {"name": "🎌 日系漫画", "prompt": "Japanese manga style"},
    "manhwa": {"name": "🇰🇷 韩系漫画", "prompt": "Korean manhwa style"},
    "manhua": {"name": "🇨🇳 国风漫画", "prompt": "Chinese manhua style"},
    "watercolor": {"name": "🎨 水彩画风", "prompt": "watercolor illustration"},
    "pixel": {"name": "👾 像素风", "prompt": "pixel art style"},
    "realistic": {"name": "📷 写实风", "prompt": "photorealistic style"},
    "chibi": {"name": "🧸 Q版萌系", "prompt": "chibi cute style"},
    "cyberpunk": {"name": "🌆 赛博朋克", "prompt": "cyberpunk neon style"},
}

# ============ 核心功能配置 ============

CONTENT_ANALYSIS_CONFIG = {
    "enabled": True,
    "analysis_depth": "deep",
    "metrics": {
        "engagement_score": True, "emotion_curve": True,
        "plot_complexity": True, "character_arc": True, "pacing_analysis": True,
    },
    "real_time": {"enabled": True, "update_interval": 5},
    "export_formats": ["json", "csv", "pdf"],
    "heatmap": {"enabled": True, "colorscale": "viridis", "resolution": "high"},
}

MULTIMODAL_CONFIG = {
    "voice_input": {"enabled": True, "language": "zh-CN", "mode": "continuous", "wake_word": "小漫"},
    "gesture_control": {"enabled": True, "camera_index": 0, "recognition_model": "mediapipe"},
    "sketch_generation": {"enabled": True, "style_transfer": True, "auto_complete": True},
    "ai_chat": {"enabled": True, "model": "gpt-4", "context_window": 10},
    "ar_preview": {"enabled": False, "platform": "webxr", "render_quality": "medium"},
}

CREATOR_CENTER_CONFIG = {
    "profile": {"avatar_required": True, "bio_max_length": 500, "portfolio_enabled": True},
    "works": {"max_works": 100, "categories": ["漫画", "动画", "同人", "原创", "教程"], "auto_tags": True},
}

# ============ v34 新增配置 ============

# 智能助手配置
SMART_ASSISTANT_CONFIG = {
    "enabled": True,
    "floating_button": True,
    "quick_actions": [
        {"id": "new_project", "label": "新建项目", "icon": "➕", "shortcut": "Ctrl+N"},
        {"id": "quick_generate", "label": "快速生成", "icon": "⚡", "shortcut": "Ctrl+G"},
        {"id": "save_draft", "label": "保存草稿", "icon": "💾", "shortcut": "Ctrl+S"},
        {"id": "export", "label": "导出作品", "icon": "📤", "shortcut": "Ctrl+E"},
        {"id": "share", "label": "分享", "icon": "🔗", "shortcut": "Ctrl+Shift+S"},
        {"id": "help", "label": "使用帮助", "icon": "❓", "shortcut": "F1"},
    ],
    "tips_interval": 30,
    "context_aware": True,
}

# 草稿箱配置
DRAFT_CONFIG = {
    "auto_save_interval": 60,
    "max_drafts": 50,
    "preview_enabled": True,
    "thumbnail_size": [200, 150],
    "retention_days": 90,
}

# 作品统计配置
WORK_STATISTICS_CONFIG = {
    "enabled": True,
    "metrics": ["views", "likes", "shares", "comments", "favorites", "completion_rate"],
    "trend_analysis": True,
    "comparison_enabled": True,
    "export_formats": ["json", "csv"],
}

# 性能优化配置
PERFORMANCE_CONFIG = {
    "image_cache_size": 100,
    "lazy_load_threshold": 10,
    "debounce_ms": 300,
    "batch_api_calls": True,
    "max_concurrent_requests": 5,
    "render_chunk_size": 20,
}

# 页面导航配置（优化后的分组导航）
NAV_GROUPS = {
    "创作": {
        "icon": "🎨",
        "pages": [
            ("创作工坊", "🎨"), ("故事引擎", "📖"), ("剧本续写", "📝"),
            ("角色管理", "👥"), ("角色对话", "💬"), ("角色关系", "🕸️"),
            ("角色故事线", "📚"), ("世界观", "🌍"), ("互动剧情", "🎭"),
        ]
    },
    "制作": {
        "icon": "🎬",
        "pages": [
            ("配音系统", "🎙️"), ("视频生成", "🎬"), ("视频风格", "🎞️"),
            ("运镜建议", "🎥"), ("智能剪辑", "✂️"), ("特效库", "✨"),
            ("画质增强", "🖼️"), ("BGM推荐", "🎵"),
        ]
    },
    "运营": {
        "icon": "📊",
        "pages": [
            ("数据中心", "📊"), ("AI分析", "🔍"), ("选题中心", "💡"),
            ("发布系统", "📤"), ("营销工具", "📣"), ("粉丝运营", "👥"),
        ]
    },
    "社区": {
        "icon": "💬",
        "pages": [
            ("社区", "💬"), ("观众互动", "🎉"), ("互动增强", "🎮"),
            ("社交裂变", "🔥"), ("极速分享", "🚀"), ("版权保护", "🔒"),
        ]
    },
    "变现": {
        "icon": "💰",
        "pages": [
            ("变现中心", "💰"), ("收益中心", "💎"), ("会员中心", "👑"),
        ]
    },
    "成长": {
        "icon": "🏆",
        "pages": [
            ("创作者中心", "👤"), ("成长体系", "🌟"), ("培训学院", "🎓"),
            ("创作工具", "🛠️"), ("成就系统", "🏅"),
        ]
    },
    "工具": {
        "icon": "🔧",
        "pages": [
            ("灵感库", "💡"), ("素材广场", "🏪"), ("一键美化", "✨"),
            ("批量处理", "📚"), ("版本历史", "📜"), ("素材库", "📦"),
            ("校对工具", "✍️"), ("多语言", "🌐"), ("IP改编", "📚"),
            ("智能客服", "🤖"), ("智能助手", "💡"),
            ("全局搜索", "🔍"), ("通知中心", "🔔"), ("主题设置", "🎨"),
            ("节奏控制", "🎵"), ("剧情时间轴", "📅"),
            ("海报生成", "🖼️"), ("作品合集", "📚"),
        ]
    },
}
