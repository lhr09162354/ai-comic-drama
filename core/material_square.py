# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 素材广场
热门素材快速使用，发现优质创作素材
"""

import random
from typing import List, Dict


# ============ 素材广场数据 ============

HOT_MATERIALS = {
    "角色": [
        {"name": "冷面总裁", "tags": ["现代", "甜宠", "霸道"], "uses": 12800, "rating": 4.8},
        {"name": "古灵精怪少女", "tags": ["校园", "日常", "活泼"], "uses": 10500, "rating": 4.7},
        {"name": "神秘法师", "tags": ["奇幻", "魔法", "神秘"], "uses": 9800, "rating": 4.6},
        {"name": "热血少年", "tags": ["冒险", "热血", "成长"], "uses": 9200, "rating": 4.5},
        {"name": "腹黑军师", "tags": ["古风", "谋略", "智斗"], "uses": 8700, "rating": 4.7},
        {"name": "双面侦探", "tags": ["悬疑", "推理", "反转"], "uses": 8100, "rating": 4.6},
        {"name": "温柔医者", "tags": ["治愈", "古风", "温暖"], "uses": 7600, "rating": 4.5},
        {"name": "赛博黑客", "tags": ["科幻", "赛博朋克", "酷炫"], "uses": 7200, "rating": 4.4},
    ],
    "场景": [
        {"name": "樱花校园", "tags": ["校园", "春天", "浪漫"], "uses": 11200, "rating": 4.8},
        {"name": "霓虹街道", "tags": ["赛博朋克", "夜晚", "未来"], "uses": 9800, "rating": 4.7},
        {"name": "仙山云海", "tags": ["修仙", "奇幻", "壮美"], "uses": 9100, "rating": 4.6},
        {"name": "咖啡馆角落", "tags": ["日常", "温馨", "约会"], "uses": 8500, "rating": 4.5},
        {"name": "古代宫殿", "tags": ["古风", "宫斗", "华丽"], "uses": 8200, "rating": 4.6},
        {"name": "太空站", "tags": ["科幻", "太空", "孤独"], "uses": 7400, "rating": 4.4},
    ],
    "画风": [
        {"name": "水彩温柔风", "tags": ["水彩", "温柔", "治愈"], "uses": 15000, "rating": 4.9},
        {"name": "赛博霓虹风", "tags": ["赛博朋克", "霓虹", "酷炫"], "uses": 12000, "rating": 4.7},
        {"name": "日系萌系", "tags": ["Q版", "可爱", "日常"], "uses": 11800, "rating": 4.8},
        {"name": "国风水墨", "tags": ["水墨", "古风", "意境"], "uses": 10500, "rating": 4.7},
        {"name": "暗黑哥特", "tags": ["哥特", "暗黑", "神秘"], "uses": 8900, "rating": 4.5},
        {"name": "像素复古风", "tags": ["像素", "复古", "怀旧"], "uses": 7800, "rating": 4.4},
    ],
    "音乐": [
        {"name": "樱花之约", "tags": ["钢琴", "浪漫", "春日"], "uses": 13200, "rating": 4.8},
        {"name": "暗夜追逐", "tags": ["电子", "紧张", "悬疑"], "uses": 9800, "rating": 4.6},
        {"name": "古韵悠长", "tags": ["古风", "琴箫", "悠远"], "uses": 9200, "rating": 4.7},
        {"name": "热血征途", "tags": ["摇滚", "热血", "战斗"], "uses": 8600, "rating": 4.5},
        {"name": "星空物语", "tags": ["氛围", "科幻", "空灵"], "uses": 7900, "rating": 4.6},
    ],
    "特效": [
        {"name": "樱花飘落", "tags": ["粒子", "浪漫", "春日"], "uses": 14000, "rating": 4.9},
        {"name": "闪电霹雳", "tags": ["战斗", "特效", "震撼"], "uses": 10800, "rating": 4.6},
        {"name": "水墨晕染", "tags": ["转场", "国风", "优雅"], "uses": 9500, "rating": 4.7},
        {"name": "星辰坠落", "tags": ["奇幻", "壮观", "魔幻"], "uses": 8800, "rating": 4.5},
        {"name": "火焰爆发", "tags": ["战斗", "热血", "冲击"], "uses": 8200, "rating": 4.4},
    ],
}


class MaterialSquare:
    """素材广场"""

    def __init__(self):
        self._all_materials = []
        self._build_index()

    def _build_index(self):
        for category, items in HOT_MATERIALS.items():
            for item in items:
                self._all_materials.append({"category": category, **item})

    def get_hot(self, category: str = None, limit: int = 10) -> List[Dict]:
        if category:
            return HOT_MATERIALS.get(category, [])[:limit]
        return sorted(self._all_materials, key=lambda x: x.get("uses", 0), reverse=True)[:limit]

    def get_random_picks(self, count: int = 4) -> List[Dict]:
        return random.sample(self._all_materials, min(count, len(self._all_materials)))

    def get_categories(self) -> List[str]:
        return list(HOT_MATERIALS.keys())

    def search(self, keyword: str) -> List[Dict]:
        keyword = keyword.lower()
        return [
            m for m in self._all_materials
            if keyword in m["name"].lower() or any(keyword in t.lower() for t in m.get("tags", []))
        ]


def render_material_square_page():
    """渲染素材广场页面"""
    import streamlit as st

    square = MaterialSquare()

    st.header("🏪 素材广场")
    st.caption("发现热门素材，快速开始创作")

    # 今日精选
    picks = square.get_random_picks(4)
    st.subheader("🔥 今日精选")
    cols = st.columns(4)
    for i, pick in enumerate(picks):
        with cols[i]:
            st.markdown(f"**{pick['name']}**")
            st.caption(f"{' | '.join(pick['tags'][:2])}")
            st.caption(f"⭐ {pick['rating']} | 👥 {pick['uses']}")
            if st.button("使用", key=f"use_sq_{pick['category']}_{pick['name']}"):
                st.toast(f"已选择素材: {pick['name']}")

    st.divider()

    # 分类浏览
    tab_names = [f"📁 {cat}" for cat in square.get_categories()]
    tabs = st.tabs(tab_names)

    for tab, (category, items) in zip(tabs, HOT_MATERIALS.items()):
        with tab:
            for item in items:
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    st.write(f"**{item['name']}**")
                    st.caption(" | ".join(f"#{t}" for t in item["tags"]))
                with c2:
                    st.caption(f"⭐ {item['rating']} | 使用 {item['uses']}次")
                with c3:
                    if st.button("使用", key=f"use_{category}_{item['name']}", use_container_width=True):
                        st.toast(f"已选择: {item['name']}")

    # 搜索
    st.divider()
    keyword = st.text_input("🔍 搜索素材", placeholder="输入关键词...")
    if keyword:
        results = square.search(keyword)
        if results:
            for r in results:
                st.write(f"**{r['name']}** [{r['category']}] — ⭐ {r['rating']}")
        else:
            st.info("未找到相关素材")
