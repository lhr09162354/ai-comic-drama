# -*- coding: utf-8 -*-
"""
v36: 剧情时间轴
可视化展示剧情发展，支持多线并行展示
"""
import streamlit as st
from datetime import datetime
from typing import List, Optional, Dict


TIMELINE_COLORS = {
    "主线": "#FFD700",
    "支线": "#4CAF50",
    "暗线": "#9C27B0",
    "感情线": "#E91E63",
    "冲突线": "#F44336",
    "日常线": "#00BCD4",
}


class TimelineEvent:
    def __init__(self, episode, title, description, line_type="主线",
                 characters=None, intensity=5):
        self.episode = episode
        self.title = title
        self.description = description
        self.line_type = line_type
        self.characters = characters or []
        self.intensity = intensity

    def to_dict(self):
        return {"episode": self.episode, "title": self.title,
                "description": self.description, "line_type": self.line_type,
                "characters": self.characters, "intensity": self.intensity}

    @staticmethod
    def from_dict(d):
        return TimelineEvent(d["episode"], d["title"], d["description"],
                             d.get("line_type", "主线"), d.get("characters", []),
                             d.get("intensity", 5))


class PlotTimeline:
    """剧情时间轴管理器"""

    def __init__(self):
        self.events = st.session_state.get("v36_timeline_events", [])

    def _save(self):
        st.session_state["v36_timeline_events"] = self.events

    def add_event(self, episode, title, description, line_type="主线",
                  characters=None, intensity=5):
        event = TimelineEvent(episode, title, description, line_type,
                               characters, intensity)
        self.events.append(event.to_dict())
        self.events.sort(key=lambda x: x["episode"])
        self._save()

    def remove_event(self, idx):
        if 0 <= idx < len(self.events):
            self.events.pop(idx)
            self._save()

    def get_episodes_range(self):
        if not self.events:
            return (1, 10)
        return (min(e["episode"] for e in self.events),
                max(e["episode"] for e in self.events))

    def get_by_episode(self, episode):
        return [e for e in self.events if e["episode"] == episode]

    def get_by_line_type(self, line_type):
        return [e for e in self.events if e["line_type"] == line_type]

    def get_line_types(self):
        return list(set(e["line_type"] for e in self.events))

    def auto_generate(self, total_episodes, story_type="冒险"):
        """根据故事类型自动生成时间轴"""
        self.events = []
        patterns = {
            "冒险": [
                (1, "主线", "启程", "主角踏上冒险之旅", 6),
                (2, "主线", "遭遇", "第一次遭遇危险", 7),
                (3, "支线", "伙伴", "遇到重要伙伴", 4),
                (4, "主线", "挑战", "面对重大挑战", 8),
                (5, "暗线", "秘密", "发现隐藏线索", 5),
                (6, "主线", "危机", "陷入绝境", 9),
                (7, "感情线", "羁绊", "伙伴间感情加深", 6),
                (8, "主线", "转折", "重大转折", 8),
                (9, "主线", "高潮", "最终决战", 10),
                (10, "主线", "结局", "故事结局", 5),
            ],
            "恋爱": [
                (1, "主线", "相遇", "男女主相遇", 5),
                (2, "支线", "日常", "日常相处", 3),
                (3, "感情线", "心动", "开始心动", 6),
                (4, "冲突线", "误会", "产生误会", 7),
                (5, "感情线", "和解", "误会解除感情加深", 7),
                (6, "冲突线", "阻碍", "外部阻碍出现", 8),
                (7, "主线", "抉择", "做出重要选择", 8),
                (8, "感情线", "告白", "正式告白", 9),
                (9, "冲突线", "危机", "感情面临危机", 9),
                (10, "主线", "圆满", "最终在一起", 10),
            ],
            "悬疑": [
                (1, "主线", "谜团", "案件发生", 7),
                (2, "暗线", "线索", "发现第一条线索", 5),
                (3, "支线", "嫌疑人", "排查嫌疑人", 6),
                (4, "暗线", "误导", "被假线索误导", 7),
                (5, "主线", "突破", "找到关键证据", 8),
                (6, "冲突线", "危险", "遭遇危险", 8),
                (7, "暗线", "真相", "真相开始浮出", 9),
                (8, "主线", "反转", "惊天反转", 10),
                (9, "主线", "揭秘", "完整真相揭示", 10),
                (10, "主线", "落幕", "案件告破", 5),
            ],
        }
        pattern = patterns.get(story_type, patterns["冒险"])
        for ep, lt, title, desc, intensity in pattern[:total_episodes]:
            self.add_event(ep, title, desc, lt, intensity=intensity)
        return self.events

    def render_visual_timeline(self):
        """渲染可视化时间轴"""
        if not self.events:
            return

        start_ep, end_ep = self.get_episodes_range()
        line_types = self.get_line_types()

        # 为每条线生成进度数据
        for lt in line_types:
            lt_events = self.get_by_line_type(lt)
            color = TIMELINE_COLORS.get(lt, "#999999")
            if lt_events:
                st.write(f"**{lt}**")
                chart_data = {"episode": [e["episode"] for e in lt_events],
                              "intensity": [e["intensity"] for e in lt_events]}
                st.line_chart(chart_data, x="episode", y="intensity")


def render_plot_timeline_page():
    """渲染剧情时间轴页面"""
    st.subheader("📅 剧情时间轴")
    st.caption("可视化展示剧情发展，多线并行一目了然")

    timeline = PlotTimeline()

    tab1, tab2, tab3 = st.tabs(["📊 时间轴视图", "➕ 添加事件", "🤖 智能生成"])

    with tab1:
        if not timeline.events:
            st.info("暂无时间轴事件，请添加或使用智能生成")
        else:
            # 顶部统计
            line_types = timeline.get_line_types()
            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                st.metric("总事件数", len(timeline.events))
            with c2:
                st.metric("故事线数", len(line_types))
            with c3:
                st.write("活跃故事线: " + " | ".join(f"**{lt}**" for lt in line_types))

            st.divider()

            # 强度曲线
            timeline.render_visual_timeline()

            st.divider()

            # 事件列表
            for i, event in enumerate(timeline.events):
                color = TIMELINE_COLORS.get(event["line_type"], "#999999")
                with st.container():
                    cols = st.columns([1, 1, 3, 2, 1])
                    with cols[0]:
                        st.write(f"📌 第{event['episode']}集")
                    with cols[1]:
                        st.write(f"**{event['line_type']}**")
                    with cols[2]:
                        st.write(f"**{event['title']}**")
                        st.caption(event["description"])
                    with cols[3]:
                        if event.get("characters"):
                            st.caption("👤 " + ", ".join(event["characters"]))
                    with cols[4]:
                        if st.button("🗑️", key=f"del_te_{i}"):
                            timeline.remove_event(i)
                            st.rerun()

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            episode = st.number_input("集数", 1, 999, 1, key="tl_ep")
            title = st.text_input("事件标题", key="tl_title")
        with c2:
            line_type = st.selectbox("故事线", list(TIMELINE_COLORS.keys()), key="tl_type")
            intensity = st.slider("重要度", 1, 10, 5, key="tl_intensity")

        description = st.text_area("事件描述", key="tl_desc", height=80)
        chars_input = st.text_input("涉及角色（逗号分隔）", key="tl_chars")
        characters = [c.strip() for c in chars_input.split(",") if c.strip()]

        if st.button("添加事件", type="primary", use_container_width=True):
            if title:
                timeline.add_event(episode, title, description, line_type, characters, intensity)
                st.success(f"已添加第{episode}集事件：{title}")
                st.rerun()

    with tab3:
        st.write("选择故事类型，一键生成完整时间轴")
        story_type = st.selectbox("故事类型", ["冒险", "恋爱", "悬疑"], key="tl_gen_type")
        total_eps = st.number_input("集数", 3, 30, 10, key="tl_gen_eps")

        if st.button("🤖 生成时间轴", type="primary", use_container_width=True):
            events = timeline.auto_generate(total_eps, story_type)
            st.success(f"已生成 {len(events)} 个时间轴事件")
            st.rerun()
