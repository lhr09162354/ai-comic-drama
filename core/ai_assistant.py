# -*- coding: utf-8 -*-
"""
AI助手系统 v34 - 合并模块
整合AI写作助手和AI对话式创作助手
"""

import streamlit as st
import json
import random
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Suggestion:
    """创作建议"""
    type: str
    content: str
    confidence: float
    options: List[str] = None
    metadata: Dict = None


class AIWritingAssistant:
    """AI写作助手"""

    def __init__(self):
        self.conversation_history = []
        self.current_context = {}

    def analyze_context(self, script: str, characters: List[Dict]) -> Dict:
        """分析当前上下文"""
        return {
            "script_length": len(script),
            "scene_count": script.count("【") + script.count("第"),
            "dialogue_ratio": script.count("：") / max(len(script), 1),
            "characters": characters,
            "last_dialogue": self._get_last_dialogue(script),
            "last_scene": self._get_last_scene(script),
            "genre": self._detect_genre(script),
        }

    def _get_last_dialogue(self, script: str) -> str:
        lines = script.split("：")
        return lines[-1].strip() if lines else ""

    def _get_last_scene(self, script: str) -> str:
        scenes = script.split("【")
        return scenes[-1].strip() if scenes else ""

    def _detect_genre(self, script: str) -> str:
        keywords = {
            "恋爱": ["爱", "喜欢", "心动", "甜蜜"], "冒险": ["冒险", "战斗", "挑战", "勇气"],
            "悬疑": ["谜", "真相", "线索", "可疑"], "奇幻": ["魔法", "修炼", "异世界", "仙"],
        }
        for genre, kws in keywords.items():
            if any(kw in script for kw in kws):
                return genre
        return "通用"

    def generate_suggestions(self, context: Dict) -> List[Suggestion]:
        """生成创作建议"""
        suggestions = []
        genre = context.get("genre", "通用")

        if context["dialogue_ratio"] < 0.2:
            suggestions.append(Suggestion("对话", "增加角色对话，让角色更加鲜活", 0.8))

        if context["scene_count"] < 3:
            suggestions.append(Suggestion("场景", "可以增加场景切换，丰富故事节奏", 0.7))

        suggestions.append(Suggestion("剧情", f"当前{genre}风格，可以考虑加入反转情节", 0.75))

        return suggestions

    def generate_plot_continuation(self, script: str, direction: str = "auto") -> Dict:
        """生成剧情续写"""
        directions = {
            "twist": "加入意想不到的反转",
            "escalation": "升级冲突和紧张感",
            "resolution": "逐步解决冲突",
            "comedy": "加入轻松搞笑的情节",
            "suspense": "制造悬念和伏笔",
        }
        return {
            "direction": direction,
            "suggestion": directions.get(direction, "继续推进主线剧情"),
            "confidence": round(random.uniform(0.6, 0.9), 2),
            "options": list(directions.keys()),
        }

    def generate_character_dialogue(self, character: Dict, context: str = "") -> Dict:
        """生成角色对话"""
        name = character.get("name", "角色")
        personality = character.get("personality", "温和")
        return {
            "character": name,
            "dialogue": f"[{name}的对话内容 - 基于{personality}性格]",
            "emotion": random.choice(["开心", "紧张", "平静", "激动"]),
            "confidence": round(random.uniform(0.6, 0.9), 2),
        }


class AIChatAssistant:
    """AI对话式创作助手"""

    def __init__(self):
        self.conversation_history = []
        self.current_context = {}
        self.modes = {
            "智能问答": {"icon": "🎯", "desc": "回答创作相关问题"},
            "场景联想": {"icon": "💭", "desc": "根据当前场景联想后续发展"},
            "角色对话": {"icon": "💬", "desc": "生成角色对话"},
            "情节推荐": {"icon": "📖", "desc": "推荐剧情发展方向"},
            "写作教练": {"icon": "✍️", "desc": "指导改进创作技巧"},
        }

    def chat(self, message: str, context: Dict = None) -> str:
        """对话处理"""
        self.conversation_history.append({"role": "user", "content": message})
        response = self._generate_response(message, context)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def _generate_response(self, message: str, context: Dict = None) -> str:
        ctx = context or {}
        if "角色" in message or "对话" in message:
            return "可以为角色生成符合性格的对话，请告诉我想让哪个角色说什么？"
        elif "剧情" in message or "故事" in message:
            return "可以帮你规划剧情走向。当前是哪种类型的故事？想要反转、升级还是和解？"
        elif "画面" in message or "分镜" in message:
            return "分镜设计方面，建议注意景别变化和构图平衡。需要具体的分镜建议吗？"
        elif "问题" in message or "怎么办" in message:
            return "创作遇到瓶颈很正常！试试换个视角，或者让角色做出意想不到的选择。"
        return "我是你的AI创作助手，可以帮你生成对话、规划剧情、设计分镜等。有什么需要的？"


class OneClickGenerator:
    """一键生成器"""

    def generate_full_episode(self, template: str, characters: List[Dict], style: str = "manga") -> Dict:
        """一键生成完整一集"""
        return {
            "template": template, "style": style,
            "characters": len(characters),
            "scenes": random.randint(5, 12),
            "estimated_length": f"{random.randint(3, 8)}分钟",
            "status": "ready",
        }


def render_ai_chat_page():
    """AI助手页面"""
    st.header("💬 AI创作助手")
    st.caption("智能问答、场景联想、角色对话、情节推荐")

    assistant = AIChatAssistant()

    tab1, tab2 = st.tabs(["💬 对话模式", "✍️ 写作助手"])

    with tab1:
        mode = st.selectbox("创作模式", list(assistant.modes.keys()),
                            format_func=lambda x: f"{assistant.modes[x]['icon']} {x}")
        st.caption(assistant.modes[mode]["desc"])

        if "ai_chat_messages" not in st.session_state:
            st.session_state.ai_chat_messages = []

        for msg in st.session_state.ai_chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_input = st.chat_input("输入你的问题或创作需求...")
        if user_input:
            st.session_state.ai_chat_messages.append({"role": "user", "content": user_input})
            response = assistant.chat(user_input)
            st.session_state.ai_chat_messages.append({"role": "assistant", "content": response})
            st.rerun()

    with tab2:
        writing = AIWritingAssistant()
        script = st.text_area("当前剧本", height=150, key="writing_script")
        if st.button("分析并建议", use_container_width=True):
            context = writing.analyze_context(script, [])
            suggestions = writing.generate_suggestions(context)
            for sug in suggestions:
                st.info(f"**{sug.type}建议** (置信度: {sug.confidence:.0%}): {sug.content}")

        st.divider()
        direction = st.selectbox("续写方向", ["auto", "twist", "escalation", "resolution", "comedy", "suspense"])
        if st.button("生成续写建议"):
            result = writing.generate_plot_continuation(script, direction)
            st.write(f"**方向**: {result['suggestion']}")
            st.write(f"**置信度**: {result['confidence']:.0%}")
