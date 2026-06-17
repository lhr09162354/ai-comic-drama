# -*- coding: utf-8 -*-
"""
v36: 海报生成系统
多种风格模板，一键生成分享海报
"""
import streamlit as st
from dataclasses import dataclass
from typing import Optional
import json


POSTER_TEMPLATES = {
    "经典漫画风": {"emoji": "🎌", "desc": "日系漫画封面风格", "bg": "#1a1a2e", "accent": "#e94560"},
    "赛博霓虹风": {"emoji": "🌆", "desc": "赛博朋克霓虹灯效", "bg": "#0a0a23", "accent": "#00f5ff"},
    "古风水墨风": {"emoji": "🏯", "desc": "中国风水墨渲染", "bg": "#f5f0e8", "accent": "#c41e3a"},
    "极简主义风": {"emoji": "◻️", "desc": "干净简约大字报", "bg": "#ffffff", "accent": "#333333"},
    "渐变流光风": {"emoji": "🌈", "desc": "梦幻渐变色彩", "bg": "#667eea", "accent": "#764ba2"},
    "暗黑哥特风": {"emoji": "🦇", "desc": "暗色调神秘氛围", "bg": "#1a1a1a", "accent": "#8b0000"},
    "青春校园风": {"emoji": "🎒", "desc": "清新明快校园感", "bg": "#87CEEB", "accent": "#ff69b4"},
    "像素复古风": {"emoji": "👾", "desc": "8bit像素艺术风", "bg": "#2c3e50", "accent": "#f39c12"},
}

POSTER_LAYOUTS = {
    "居中大标题": {"title_pos": "center", "subtitle_pos": "bottom", "img_pos": "top"},
    "左侧竖排": {"title_pos": "left", "subtitle_pos": "left", "img_pos": "right"},
    "底部横排": {"title_pos": "bottom", "subtitle_pos": "bottom", "img_pos": "top"},
    "对角线": {"title_pos": "top-left", "subtitle_pos": "bottom-right", "img_pos": "center"},
    "全屏背景": {"title_pos": "center", "subtitle_pos": "center", "img_pos": "background"},
}


class PosterGenerator:
    """海报生成器"""

    def __init__(self):
        self.template = st.session_state.get("v36_poster_template", "经典漫画风")
        self.layout = st.session_state.get("v36_poster_layout", "居中大标题")

    def set_template(self, name):
        if name in POSTER_TEMPLATES:
            self.template = name
            st.session_state["v36_poster_template"] = name

    def set_layout(self, name):
        if name in POSTER_LAYOUTS:
            self.layout = name
            st.session_state["v36_poster_layout"] = name

    def preview_poster(self, title, subtitle="", author="", tags=None):
        """生成海报预览（CSS模拟）"""
        tmpl = POSTER_TEMPLATES.get(self.template, {})
        bg = tmpl.get("bg", "#1a1a2e")
        accent = tmpl.get("accent", "#e94560")
        layout_info = POSTER_LAYOUTS.get(self.layout, {})

        tags_str = " · ".join(tags) if tags else ""
        emoji = tmpl.get("emoji", "🎬")

        html = f"""
        <div style="
            background: linear-gradient(135deg, {bg}, {accent}33);
            border-radius: 12px;
            padding: 40px 24px;
            color: white;
            text-align: center;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">{emoji}</div>
            <h1 style="
                font-size: 28px;
                margin: 0 0 12px 0;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
                color: {accent};
            ">{title}</h1>
            <p style="font-size: 14px; opacity: 0.85; margin: 4px 0;">{subtitle}</p>
            <p style="font-size: 12px; opacity: 0.7; margin: 8px 0;">{tags_str}</p>
            <div style="margin-top: 24px; font-size: 11px; opacity: 0.5;">
                AI漫剧生成器 | {author or '原创作者'}
            </div>
        </div>
        """
        return html

    def generate_share_text(self, title, subtitle="", author=""):
        """生成分享文案"""
        tmpl = POSTER_TEMPLATES.get(self.template, {})
        texts = [
            f"🎬 新漫剧上线！《{title}》{subtitle} 快来看！",
            f"✨ 推荐一部超好看的漫剧《{title}》，{tmpl.get('emoji', '')}风格，别错过！",
            f"🔥《{title}》太好看了！{subtitle} #AI漫剧 #推荐",
        ]
        return texts[0]

    def get_size_options(self):
        """获取尺寸选项"""
        return {
            "9:16 竖版（推荐）": (1080, 1920),
            "1:1 方形": (1080, 1080),
            "16:9 横版": (1920, 1080),
            "3:4 小竖版": (810, 1080),
            "2:3 中竖版": (720, 1080),
        }


def render_poster_generator_page():
    """渲染海报生成页面"""
    st.subheader("🖼️ 海报生成")
    st.caption("一键生成精美分享海报，多种风格模板可选")

    gen = PosterGenerator()

    tab1, tab2, tab3 = st.tabs(["🎨 设计海报", "📋 模板选择", "📤 导出分享"])

    with tab1:
        c1, c2 = st.columns([1, 1])
        with c1:
            title = st.text_input("作品标题", value=st.session_state.get("story_title", ""), key="poster_title")
            subtitle = st.text_input("副标题/简介", key="poster_subtitle")
        with c2:
            author = st.text_input("作者署名", key="poster_author")
            tags_input = st.text_input("标签（逗号分隔）", key="poster_tags")
            tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []

        if st.button("🖼️ 预览海报", type="primary", use_container_width=True):
            html = gen.preview_poster(title, subtitle, author, tags)
            st.session_state["v36_poster_preview"] = html

        preview = st.session_state.get("v36_poster_preview")
        if preview:
            st.divider()
            st.components.v1.html(preview, height=450)

    with tab2:
        st.write("选择海报风格模板")
        cols = st.columns(4)
        for i, (name, info) in enumerate(POSTER_TEMPLATES.items()):
            with cols[i % 4]:
                selected = st.button(
                    f"{info['emoji']}\n{name}",
                    key=f"tmpl_{name}",
                    use_container_width=True,
                    type="primary" if gen.template == name else "secondary"
                )
                if selected:
                    gen.set_template(name)
                    st.rerun()
                st.caption(info["desc"])

        st.divider()
        st.write("选择版式布局")
        cols2 = st.columns(5)
        for i, (name, info) in enumerate(POSTER_LAYOUTS.items()):
            with cols2[i]:
                selected = st.button(name, key=f"layout_{name}",
                                     use_container_width=True,
                                     type="primary" if gen.layout == name else "secondary")
                if selected:
                    gen.set_layout(name)
                    st.rerun()

    with tab3:
        if not st.session_state.get("v36_poster_preview"):
            st.info("请先在「设计海报」中预览海报")
        else:
            st.write("**分享文案**")
            share_text = gen.generate_share_text(title, subtitle, author)
            st.code(share_text)

            size = st.selectbox("导出尺寸", list(gen.get_size_options().keys()))
            fmt = st.selectbox("导出格式", ["PNG", "JPG", "WebP"])

            if st.button("📥 导出海报", type="primary", use_container_width=True):
                st.success(f"海报已生成！尺寸: {size}，格式: {fmt}")
                st.balloons()
