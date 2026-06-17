# -*- coding: utf-8 -*-
"""
作品统计系统 v34 - 播放量、点赞数、趋势分析
提供作品维度的数据展示与对比
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random


class WorkStatistics:
    """作品统计系统"""

    def __init__(self):
        self.metrics = ["views", "likes", "shares", "comments", "favorites", "completion_rate"]
        self.metric_labels = {
            "views": "播放量", "likes": "点赞数", "shares": "分享数",
            "comments": "评论数", "favorites": "收藏数", "completion_rate": "完播率"
        }
        self._init_session_state()

    def _init_session_state(self):
        if "work_stats_cache" not in st.session_state:
            st.session_state.work_stats_cache = {}

    def get_work_stats(self, work_id: str) -> Dict:
        """获取作品统计（模拟数据）"""
        if work_id in st.session_state.work_stats_cache:
            return st.session_state.work_stats_cache[work_id]

        base_views = random.randint(100, 50000)
        like_rate = random.uniform(0.02, 0.15)
        stats = {
            "work_id": work_id,
            "views": base_views,
            "likes": int(base_views * like_rate),
            "shares": int(base_views * random.uniform(0.005, 0.05)),
            "comments": int(base_views * random.uniform(0.01, 0.08)),
            "favorites": int(base_views * random.uniform(0.01, 0.06)),
            "completion_rate": round(random.uniform(0.35, 0.85), 2),
            "avg_watch_time": round(random.uniform(15, 120), 1),
            "trend": random.choice(["up", "stable", "down"]),
            "daily_trend": self._gen_daily_trend(base_views),
            "source_distribution": {
                "推荐": random.uniform(0.3, 0.5),
                "搜索": random.uniform(0.1, 0.2),
                "分享": random.uniform(0.15, 0.3),
                "主页": random.uniform(0.05, 0.15),
            },
            "updated_at": datetime.now().isoformat(),
        }
        st.session_state.work_stats_cache[work_id] = stats
        return stats

    def _gen_daily_trend(self, base: int) -> List[Dict]:
        """生成7日趋势"""
        trend = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6 - i)
            factor = random.uniform(0.7, 1.3)
            trend.append({
                "date": date.strftime("%m-%d"),
                "views": int(base / 7 * factor),
                "likes": int(base / 7 * factor * random.uniform(0.02, 0.1)),
            })
        return trend

    def get_overview_stats(self, work_ids: List[str] = None) -> Dict:
        """获取总览统计"""
        if not work_ids:
            work_ids = [f"work_{i}" for i in range(1, 6)]
        total = {"views": 0, "likes": 0, "shares": 0, "comments": 0, "favorites": 0}
        for wid in work_ids:
            s = self.get_work_stats(wid)
            for k in total:
                total[k] += s.get(k, 0)
        total["work_count"] = len(work_ids)
        total["avg_completion"] = round(random.uniform(0.4, 0.7), 2)
        return total

    def compare_works(self, work_ids: List[str]) -> Dict:
        """对比多个作品"""
        comparison = {}
        for wid in work_ids:
            comparison[wid] = self.get_work_stats(wid)
        return comparison


def render_work_statistics_page():
    """作品统计页面"""
    st.header("📊 作品统计")
    st.caption("查看作品播放量、点赞数等核心指标和趋势")

    stats = WorkStatistics()

    # 概览卡片
    overview = stats.get_overview_stats()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("总播放量", f"{overview['views']:,}", delta=f"+{random.randint(100, 2000)}")
    with c2:
        st.metric("总点赞", f"{overview['likes']:,}", delta=f"+{random.randint(10, 500)}")
    with c3:
        st.metric("总评论", f"{overview['comments']:,}", delta=f"+{random.randint(5, 200)}")
    with c4:
        st.metric("完播率", f"{overview['avg_completion']:.0%}")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📈 趋势分析", "📋 作品列表", "⚖️ 作品对比"])

    with tab1:
        st.subheader("近7日趋势")
        sample_work = stats.get_work_stats("work_1")
        trend = sample_work["daily_trend"]
        dates = [t["date"] for t in trend]
        views = [t["views"] for t in trend]
        likes = [t["likes"] for t in trend]

        # 简易趋势图
        chart_data = {"日期": dates, "播放量": views, "点赞数": likes}
        st.line_chart(chart_data, x="日期")

        st.divider()
        st.subheader("来源分布")
        source_dist = sample_work["source_distribution"]
        for source, pct in source_dist.items():
            pct_display = f"{pct:.0%}"
            st.markdown(f"**{source}**: {pct_display}")
            st.progress(min(pct, 1.0))

    with tab2:
        st.subheader("作品数据列表")
        for i in range(1, 6):
            work_id = f"work_{i}"
            ws = stats.get_work_stats(work_id)
            trend_icon = "📈" if ws["trend"] == "up" else ("➡️" if ws["trend"] == "stable" else "📉")
            with st.expander(f"{trend_icon} 作品 {i} — {ws['views']:,} 播放"):
                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.metric("播放量", f"{ws['views']:,}")
                    st.metric("分享数", f"{ws['shares']:,}")
                with mc2:
                    st.metric("点赞数", f"{ws['likes']:,}")
                    st.metric("收藏数", f"{ws['favorites']:,}")
                with mc3:
                    st.metric("评论数", f"{ws['comments']:,}")
                    st.metric("完播率", f"{ws['completion_rate']:.0%}")

    with tab3:
        st.subheader("作品对比")
        selected = st.multiselect("选择对比作品（最多3个）",
                                  [f"作品 {i}" for i in range(1, 6)],
                                  default=["作品 1", "作品 2"],
                                  max_selections=3)
        if selected:
            work_ids = [f"work_{s.split()[-1]}" for s in selected]
            comparison = stats.compare_works(work_ids)
            for metric_key, metric_label in stats.metric_labels.items():
                st.markdown(f"**{metric_label}**")
                vals = []
                for wid, wdata in comparison.items():
                    val = wdata.get(metric_key, 0)
                    vals.append(val)
                    name = f"作品 {wid.split('_')[-1]}"
                    if metric_key == "completion_rate":
                        st.markdown(f"- {name}: {val:.0%}")
                    else:
                        st.markdown(f"- {name}: {val:,}")
                if vals and max(vals) > 0:
                    best_idx = vals.index(max(vals))
                    best_name = list(comparison.keys())[best_idx]
                    st.caption(f"🏆 领先: 作品 {best_name.split('_')[-1]}")
                st.markdown("")
