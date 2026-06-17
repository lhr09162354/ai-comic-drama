# -*- coding: utf-8 -*-
"""
v36: 运镜建议系统
支持推/拉/摇/移/跟/升降等运镜方式，为视频分镜提供专业运镜建议
"""
import streamlit as st
from dataclasses import dataclass
from typing import Optional, List
import random


CAMERA_MOVES = {
    "推": {"emoji": "🔭", "en": "Push In", "desc": "镜头由远及近，聚焦重点", "适用": "情感爆发、关键发现、角色觉醒"},
    "拉": {"emoji": "🔭", "en": "Pull Out", "desc": "镜头由近及远，展示全貌", "适用": "场景转换、揭露真相、结尾留白"},
    "摇": {"emoji": "🔄", "en": "Pan", "desc": "镜头水平/垂直旋转", "适用": "跟踪移动、展示环境、角色对视"},
    "移": {"emoji": "➡️", "en": "Tracking", "desc": "镜头平行移动跟随主体", "适用": "行走对话、追逐场景、空间转换"},
    "跟": {"emoji": "🏃", "en": "Follow", "desc": "镜头跟随角色行动", "适用": "角色独白、探路寻宝、紧张逃亡"},
    "升降": {"emoji": "↕️", "en": "Crane", "desc": "镜头垂直升降运动", "适用": "宏大场景、高低位对比、情感升华"},
    "环绕": {"emoji": "🌀", "en": "Orbit", "desc": "镜头围绕主体旋转", "适用": "角色登场、战斗场面、情感高潮"},
    "手持": {"emoji": "📱", "en": "Handheld", "desc": "模拟手持晃动感", "适用": "紧张恐惧、纪实风格、混乱场面"},
    "固定": {"emoji": "📌", "en": "Static", "desc": "固定机位，画面稳定", "适用": "对话场景、沉思时刻、静态构图"},
    "航拍": {"emoji": "🛸", "en": "Aerial", "desc": "鸟瞰俯拍视角", "适用": "城市全貌、战场全景、自然风光"},
}

SHOT_TYPES = {
    "特写": {"emoji": "🔍", "range": "面部/物品", "desc": "极度放大细节"},
    "近景": {"emoji": "👤", "range": "胸部以上", "desc": "展现表情情感"},
    "中景": {"emoji": "🧍", "range": "腰部以上", "desc": "动作+表情兼顾"},
    "全景": {"emoji": "🏞️", "range": "全身+环境", "desc": "人物与环境关系"},
    "远景": {"emoji": "🌄", "range": "大场景", "desc": "交代时空背景"},
    "过肩": {"emoji": "👥", "range": "对话视角", "desc": "对话场景常用"},
}

ANGLE_TYPES = {
    "平视": {"emoji": "➡️", "desc": "与人眼等高，客观自然"},
    "俯拍": {"emoji": "⬇️", "desc": "从上往下，渺小感"},
    "仰拍": {"emoji": "⬆️", "desc": "从下往上，崇高感"},
    "鸟瞰": {"emoji": "🦅", "desc": "垂直向下，上帝视角"},
    "荷兰角": {"emoji": "↗️", "desc": "倾斜构图，不安感"},
}

# 场景-运镜映射建议
SCENE_CAMERA_MAP = {
    "对话": [("固定", "平视"), ("推", "近景"), ("摇", "过肩")],
    "战斗": [("跟", "中景"), ("环绕", "全景"), ("手持", "近景")],
    "逃亡": [("跟", "中景"), ("手持", "近景"), ("移", "全景")],
    "告白": [("推", "特写"), ("固定", "近景"), ("升降", "全景")],
    "发现": [("推", "特写"), ("拉", "中景"), ("摇", "全景")],
    "悲伤": [("拉", "远景"), ("升降", "全景"), ("固定", "近景")],
    "欢乐": [("移", "全景"), ("跟", "中景"), ("环绕", "全景")],
    "恐惧": [("手持", "近景"), ("推", "特写"), ("荷兰角", "中景")],
    "回忆": [("拉", "远景"), ("升降", "全景"), ("固定", "近景")],
    "登场": [("升降", "全景"), ("推", "近景"), ("环绕", "中景")],
    "日常": [("固定", "中景"), ("移", "全景"), ("摇", "中景")],
    "高潮": [("环绕", "全景"), ("升降", "远景"), ("推", "特写")],
}


@dataclass
class CameraSuggestion:
    move: str
    shot: str
    angle: str
    reason: str
    timing: str = ""


class CameraMoveAdvisor:
    """运镜建议系统"""

    def __init__(self):
        self.suggestions = st.session_state.get("v36_camera_suggestions", [])

    def suggest_for_scene(self, scene_type, emotion="", context=""):
        """根据场景类型生成运镜建议"""
        options = SCENE_CAMERA_MAP.get(scene_type, SCENE_CAMERA_MAP.get("日常", []))
        suggestions = []
        for move, shot in options[:3]:
            angle = "平视"
            if emotion == "恐惧":
                angle = random.choice(["荷兰角", "俯拍"])
            elif emotion == "崇高":
                angle = "仰拍"
            elif emotion == "渺小":
                angle = "俯拍"
            move_info = CAMERA_MOVES.get(move, {})
            shot_info = SHOT_TYPES.get(shot, {})
            angle_info = ANGLE_TYPES.get(angle, {})
            reason = f"{move_info.get('desc', '')}，{shot_info.get('desc', '')}，{angle_info.get('desc', '')}"
            suggestions.append(CameraSuggestion(
                move=move, shot=shot, angle=angle,
                reason=reason,
                timing=self._suggest_timing(move)
            ))
        return suggestions

    def _suggest_timing(self, move):
        """建议运镜时长"""
        timing_map = {"推": "2-3秒", "拉": "2-3秒", "摇": "3-5秒", "移": "3-5秒",
                      "跟": "5-10秒", "升降": "3-5秒", "环绕": "5-8秒",
                      "手持": "灵活", "固定": "按需", "航拍": "5-10秒"}
        return timing_map.get(move, "3-5秒")

    def generate_script_camera_plan(self, scenes: List[dict]):
        """为整个剧本生成运镜方案"""
        plan = []
        for i, scene in enumerate(scenes):
            scene_type = scene.get("type", "日常")
            emotion = scene.get("emotion", "")
            suggestions = self.suggest_for_scene(scene_type, emotion)
            plan.append({"scene_index": i + 1, "scene": scene, "camera_plan": suggestions})
        self.suggestions = plan
        st.session_state["v36_camera_suggestions"] = plan
        return plan

    def get_quick_tip(self):
        """获取随机运镜技巧"""
        move = random.choice(list(CAMERA_MOVES.keys()))
        info = CAMERA_MOVES[move]
        return f"💡 运镜技巧：{info['emoji']} {move}（{info['en']}）— {info['desc']}，适用于{info['适用']}"


def render_camera_move_page():
    """渲染运镜建议页面"""
    st.subheader("🎬 运镜建议")
    st.caption("专业运镜指导，让视频分镜更有电影感")

    advisor = CameraMoveAdvisor()

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 快速建议", "📋 运镜手册", "📊 剧本运镜方案", "🎲 随机技巧"])

    with tab1:
        st.write("选择场景类型，获取运镜建议")
        c1, c2 = st.columns([1, 1])
        with c1:
            scene_type = st.selectbox("场景类型", list(SCENE_CAMERA_MAP.keys()), key="cam_scene")
            emotion = st.selectbox("情绪倾向", ["", "恐惧", "崇高", "渺小", "紧张", "温馨"], key="cam_emotion")
        with c2:
            context = st.text_input("场景描述（可选）", key="cam_context")
            if st.button("获取运镜建议", type="primary", use_container_width=True):
                suggestions = advisor.suggest_for_scene(scene_type, emotion, context)
                st.session_state["v36_quick_cam"] = suggestions

        quick_suggestions = st.session_state.get("v36_quick_cam", [])
        if quick_suggestions:
            st.divider()
            for i, s in enumerate(quick_suggestions):
                move_info = CAMERA_MOVES.get(s.move, {})
                shot_info = SHOT_TYPES.get(s.shot, {})
                angle_info = ANGLE_TYPES.get(s.angle, {})
                with st.container():
                    cols = st.columns([1, 1, 1, 2, 1])
                    with cols[0]:
                        st.write(f"{move_info.get('emoji', '📌')} **{s.move}**")
                        st.caption(s.move)
                    with cols[1]:
                        st.write(f"{shot_info.get('emoji', '👤')} **{s.shot}**")
                        st.caption(shot_info.get("range", ""))
                    with cols[2]:
                        st.write(f"{angle_info.get('emoji', '➡️')} **{s.angle}**")
                        st.caption(angle_info.get("desc", ""))
                    with cols[3]:
                        st.write(s.reason)
                    with cols[4]:
                        st.caption(f"⏱️ {s.timing}")
                    st.divider()

    with tab2:
        st.subheader("运镜方式大全")
        for move_name, info in CAMERA_MOVES.items():
            with st.expander(f"{info['emoji']} {move_name}（{info['en']}）"):
                st.write(f"**说明**: {info['desc']}")
                st.write(f"**适用场景**: {info['适用']}")
                # 推荐搭配
                st.write("**推荐景别搭配**:")
                suitable_shots = {"推": ["特写", "近景"], "拉": ["全景", "远景"],
                                  "摇": ["中景", "全景"], "移": ["中景", "全景"],
                                  "跟": ["中景", "近景"], "升降": ["全景", "远景"],
                                  "环绕": ["全景", "中景"], "手持": ["近景", "特写"],
                                  "固定": ["中景", "近景", "全景"], "航拍": ["远景", "全景"]}
                for shot in suitable_shots.get(move_name, ["中景"]):
                    shot_info = SHOT_TYPES.get(shot, {})
                    st.write(f"  - {shot_info.get('emoji', '')} {shot}: {shot_info.get('desc', '')}")

    with tab3:
        st.write("为整个剧本生成运镜方案")
        num_scenes = st.number_input("场景数量", 1, 30, 5, key="cam_plan_num")
        if st.button("生成运镜方案", use_container_width=True):
            demo_scenes = []
            scene_types = list(SCENE_CAMERA_MAP.keys())
            for i in range(num_scenes):
                stype = scene_types[i % len(scene_types)]
                demo_scenes.append({"type": stype, "emotion": ""})
            plan = advisor.generate_script_camera_plan(demo_scenes)
            st.success(f"已生成 {len(plan)} 个场景的运镜方案")
            st.rerun()

        # 展示已有方案
        for item in advisor.suggestions:
            with st.expander(f"🎬 场景 {item['scene_index']}: {item['scene'].get('type', '未命名')}"):
                for s in item["camera_plan"]:
                    st.write(f"- {CAMERA_MOVES.get(s.move, {}).get('emoji', '')} **{s.move}** + "
                             f"{SHOT_TYPES.get(s.shot, {}).get('emoji', '')} **{s.shot}** + "
                             f"{ANGLE_TYPES.get(s.angle, {}).get('emoji', '')} **{s.angle}** "
                             f"({s.timing}) — {s.reason}")

    with tab4:
        st.subheader("🎲 运镜技巧随机学")
        if st.button("换一个技巧 🎲", use_container_width=True):
            st.session_state["v36_cam_tip"] = advisor.get_quick_tip()
        tip = st.session_state.get("v36_cam_tip", advisor.get_quick_tip())
        st.info(tip)
