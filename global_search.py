# -*- coding: utf-8 -*-
"""
v36: 全局搜索增强
跨模块查找角色、剧本、素材、设置等
"""
import streamlit as st
from typing import List, Optional


SEARCH_CATEGORIES = {
    "全部": {"emoji": "🔍", "desc": "搜索所有模块"},
    "角色": {"emoji": "👤", "desc": "搜索角色名称、性格、外貌"},
    "剧本": {"emoji": "📝", "desc": "搜索剧本标题、内容、标签"},
    "素材": {"emoji": "📦", "desc": "搜索素材名称、类型"},
    "模板": {"emoji": "📋", "desc": "搜索故事模板、风格模板"},
    "设置": {"emoji": "⚙️", "desc": "搜索设置项、配置"},
    "教程": {"emoji": "📚", "desc": "搜索使用教程、技巧"},
}


class GlobalSearchEngine:
    """全局搜索引擎"""

    def search_characters(self, query):
        """搜索角色"""
        results = []
        for c in st.session_state.get("characters", []):
            if not isinstance(c, dict):
                continue
            name = c.get("name", "")
            personality = c.get("personality", "")
            appearance = c.get("appearance", "")
            if query.lower() in name.lower() or query.lower() in personality.lower() or query.lower() in appearance.lower():
                results.append({
                    "category": "角色", "emoji": "👤",
                    "title": name, "desc": f"性格: {personality}",
                    "action": "角色管理"
                })
        return results

    def search_scripts(self, query):
        """搜索剧本"""
        results = []
        script = st.session_state.get("generated_script", "")
        story_title = st.session_state.get("story_title", "")
        if query.lower() in story_title.lower():
            results.append({
                "category": "剧本", "emoji": "📝",
                "title": story_title, "desc": "当前剧本",
                "action": "创作工坊"
            })
        if script and query.lower() in str(script).lower():
            results.append({
                "category": "剧本", "emoji": "📝",
                "title": f"包含「{query}」的剧本内容", "desc": "剧本内容匹配",
                "action": "创作工坊"
            })
        return results

    def search_templates(self, query):
        """搜索模板"""
        results = []
        from config import STORY_TEMPLATES, ART_STYLES
        for key, tmpl in STORY_TEMPLATES.items():
            theme = tmpl.get("theme", "")
            desc = tmpl.get("desc", "")
            if query.lower() in theme.lower() or query.lower() in desc.lower():
                results.append({
                    "category": "模板", "emoji": "📋",
                    "title": theme, "desc": desc,
                    "action": "创作工坊"
                })
        for key, style in ART_STYLES.items():
            name = style.get("name", "")
            if query.lower() in name.lower():
                results.append({
                    "category": "模板", "emoji": "🎨",
                    "title": name, "desc": "画风模板",
                    "action": "创作工坊"
                })
        return results

    def search_all(self, query, category="全部"):
        """全局搜索"""
        if not query.strip():
            return []
        results = []
        if category in ("全部", "角色"):
            results.extend(self.search_characters(query))
        if category in ("全部", "剧本"):
            results.extend(self.search_scripts(query))
        if category in ("全部", "模板"):
            results.extend(self.search_templates(query))
        return results

    def get_hot_keywords(self):
        """获取热门搜索词"""
        return ["甜宠", "修仙", "校园", "赛博朋克", "悬疑", "国风", "古风", "热血"]

    def get_recent_searches(self):
        """获取最近搜索"""
        return st.session_state.get("v36_recent_searches", [])

    def add_recent_search(self, query):
        """添加最近搜索"""
        recent = st.session_state.get("v36_recent_searches", [])
        if query in recent:
            recent.remove(query)
        recent.insert(0, query)
        st.session_state["v36_recent_searches"] = recent[:10]


def render_global_search_page():
    """渲染全局搜索页面"""
    st.subheader("🔍 全局搜索")
    st.caption("跨模块搜索角色、剧本、模板、素材")

    engine = GlobalSearchEngine()

    # 搜索栏
    c1, c2 = st.columns([4, 1])
    with c1:
        query = st.text_input("搜索", placeholder="输入关键词搜索...", key="v36_global_search")
    with c2:
        category = st.selectbox("分类", list(SEARCH_CATEGORIES.keys()),
                                 format_func=lambda x: f"{SEARCH_CATEGORIES[x]['emoji']} {x}",
                                 key="v36_search_cat")

    if st.button("🔍 搜索", type="primary", use_container_width=True) or query:
        if query:
            engine.add_recent_search(query)
            results = engine.search_all(query, category)
            st.session_state["v36_search_results"] = results

    # 搜索结果
    results = st.session_state.get("v36_search_results", [])
    if results:
        st.write(f"找到 **{len(results)}** 个结果")
        for r in results:
            with st.container():
                cols = st.columns([1, 6, 2])
                with cols[0]:
                    st.write(r["emoji"])
                with cols[1]:
                    st.write(f"**{r['title']}**")
                    st.caption(r["desc"])
                with cols[2]:
                    st.caption(f"📂 {r['category']}")
                    if st.button("前往", key=f"goto_{r['title']}", use_container_width=True):
                        st.session_state.active_tab = r["action"]
                        st.rerun()
    elif query:
        st.info(f"未找到与「{query}」相关的内容")

    st.divider()

    # 热门搜索
    c1, c2 = st.columns(2)
    with c1:
        st.write("**🔥 热门搜索**")
        for kw in engine.get_hot_keywords():
            if st.button(kw, key=f"hot_{kw}", use_container_width=True):
                st.session_state["v36_global_search"] = kw
                st.rerun()

    with c2:
        recent = engine.get_recent_searches()
        if recent:
            st.write("**🕐 最近搜索**")
            for kw in recent[:5]:
                if st.button(kw, key=f"recent_{kw}", use_container_width=True):
                    st.session_state["v36_global_search"] = kw
                    st.rerun()
