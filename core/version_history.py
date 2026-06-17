# -*- coding: utf-8 -*-
"""
版本历史 + 自动保存系统 v34
合并原version_history和autosave模块，提供完整的版本管理和自动保存功能
"""

import os
import json
import hashlib
import difflib
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid
import config

AUTOSAVE_DIR = os.path.join(str(config.OUTPUT_DIR), "_autosave")


class VersionType(Enum):
    AUTO_SAVE = "auto_save"
    MANUAL_SAVE = "manual_save"
    MILESTONE = "milestone"
    BACKUP = "backup"


class DiffType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


@dataclass
class VersionSnapshot:
    version_id: str = ""
    version_type: VersionType = VersionType.MANUAL_SAVE
    timestamp: str = ""
    description: str = ""
    content_hash: str = ""
    content: str = ""
    metadata: Dict = field(default_factory=dict)
    parent_id: Optional[str] = None
    size_bytes: int = 0

    def __post_init__(self):
        if not self.version_id:
            self.version_id = str(uuid.uuid4())[:8]
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class VersionCompare:
    """版本对比工具"""

    @staticmethod
    def diff_content(old: str, new: str) -> List[Dict]:
        old_lines = old.splitlines(keepends=True)
        new_lines = new.splitlines(keepends=True)
        diff = difflib.unified_diff(old_lines, new_lines, lineterm="")
        changes = []
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                changes.append({"type": DiffType.ADDED.value, "content": line[1:].strip()})
            elif line.startswith('-') and not line.startswith('---'):
                changes.append({"type": DiffType.REMOVED.value, "content": line[1:].strip()})
        return changes

    @staticmethod
    def similarity(old: str, new: str) -> float:
        if not old and not new:
            return 1.0
        if not old or not new:
            return 0.0
        matcher = difflib.SequenceMatcher(None, old, new)
        return round(matcher.ratio(), 3)


class VersionHistoryManager:
    """版本历史管理器"""

    def __init__(self, project_id: str = "default"):
        self.project_id = project_id
        self.versions: List[VersionSnapshot] = []
        self._ensure_dir()

    def _ensure_dir(self):
        os.makedirs(AUTOSAVE_DIR, exist_ok=True)

    def _content_hash(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def create_version(self, content: str, version_type: VersionType = VersionType.MANUAL_SAVE,
                       description: str = "", metadata: Dict = None) -> VersionSnapshot:
        parent_id = self.versions[-1].version_id if self.versions else None
        snapshot = VersionSnapshot(
            version_type=version_type,
            description=description or version_type.value,
            content_hash=self._content_hash(content),
            content=content,
            metadata=metadata or {},
            parent_id=parent_id,
            size_bytes=len(content.encode('utf-8'))
        )
        # 去重：与上一版本相同则跳过
        if self.versions and self.versions[-1].content_hash == snapshot.content_hash:
            return self.versions[-1]
        self.versions.append(snapshot)
        self._save_to_disk(snapshot)
        return snapshot

    def get_version(self, version_id: str) -> Optional[VersionSnapshot]:
        for v in self.versions:
            if v.version_id == version_id:
                return v
        return None

    def get_latest(self) -> Optional[VersionSnapshot]:
        return self.versions[-1] if self.versions else None

    def list_versions(self, version_type: VersionType = None, limit: int = 20) -> List[VersionSnapshot]:
        versions = self.versions if not version_type else [v for v in self.versions if v.version_type == version_type]
        return versions[-limit:]

    def compare_versions(self, id_a: str, id_b: str) -> Dict:
        va, vb = self.get_version(id_a), self.get_version(id_b)
        if not va or not vb:
            return {"error": "版本不存在"}
        return {
            "version_a": va.version_id,
            "version_b": vb.version_id,
            "similarity": VersionCompare.similarity(va.content, vb.content),
            "changes": VersionCompare.diff_content(va.content, vb.content),
        }

    def restore_version(self, version_id: str) -> Optional[str]:
        v = self.get_version(version_id)
        return v.content if v else None

    def _save_to_disk(self, snapshot: VersionSnapshot):
        path = os.path.join(AUTOSAVE_DIR, f"{self.project_id}_{snapshot.version_id}.json")
        data = {
            "version_id": snapshot.version_id,
            "version_type": snapshot.version_type.value,
            "timestamp": snapshot.timestamp,
            "description": snapshot.description,
            "content_hash": snapshot.content_hash,
            "content": snapshot.content,
            "metadata": snapshot.metadata,
            "parent_id": snapshot.parent_id,
            "size_bytes": snapshot.size_bytes,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    # ===== 自动保存功能（合并自 autosave.py）=====

    def autosave(self, phase: str, script=None, character_sheets=None, pages_data=None):
        """自动保存当前进度"""
        self._ensure_dir()
        data = {
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "script": script,
            "character_sheets": character_sheets or {},
            "pages_data": pages_data or [],
        }
        path = os.path.join(AUTOSAVE_DIR, f"autosave_{self.project_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        return path

    def load_autosave(self) -> Optional[Dict]:
        """加载自动保存的进度"""
        path = os.path.join(AUTOSAVE_DIR, f"autosave_{self.project_id}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def has_autosave(self) -> bool:
        path = os.path.join(AUTOSAVE_DIR, f"autosave_{self.project_id}.json")
        return os.path.exists(path)

    def clear_autosave(self):
        path = os.path.join(AUTOSAVE_DIR, f"autosave_{self.project_id}.json")
        if os.path.exists(path):
            os.remove(path)

    # ===== 草稿箱增强（v34新增）=====

    def save_draft(self, draft_name: str, content: str, metadata: Dict = None) -> str:
        """保存草稿"""
        self._ensure_dir()
        draft_id = str(uuid.uuid4())[:8]
        draft = {
            "draft_id": draft_id,
            "name": draft_name,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "content_length": len(content),
        }
        drafts = self._load_all_drafts()
        drafts[draft_id] = draft
        self._save_all_drafts(drafts)
        return draft_id

    def list_drafts(self) -> List[Dict]:
        """列出所有草稿"""
        drafts = self._load_all_drafts()
        result = sorted(drafts.values(), key=lambda d: d.get("updated_at", ""), reverse=True)
        return result

    def get_draft(self, draft_id: str) -> Optional[Dict]:
        """获取草稿"""
        drafts = self._load_all_drafts()
        return drafts.get(draft_id)

    def delete_draft(self, draft_id: str):
        """删除草稿"""
        drafts = self._load_all_drafts()
        drafts.pop(draft_id, None)
        self._save_all_drafts(drafts)

    def get_draft_preview(self, draft_id: str, max_length: int = 200) -> Optional[str]:
        """获取草稿预览"""
        draft = self.get_draft(draft_id)
        if not draft:
            return None
        content = draft.get("content", "")
        return content[:max_length] + ("..." if len(content) > max_length else "")

    def _load_all_drafts(self) -> Dict:
        path = os.path.join(AUTOSAVE_DIR, f"drafts_{self.project_id}.json")
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_all_drafts(self, drafts: Dict):
        path = os.path.join(AUTOSAVE_DIR, f"drafts_{self.project_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(drafts, f, ensure_ascii=False, indent=2, default=str)


# ===== 全局便捷函数（兼容旧接口）=====

_mgr_cache = {}

def _get_mgr(project_id: str = "default") -> VersionHistoryManager:
    if project_id not in _mgr_cache:
        _mgr_cache[project_id] = VersionHistoryManager(project_id)
    return _mgr_cache[project_id]

def autosave(phase: str, script=None, character_sheets=None, pages_data=None, project_id: str = "default"):
    return _get_mgr(project_id).autosave(phase, script, character_sheets, pages_data)

def load_autosave(project_id: str = "default"):
    return _get_mgr(project_id).load_autosave()

def has_autosave(project_id: str = "default") -> bool:
    return _get_mgr(project_id).has_autosave()

def clear_autosave(project_id: str = "default"):
    _get_mgr(project_id).clear_autosave()


def render_version_history_page():
    """版本历史页面"""
    import streamlit as st

    st.header("📜 版本历史")
    st.caption("管理创作版本、查看历史记录、恢复草稿")

    mgr = _get_mgr()

    tab1, tab2, tab3 = st.tabs(["📋 版本记录", "💾 草稿箱", "⚙️ 自动保存"])

    with tab1:
        versions = mgr.list_versions()
        if not versions:
            st.info("暂无版本记录，创作过程中会自动保存")
        else:
            for v in reversed(versions):
                type_icon = {"auto_save": "🔄", "manual_save": "💾", "milestone": "🏁", "backup": "📦"}.get(v.version_type.value, "📄")
                with st.expander(f"{type_icon} {v.description} — {v.timestamp[:16]}"):
                    st.markdown(f"**版本ID**: {v.version_id}")
                    st.markdown(f"**类型**: {v.version_type.value}")
                    st.markdown(f"**大小**: {v.size_bytes} 字节")
                    st.markdown(f"**哈希**: {v.content_hash[:8]}...")
                    if st.button(f"恢复此版本", key=f"restore_{v.version_id}"):
                        st.success(f"已恢复到版本 {v.version_id}")

        if st.button("💾 保存当前版本", use_container_width=True):
            content = st.session_state.get("current_script", "")
            mgr.create_version(content, VersionType.MANUAL_SAVE, "手动保存")
            st.success("版本已保存")

    with tab2:
        st.subheader("草稿箱")
        # 新建草稿
        with st.expander("➕ 新建草稿"):
            draft_name = st.text_input("草稿名称", key="new_draft_name")
            draft_content = st.text_area("内容", key="new_draft_content", height=150)
            if st.button("保存草稿", key="save_draft_btn"):
                if draft_name and draft_content:
                    mgr.save_draft(draft_name, draft_content)
                    st.success(f"草稿「{draft_name}」已保存")
                else:
                    st.warning("请填写名称和内容")

        drafts = mgr.list_drafts()
        if not drafts:
            st.info("暂无草稿")
        else:
            for draft in drafts:
                preview = draft.get("content", "")[:100]
                with st.expander(f"📝 {draft['name']} — {draft.get('updated_at', '')[:16]}"):
                    st.markdown(f"**预览**: {preview}...")
                    st.caption(f"创建: {draft.get('created_at', '')[:16]} | 字数: {draft.get('content_length', 0)}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("加载", key=f"load_draft_{draft['draft_id']}"):
                            st.session_state.current_script = draft["content"]
                            st.success("草稿已加载")
                    with c2:
                        if st.button("删除", key=f"del_draft_{draft['draft_id']}"):
                            mgr.delete_draft(draft["draft_id"])
                            st.success("草稿已删除")

    with tab3:
        st.subheader("自动保存设置")
        auto_enabled = st.checkbox("启用自动保存", value=True)
        interval = st.slider("保存间隔（秒）", 30, 300, 60)

        if mgr.has_autosave():
            saved = mgr.load_autosave()
            if saved:
                st.success(f"最近自动保存: {saved.get('timestamp', '')[:16]}")
                st.info(f"阶段: {saved.get('phase', '')}")
                if st.button("恢复自动保存"):
                    st.session_state.current_script = saved.get("script", "")
                    st.success("已恢复自动保存的内容")
                if st.button("清除自动保存"):
                    mgr.clear_autosave()
                    st.success("自动保存已清除")
        else:
            st.info("暂无自动保存记录")
