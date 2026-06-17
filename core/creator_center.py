# -*- coding: utf-8 -*-
"""
创作者中心 v34 - 合并模块
整合创作者中心、生态系统、成长体系，统一管理创作者等级、成就、勋章
"""

import os
import json
import time
import random
import hashlib
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


# ============ 数据模型 ============

class CreatorLevelType(Enum):
    NEWBIE = "newbie"
    CREATOR = "creator"
    RISING_STAR = "rising_star"
    MASTER = "master"
    LEGEND = "legend"


@dataclass
class CreatorProfileData:
    """创作者档案数据"""
    user_id: str
    username: str = ""
    avatar: Optional[str] = None
    bio: str = ""
    level: int = 1
    xp: int = 0
    coins: int = 0
    total_exp: int = 0
    works_count: int = 0
    total_views: int = 0
    total_likes: int = 0
    followers: int = 0
    achievements: List[str] = field(default_factory=list)
    badges: Dict = field(default_factory=dict)
    created_at: str = ""
    last_active: str = ""


@dataclass
class WorkItem:
    """作品数据"""
    work_id: str
    creator_id: str
    title: str
    description: str = ""
    category: str = "原创"
    tags: List[str] = field(default_factory=list)
    status: str = "draft"
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    created_at: float = 0
    published_at: Optional[float] = None


# ============ 等级系统 ============

LEVEL_SYSTEM = {
    1: {"name": "新手创作者", "exp": 0, "icon": "🌱", "benefits": ["基础模板", "每日5次生成"]},
    2: {"name": "入门创作者", "exp": 100, "icon": "🌿", "benefits": ["标准模板", "每日15次生成", "基础分析"]},
    3: {"name": "成长创作者", "exp": 300, "icon": "🌳", "benefits": ["高级模板", "每日30次生成", "详细分析", "社区功能"]},
    4: {"name": "资深创作者", "exp": 600, "icon": "⭐", "benefits": ["全部模板", "无限生成", "优先客服", "收益功能"]},
    5: {"name": "明星创作者", "exp": 1000, "icon": "🌟", "benefits": ["定制模板", "专属客服", "推广位", "合作邀请"]},
    6: {"name": "大师创作者", "exp": 2000, "icon": "🏆", "benefits": ["品牌特权", "线下活动", "投资机会", "导师指导"]},
    7: {"name": "传奇创作者", "icon": "👑", "exp": 5000, "benefits": ["终身VIP", "专属团队", "版权分成", "名人堂"]},
}

EXP_RULES = {
    "create_work": 10, "complete_work": 20, "share_work": 15,
    "receive_like": 2, "receive_comment": 3, "receive_follow": 5,
    "daily_login": 5, "complete_tutorial": 30, "achieve_milestone": 50,
}

# ============ 成就系统 ============

ACHIEVEMENT_CATEGORIES = {
    "创作": ["first_work", "ten_works", "hundred_works", "series_master", "speed_demon"],
    "社交": ["first_fan", "hundred_fans", "viral_creator", "social_butterfly", "collaboration_king"],
    "质量": ["quality_master", "consistency_king", "perfectionist", "aesthetic_expert", "story_teller"],
    "收益": ["first_coin", "hundred_coins", "rich_creator", "investor_mind", "revenue_master"],
    "探索": ["template_collector", "feature_explorer", "early_adopter", "beta_tester", "feedback_hero"],
}

ACHIEVEMENTS = {
    "first_work": {"name": "初次创作", "desc": "完成你的第一部漫剧作品", "icon": "🎬", "exp": 20, "coins": 10},
    "ten_works": {"name": "十部作品", "desc": "累计完成10部漫剧作品", "icon": "📚", "exp": 50, "coins": 30},
    "hundred_works": {"name": "百部作品", "desc": "累计完成100部漫剧作品", "icon": "🏆", "exp": 200, "coins": 100},
    "series_master": {"name": "连载大师", "desc": "完成一个10章以上的连载作品", "icon": "📖", "exp": 100, "coins": 50},
    "speed_demon": {"name": "速度达人", "desc": "在10分钟内完成一部完整作品", "icon": "⚡", "exp": 30, "coins": 20},
    "first_fan": {"name": "第一位粉丝", "desc": "获得第一位关注者", "icon": "👋", "exp": 15, "coins": 10},
    "hundred_fans": {"name": "百人粉丝团", "desc": "获得100位关注者", "icon": "👥", "exp": 80, "coins": 50},
    "viral_creator": {"name": "病毒式传播", "desc": "单部作品获得1000次浏览", "icon": "🔥", "exp": 150, "coins": 80},
    "social_butterfly": {"name": "社交达人", "desc": "关注100位其他创作者", "icon": "🦋", "exp": 40, "coins": 25},
    "collaboration_king": {"name": "协作之王", "desc": "完成5次合作创作", "icon": "🤝", "exp": 100, "coins": 60},
    "quality_master": {"name": "质量大师", "desc": "连续10部作品获得4.5分以上", "icon": "💎", "exp": 120, "coins": 70},
    "consistency_king": {"name": "稳定发挥", "desc": "连续30天每天完成至少1部作品", "icon": "📅", "exp": 200, "coins": 100},
    "perfectionist": {"name": "完美主义者", "desc": "单部作品修改超过20次", "icon": "🔍", "exp": 30, "coins": 15},
    "aesthetic_expert": {"name": "美学专家", "desc": "使用10种不同画风创作", "icon": "🎨", "exp": 60, "coins": 35},
    "story_teller": {"name": "故事大师", "desc": "创作一个超过5000字的故事", "icon": "✍️", "exp": 80, "coins": 45},
    "first_coin": {"name": "第一桶金", "desc": "获得第一枚创作币", "icon": "🪙", "exp": 10, "coins": 5},
    "hundred_coins": {"name": "百币大户", "desc": "累计获得100枚创作币", "icon": "💰", "exp": 60, "coins": 30},
    "rich_creator": {"name": "富有创作者", "desc": "账户余额超过500创作币", "icon": "💎", "exp": 100, "coins": 50},
    "investor_mind": {"name": "投资者思维", "desc": "使用收益功能进行推广投资", "icon": "📈", "exp": 40, "coins": 25},
    "revenue_master": {"name": "收益大师", "desc": "单月收益超过1000创作币", "icon": "🤑", "exp": 150, "coins": 80},
    "template_collector": {"name": "模板收藏家", "desc": "解锁并使用20种不同模板", "icon": "📋", "exp": 50, "coins": 30},
    "feature_explorer": {"name": "功能探索者", "desc": "使用过所有主要功能", "icon": "🧭", "exp": 70, "coins": 40},
    "early_adopter": {"name": "早期用户", "desc": "在正式发布前开始使用", "icon": "🚀", "exp": 100, "coins": 50},
    "beta_tester": {"name": "测试工程师", "desc": "提交10条有效反馈", "icon": "🛠️", "exp": 80, "coins": 45},
    "feedback_hero": {"name": "反馈英雄", "desc": "提交的反馈被采纳5次", "icon": "🦸", "exp": 150, "coins": 100},
}

# ============ 勋章系统 ============

BADGES = {
    "creation_master": {"name": "创作大师", "icon": "🎨", "desc": "累计创作达到里程碑",
        "tiers": {"bronze": "10部作品", "silver": "50部作品", "gold": "100部作品", "diamond": "500部作品"}},
    "social_star": {"name": "社交之星", "icon": "⭐", "desc": "获得社区认可",
        "tiers": {"bronze": "100粉丝", "silver": "500粉丝", "gold": "5000粉丝", "diamond": "50000粉丝"}},
    "quality_artist": {"name": "品质之匠", "icon": "💎", "desc": "作品质量达到高标准",
        "tiers": {"bronze": "平均3.5分", "silver": "平均4.0分", "gold": "平均4.5分", "diamond": "平均4.8分"}},
    "revenue_earner": {"name": "收益达人", "icon": "💰", "desc": "通过创作获得收益",
        "tiers": {"bronze": "100创作币", "silver": "1000创作币", "gold": "10000创作币", "diamond": "100000创作币"}},
    "innovation_pioneer": {"name": "创新先锋", "icon": "🚀", "desc": "使用创新功能",
        "tiers": {"bronze": "使用5种功能", "silver": "使用10种功能", "gold": "使用20种功能", "diamond": "全功能体验"}},
}


# ============ 创作者中心主类 ============

class CreatorCenterManager:
    """创作者中心统一管理器"""

    def __init__(self):
        self.creators: Dict[str, CreatorProfileData] = {}
        self.daily_challenges = self._gen_daily_challenges()

    def _gen_daily_challenges(self) -> List[Dict]:
        return [
            {"id": "daily_create", "name": "每日创作", "desc": "完成1部漫剧作品", "exp": 20, "coins": 10, "target": 1},
            {"id": "daily_share", "name": "每日分享", "desc": "分享1部作品到社区", "exp": 15, "coins": 8, "target": 1},
            {"id": "daily_interact", "name": "每日互动", "desc": "评论或点赞5部作品", "exp": 25, "coins": 12, "target": 5},
        ]

    def get_or_create(self, user_id: str) -> CreatorProfileData:
        if user_id not in self.creators:
            self.creators[user_id] = CreatorProfileData(
                user_id=user_id,
                username=f"创作者{user_id[:4]}",
                created_at=datetime.now().isoformat(),
                last_active=datetime.now().isoformat(),
            )
        return self.creators[user_id]

    def add_exp(self, user_id: str, amount: int, reason: str = ""):
        creator = self.get_or_create(user_id)
        creator.xp += amount
        creator.total_exp += amount
        # 检查升级
        for lvl in sorted(LEVEL_SYSTEM.keys(), reverse=True):
            if creator.xp >= LEVEL_SYSTEM[lvl]["exp"]:
                creator.level = lvl
                break

    def add_coins(self, user_id: str, amount: int):
        creator = self.get_or_create(user_id)
        creator.coins += amount

    def check_achievements(self, user_id: str) -> List[Dict]:
        creator = self.get_or_create(user_id)
        new_achievements = []
        for ach_id, ach in ACHIEVEMENTS.items():
            if ach_id not in creator.achievements:
                # 简单条件检查
                unlocked = self._check_condition(ach_id, creator)
                if unlocked:
                    creator.achievements.append(ach_id)
                    self.add_exp(user_id, ach["exp"])
                    self.add_coins(user_id, ach["coins"])
                    new_achievements.append(ach)
        return new_achievements

    def _check_condition(self, ach_id: str, creator: CreatorProfileData) -> bool:
        if ach_id == "first_work" and creator.works_count >= 1:
            return True
        if ach_id == "ten_works" and creator.works_count >= 10:
            return True
        if ach_id == "first_fan" and creator.followers >= 1:
            return True
        if ach_id == "hundred_fans" and creator.followers >= 100:
            return True
        return False

    def get_level_info(self, xp: int) -> Dict:
        current_level = 1
        for lvl, info in LEVEL_SYSTEM.items():
            if xp >= info["exp"]:
                current_level = lvl
            else:
                break
        info = LEVEL_SYSTEM[current_level]
        next_lvl = current_level + 1 if current_level < 7 else None
        next_exp = LEVEL_SYSTEM[next_lvl]["exp"] if next_lvl else None
        progress = 0
        if next_exp:
            progress = (xp - info["exp"]) / (next_exp - info["exp"])
        return {"level": current_level, "info": info, "next_exp": next_exp, "progress": min(progress, 1.0)}

    # ============ 渲染方法 ============

    def render_dashboard(self, user_id: str):
        creator = self.get_or_create(user_id)
        level_info = self.get_level_info(creator.xp)
        info = level_info["info"]

        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            st.metric(f"{info['icon']} {info['name']}", f"Lv.{level_info['level']}")
        with c2:
            next_exp = level_info.get("next_exp", "MAX")
            st.progress(level_info["progress"], text=f"经验: {creator.xp}/{next_exp}")
        with c3:
            st.metric("💰 创作币", creator.coins)

        st.markdown("---")
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.metric("📚 作品", creator.works_count)
        with mc2:
            st.metric("👁️ 浏览", creator.total_views)
        with mc3:
            st.metric("❤️ 点赞", creator.total_likes)
        with mc4:
            st.metric("👥 粉丝", creator.followers)

        with st.expander("🌟 等级特权"):
            for benefit in info.get("benefits", []):
                st.write(f"✅ {benefit}")

    def render_achievements(self, user_id: str):
        creator = self.get_or_create(user_id)
        st.subheader("🏆 成就中心")
        unlocked = set(creator.achievements)
        total = len(ACHIEVEMENTS)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("已解锁", len(unlocked))
        with c2:
            st.metric("未解锁", total - len(unlocked))

        for category, ach_ids in ACHIEVEMENT_CATEGORIES.items():
            with st.expander(f"📁 {category}类成就"):
                for ach_id in ach_ids:
                    ach = ACHIEVEMENTS.get(ach_id, {})
                    status = "✅" if ach_id in unlocked else "🔒"
                    st.write(f"{status} **{ach.get('icon', '')} {ach.get('name', '')}** - {ach.get('desc', '')}")

    def render_badges(self, user_id: str):
        creator = self.get_or_create(user_id)
        st.subheader("🏅 勋章中心")
        cols = st.columns(min(len(BADGES), 5))
        tier_icons = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "diamond": "💎"}
        for idx, (bid, badge) in enumerate(BADGES.items()):
            with cols[idx % len(cols)]:
                tier = creator.badges.get(bid)
                icon = tier_icons.get(tier, "🔒") if tier else "🔒"
                st.write(f"{icon} **{badge['icon']} {badge['name']}**")
                st.caption(f"等级: {tier or '未解锁'}")

    def render_challenges(self, user_id: str):
        st.subheader("📅 每日挑战")
        for ch in self.daily_challenges:
            progress = random.uniform(0.2, 0.8)
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.write(f"**{ch['name']}**")
                    st.caption(ch['desc'])
                with c2:
                    st.write(f"💎 {ch['coins']}")
                with c3:
                    st.write(f"⭐ {ch['exp']}")
                st.progress(progress, text=f"{int(progress * ch['target'])}/{ch['target']}")

    def render_leaderboard(self, user_id: str):
        st.subheader("🏅 创作者排行榜")
        leaders = [
            {"rank": 1, "name": "创意大师小明", "exp": 5800, "icon": "👑"},
            {"rank": 2, "name": "高产达人小红", "exp": 4200, "icon": "⭐"},
            {"rank": 3, "name": "新星创作者", "exp": 3800, "icon": "🌟"},
            {"rank": 4, "name": "漫剧狂热者", "exp": 2900, "icon": "🎭"},
            {"rank": 5, "name": "故事编织者", "exp": 2100, "icon": "📖"},
        ]
        for leader in leaders:
            c1, c2, c3 = st.columns([1, 4, 1])
            with c1:
                st.write(f"**#{leader['rank']}**")
            with c2:
                st.write(f"{leader['icon']} {leader['name']}")
            with c3:
                st.write(f"⭐ {leader['exp']}")

    def render_growth_page(self, user_id: str):
        """成长体系页面（合并自creator_growth）"""
        st.subheader("🌟 创作者成长体系")
        creator = self.get_or_create(user_id)
        level_info = self.get_level_info(creator.xp)

        # 等级进度
        st.write(f"**当前等级**: {level_info['info']['icon']} {level_info['info']['name']}")
        st.progress(level_info["progress"])

        # 等级路线图
        with st.expander("🗺️ 等级路线图"):
            for lvl, info in LEVEL_SYSTEM.items():
                status = "✅" if creator.xp >= info["exp"] else "🔒"
                st.write(f"{status} Lv.{lvl} {info['icon']} {info['name']} (需要 {info['exp']} EXP)")

        # 成长任务
        with st.expander("📋 成长任务"):
            for rule_name, exp in EXP_RULES.items():
                st.write(f"- {rule_name}: +{exp} EXP")


# 全局实例
_center_mgr = None

def get_creator_center() -> CreatorCenterManager:
    global _center_mgr
    if _center_mgr is None:
        _center_mgr = CreatorCenterManager()
    return _center_mgr

# 兼容旧接口
get_creator_ecosystem = get_creator_center


def render_creator_center_page():
    """创作者中心页面"""
    st.header("👤 创作者中心")
    st.caption("作品管理、数据分析、成就系统、成长路径")

    mgr = get_creator_center()
    user_id = "current_user"

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 仪表盘", "🏆 成就", "🏅 勋章", "📅 挑战", "🏆 排行榜"])

    with tab1:
        mgr.render_dashboard(user_id)
    with tab2:
        mgr.render_achievements(user_id)
    with tab3:
        mgr.render_badges(user_id)
    with tab4:
        mgr.render_challenges(user_id)
    with tab5:
        mgr.render_leaderboard(user_id)


def render_growth_center_page():
    """成长中心页面"""
    st.header("🌟 创作者成长中心")
    mgr = get_creator_center()
    user_id = "current_user"
    mgr.render_growth_page(user_id)
