# -*- coding: utf-8 -*-
"""
v36: 深色模式系统
支持亮色/暗色主题切换，保护眼睛
"""
import streamlit as st
from typing import Optional


# 深色模式CSS
DARK_THEME_CSS = """
<style>
/* 深色模式全局样式 */
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    color: #e0e0e0;
}
[data-testid="stSidebar"] {
    background-color: #161b22;
    color: #e0e0e0;
}
[data-testid="stHeader"] {
    background-color: #0e1117;
}
[data-testid="stMarkdownContainer"] {
    color: #e0e0e0;
}
.stButton>button {
    background-color: #21262d;
    color: #e0e0e0;
    border-color: #30363d;
}
.stButton>button:hover {
    background-color: #30363d;
    border-color: #58a6ff;
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #0d1117;
    color: #e0e0e0;
    border-color: #30363d;
}
.stSelectbox>div>div>select {
    background-color: #0d1117;
    color: #e0e0e0;
}
.stSlider>div>div>div>div {
    background-color: #58a6ff;
}
.stTabs>div>div>div {
    background-color: #161b22;
    color: #e0e0e0;
}
.stExpander>div>div {
    background-color: #161b22;
    color: #e0e0e0;
}
.stMetric>div>div>div {
    color: #e0e0e0;
}
.stCaption {
    color: #8b949e !important;
}
.stInfo {
    background-color: #1a2332;
    border-color: #58a6ff;
    color: #e0e0e0;
}
.stSuccess {
    background-color: #1a2e1a;
    border-color: #3fb950;
    color: #e0e0e0;
}
.stWarning {
    background-color: #2e2a1a;
    border-color: #d29922;
    color: #e0e0e0;
}
.stError {
    background-color: #2e1a1a;
    border-color: #f85149;
    color: #e0e0e0;
}
/* 深色模式卡片 */
.dark-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 16px;
    color: #e0e0e0;
}
</style>
"""

# 亮色模式额外CSS
LIGHT_THEME_CSS = """
<style>
.light-card {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 16px;
}
</style>
"""


class ThemeManager:
    """主题管理器"""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"

    def __init__(self):
        self.current = st.session_state.get("v36_theme", self.AUTO)

    def set_theme(self, theme):
        self.current = theme
        st.session_state["v36_theme"] = theme

    def is_dark(self):
        if self.current == self.AUTO:
            # 简单策略：默认亮色
            return st.session_state.get("v36_force_dark", False)
        return self.current == self.DARK

    def toggle(self):
        new_theme = self.DARK if self.current != self.DARK else self.LIGHT
        self.set_theme(new_theme)

    def apply_theme(self):
        """应用主题CSS"""
        if self.is_dark():
            st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
        else:
            st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)

    def get_theme_icon(self):
        return "🌙" if self.is_dark() else "☀️"

    def get_theme_name(self):
        return "深色模式" if self.is_dark() else "浅色模式"

    def render_toggle_button(self):
        """渲染主题切换按钮"""
        icon = self.get_theme_icon()
        if st.button(f"{icon} {self.get_theme_name()}", use_container_width=True, key="theme_toggle"):
            self.toggle()
            st.rerun()

    def render_settings(self):
        """渲染主题设置"""
        st.write("### 🎨 主题设置")
        theme = st.radio(
            "选择主题",
            [self.LIGHT, self.DARK, self.AUTO],
            format_func=lambda x: {"light": "☀️ 浅色模式", "dark": "🌙 深色模式", "auto": "🔄 自动跟随"}.get(x, x),
            index=[self.LIGHT, self.DARK, self.AUTO].index(self.current),
            key="theme_radio"
        )
        if theme != self.current:
            self.set_theme(theme)
            st.rerun()


def render_theme_settings_page():
    """渲染主题设置页面"""
    st.subheader("🎨 主题设置")
    st.caption("选择适合你的主题，保护眼睛")

    manager = ThemeManager()
    manager.apply_theme()
    manager.render_settings()

    st.divider()
    # 预览卡片
    is_dark = manager.is_dark()
    card_class = "dark-card" if is_dark else "light-card"
    st.markdown(f"""
    <div class="{card_class}">
        <h3>主题预览</h3>
        <p>当前为{'深色' if is_dark else '浅色'}模式</p>
        <p>深色模式可以减少屏幕蓝光，在夜间使用时更加舒适。</p>
    </div>
    """, unsafe_allow_html=True)
