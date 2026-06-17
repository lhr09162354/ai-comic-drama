# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 新用户引导
首次使用引导流程，让新用户体验更顺畅
"""

from typing import Dict, List


# ============ 引导步骤 ============

ONBOARDING_STEPS = [
    {
        "step": 1,
        "title": "欢迎来到AI漫剧生成器！",
        "desc": "在这里，你可以用AI创作属于你的漫剧作品。让我们花1分钟了解基本功能吧！",
        "icon": "🎉",
        "tip": "点击「下一步」继续",
    },
    {
        "step": 2,
        "title": "选择故事模板",
        "desc": "我们提供了12种故事模板，从甜宠到悬疑，从热血到治愈，总有一款适合你。选择模板后AI会帮你快速生成剧本！",
        "icon": "📖",
        "tip": "试试在创作工坊中选择一个模板",
    },
    {
        "step": 3,
        "title": "设定角色",
        "desc": "添加你的角色——设定性格、外貌和声线。角色设定越详细，AI生成的对话和行为就越精准！",
        "icon": "👥",
        "tip": "3-5个角色是故事的最佳人数",
    },
    {
        "step": 4,
        "title": "AI创作助手",
        "desc": "不确定怎么写？让AI帮你！点击「AI生成剧本」按钮，AI会根据你的模板和角色自动创作。你还可以让AI优化、续写、改写。",
        "icon": "🤖",
        "tip": "AI是你的创作搭档，不是替代品",
    },
    {
        "step": 5,
        "title": "生成画面与视频",
        "desc": "剧本写好后，可以生成分镜画面、配音、视频。支持多种画风和视频风格，一键出片！",
        "icon": "🎬",
        "tip": "试试不同画风，找到最适合你故事的风格",
    },
    {
        "step": 6,
        "title": "分享与互动",
        "desc": "作品完成后，可以分享到社区、让观众投票选择剧情走向。还可以通过订阅和付费内容获得收益！",
        "icon": "🚀",
        "tip": "好的互动能让观众成为你故事的一部分",
    },
]

QUICK_START_OPTIONS = [
    {"title": "⚡ 3分钟速成", "desc": "用一个现成模板快速生成你的第一部漫剧", "action": "创作工坊"},
    {"title": "🎨 自由创作", "desc": "从空白开始，一步一步创作你的故事", "action": "创作工坊"},
    {"title": "💡 找灵感", "desc": "浏览灵感库，找到让你心动的故事点子", "action": "灵感库"},
    {"title": "📚 学习教程", "desc": "看看其他创作者的技巧和经验", "action": "培训学院"},
]


class OnboardingManager:
    """新用户引导管理"""

    def __init__(self):
        pass

    def get_steps(self) -> List[Dict]:
        return ONBOARDING_STEPS

    def get_quick_start_options(self) -> List[Dict]:
        return QUICK_START_OPTIONS

    def is_new_user(self) -> bool:
        """判断是否新用户（基于是否有作品）"""
        import streamlit as st
        return not st.session_state.get("projects") and not st.session_state.get("current_script")

    def get_step(self, step_num: int) -> Dict:
        for s in ONBOARDING_STEPS:
            if s["step"] == step_num:
                return s
        return ONBOARDING_STEPS[-1]


def render_onboarding():
    """渲染新用户引导"""
    import streamlit as st

    mgr = OnboardingManager()

    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 0

    if st.session_state.onboarding_step < len(ONBOARDING_STEPS):
        step = ONBOARDING_STEPS[st.session_state.onboarding_step]

        # 步骤展示
        st.markdown(f"### {step['icon']} {step['title']}")
        st.write(step["desc"])
        st.caption(f"💡 {step['tip']}")

        # 进度条
        progress = (st.session_state.onboarding_step + 1) / len(ONBOARDING_STEPS)
        st.progress(progress, text=f"步骤 {st.session_state.onboarding_step + 1}/{len(ONBOARDING_STEPS)}")

        c1, c2 = st.columns(2)
        with c1:
            if st.session_state.onboarding_step > 0:
                if st.button("⬅️ 上一步", use_container_width=True):
                    st.session_state.onboarding_step -= 1
                    st.rerun()
        with c2:
            if st.button("下一步 ➡️", use_container_width=True, type="primary"):
                st.session_state.onboarding_step += 1
                st.rerun()

        st.divider()

    # 快速开始选项
    st.subheader("🚀 快速开始")
    for opt in mgr.get_quick_start_options():
        with st.expander(f"{opt['title']}"):
            st.write(opt["desc"])
            if st.button(f"前往 {opt['action']}", key=f"goto_{opt['action']}", use_container_width=True):
                st.session_state.active_tab = opt["action"]
                st.rerun()
