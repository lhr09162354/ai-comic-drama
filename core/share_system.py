# -*- coding: utf-8 -*-
"""
分享系统 v34 - 合并模块
整合分享系统与极速分享，统一管理多平台分享、水印、格式适配
"""

import streamlit as st
import json
import base64
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from io import BytesIO


# ============ 分享平台配置 ============

SHARE_PLATFORMS = {
    "douyin": {"name": "抖音", "icon": "🎵", "color": "#00f2ea", "max_duration": "60秒/3分钟", "ratio": "9:16"},
    "xiaohongshu": {"name": "小红书", "icon": "📕", "color": "#ff2442", "max_duration": "5分钟", "ratio": "3:4"},
    "bilibili": {"name": "哔哩哔哩", "icon": "📺", "color": "#00a1d6", "max_duration": "无限制", "ratio": "16:9"},
    "wechat": {"name": "微信", "icon": "💬", "color": "#07c160", "max_duration": "5分钟", "ratio": "1:1"},
    "weibo": {"name": "微博", "icon": "🔴", "color": "#ff8200", "max_duration": "5分钟", "ratio": "16:9"},
    "kuaishou": {"name": "快手", "icon": "🎬", "color": "#ff4906", "max_duration": "10分钟", "ratio": "9:16"},
    "twitter": {"name": "X/Twitter", "icon": "🐦", "color": "#1da1f2", "max_duration": "2分20秒", "ratio": "16:9"},
    "tiktok": {"name": "TikTok", "icon": "🎵", "color": "#000000", "max_duration": "3分钟", "ratio": "9:16"},
}

WATERMARK_POSITIONS = ["右下角", "左下角", "居中", "右上角", "左上角", "无水印"]

SHARE_TEMPLATES = {
    "标准分享": {"desc": "基础分享卡片", "elements": ["封面图", "标题", "简介", "二维码"]},
    "海报分享": {"desc": "精美海报样式", "elements": ["大封面", "装饰框", "标题", "作者", "二维码"]},
    "预告片分享": {"desc": "视频预告+链接", "elements": ["视频片段", "标题", "发布时间", "链接"]},
    "故事卡片": {"desc": "叙事式分享", "elements": ["场景图", "对白", "角色", "链接"]},
    "对比图分享": {"desc": "前后对比效果", "elements": ["原图", "效果图", "标题", "链接"]},
}


class ShareSystem:
    """分享系统主类"""

    def __init__(self):
        self.platforms = SHARE_PLATFORMS
        self.share_history = []

    def create_share_config(self, platform: str, work_data: Dict) -> Dict:
        """创建平台适配的分享配置"""
        plat = self.platforms.get(platform, {})
        return {
            "platform": platform,
            "platform_name": plat.get("name", platform),
            "aspect_ratio": plat.get("ratio", "16:9"),
            "max_duration": plat.get("max_duration", "无限制"),
            "watermark_position": "右下角",
            "auto_caption": True,
            "include_qr": True,
        }

    def generate_share_link(self, work_id: str, platform: str) -> str:
        """生成分享链接"""
        base = "https://comic-drama.app/share/"
        return f"{base}{work_id}?p={platform}&t={datetime.now().strftime('%Y%m%d')}"

    def get_share_preview(self, platform: str, template: str = "标准分享") -> Dict:
        """获取分享预览"""
        plat = self.platforms.get(platform, {})
        tmpl = SHARE_TEMPLATES.get(template, {})
        return {
            "platform": plat.get("name", platform),
            "template": template,
            "elements": tmpl.get("elements", []),
            "aspect_ratio": plat.get("ratio", "16:9"),
        }

    def quick_share(self, work_id: str, platforms: List[str]) -> Dict:
        """一键多平台分享"""
        results = {}
        for plat in platforms:
            results[plat] = {
                "link": self.generate_share_link(work_id, plat),
                "status": "ready",
                "config": self.create_share_config(plat, {}),
            }
        self.share_history.append({
            "work_id": work_id, "platforms": platforms,
            "timestamp": datetime.now().isoformat(), "results": results,
        })
        return results


class QuickShareSystem:
    """极速分享（轻量级）"""

    def __init__(self):
        self.system = ShareSystem()

    def one_click_share(self, work_id: str) -> Dict:
        """一键分享到所有主要平台"""
        main_platforms = ["douyin", "xiaohongshu", "bilibili", "wechat"]
        return self.system.quick_share(work_id, main_platforms)

    def share_with_caption(self, work_id: str, platform: str, caption: str) -> Dict:
        """带文案分享"""
        link = self.system.generate_share_link(work_id, platform)
        return {"link": link, "caption": caption, "platform": platform}


def render_share_page():
    """分享页面"""
    st.header("📤 分享系统")
    st.caption("多平台分享、格式适配、一键发布")

    system = ShareSystem()
    quick = QuickShareSystem()

    tab1, tab2, tab3 = st.tabs(["🔗 分享作品", "⚡ 极速分享", "📋 分享记录"])

    with tab1:
        st.subheader("分享到指定平台")
        work_id = st.text_input("作品ID", value="demo_work")
        platform = st.selectbox("选择平台", list(SHARE_PLATFORMS.keys()),
                                format_func=lambda x: f"{SHARE_PLATFORMS[x]['icon']} {SHARE_PLATFORMS[x]['name']}")
        template = st.selectbox("分享模板", list(SHARE_TEMPLATES.keys()))
        watermark = st.selectbox("水印位置", WATERMARK_POSITIONS)

        if st.button("生成分享链接", use_container_width=True):
            config = system.create_share_config(platform, {})
            link = system.generate_share_link(work_id, platform)
            st.success(f"✅ 分享链接已生成")
            st.code(link)
            preview = system.get_share_preview(platform, template)
            st.json(preview)

    with tab2:
        st.subheader("一键多平台分享")
        work_id_q = st.text_input("作品ID", value="demo_work", key="quick_share_id")
        selected_platforms = st.multiselect("选择平台", list(SHARE_PLATFORMS.keys()),
                                            default=["douyin", "xiaohongshu", "bilibili"],
                                            format_func=lambda x: f"{SHARE_PLATFORMS[x]['icon']} {SHARE_PLATFORMS[x]['name']}")

        if st.button("⚡ 一键分享", use_container_width=True):
            results = system.quick_share(work_id_q, selected_platforms)
            for plat, info in results.items():
                plat_name = SHARE_PLATFORMS.get(plat, {}).get("name", plat)
                st.success(f"{plat_name}: 分享链接已就绪")

    with tab3:
        st.subheader("分享历史")
        if system.share_history:
            for record in system.share_history[-10:]:
                with st.expander(f"📤 {record['timestamp'][:16]} - {', '.join(record['platforms'])}"):
                    for plat, info in record.get("results", {}).items():
                        st.write(f"- {plat}: {info.get('status', 'unknown')}")
        else:
            st.info("暂无分享记录")


# 兼容旧接口
SharePlatform = type('SharePlatform', (), {'DOUYIN': 'douyin', 'XIAOHONGSHU': 'xiaohongshu',
                                            'BILIBILI': 'bilibili', 'WECHAT': 'wechat'})
ShareConfig = type('ShareConfig', (), {})
WatermarkPosition = type('WatermarkPosition', (), {})
PlatformConfigManager = type('PlatformConfigManager', (), {})
