# -*- coding: utf-8 -*-
"""
v36: BGM推荐系统
根据场景推荐背景音乐，支持多种情绪和风格
"""
import streamlit as st
from typing import List, Optional, Dict
import random


BGM_MOODS = {
    "欢乐": {"emoji": "😊", "bpm": "120-140", "instruments": "钢琴/尤克里里/口哨", "style": "轻快活泼"},
    "悲伤": {"emoji": "😢", "bpm": "60-80", "instruments": "钢琴/大提琴/小提琴", "style": "舒缓忧郁"},
    "紧张": {"emoji": "😰", "bpm": "140-180", "instruments": "弦乐群/定音鼓/电子音效", "style": "紧凑悬疑"},
    "浪漫": {"emoji": "💕", "bpm": "80-100", "instruments": "钢琴/吉他/长笛", "style": "温柔甜美"},
    "热血": {"emoji": "🔥", "bpm": "150-180", "instruments": "电吉他/架子鼓/铜管", "style": "激昂澎湃"},
    "恐怖": {"emoji": "👻", "bpm": "60-90", "instruments": "低音弦乐/合成器/音效", "style": "阴森诡异"},
    "史诗": {"emoji": "⚔️", "bpm": "100-130", "instruments": "管弦乐团/合唱/定音鼓", "style": "恢宏壮阔"},
    "日常": {"emoji": "☀️", "bpm": "90-110", "instruments": "吉他/钢琴/轻打击", "style": "轻松自然"},
    "回忆": {"emoji": "💭", "bpm": "70-90", "instruments": "钢琴/竖琴/长笛", "style": "温柔怀旧"},
    "悬疑": {"emoji": "🔍", "bpm": "90-120", "instruments": "弦乐/电子/音效", "style": "神秘紧张"},
    "治愈": {"emoji": "🌸", "bpm": "80-100", "instruments": "钢琴/吉他/口琴", "style": "温暖治愈"},
    "冒险": {"emoji": "🗺️", "bpm": "120-150", "instruments": "管乐/弦乐/打击乐", "style": "激昂探索"},
}

# 场景-情绪映射
SCENE_BGM_MAP = {
    "开场": ["日常", "冒险", "史诗"],
    "对话": ["日常", "浪漫", "治愈"],
    "战斗": ["热血", "史诗", "紧张"],
    "告白": ["浪漫", "治愈", "回忆"],
    "分别": ["悲伤", "回忆", "治愈"],
    "重逢": ["欢乐", "治愈", "浪漫"],
    "危机": ["紧张", "悬疑", "恐怖"],
    "胜利": ["热血", "欢乐", "史诗"],
    "回忆": ["回忆", "悲伤", "治愈"],
    "日常": ["日常", "欢乐", "治愈"],
    "登场": ["史诗", "热血", "悬疑"],
    "离别": ["悲伤", "回忆", "治愈"],
}

# BGM标签
BGM_TAGS = ["无版权", "轻音乐", "电子", "古典", "流行", "摇滚", "民谣", "爵士", "氛围", "Lo-Fi"]


class BGMRecommender:
    """BGM推荐系统"""

    def __init__(self):
        self.favorites = st.session_state.get("v36_bgm_favorites", [])

    def recommend_for_scene(self, scene_type):
        """根据场景类型推荐BGM"""
        moods = SCENE_BGM_MAP.get(scene_type, ["日常"])
        recommendations = []
        for mood_name in moods:
            mood_info = BGM_MOODS.get(mood_name, BGM_MOODS["日常"])
            recommendations.append({
                "mood": mood_name,
                "emoji": mood_info["emoji"],
                "bpm": mood_info["bpm"],
                "instruments": mood_info["instruments"],
                "style": mood_info["style"],
                "suggested_tracks": self._generate_track_names(mood_name, 3),
            })
        return recommendations

    def recommend_for_mood(self, mood_name):
        """根据情绪推荐BGM"""
        mood_info = BGM_MOODS.get(mood_name, BGM_MOODS["日常"])
        return {
            "mood": mood_name,
            "emoji": mood_info["emoji"],
            "bpm": mood_info["bpm"],
            "instruments": mood_info["instruments"],
            "style": mood_info["style"],
            "suggested_tracks": self._generate_track_names(mood_name, 5),
        }

    def _generate_track_names(self, mood, count=3):
        """生成示例曲目名"""
        prefixes = {
            "欢乐": ["阳光", "微笑", "快乐"], "悲伤": ["雨声", "离别", "思念"],
            "紧张": ["心跳", "暗影", "迫近"], "浪漫": ["月光", "花语", "心跳"],
            "热血": ["燃烧", "冲锋", "不屈"], "恐怖": ["深渊", "低语", "噩梦"],
            "史诗": ["征程", "荣耀", "传说"], "日常": ["午后", "清风", "闲步"],
            "回忆": ["旧时光", "回响", "那年"], "悬疑": ["迷雾", "真相", "暗线"],
            "治愈": ["暖阳", "微光", "拥抱"], "冒险": ["远方", "启航", "探索"],
        }
        names = prefixes.get(mood, ["旋律"])
        tracks = []
        suffixes = ["之歌", "小调", "幻想曲", "序曲", "回旋曲"]
        for i in range(count):
            name = random.choice(names) + random.choice(suffixes)
            tracks.append({"name": name, "duration": f"{random.randint(2,5)}:{random.randint(10,59):02d}"})
        return tracks

    def add_favorite(self, track_name, mood):
        self.favorites.append({"name": track_name, "mood": mood})
        st.session_state["v36_bgm_favorites"] = self.favorites

    def generate_bgm_plan(self, scenes):
        """为整个剧本生成BGM方案"""
        plan = []
        for scene in scenes:
            scene_type = scene.get("type", "日常")
            recs = self.recommend_for_scene(scene_type)
            plan.append({"scene": scene_type, "recommendations": recs})
        return plan


def render_bgm_recommend_page():
    """渲染BGM推荐页面"""
    st.subheader("🎵 BGM推荐")
    st.caption("根据场景情绪推荐背景音乐，让作品更有氛围")

    recommender = BGMRecommender()

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 场景推荐", "😊 情绪推荐", "📋 全剧配乐", "❤️ 我的收藏"])

    with tab1:
        scene_type = st.selectbox("选择场景", list(SCENE_BGM_MAP.keys()), key="bgm_scene")
        if st.button("获取BGM推荐", type="primary", use_container_width=True):
            recs = recommender.recommend_for_scene(scene_type)
            st.session_state["v36_scene_recs"] = recs

        recs = st.session_state.get("v36_scene_recs", [])
        for rec in recs:
            with st.expander(f"{rec['emoji']} {rec['mood']} — {rec['style']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**BPM**: {rec['bpm']}")
                    st.write(f"**乐器**: {rec['instruments']}")
                with c2:
                    st.write("**推荐曲目**:")
                    for track in rec["suggested_tracks"]:
                        st.write(f"- 🎵 {track['name']} ({track['duration']})")

    with tab2:
        mood_cols = st.columns(4)
        selected_mood = None
        for i, (name, info) in enumerate(BGM_MOODS.items()):
            with mood_cols[i % 4]:
                if st.button(f"{info['emoji']} {name}", key=f"mood_{name}", use_container_width=True):
                    selected_mood = name
                    st.session_state["v36_selected_mood"] = name
                    st.rerun()

        current_mood = st.session_state.get("v36_selected_mood")
        if current_mood:
            rec = recommender.recommend_for_mood(current_mood)
            st.divider()
            c1, c2 = st.columns([1, 2])
            with c1:
                st.write(f"**{rec['emoji']} {current_mood}**")
                st.write(f"BPM: {rec['bpm']}")
                st.write(f"乐器: {rec['instruments']}")
                st.write(f"风格: {rec['style']}")
            with c2:
                st.write("**推荐曲目**:")
                for track in rec["suggested_tracks"]:
                    cols = st.columns([3, 1, 1])
                    with cols[0]:
                        st.write(f"🎵 {track['name']}")
                    with cols[1]:
                        st.caption(track["duration"])
                    with cols[2]:
                        if st.button("❤️", key=f"fav_{track['name']}"):
                            recommender.add_favorite(track["name"], current_mood)
                            st.success("已收藏")

    with tab3:
        st.write("为整个剧本生成BGM配乐方案")
        num_scenes = st.number_input("场景数", 1, 30, 8, key="bgm_plan_num")
        if st.button("生成配乐方案", use_container_width=True):
            scenes = [{"type": list(SCENE_BGM_MAP.keys())[i % len(SCENE_BGM_MAP)]}
                      for i in range(num_scenes)]
            plan = recommender.generate_bgm_plan(scenes)
            st.session_state["v36_bgm_plan"] = plan

        plan = st.session_state.get("v36_bgm_plan", [])
        for i, item in enumerate(plan):
            with st.expander(f"🎬 场景 {i+1}: {item['scene']}"):
                for rec in item["recommendations"]:
                    st.write(f"{rec['emoji']} **{rec['mood']}** — {rec['style']} (BPM: {rec['bpm']})")

    with tab4:
        if not recommender.favorites:
            st.info("暂无收藏，在推荐页面中点击❤️收藏")
        else:
            for fav in recommender.favorites:
                mood_info = BGM_MOODS.get(fav["mood"], {})
                st.write(f"{mood_info.get('emoji', '🎵')} **{fav['name']}** — {fav['mood']}")
