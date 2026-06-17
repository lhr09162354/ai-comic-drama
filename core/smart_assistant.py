# -*- coding: utf-8 -*-
"""
智能助手系统 v34 - 悬浮按钮 + 快捷指令 + 使用帮助
提供随时可用的AI创作辅助和操作引导
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random


class SmartAssistant:
    """智能助手 - 全局浮动辅助系统"""

    def __init__(self):
        self.tips_db = self._init_tips()
        self.faq_db = self._init_faq()
        self.shortcuts = self._init_shortcuts()
        self.context_help = self._init_context_help()
        self._init_session_state()

    def _init_session_state(self):
        defaults = {
            "assistant_open": False,
            "assistant_tab": "help",
            "tips_index": 0,
            "tips_dismissed": set(),
            "assistant_history": [],
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                if isinstance(v, set):
                    st.session_state[k] = list(v)
                else:
                    st.session_state[k] = v

    def _init_tips(self) -> List[Dict]:
        return [
            {"id": "tip_1", "title": "快速开始创作", "content": "选择故事模板，输入关键词，一键生成剧本和画面",
             "category": "入门", "icon": "🚀"},
            {"id": "tip_2", "title": "角色对话生成", "content": "在角色管理中设定性格后，AI可以自动生成符合人设的对话",
             "category": "角色", "icon": "💬"},
            {"id": "tip_3", "title": "分支剧情玩法", "content": "在故事引擎中创建分支节点，让观众选择剧情走向",
             "category": "互动", "icon": "🔀"},
            {"id": "tip_4", "title": "一键配音", "content": "选择角色声线，AI自动为对白生成配音和音效",
             "category": "配音", "icon": "🎙️"},
            {"id": "tip_5", "title": "智能剪辑", "content": "上传视频后，AI自动检测精彩片段并生成预告",
             "category": "剪辑", "icon": "✂️"},
            {"id": "tip_6", "title": "草稿自动保存", "content": "创作内容每分钟自动保存，随时恢复进度",
             "category": "效率", "icon": "💾"},
            {"id": "tip_7", "title": "多语言发布", "content": "一键将作品翻译为多国语言，拓展海外受众",
             "category": "发布", "icon": "🌐"},
            {"id": "tip_8", "title": "数据看板", "content": "在数据中心查看作品播放量、点赞趋势等核心指标",
             "category": "数据", "icon": "📊"},
            {"id": "tip_9", "title": "批量生成", "content": "设置模板后可批量生成多集内容，提升创作效率",
             "category": "效率", "icon": "⚡"},
            {"id": "tip_10", "title": "IP改编助手", "content": "将小说/漫画等IP智能改编为漫剧剧本",
             "category": "改编", "icon": "📚"},
        ]

    def _init_faq(self) -> List[Dict]:
        return [
            {"q": "如何创建第一个作品？",
             "a": "点击「创作工坊」，选择故事模板或自定义输入，设置角色和画风，点击生成即可。"},
            {"q": "如何给角色配音？",
             "a": "进入「配音系统」页面，选择角色和声线，AI会自动为对白生成语音。"},
            {"q": "如何导出视频？",
             "a": "在「视频生成」页面选择输出格式和质量，点击导出。支持MP4、GIF等格式。"},
            {"q": "草稿保存在哪里？",
             "a": "草稿自动保存在本地，可在「版本历史」中查看和恢复所有保存记录。"},
            {"q": "如何分享作品？",
             "a": "在「极速分享」页面，选择目标平台，一键生成适配格式并分享。"},
            {"q": "如何使用分支剧情？",
             "a": "在「互动剧情」中创建分支节点，设置选择项和对应剧情，观众可以交互选择。"},
            {"q": "如何查看作品数据？",
             "a": "进入「数据中心」或「作品统计」，查看播放量、点赞数等核心指标和趋势。"},
            {"q": "如何参与社区互动？",
             "a": "在「社区」页面浏览作品、发表评论、关注创作者、参与活动。"},
        ]

    def _init_shortcuts(self) -> List[Dict]:
        return [
            {"id": "new_project", "label": "新建项目", "icon": "➕", "action": "new_project",
             "description": "快速创建新漫剧项目"},
            {"id": "quick_generate", "label": "快速生成", "icon": "⚡", "action": "quick_generate",
             "description": "使用当前设置一键生成内容"},
            {"id": "save_draft", "label": "保存草稿", "icon": "💾", "action": "save_draft",
             "description": "立即保存当前创作进度"},
            {"id": "export", "label": "导出作品", "icon": "📤", "action": "export",
             "description": "导出当前项目为视频/图片"},
            {"id": "share", "label": "极速分享", "icon": "🔗", "action": "share",
             "description": "分享到社交平台"},
            {"id": "preview", "label": "预览效果", "icon": "👁️", "action": "preview",
             "description": "预览当前作品效果"},
            {"id": "ai_enhance", "label": "AI优化", "icon": "✨", "action": "ai_enhance",
             "description": "使用AI优化剧本和画面"},
            {"id": "undo", "label": "撤销操作", "icon": "↩️", "action": "undo",
             "description": "撤销上一步操作"},
        ]

    def _init_context_help(self) -> Dict:
        return {
            "创作": {"tips": ["选择模板后可自定义修改", "角色设定越详细，AI生成越精准"],
                     "related_features": ["角色管理", "故事引擎", "AI优化"]},
            "故事引擎": {"tips": ["使用分支节点增加互动性", "情感曲线帮助把控节奏"],
                         "related_features": ["互动剧情", "世界观"]},
            "配音系统": {"tips": ["选择匹配角色性格的声线", "可以调整语速和情感"],
                         "related_features": ["特效库", "视频生成"]},
            "视频生成": {"tips": ["竖屏9:16适合短视频平台", "横屏16:9适合长视频"],
                         "related_features": ["智能剪辑", "画质增强"]},
            "智能剪辑": {"tips": ["AI自动检测精彩片段", "支持多种转场和特效"],
                         "related_features": ["视频生成", "特效库"]},
        }

    def get_tip(self) -> Optional[Dict]:
        """获取当前提示"""
        dismissed = set(st.session_state.get("tips_dismissed", []))
        available = [t for t in self.tips_db if t["id"] not in dismissed]
        if not available:
            st.session_state.tips_dismissed = []
            available = self.tips_db
        idx = st.session_state.get("tips_index", 0) % len(available)
        return available[idx]

    def next_tip(self):
        st.session_state.tips_index = st.session_state.get("tips_index", 0) + 1

    def dismiss_tip(self, tip_id: str):
        dismissed = list(st.session_state.get("tips_dismissed", []))
        if tip_id not in dismissed:
            dismissed.append(tip_id)
        st.session_state.tips_dismissed = dismissed

    def get_context_help(self, page: str) -> Dict:
        return self.context_help.get(page, {"tips": [], "related_features": []})

    def search_help(self, query: str) -> List[Dict]:
        results = []
        q = query.lower()
        for faq in self.faq_db:
            if q in faq["q"].lower() or q in faq["a"].lower():
                results.append({"type": "faq", **faq})
        for tip in self.tips_db:
            if q in tip["title"].lower() or q in tip["content"].lower():
                results.append({"type": "tip", **tip})
        return results[:8]

    def render_floating_button(self):
        """渲染悬浮按钮"""
        if st.button("💡 智能助手", key="assistant_fab", use_container_width=True):
            st.session_state.assistant_open = not st.session_state.assistant_open

    def render_assistant_panel(self, current_page: str = "创作"):
        """渲染助手面板"""
        if not st.session_state.get("assistant_open", False):
            return

        with st.container():
            st.markdown("---")
            st.markdown("### 💡 智能助手")

            tab_help, tab_shortcut, tab_faq = st.tabs(["📖 帮助", "⚡ 快捷", "❓ 常见问题"])

            with tab_help:
                context = self.get_context_help(current_page)
                if context["tips"]:
                    st.markdown(f"**{current_page} 页面提示：**")
                    for tip in context["tips"]:
                        st.markdown(f"- 💡 {tip}")
                    if context["related_features"]:
                        st.markdown("**相关功能：** " + " · ".join(context["related_features"]))

                st.divider()
                tip = self.get_tip()
                if tip:
                    st.info(f"{tip['icon']} **{tip['title']}**\n\n{tip['content']}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("下一个提示", key="next_tip_btn"):
                            self.next_tip()
                            st.rerun()
                    with c2:
                        if st.button("关闭此提示", key="dismiss_tip_btn"):
                            self.dismiss_tip(tip["id"])
                            st.rerun()

            with tab_shortcut:
                st.markdown("**快捷操作**")
                cols = st.columns(4)
                for i, sc in enumerate(self.shortcuts):
                    with cols[i % 4]:
                        if st.button(f"{sc['icon']}\n{sc['label']}", key=f"sc_{sc['id']}", use_container_width=True):
                            st.toast(f"执行: {sc['label']}")
                            self._execute_shortcut(sc["action"])

            with tab_faq:
                search_q = st.text_input("🔍 搜索问题", key="assistant_search")
                if search_q:
                    results = self.search_help(search_q)
                    if results:
                        for r in results:
                            if r["type"] == "faq":
                                st.markdown(f"**{r['q']}**")
                                st.markdown(r["a"])
                            else:
                                st.markdown(f"{r.get('icon', '💡')} **{r.get('title', '')}**")
                                st.markdown(r.get("content", ""))
                    else:
                        st.info("未找到相关问题，请换个关键词试试")
                else:
                    for faq in self.faq_db[:5]:
                        with st.expander(faq["q"]):
                            st.markdown(faq["a"])

            if st.button("关闭助手 ✕", key="close_assistant"):
                st.session_state.assistant_open = False
                st.rerun()

    def _execute_shortcut(self, action: str):
        action_map = {
            "new_project": lambda: st.session_state.update(active_tab="创作"),
            "quick_generate": lambda: None,
            "save_draft": lambda: None,
            "export": lambda: st.session_state.update(active_tab="视频生成"),
            "share": lambda: st.session_state.update(active_tab="极速分享"),
            "preview": lambda: None,
            "ai_enhance": lambda: st.session_state.update(active_tab="画质增强"),
            "undo": lambda: None,
        }
        handler = action_map.get(action)
        if handler:
            handler()


def render_smart_assistant_page():
    """智能助手独立页面"""
    st.header("💡 智能助手中心")
    st.caption("AI创作辅助、使用指南、快捷操作")

    assistant = SmartAssistant()

    tab1, tab2, tab3, tab4 = st.tabs(["📖 使用指南", "⚡ 快捷指令", "❓ 常见问题", "🎯 创作技巧"])

    with tab1:
        st.subheader("快速入门")
        steps = [
            ("1️⃣ 选择模板", "从12种故事模板中选择，或自定义输入"),
            ("2️⃣ 设定角色", "定义角色性格、外貌、关系，让AI更精准"),
            ("3️⃣ 生成剧本", "AI根据设定自动生成完整剧本和分镜"),
            ("4️⃣ 配音配乐", "选择声线，AI自动生成配音和音效"),
            ("5️⃣ 导出分享", "一键导出视频，分享到各大平台"),
        ]
        for title, desc in steps:
            st.markdown(f"**{title}**\n\n{desc}")

        st.divider()
        st.subheader("功能导览")
        from config import NAV_GROUPS
        for group_name, group_info in NAV_GROUPS.items():
            with st.expander(f"{group_info['icon']} {group_name}"):
                for page_name, page_icon in group_info["pages"]:
                    st.markdown(f"- {page_icon} {page_name}")

    with tab2:
        st.subheader("快捷指令列表")
        for sc in assistant.shortcuts:
            st.markdown(f"**{sc['icon']} {sc['label']}** — {sc['description']}")

    with tab3:
        st.subheader("常见问题")
        search = st.text_input("搜索问题", key="faq_search_page")
        faqs = assistant.faq_db
        if search:
            faqs = [f for f in faqs if search.lower() in f["q"].lower() or search.lower() in f["a"].lower()]
        for faq in faqs:
            with st.expander(faq["q"]):
                st.markdown(faq["a"])

    with tab4:
        st.subheader("创作技巧")
        categories = {}
        for tip in assistant.tips_db:
            cat = tip.get("category", "其他")
            categories.setdefault(cat, []).append(tip)
        for cat, tips in categories.items():
            with st.expander(f"📂 {cat}"):
                for tip in tips:
                    st.markdown(f"{tip['icon']} **{tip['title']}**\n\n{tip['content']}")
