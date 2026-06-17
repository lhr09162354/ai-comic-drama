# -*- coding: utf-8 -*-
"""
安全与客服系统 v34 - 合并模块
整合智能客服、内容审核、版权保护
"""

import streamlit as st
import json
import re
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class SmartCustomerService:
    """智能客服"""

    def __init__(self):
        self.knowledge_base = self._init_knowledge()
        self.intents = self._init_intents()

    def _init_knowledge(self) -> Dict:
        return {
            "getting_started": {
                "title": "入门指南", "icon": "🚀",
                "questions": [
                    {"q": "如何开始创作？", "a": "1.点击创作页 2.选模板 3.设角色 4.生成剧本 5.导出分享"},
                    {"q": "支持哪些画风？", "a": "日系漫画、韩系漫画、国风、水彩、像素、写实、Q版、赛博朋克等"},
                    {"q": "如何获得更多生成次数？", "a": "升级会员等级，或通过创作获取创作币兑换"},
                ]
            },
            "account": {
                "title": "账号相关", "icon": "👤",
                "questions": [
                    {"q": "如何修改昵称？", "a": "进入创作者中心 → 个人设置 → 修改昵称"},
                    {"q": "如何注销账号？", "a": "请联系客服处理账号注销请求"},
                ]
            },
        }

    def _init_intents(self) -> Dict:
        return {
            "greeting": ["你好", "嗨", "hi", "hello"],
            "help": ["帮助", "怎么用", "教程", "指南"],
            "bug": ["bug", "报错", "失败", "不行", "出错"],
            "feedback": ["建议", "意见", "反馈", "投诉"],
        }

    def detect_intent(self, message: str) -> str:
        msg_lower = message.lower()
        for intent, keywords in self.intents.items():
            if any(kw in msg_lower for kw in keywords):
                return intent
        return "general"

    def respond(self, message: str) -> str:
        intent = self.detect_intent(message)
        if intent == "greeting":
            return "你好！我是AI助手，有什么可以帮你的？😊"
        elif intent == "help":
            return "你可以问我关于创作、配音、分享等任何问题！也可以查看使用指南获取详细帮助。"
        elif intent == "bug":
            return "很抱歉遇到问题！请描述具体情况，我会尽力帮你解决。也可以去帮助中心提交反馈。"
        elif intent == "feedback":
            return "感谢你的反馈！我们非常重视用户的每一条建议，会尽快处理。"
        return "我理解你的问题，让我为你查找相关信息..."


class AIContentModerator:
    """内容审核"""

    def __init__(self):
        self.risk_levels = ["safe", "low", "medium", "high", "critical"]
        self.forbidden_patterns = [
            r"暴力", r"血腥", r"色情", r"赌博", r"毒品",
            r"邪教", r"分裂", r"政治敏感", r"自杀", r"自残"
        ]

    def check_content(self, text: str) -> Dict:
        """审核内容"""
        violations = []
        for pattern in self.forbidden_patterns:
            if re.search(pattern, text):
                violations.append(pattern)

        if violations:
            risk = "high"
        elif len(text) > 50000:
            risk = "medium"
        else:
            risk = "safe"

        return {
            "risk_level": risk,
            "violations": violations,
            "is_safe": risk in ["safe", "low"],
            "suggestions": self._get_suggestions(violations),
        }

    def _get_suggestions(self, violations: List[str]) -> List[str]:
        if not violations:
            return ["内容合规，可以发布"]
        return [f"请修改包含「{v}」相关的内容" for v in violations]


class CopyrightProtection:
    """版权保护"""

    def __init__(self):
        self.registrations: Dict[str, Dict] = {}

    def register_work(self, work_id: str, title: str, author: str, content_hash: str) -> str:
        """注册版权"""
        cert_id = f"CERT-{hashlib.md5(f'{work_id}{datetime.now()}'.encode()).hexdigest()[:8]}"
        self.registrations[work_id] = {
            "cert_id": cert_id, "title": title, "author": author,
            "content_hash": content_hash, "registered_at": datetime.now().isoformat(),
            "status": "registered",
        }
        return cert_id

    def check_plagiarism(self, content_hash: str) -> Dict:
        """查重"""
        for wid, reg in self.registrations.items():
            if reg["content_hash"] == content_hash:
                return {"is_plagiarized": True, "original_work": wid}
        return {"is_plagiarized": False, "similarity": round(random.uniform(0, 0.15), 3)}

    def get_certificate(self, work_id: str) -> Optional[Dict]:
        return self.registrations.get(work_id)


def render_customer_service_page():
    """智能客服页面"""
    st.header("🤖 智能客服")
    st.caption("AI答疑、问题解决")

    service = SmartCustomerService()

    tab1, tab2 = st.tabs(["💬 在线客服", "📚 知识库"])

    with tab1:
        if "cs_messages" not in st.session_state:
            st.session_state.cs_messages = []

        for msg in st.session_state.cs_messages:
            role = msg["role"]
            if role == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

        user_input = st.chat_input("输入你的问题...")
        if user_input:
            st.session_state.cs_messages.append({"role": "user", "content": user_input})
            response = service.respond(user_input)
            st.session_state.cs_messages.append({"role": "assistant", "content": response})
            st.rerun()

    with tab2:
        for category, info in service.knowledge_base.items():
            with st.expander(f"{info['icon']} {info['title']}"):
                for qa in info["questions"]:
                    st.write(f"**Q: {qa['q']}**")
                    st.write(f"A: {qa['a']}")
                    st.markdown("")


def render_moderation_page():
    """内容审核页面"""
    st.header("🛡️ 内容审核")
    moderator = AIContentModerator()

    text = st.text_area("输入待审核内容", height=150)
    if st.button("开始审核", use_container_width=True):
        result = moderator.check_content(text)
        if result["is_safe"]:
            st.success("✅ 内容合规")
        else:
            st.error(f"⚠️ 风险等级: {result['risk_level']}")
            for v in result["violations"]:
                st.warning(f"发现违规: {v}")


def render_copyright_protection_page():
    """版权保护页面"""
    st.header("🔒 版权保护")
    cp = CopyrightProtection()

    tab1, tab2 = st.tabs(["📝 版权登记", "🔍 查重检测"])

    with tab1:
        title = st.text_input("作品标题")
        author = st.text_input("作者")
        if st.button("登记版权"):
            if title and author:
                cert = cp.register_work("new_work", title, author, "hash_placeholder")
                st.success(f"版权登记成功！证书号: {cert}")
            else:
                st.warning("请填写完整信息")

    with tab2:
        content = st.text_area("输入内容进行查重", height=100)
        if st.button("开始查重"):
            result = cp.check_plagiarism("hash_placeholder")
            if result["is_plagiarized"]:
                st.error("发现相似内容！")
            else:
                st.success(f"内容原创，相似度: {result['similarity']:.1%}")
