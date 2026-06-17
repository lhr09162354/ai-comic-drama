# -*- coding: utf-8 -*-
"""
v36: 角色故事线
为每个角色生成独立故事线，支持主线/支线/暗线
"""
import streamlit as st
from datetime import datetime
from typing import List, Optional


STORYLINE_TYPES = {
    "主线": {"emoji": "🌟", "color": "#FFD700", "desc": "角色核心故事，推动整体剧情"},
    "支线": {"emoji": "🌿", "color": "#4CAF50", "desc": "丰富角色背景，增加故事层次"},
    "暗线": {"emoji": "🌑", "color": "#9C27B0", "desc": "隐藏线索，后期反转揭示"},
    "成长线": {"emoji": "📈", "color": "#2196F3", "desc": "角色成长蜕变轨迹"},
    "感情线": {"emoji": "💕", "color": "#E91E63", "desc": "角色间情感发展"},
    "冲突线": {"emoji": "⚡", "color": "#F44336", "desc": "角色面临的对抗与矛盾"},
}

STORYLINE_TEMPLATES = {
    "逆袭": ["低谷起点→遭遇挫折→获得机遇→奋力崛起→成就自我"],
    "救赎": ["犯下错误→内心煎熬→寻找救赎→付出代价→获得原谅"],
    "成长": ["懵懂无知→遭遇困难→获得指引→历练成长→蜕变成熟"],
    "守护": ["发现威胁→决心守护→遭遇挑战→坚守信念→守护成功"],
    "复仇": ["遭受背叛→隐忍蓄力→步步为营→真相大白→完成复仇"],
    "寻找": ["失去重要之物→踏上寻找之路→经历磨难→发现真相→完成寻找"],
}


class CharacterStoryline:
    """角色故事线管理器"""

    def __init__(self):
        self.storylines = st.session_state.get("v36_storylines", [])

    def _save(self):
        st.session_state["v36_storylines"] = self.storylines

    def add_storyline(self, char_name, line_type, title, description, episodes="1-10",
                      key_events=None):
        storyline = {
            "char_name": char_name,
            "type": line_type,
            "title": title,
            "description": description,
            "episodes": episodes,
            "key_events": key_events or [],
            "created_at": datetime.now().strftime("%m-%d %H:%M"),
        }
        self.storylines.append(storyline)
        self._save()
        return storyline

    def remove_storyline(self, idx):
        if 0 <= idx < len(self.storylines):
            self.storylines.pop(idx)
            self._save()

    def get_for_character(self, char_name):
        return [s for s in self.storylines if s["char_name"] == char_name]

    def get_by_type(self, line_type):
        return [s for s in self.storylines if s["type"] == line_type]

    def auto_generate(self, char_name, personality="", template="成长"):
        """根据模板自动生成故事线"""
        template_steps = STORYLINE_TEMPLATES.get(template, STORYLINE_TEMPLATES["成长"])
        steps = template_steps[0].split("→")
        key_events = [f"第{i+1}阶段: {step}" for i, step in enumerate(steps)]
        storyline = self.add_storyline(
            char_name=char_name,
            line_type="主线",
            title=f"{char_name}的{template}之路",
            description=f"基于「{template}」模板生成的故事线",
            episodes=f"1-{len(steps)*3}",
            key_events=key_events,
        )
        return storyline

    def get_timeline_data(self, char_name=None):
        """获取时间轴数据"""
        lines = self.get_for_character(char_name) if char_name else self.storylines
        timeline = []
        for s in lines:
            info = STORYLINE_TYPES.get(s["type"], STORYLINE_TYPES["主线"])
            timeline.append({
                "char": s["char_name"],
                "type": s["type"],
                "emoji": info["emoji"],
                "title": s["title"],
                "episodes": s["episodes"],
            })
        return timeline


def render_character_storyline_page():
    """渲染角色故事线页面"""
    st.subheader("📚 角色故事线")
    st.caption("为每个角色规划独立故事线，让角色更加立体")

    manager = CharacterStoryline()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 故事线总览", "➕ 创建故事线", "🤖 智能生成", "📅 时间轴"])

    with tab1:
        if not manager.storylines:
            st.info("暂无故事线，请在「创建故事线」或「智能生成」中添加")
        else:
            # 按角色分组
            chars = {}
            for s in manager.storylines:
                chars.setdefault(s["char_name"], []).append(s)

            for char_name, lines in chars.items():
                with st.expander(f"👤 {char_name}（{len(lines)}条线）"):
                    for i, s in enumerate(lines):
                        info = STORYLINE_TYPES.get(s["type"], {})
                        cols = st.columns([1, 3, 2, 1])
                        with cols[0]:
                            st.write(f"{info.get('emoji', '📌')} {s['type']}")
                        with cols[1]:
                            st.write(f"**{s['title']}**")
                            st.caption(s["description"])
                        with cols[2]:
                            st.caption(f"📋 集数: {s['episodes']}")
                            if s.get("key_events"):
                                for evt in s["key_events"][:3]:
                                    st.caption(f"  • {evt}")
                        with cols[3]:
                            if st.button("🗑️", key=f"del_sl_{i}"):
                                manager.remove_storyline(i)
                                st.rerun()

    with tab2:
        characters = st.session_state.get("characters", [])
        char_names = [c["name"] for c in characters if isinstance(c, dict) and c.get("name")]
        if not char_names:
            char_names = ["角色A", "角色B"]

        c1, c2 = st.columns(2)
        with c1:
            char_name = st.selectbox("角色", char_names, key="sl_char")
            line_type = st.selectbox("故事线类型", list(STORYLINE_TYPES.keys()),
                                     format_func=lambda x: f"{STORYLINE_TYPES[x]['emoji']} {x} - {STORYLINE_TYPES[x]['desc']}",
                                     key="sl_type")
        with c2:
            title = st.text_input("故事线标题", key="sl_title")
            episodes = st.text_input("涉及集数", value="1-10", key="sl_episodes")

        description = st.text_area("故事线描述", key="sl_desc", height=100)

        if st.button("创建故事线", type="primary", use_container_width=True):
            if title:
                manager.add_storyline(char_name, line_type, title, description, episodes)
                st.success(f"已为「{char_name}」创建故事线：{title}")
                st.rerun()
            else:
                st.error("请输入故事线标题")

    with tab3:
        st.write("选择角色和模板，一键生成故事线")
        c1, c2 = st.columns(2)
        with c1:
            gen_char = st.selectbox("选择角色", char_names, key="gen_sl_char")
        with c2:
            gen_template = st.selectbox("故事模板", list(STORYLINE_TEMPLATES.keys()), key="gen_sl_template")

        if st.button("🤖 一键生成", type="primary", use_container_width=True):
            sl = manager.auto_generate(gen_char, template=gen_template)
            st.success(f"已为「{gen_char}」生成「{gen_template}」故事线")
            st.rerun()

        # 显示模板说明
        st.divider()
        for name, steps in STORYLINE_TEMPLATES.items():
            with st.expander(f"📋 {name}模板"):
                st.write(steps[0].replace("→", " → "))

    with tab4:
        st.subheader("📅 剧情时间轴")
        st.caption("可视化展示各角色故事线的发展时间轴")

        if not manager.storylines:
            st.info("请先创建故事线")
        else:
            # 简易时间轴
            for s in manager.storylines:
                info = STORYLINE_TYPES.get(s["type"], {})
                cols = st.columns([1, 1, 3, 2])
                with cols[0]:
                    st.write(f"{info.get('emoji', '📌')}")
                with cols[1]:
                    st.write(f"**{s['char_name']}**")
                with cols[2]:
                    st.write(s["title"])
                    st.caption(f"集数: {s['episodes']}")
                with cols[3]:
                    st.caption(s["type"])
