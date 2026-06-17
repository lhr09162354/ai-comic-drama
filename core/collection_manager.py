# -*- coding: utf-8 -*-
"""
v36: 作品合集系统
将多个作品整理成合集/系列
"""
import streamlit as st
from datetime import datetime
from typing import List, Optional


COLLECTION_STYLES = {
    "连续剧": {"emoji": "📺", "desc": "按顺序观看的连续剧集"},
    "单元剧": {"emoji": "🎭", "desc": "独立故事，共享世界观"},
    "选集": {"emoji": "📚", "desc": "精选作品合集"},
    "系列": {"emoji": "🔄", "desc": "同一主题的系列作品"},
    " anthology": {"emoji": "📖", "desc": "短篇故事集"},
}


class Collection:
    """作品合集"""

    def __init__(self, name, style="连续剧", description="", cover_emoji="📺"):
        self.name = name
        self.style = style
        self.description = description
        self.cover_emoji = cover_emoji
        self.works = []
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.updated_at = self.created_at

    def add_work(self, work_title, work_type="单集", episode_num=None):
        work = {
            "title": work_title,
            "type": work_type,
            "episode": episode_num or len(self.works) + 1,
            "added_at": datetime.now().strftime("%m-%d %H:%M"),
            "status": "已发布",
        }
        self.works.append(work)
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def remove_work(self, idx):
        if 0 <= idx < len(self.works):
            self.works.pop(idx)
            # 重新编号
            for i, w in enumerate(self.works):
                w["episode"] = i + 1

    def to_dict(self):
        return {
            "name": self.name, "style": self.style,
            "description": self.description, "cover_emoji": self.cover_emoji,
            "works": self.works,
            "created_at": self.created_at, "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(d):
        c = Collection(d["name"], d.get("style", "连续剧"),
                        d.get("description", ""), d.get("cover_emoji", "📺"))
        c.works = d.get("works", [])
        c.created_at = d.get("created_at", "")
        c.updated_at = d.get("updated_at", "")
        return c


class CollectionManager:
    """合集管理器"""

    def __init__(self):
        self.collections = self._load()

    def _load(self):
        return st.session_state.get("v36_collections", [])

    def _save(self):
        st.session_state["v36_collections"] = self.collections

    def create_collection(self, name, style, description, cover_emoji):
        coll = Collection(name, style, description, cover_emoji)
        self.collections.append(coll.to_dict())
        self._save()
        return coll

    def delete_collection(self, idx):
        if 0 <= idx < len(self.collections):
            self.collections.pop(idx)
            self._save()

    def add_work_to_collection(self, coll_idx, work_title, work_type="单集"):
        if 0 <= coll_idx < len(self.collections):
            coll = self.collections[coll_idx]
            ep_num = len(coll.get("works", [])) + 1
            work = {
                "title": work_title, "type": work_type,
                "episode": ep_num,
                "added_at": datetime.now().strftime("%m-%d %H:%M"),
                "status": "已发布",
            }
            coll.setdefault("works", []).append(work)
            coll["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self._save()

    def remove_work_from_collection(self, coll_idx, work_idx):
        if 0 <= coll_idx < len(self.collections):
            coll = self.collections[coll_idx]
            works = coll.get("works", [])
            if 0 <= work_idx < len(works):
                works.pop(work_idx)
                for i, w in enumerate(works):
                    w["episode"] = i + 1
                self._save()

    def get_stats(self):
        total_collections = len(self.collections)
        total_works = sum(len(c.get("works", [])) for c in self.collections)
        return {"collections": total_collections, "works": total_works}


def render_collection_page():
    """渲染作品合集页面"""
    st.subheader("📚 作品合集")
    st.caption("将多个作品整理成合集/系列，统一管理")

    manager = CollectionManager()
    stats = manager.get_stats()

    # 顶部统计
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("合集数", stats["collections"])
    with c2:
        st.metric("作品数", stats["works"])
    with c3:
        if st.button("➕ 新建合集", use_container_width=True, type="primary"):
            st.session_state["v36_show_create_coll"] = True

    # 创建合集弹窗
    if st.session_state.get("v36_show_create_coll"):
        with st.form("create_collection_form"):
            st.write("### 新建合集")
            c1, c2 = st.columns(2)
            with c1:
                coll_name = st.text_input("合集名称", key="coll_name")
                coll_style = st.selectbox("合集类型", list(COLLECTION_STYLES.keys()),
                                          format_func=lambda x: f"{COLLECTION_STYLES[x]['emoji']} {x}",
                                          key="coll_style")
            with c2:
                coll_desc = st.text_area("合集描述", key="coll_desc", height=80)
                coll_emoji = st.text_input("封面图标", value="📺", key="coll_emoji")

            c1, c2 = st.columns(2)
            with c1:
                if st.form_submit_button("创建", type="primary"):
                    if coll_name:
                        manager.create_collection(coll_name, coll_style, coll_desc, coll_emoji)
                        st.session_state["v36_show_create_coll"] = False
                        st.success(f"合集「{coll_name}」创建成功")
                        st.rerun()
            with c2:
                if st.form_submit_button("取消"):
                    st.session_state["v36_show_create_coll"] = False
                    st.rerun()

    st.divider()

    # 合集列表
    if not manager.collections:
        st.info("暂无合集，点击上方「新建合集」开始整理作品")
    else:
        for i, coll in enumerate(manager.collections):
            style_info = COLLECTION_STYLES.get(coll.get("style", "连续剧"), {})
            with st.expander(f"{coll.get('cover_emoji', '📺')} **{coll['name']}** "
                             f"({style_info.get('emoji', '')} {coll.get('style', '')}) — "
                             f"{len(coll.get('works', []))}部作品"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(coll.get("description", ""))
                    st.caption(f"📅 创建: {coll.get('created_at', '')} | 更新: {coll.get('updated_at', '')}")
                with c2:
                    if st.button("🗑️ 删除合集", key=f"del_coll_{i}"):
                        manager.delete_collection(i)
                        st.rerun()

                # 作品列表
                st.divider()
                works = coll.get("works", [])
                if works:
                    for j, work in enumerate(works):
                        cols = st.columns([1, 3, 1, 1, 1])
                        with cols[0]:
                            st.write(f"EP{work['episode']}")
                        with cols[1]:
                            st.write(f"**{work['title']}**")
                        with cols[2]:
                            st.caption(work["type"])
                        with cols[3]:
                            st.caption(work.get("status", ""))
                        with cols[4]:
                            if st.button("❌", key=f"del_work_{i}_{j}"):
                                manager.remove_work_from_collection(i, j)
                                st.rerun()
                else:
                    st.info("暂无作品")

                # 添加作品
                with st.form(f"add_work_{i}"):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        new_title = st.text_input("作品标题", key=f"wt_{i}")
                    with c2:
                        new_type = st.selectbox("类型", ["单集", "番外", "OVA", "特别篇"], key=f"wty_{i}")
                    with c3:
                        st.write(" ")  # 占位
                        submitted = st.form_submit_button("添加作品")
                    if submitted and new_title:
                        manager.add_work_to_collection(i, new_title, new_type)
                        st.success(f"已添加「{new_title}」")
                        st.rerun()
