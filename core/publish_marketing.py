# -*- coding: utf-8 -*-
"""
发布与营销系统 v34 - 合并模块
整合选题、发布、营销、粉丝运营
"""

import streamlit as st
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class TopicIntelligence:
    """选题情报"""

    def __init__(self):
        self.hot_topics = self._gen_hot_topics()

    def _gen_hot_topics(self) -> List[Dict]:
        return [
            {"topic": "甜宠逆袭", "heat": 95, "trend": "up", "category": "恋爱"},
            {"topic": "异世界重生", "heat": 88, "trend": "stable", "category": "奇幻"},
            {"topic": "都市修仙", "heat": 82, "trend": "up", "category": "玄幻"},
            {"topic": "校园日常", "heat": 76, "trend": "stable", "category": "青春"},
            {"topic": "悬疑推理", "heat": 73, "trend": "up", "category": "推理"},
            {"topic": "赛博朋克", "heat": 68, "trend": "up", "category": "科幻"},
            {"topic": "古风宫廷", "heat": 65, "trend": "down", "category": "历史"},
            {"topic": "搞笑吐槽", "heat": 62, "trend": "stable", "category": "喜剧"},
        ]

    def predict_hit(self, topic: str) -> Dict:
        heat = random.uniform(0.5, 0.95)
        return {"topic": topic, "hit_probability": round(heat, 2), "competition": round(random.uniform(0.3, 0.8), 2)}


class OneClickPublisher:
    """一键发布"""

    def __init__(self):
        self.platforms = {
            "douyin": {"name": "抖音", "icon": "🎵"},
            "xiaohongshu": {"name": "小红书", "icon": "📕"},
            "bilibili": {"name": "B站", "icon": "📺"},
            "wechat": {"name": "微信视频号", "icon": "💬"},
        }

    def publish(self, work_id: str, platforms: List[str]) -> Dict:
        results = {}
        for plat in platforms:
            results[plat] = {"status": "success", "url": f"https://{plat}.com/work/{work_id}"}
        return results


class MarketingTools:
    """营销工具"""

    def __init__(self):
        self.tools = {
            "promotion": {"name": "推广投放", "icon": "📢", "desc": "精准推广，提升曝光"},
            "coupon": {"name": "优惠券", "icon": "🎟️", "desc": "发放优惠券吸引新用户"},
            "collaboration": {"name": "合作推广", "icon": "🤝", "desc": "与其他创作者联合推广"},
            "event": {"name": "活动策划", "icon": "🎉", "desc": "策划营销活动"},
            "seo": {"name": "SEO优化", "icon": "🔍", "desc": "优化搜索排名"},
        }

    def create_promotion(self, budget: float, target: str) -> Dict:
        return {
            "budget": budget, "target": target,
            "estimated_reach": int(budget * random.uniform(50, 200)),
            "estimated_conversion": round(budget * random.uniform(0.02, 0.1), 2),
        }


class FanManagement:
    """粉丝运营"""

    def __init__(self):
        self.fan_tiers = {
            "普通粉丝": {"icon": "👤", "range": "0-10互动"},
            "活跃粉丝": {"icon": "⭐", "range": "10-50互动"},
            "核心粉丝": {"icon": "💎", "range": "50-200互动"},
            "超级粉丝": {"icon": "👑", "range": "200+互动"},
        }

    def get_fan_stats(self) -> Dict:
        return {
            "total_fans": random.randint(500, 50000),
            "new_today": random.randint(5, 100),
            "active_rate": round(random.uniform(0.15, 0.45), 2),
            "top_tier": random.randint(10, 500),
        }


def render_topic_center_page():
    """选题中心页面"""
    st.header("💡 选题中心")
    st.caption("热门选题、竞品分析、爆款预测")

    ti = TopicIntelligence()

    tab1, tab2 = st.tabs(["🔥 热门选题", "🔮 爆款预测"])

    with tab1:
        for topic in ti.hot_topics:
            trend_icon = "📈" if topic["trend"] == "up" else ("📉" if topic["trend"] == "down" else "➡️")
            with st.expander(f"{trend_icon} {topic['topic']} — 热度 {topic['heat']}"):
                st.write(f"类别: {topic['category']} | 热度: {topic['heat']} | 趋势: {topic['trend']}")
                st.progress(topic["heat"] / 100)

    with tab2:
        topic_input = st.text_input("输入选题关键词")
        if st.button("预测爆款潜力"):
            result = ti.predict_hit(topic_input)
            st.metric("爆款概率", f"{result['hit_probability']:.0%}")
            st.metric("竞争度", f"{result['competition']:.0%}")


def render_publish_page():
    """发布系统页面"""
    st.header("📤 发布系统")
    st.caption("一键多平台发布、格式适配")

    publisher = OneClickPublisher()

    work_id = st.text_input("作品ID", value="my_work")
    selected = st.multiselect("选择发布平台", list(publisher.platforms.keys()),
                              format_func=lambda x: f"{publisher.platforms[x]['icon']} {publisher.platforms[x]['name']}")

    if st.button("一键发布", use_container_width=True):
        if selected:
            results = publisher.publish(work_id, selected)
            for plat, info in results.items():
                st.success(f"{publisher.platforms[plat]['name']}: 发布成功")
        else:
            st.warning("请选择至少一个平台")


def render_marketing_tools_page():
    """营销工具页面"""
    st.header("📣 营销工具")
    st.caption("推广、活动、SEO优化")

    mt = MarketingTools()

    for tool_id, tool in mt.tools.items():
        with st.expander(f"{tool['icon']} {tool['name']}"):
            st.write(tool["desc"])
            if tool_id == "promotion":
                budget = st.number_input("推广预算（元）", min_value=10, value=100, key=f"budget_{tool_id}")
                if st.button("创建推广", key=f"promo_{tool_id}"):
                    result = mt.create_promotion(budget, "涨粉")
                    st.success(f"预计触达: {result['estimated_reach']}人")


def render_fan_page():
    """粉丝运营页面"""
    st.header("👥 粉丝运营")
    st.caption("粉丝分层、互动管理、粉丝画像")

    fm = FanManagement()
    stats = fm.get_fan_stats()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("总粉丝", f"{stats['total_fans']:,}")
    with c2:
        st.metric("今日新增", stats['new_today'])
    with c3:
        st.metric("活跃率", f"{stats['active_rate']:.0%}")
    with c4:
        st.metric("核心粉丝", stats['top_tier'])

    st.divider()
    st.subheader("粉丝分层")
    for tier, info in fm.fan_tiers.items():
        st.write(f"{info['icon']} **{tier}** — {info['range']}")
