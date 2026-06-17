# -*- coding: utf-8 -*-
"""
v36: 剧情节奏控制
支持快节奏/慢热/悬疑铺垫/高潮迭起等节奏模式
"""
import streamlit as st
from dataclasses import dataclass
from typing import List, Optional
import json


RHYTHM_PRESETS = {
    "快节奏": {
        "emoji": "⚡", "desc": "节奏紧凑，每集都有爆点",
        "scene_density": "高", "dialogue_ratio": "4:6",
        "tips": ["每3个分镜内设置一个冲突点", "减少过渡场景", "对话精炼有力", "多用动作描写"],
        "template": "开篇即入高潮→冲突升级→反转→下一集钩子"
    },
    "慢热型": {
        "emoji": "🍂", "desc": "徐徐展开，人物刻画深入",
        "scene_density": "低", "dialogue_ratio": "7:3",
        "tips": ["前3集重点塑造角色", "用日常细节铺垫情感", "伏笔埋得深", "高潮放在中后段"],
        "template": "日常铺垫→暗流涌动→矛盾显现→集中爆发"
    },
    "悬疑铺垫": {
        "emoji": "🔍", "desc": "层层设置悬念，吊足胃口",
        "scene_density": "中", "dialogue_ratio": "5:5",
        "tips": ["每集结尾设置悬念", "真假信息交替", "关键线索分散放置", "误导与真相并行"],
        "template": "抛出谜团→收集线索→排除错误→揭示真相"
    },
    "高潮迭起": {
        "emoji": "🎢", "desc": "一波未平一波又起",
        "scene_density": "高", "dialogue_ratio": "3:7",
        "tips": ["连续制造冲突", "不给角色喘息空间", "多线并进", "每集至少一个转折"],
        "template": "冲突→升级→更大冲突→爆点→新冲突"
    },
    "舒缓治愈": {
        "emoji": "🌸", "desc": "温暖治愈，给人心灵慰藉",
        "scene_density": "低", "dialogue_ratio": "8:2",
        "tips": ["多描写自然景色", "角色互动温暖有爱", "每集一个小确幸", "冲突温和化解"],
        "template": "日常小烦恼→互相帮助→温暖结局→下一集小确幸"
    },
    "反转不断": {
        "emoji": "🔄", "desc": "出人意料，颠覆认知",
        "scene_density": "中高", "dialogue_ratio": "4:6",
        "tips": ["前半段建立认知", "中期植入反转种子", "反转要合理有伏笔", "反转后重建新认知"],
        "template": "建立假设→伏笔暗埋→打破认知→揭示真相→新世界观"
    },
}


@dataclass
class RhythmPoint:
    episode: int
    action: str  # "冲突" / "高潮" / "铺垫" / "反转" / "日常" / "结局"
    description: str
    intensity: int  # 1-10


class RhythmController:
    """剧情节奏控制器"""

    def __init__(self):
        self.preset = st.session_state.get("v36_rhythm_preset", "快节奏")
        self.points = st.session_state.get("v36_rhythm_points", [])

    def set_preset(self, preset_name):
        if preset_name in RHYTHM_PRESETS:
            self.preset = preset_name
            st.session_state["v36_rhythm_preset"] = preset_name

    def add_point(self, episode, action, description, intensity):
        point = {"episode": episode, "action": action,
                 "description": description, "intensity": intensity}
        self.points.append(point)
        self.points.sort(key=lambda x: x["episode"])
        st.session_state["v36_rhythm_points"] = self.points

    def remove_point(self, idx):
        if 0 <= idx < len(self.points):
            self.points.pop(idx)
            st.session_state["v36_rhythm_points"] = self.points

    def generate_rhythm_curve(self):
        """生成节奏曲线数据"""
        if not self.points:
            return [], []
        episodes = [p["episode"] for p in self.points]
        intensities = [p["intensity"] for p in self.points]
        return episodes, intensities

    def get_preset_tips(self):
        return RHYTHM_PRESETS.get(self.preset, {}).get("tips", [])

    def auto_plan(self, total_episodes, preset_name=None):
        """根据预设自动规划节奏"""
        preset = preset_name or self.preset
        self.points = []
        if preset == "快节奏":
            for i in range(1, total_episodes + 1):
                if i == 1:
                    self.add_point(i, "冲突", "开篇冲突，抓住眼球", 8)
                elif i == total_episodes:
                    self.add_point(i, "高潮", "终极爆点", 10)
                elif i % 2 == 0:
                    self.add_point(i, "反转", "节奏反转", 7)
                else:
                    self.add_point(i, "冲突", "冲突升级", 8)
        elif preset == "慢热型":
            for i in range(1, total_episodes + 1):
                if i <= 3:
                    self.add_point(i, "铺垫", "日常与角色铺垫", i + 1)
                elif i <= total_episodes - 2:
                    self.add_point(i, "冲突", "矛盾逐渐显现", 4 + i // 2)
                elif i == total_episodes - 1:
                    self.add_point(i, "高潮", "情感爆发", 9)
                else:
                    self.add_point(i, "结局", "温馨收尾", 5)
        elif preset == "悬疑铺垫":
            for i in range(1, total_episodes + 1):
                if i == 1:
                    self.add_point(i, "冲突", "抛出核心谜团", 7)
                elif i < total_episodes - 1:
                    self.add_point(i, "铺垫", f"第{i}条线索", 3 + (i % 3))
                elif i == total_episodes - 1:
                    self.add_point(i, "反转", "真相浮出水面", 9)
                else:
                    self.add_point(i, "结局", "谜底揭晓", 10)
        elif preset == "高潮迭起":
            for i in range(1, total_episodes + 1):
                base = 6 + (i % 3) * 2
                action = ["冲突", "高潮", "反转"][(i - 1) % 3]
                self.add_point(i, action, f"第{i}波{action}", min(base, 10))
        else:
            # 默认舒缓
            for i in range(1, total_episodes + 1):
                self.add_point(i, "日常", f"第{i}个温暖故事", 3 + i % 3)
        return self.points

    def analyze_pacing(self):
        """分析当前节奏"""
        if len(self.points) < 2:
            return {"status": "数据不足", "suggestion": "至少需要2个节奏点"}
        intensities = [p["intensity"] for p in self.points]
        avg = sum(intensities) / len(intensities)
        max_gap = max(abs(intensities[i] - intensities[i + 1]) for i in range(len(intensities) - 1))
        issues = []
        # 连续低强度
        low_streak = 0
        for v in intensities:
            if v <= 3:
                low_streak += 1
                if low_streak >= 3:
                    issues.append("连续3集以上低强度，观众可能流失")
            else:
                low_streak = 0
        # 连续高强度
        high_streak = 0
        for v in intensities:
            if v >= 9:
                high_streak += 1
                if high_streak >= 3:
                    issues.append("连续3集以上高强度，观众容易疲劳")
            else:
                high_streak = 0
        return {"avg_intensity": round(avg, 1), "max_gap": max_gap, "issues": issues}


def render_rhythm_control_page():
    """渲染剧情节奏控制页面"""
    st.subheader("🎵 剧情节奏控制")
    st.caption("规划剧情节奏，让故事张弛有度")

    controller = RhythmController()

    tab1, tab2, tab3 = st.tabs(["🎛️ 节奏模式", "📊 节奏规划", "📈 节奏分析"])

    with tab1:
        st.write("选择节奏模式，获取创作建议")
        cols = st.columns(3)
        for i, (name, info) in enumerate(RHYTHM_PRESETS.items()):
            with cols[i % 3]:
                selected = st.button(
                    f"{info['emoji']} {name}",
                    key=f"rhythm_{name}",
                    use_container_width=True,
                    type="primary" if controller.preset == name else "secondary"
                )
                if selected:
                    controller.set_preset(name)
                    st.rerun()
                st.caption(info["desc"])

        # 当前模式提示
        preset = RHYTHM_PRESETS.get(controller.preset, {})
        if preset:
            st.divider()
            st.subheader(f"{preset['emoji']} {controller.preset} 创作指南")
            st.write(f"**节奏模板**: {preset['template']}")
            st.write(f"**场景密度**: {preset['scene_density']} | **对话:动作比**: {preset['dialogue_ratio']}")
            st.write("**创作要点**:")
            for tip in preset["tips"]:
                st.write(f"- {tip}")

    with tab2:
        c1, c2 = st.columns([1, 2])
        with c1:
            total_eps = st.number_input("总集数", 3, 50, 10, key="rhythm_total_eps")
            if st.button("🤖 自动规划", use_container_width=True):
                points = controller.auto_plan(total_eps, controller.preset)
                st.success(f"已生成 {len(points)} 个节奏点")
                st.rerun()

            # 手动添加
            st.divider()
            st.write("**手动添加节奏点**")
            ep = st.number_input("集数", 1, 99, 1, key="rhythm_ep")
            action = st.selectbox("类型", ["冲突", "高潮", "铺垫", "反转", "日常", "结局"], key="rhythm_action")
            desc = st.text_input("描述", key="rhythm_desc")
            intensity = st.slider("强度", 1, 10, 5, key="rhythm_intensity")
            if st.button("添加节奏点", use_container_width=True):
                controller.add_point(ep, action, desc, intensity)
                st.success("已添加")
                st.rerun()

        with c2:
            if not controller.points:
                st.info("请先自动规划或手动添加节奏点")
            else:
                # 节奏曲线
                episodes, intensities = controller.generate_rhythm_curve()
                st.write("**节奏曲线**")
                chart_data = {"episode": episodes, "intensity": intensities}
                st.line_chart(chart_data, x="episode", y="intensity")

                # 节奏点列表
                st.divider()
                for i, p in enumerate(controller.points):
                    action_emoji = {"冲突": "💥", "高潮": "🔥", "铺垫": "🌿",
                                    "反转": "🔄", "日常": "☀️", "结局": "🎬"}.get(p["action"], "📌")
                    cols = st.columns([1, 2, 3, 1, 1])
                    with cols[0]:
                        st.write(f"第{p['episode']}集")
                    with cols[1]:
                        st.write(f"{action_emoji} {p['action']}")
                    with cols[2]:
                        st.write(p["description"])
                    with cols[3]:
                        st.write(f"⚡{p['intensity']}")
                    with cols[4]:
                        if st.button("🗑️", key=f"del_rp_{i}"):
                            controller.remove_point(i)
                            st.rerun()

    with tab3:
        if not controller.points:
            st.info("请先在「节奏规划」中添加节奏点")
        else:
            analysis = controller.analyze_pacing()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("平均强度", analysis["avg_intensity"])
            with c2:
                st.metric("最大波动", analysis["max_gap"])
            with c3:
                st.metric("发现问题", len(analysis.get("issues", [])))

            if analysis.get("issues"):
                st.warning("**节奏问题**:")
                for issue in analysis["issues"]:
                    st.write(f"- ⚠️ {issue}")
            else:
                st.success("节奏规划合理，无重大问题")
