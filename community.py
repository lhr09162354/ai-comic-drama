# -*- coding: utf-8 -*-
"""
社区系统 v34 - 合并模块
整合社区互动与社交裂变，统一管理评论、关注、动态、裂变传播
"""

import streamlit as st
import json
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    SYSTEM = "system"
    ACTIVITY = "activity"


class NotificationType(Enum):
    FOLLOW = "follow"
    COMMENT = "comment"
    LIKE = "like"
    MESSAGE = "message"
    MENTION = "mention"
    SYSTEM = "system"


class ActivityType(Enum):
    POST_WORK = "post_work"
    UPDATE_WORK = "update_work"
    COMMENT = "comment"
    LIKE = "like"
    FOLLOW = "follow"
    ACHIEVEMENT = "achievement"


@dataclass
class CommentData:
    comment_id: str = ""
    user_id: str = ""
    content: str = ""
    created_at: str = ""
    likes: int = 0
    replies: List = field(default_factory=list)


@dataclass
class NotificationData:
    notif_id: str = ""
    user_id: str = ""
    type: str = ""
    content: str = ""
    created_at: str = ""
    read: bool = False


@dataclass
class ActivityData:
    activity_id: str = ""
    user_id: str = ""
    type: str = ""
    content: str = ""
    created_at: str = ""
    likes: int = 0
    comments: int = 0


class CommunityManager:
    """社区管理器"""

    def __init__(self):
        self.users: Dict[str, Dict] = {}
        self.comments: List[CommentData] = []
        self.notifications: List[NotificationData] = []
        self.activities: List[ActivityData] = []
        self.follows: Dict[str, set] = {}

    def post_comment(self, user_id: str, content: str, target_id: str = "") -> CommentData:
        comment = CommentData(
            comment_id=str(uuid.uuid4())[:8], user_id=user_id, content=content,
            created_at=datetime.now().isoformat()
        )
        self.comments.append(comment)
        return comment

    def follow_user(self, follower_id: str, target_id: str):
        if follower_id not in self.follows:
            self.follows[follower_id] = set()
        self.follows[follower_id].add(target_id)

    def get_feed(self, user_id: str = None, limit: int = 20) -> List[ActivityData]:
        return self.activities[:limit]

    def get_notifications(self, user_id: str) -> List[NotificationData]:
        return [n for n in self.notifications if n.user_id == user_id][:20]


class SocialFissionManager:
    """社交裂变管理器"""

    def __init__(self):
        self.fission_modes = {
            "invite_friend": {"name": "邀请好友", "icon": "👥", "reward": 50},
            "share_work": {"name": "分享作品", "icon": "📤", "reward": 10},
            "group_watching": {"name": "组队观看", "icon": "🎬", "min": 3},
            "challenge": {"name": "挑战赛", "icon": "🏆", "reward": 100},
        }
        self.invites: Dict[str, List] = {}

    def create_invite(self, user_id: str) -> str:
        code = f"INV_{user_id[:4]}_{random.randint(1000, 9999)}"
        if user_id not in self.invites:
            self.invites[user_id] = []
        self.invites[user_id].append({"code": code, "created_at": datetime.now().isoformat()})
        return code

    def process_invite(self, code: str, new_user_id: str) -> bool:
        return True

    def get_fission_stats(self, user_id: str) -> Dict:
        invites = len(self.invites.get(user_id, []))
        return {
            "total_invites": invites,
            "successful_invites": max(invites - 1, 0),
            "total_reward": invites * 50,
            "share_count": random.randint(5, 50),
            "group_count": random.randint(1, 10),
        }


def render_community_page():
    """社区页面"""
    st.header("💬 社区")
    st.caption("互动交流、关注创作者、社交裂变")

    mgr = CommunityManager()
    fission = SocialFissionManager()

    tab1, tab2, tab3, tab4 = st.tabs(["📰 动态", "💬 评论", "🔔 通知", "🔥 社交裂变"])

    with tab1:
        st.subheader("社区动态")
        # 模拟动态
        mock_activities = [
            {"user": "创意大师小明", "type": "发布作品", "content": "《星际冒险》第3集", "time": "2分钟前"},
            {"user": "漫画达人", "type": "获得成就", "content": "解锁「连载大师」", "time": "15分钟前"},
            {"user": "故事编织者", "type": "发布作品", "content": "《甜蜜日常》", "time": "1小时前"},
        ]
        for act in mock_activities:
            with st.container():
                st.write(f"**{act['user']}** {act['type']}: {act['content']}")
                st.caption(act['time'])
                st.divider()

    with tab2:
        st.subheader("热门评论")
        comment = st.text_area("发表评论", height=80)
        if st.button("发送"):
            if comment:
                st.success("评论已发送")

    with tab3:
        st.subheader("通知")
        notifs = mgr.get_notifications("current_user")
        if notifs:
            for n in notifs:
                icon = {"follow": "👤", "comment": "💬", "like": "❤️", "system": "🔔"}.get(n.type, "🔔")
                st.write(f"{icon} {n.content}")
        else:
            st.info("暂无新通知")

    with tab4:
        st.subheader("社交裂变")
        stats = fission.get_fission_stats("current_user")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("邀请好友", stats["total_invites"])
        with c2:
            st.metric("分享次数", stats["share_count"])
        with c3:
            st.metric("裂变奖励", f"{stats['total_reward']}币")

        st.divider()
        if st.button("生成邀请链接", use_container_width=True):
            code = fission.create_invite("current_user")
            st.success(f"邀请码: {code}")

        with st.expander("裂变模式说明"):
            for mode_id, mode in fission.fission_modes.items():
                st.write(f"{mode['icon']} **{mode['name']}** - 奖励: {mode.get('reward', 0)}币")


# 兼容旧接口
User = type('User', (), {})
Comment = CommentData
Message = NotificationData
Notification = NotificationData
Activity = ActivityData
FollowManager = type('FollowManager', (), {})
