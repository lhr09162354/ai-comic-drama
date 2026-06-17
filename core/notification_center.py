# -*- coding: utf-8 -*-
"""
v36: 通知中心
重要消息和更新提醒系统
"""
import streamlit as st
from datetime import datetime
from typing import List, Optional


NOTIFICATION_TYPES = {
    "system": {"emoji": "🔔", "label": "系统通知", "color": "#2196F3"},
    "update": {"emoji": "🆕", "label": "功能更新", "color": "#4CAF50"},
    "social": {"emoji": "💬", "label": "社交消息", "color": "#FF9800"},
    "achievement": {"emoji": "🏆", "label": "成就解锁", "color": "#9C27B0"},
    "reminder": {"emoji": "⏰", "label": "创作提醒", "color": "#F44336"},
    "tip": {"emoji": "💡", "label": "创作技巧", "color": "#00BCD4"},
}


class Notification:
    def __init__(self, ntype, title, content, time=None, read=False, sticky=False):
        self.type = ntype
        self.title = title
        self.content = content
        self.time = time or datetime.now().strftime("%m-%d %H:%M")
        self.read = read
        self.sticky = sticky  # 不自动消失

    def to_dict(self):
        return {"type": self.type, "title": self.title, "content": self.content,
                "time": self.time, "read": self.read, "sticky": self.sticky}

    @staticmethod
    def from_dict(d):
        return Notification(d["type"], d["title"], d["content"],
                           d.get("time"), d.get("read", False), d.get("sticky", False))


class NotificationCenter:
    """通知中心管理器"""

    def __init__(self):
        self.notifications = self._load()

    def _load(self):
        defaults = self._default_notifications()
        saved = st.session_state.get("v36_notifications", None)
        if saved is None:
            st.session_state["v36_notifications"] = defaults
            return defaults
        return saved

    def _save(self):
        st.session_state["v36_notifications"] = self.notifications

    def _default_notifications(self):
        return [
            {"type": "update", "title": "v36新功能上线", "content": "角色关系图谱、剧情节奏控制、运镜建议、海报生成等新功能已上线，快来体验！", "time": "06-17 08:00", "read": False, "sticky": True},
            {"type": "tip", "title": "运镜技巧", "content": "试试在视频生成时使用运镜建议，让作品更有电影感！", "time": "06-17 07:30", "read": False, "sticky": False},
            {"type": "system", "title": "欢迎回来", "content": "今天想创作什么类型的故事呢？", "time": "06-17 07:00", "read": False, "sticky": False},
        ]

    def add_notification(self, ntype, title, content, sticky=False):
        n = Notification(ntype, title, content, sticky=sticky)
        self.notifications.insert(0, n.to_dict())
        self._save()

    def mark_read(self, idx):
        if 0 <= idx < len(self.notifications):
            self.notifications[idx]["read"] = True
            self._save()

    def mark_all_read(self):
        for n in self.notifications:
            n["read"] = True
        self._save()

    def remove_notification(self, idx):
        if 0 <= idx < len(self.notifications):
            self.notifications.pop(idx)
            self._save()

    def clear_read(self):
        self.notifications = [n for n in self.notifications if not n["read"] or n.get("sticky")]
        self._save()

    def get_unread_count(self):
        return sum(1 for n in self.notifications if not n["read"])

    def get_by_type(self, ntype):
        return [n for n in self.notifications if n["type"] == ntype]


def render_notification_center_page():
    """渲染通知中心页面"""
    st.subheader("🔔 通知中心")
    st.caption("查看系统通知、功能更新和创作提醒")

    center = NotificationCenter()
    unread = center.get_unread_count()

    # 顶部操作栏
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.metric("未读通知", unread)
    with c2:
        if st.button("✅ 全部已读", use_container_width=True, disabled=unread == 0):
            center.mark_all_read()
            st.rerun()
    with c3:
        if st.button("🗑️ 清除已读", use_container_width=True):
            center.clear_read()
            st.rerun()

    # 筛选
    filter_type = st.selectbox("筛选类型", ["全部"] + list(NOTIFICATION_TYPES.keys()),
                                format_func=lambda x: "全部" if x == "全部" else f"{NOTIFICATION_TYPES[x]['emoji']} {NOTIFICATION_TYPES[x]['label']}")

    st.divider()

    # 通知列表
    notifications = center.notifications
    if filter_type != "全部":
        notifications = [n for n in notifications if n["type"] == filter_type]

    if not notifications:
        st.info("暂无通知 🎉")
    else:
        for i, n in enumerate(notifications):
            info = NOTIFICATION_TYPES.get(n["type"], NOTIFICATION_TYPES["system"])
            bg = "#1a2332" if not n["read"] else "transparent"
            border = f"border-left: 3px solid {info['color']}" if not n["read"] else ""

            with st.container():
                cols = st.columns([1, 8, 1])
                with cols[0]:
                    st.write(info["emoji"])
                with cols[1]:
                    st.write(f"**{n['title']}**" if not n["read"] else n["title"])
                    st.caption(f"{n['content']}")
                    st.caption(f"📅 {n['time']} | {info['label']}")
                with cols[2]:
                    if not n["read"]:
                        if st.button("✓", key=f"read_{i}"):
                            center.mark_read(i)
                            st.rerun()

    # 快捷创建提醒
    st.divider()
    with st.expander("➕ 创建创作提醒"):
        c1, c2 = st.columns(2)
        with c1:
            remind_title = st.text_input("提醒标题", key="remind_title")
            remind_time = st.text_input("提醒时间", placeholder="例如：每天 20:00", key="remind_time")
        with c2:
            remind_type = st.selectbox("类型", list(NOTIFICATION_TYPES.keys()),
                                        format_func=lambda x: f"{NOTIFICATION_TYPES[x]['emoji']} {NOTIFICATION_TYPES[x]['label']}",
                                        key="remind_type")
            remind_content = st.text_input("提醒内容", key="remind_content")

        if st.button("创建提醒", use_container_width=True):
            if remind_title:
                center.add_notification(remind_type, remind_title, remind_content or remind_time)
                st.success("提醒已创建")
                st.rerun()
