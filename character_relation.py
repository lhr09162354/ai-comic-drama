# -*- coding: utf-8 -*-
"""
v36: 角色关系图谱
支持朋友/恋人/敌人/家人等关系网络，可视化展示角色关系
"""
import streamlit as st
from dataclasses import dataclass, field
from typing import Optional
import json


RELATION_TYPES = {
    "朋友": {"emoji": "🤝", "color": "#4CAF50", "desc": "互相信任的好友"},
    "恋人": {"emoji": "💕", "color": "#E91E63", "desc": "彼此相爱的伴侣"},
    "敌人": {"emoji": "⚔️", "color": "#F44336", "desc": "针锋相对的对手"},
    "家人": {"emoji": "🏠", "color": "#FF9800", "desc": "血脉相连的亲人"},
    "师徒": {"emoji": "📜", "color": "#9C27B0", "desc": "传授与学习的纽带"},
    "同事": {"emoji": "💼", "color": "#607D8B", "desc": "工作上的伙伴"},
    "暗恋": {"emoji": "💗", "color": "#E91E63", "desc": "默默关注的情感"},
    "宿敌": {"emoji": "🔥", "color": "#FF5722", "desc": "不死不休的对手"},
    "盟友": {"emoji": "🛡️", "color": "#2196F3", "desc": "利益一致的联盟"},
    "邻居": {"emoji": "🏡", "color": "#8BC34A", "desc": "比邻而居"},
    "同学": {"emoji": "📚", "color": "#00BCD4", "desc": "同窗之谊"},
    "上下级": {"emoji": "👔", "color": "#795548", "desc": "职场层级关系"},
}


@dataclass
class Relation:
    char_a: str
    char_b: str
    relation_type: str
    detail: str = ""
    intensity: int = 5  # 1-10 关系强度

    def to_dict(self):
        return {"char_a": self.char_a, "char_b": self.char_b,
                "relation_type": self.relation_type, "detail": self.detail,
                "intensity": self.intensity}

    @staticmethod
    def from_dict(d):
        return Relation(d["char_a"], d["char_b"], d["relation_type"],
                        d.get("detail", ""), d.get("intensity", 5))


class CharacterRelationGraph:
    """角色关系图谱管理器"""

    def __init__(self):
        self.relations = self._load()

    def _load(self):
        return st.session_state.get("v36_relations", [])

    def _save(self):
        st.session_state["v36_relations"] = self.relations

    def add_relation(self, char_a, char_b, rel_type, detail="", intensity=5):
        # 去重：同对角色同类型只保留一个
        for r in self.relations:
            if ((r["char_a"] == char_a and r["char_b"] == char_b) or
                (r["char_a"] == char_b and r["char_b"] == char_a)) and r["relation_type"] == rel_type:
                return False
        rel = Relation(char_a, char_b, rel_type, detail, intensity).to_dict()
        self.relations.append(rel)
        self._save()
        return True

    def remove_relation(self, idx):
        if 0 <= idx < len(self.relations):
            self.relations.pop(idx)
            self._save()

    def get_relations_for(self, char_name):
        result = []
        for r in self.relations:
            if r["char_a"] == char_name or r["char_b"] == char_name:
                other = r["char_b"] if r["char_a"] == char_name else r["char_a"]
                result.append({"other": other, **r})
        return result

    def get_all_characters(self):
        chars = set()
        for r in self.relations:
            chars.add(r["char_a"])
            chars.add(r["char_b"])
        # 合并 session_state 中的角色
        for c in st.session_state.get("characters", []):
            if isinstance(c, dict) and c.get("name"):
                chars.add(c["name"])
        return sorted(chars)

    def generate_mermaid(self):
        """生成 Mermaid 关系图"""
        if not self.relations:
            return ""
        lines = ["graph LR"]
        for r in self.relations:
            a = r["char_a"].replace(" ", "_")
            b = r["char_b"].replace(" ", "_")
            info = RELATION_TYPES.get(r["relation_type"], {})
            label = f'{info.get("emoji", "")}{r["relation_type"]}'
            style = f'style {a} fill:#E3F2FD\nstyle {b} fill:#E3F2FD'
            lines.append(f'    {a} --"{label}"--> {b}')
        return "\n".join(lines)

    def auto_suggest(self, characters):
        """基于角色特征自动建议关系"""
        suggestions = []
        if len(characters) < 2:
            return suggestions
        names = [c["name"] for c in characters if c.get("name")]
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                ci, cj = characters[i], characters[j]
                # 简单规则：性格互补建议朋友/恋人
                p1 = ci.get("personality", "")
                p2 = cj.get("personality", "")
                if "霸道" in p1 and "温柔" in p2:
                    suggestions.append((names[i], names[j], "恋人", "性格互补"))
                elif "冷酷" in p1 and "活泼" in p2:
                    suggestions.append((names[i], names[j], "朋友", "互补吸引"))
                elif p1 and p2 and p1 == p2:
                    suggestions.append((names[i], names[j], "朋友", "志趣相投"))
        return suggestions[:5]


def render_character_relation_page():
    """渲染角色关系图谱页面"""
    st.subheader("🕸️ 角色关系图谱")
    st.caption("构建角色之间的关系网络，让故事更有层次")

    graph = CharacterRelationGraph()
    characters = graph.get_all_characters()

    tab1, tab2, tab3 = st.tabs(["🕸️ 关系图谱", "➕ 添加关系", "💡 智能建议"])

    with tab1:
        if not graph.relations:
            st.info("暂无角色关系，请在「添加关系」中创建")
        else:
            # 关系列表
            for i, r in enumerate(graph.relations):
                info = RELATION_TYPES.get(r["relation_type"], {})
                emoji = info.get("emoji", "🔗")
                cols = st.columns([3, 2, 3, 1])
                with cols[0]:
                    st.write(f"**{r['char_a']}**")
                with cols[1]:
                    st.write(f"{emoji} {r['relation_type']}")
                with cols[2]:
                    st.write(f"**{r['char_b']}**")
                with cols[3]:
                    if st.button("🗑️", key=f"del_rel_{i}"):
                        graph.remove_relation(i)
                        st.rerun()

            # Mermaid 图谱
            st.divider()
            st.subheader("📊 关系网络图")
            mermaid_code = graph.generate_mermaid()
            if mermaid_code:
                st.markdown(f"```mermaid\n{mermaid_code}\n```")

            # 统计
            st.divider()
            rel_counts = {}
            for r in graph.relations:
                t = r["relation_type"]
                rel_counts[t] = rel_counts.get(t, 0) + 1
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("角色数", len(characters))
            with c2:
                st.metric("关系数", len(graph.relations))
            with c3:
                top = max(rel_counts, key=rel_counts.get) if rel_counts else "-"
                st.metric("最多关系类型", top)

    with tab2:
        if len(characters) < 2:
            st.warning("至少需要2个角色才能创建关系")
            if st.button("前往角色管理"):
                st.session_state.active_tab = "角色管理"
                st.rerun()
        else:
            c1, c2 = st.columns(2)
            with c1:
                char_a = st.selectbox("角色A", characters, key="rel_char_a")
            with c2:
                char_b = st.selectbox("角色B", [c for c in characters if c != char_a], key="rel_char_b")

            rel_type = st.selectbox("关系类型", list(RELATION_TYPES.keys()),
                                    format_func=lambda x: f"{RELATION_TYPES[x]['emoji']} {x} - {RELATION_TYPES[x]['desc']}")
            detail = st.text_input("关系描述（可选）", placeholder="例如：青梅竹马，一起长大")
            intensity = st.slider("关系强度", 1, 10, 5)

            if st.button("添加关系", type="primary", use_container_width=True):
                if char_a != char_b:
                    if graph.add_relation(char_a, char_b, rel_type, detail, intensity):
                        st.success(f"已添加关系：{char_a} ↔ {char_b} ({RELATION_TYPES[rel_type]['emoji']}{rel_type})")
                        st.rerun()
                    else:
                        st.warning("该关系已存在")
                else:
                    st.error("不能选择相同的角色")

    with tab3:
        st.subheader("💡 智能关系建议")
        chars = st.session_state.get("characters", [])
        if len(chars) < 2:
            st.info("至少需要2个角色才能生成建议")
        else:
            suggestions = graph.auto_suggest(chars)
            if not suggestions:
                st.info("暂无智能建议，可以为角色添加更多性格描述")
            else:
                for a, b, rel, reason in suggestions:
                    with st.container():
                        c1, c2 = st.columns([4, 1])
                        with c1:
                            info = RELATION_TYPES.get(rel, {})
                            st.write(f"**{a}** {info.get('emoji', '')} {rel} **{b}** — {reason}")
                        with c2:
                            if st.button("采纳", key=f"adopt_{a}_{b}_{rel}"):
                                graph.add_relation(a, b, rel, reason)
                                st.success("已采纳")
                                st.rerun()
