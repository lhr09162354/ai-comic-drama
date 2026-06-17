"""
AI Comic Drama Generator v17 - 实时协作模块
多人实时编辑 + 批注评论 + 协作房间
"""

import streamlit as st
import json
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Collaborator:
    """协作者"""
    id: str
    name: str
    avatar: str
    role: str = "editor"      # owner, editor, viewer
    status: str = "online"    # online, away, offline
    cursor_position: Optional[int] = None
    last_active: datetime = None

@dataclass
class Annotation:
    """批注"""
    id: str
    type: str                 # comment, suggestion, todo, question
    content: str
    author: str
    created_at: datetime
    position: Dict            # 面板位置
    resolved: bool = False
    replies: List[Dict] = field(default_factory=list)

@dataclass
class Room:
    """协作房间"""
    id: str
    name: str
    project_id: str
    owner: str
    created_at: datetime
    collaborators: List[Collaborator] = field(default_factory=list)
    annotations: List[Annotation] = field(default_factory=list)
    invite_code: str = None
    is_active: bool = True

class CollaborationManager:
    """协作管理器"""
    
    def __init__(self):
        self.rooms = {}
        self.current_room = None
        self.current_user = None
    
    def create_room(
        self,
        name: str,
        project_id: str,
        owner_name: str
    ) -> Room:
        """创建协作房间"""
        room_id = str(uuid.uuid4())[:8]
        invite_code = self._generate_invite_code()
        
        owner = Collaborator(
            id=str(uuid.uuid4()),
            name=owner_name,
            avatar="👤",
            role="owner",
            status="online",
            last_active=datetime.now()
        )
        
        room = Room(
            id=room_id,
            name=name,
            project_id=project_id,
            owner=owner.id,
            collaborators=[owner],
            invite_code=invite_code,
            created_at=datetime.now()
        )
        
        self.rooms[room_id] = room
        self.current_room = room_id
        
        return room
    
    def _generate_invite_code(self, length: int = 6) -> str:
        """生成邀请码"""
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def join_room(
        self,
        invite_code: str,
        user_name: str,
        role: str = "editor"
    ) -> Optional[Room]:
        """加入协作房间"""
        for room in self.rooms.values():
            if room.invite_code == invite_code and room.is_active:
                collaborator = Collaborator(
                    id=str(uuid.uuid4()),
                    name=user_name,
                    avatar="👤",
                    role=role,
                    status="online",
                    last_active=datetime.now()
                )
                room.collaborators.append(collaborator)
                self.current_room = room.id
                self.current_user = collaborator.id
                return room
        
        return None
    
    def leave_room(self):
        """离开房间"""
        if self.current_room:
            room = self.rooms.get(self.current_room)
            if room and self.current_user:
                for collab in room.collaborators:
                    if collab.id == self.current_user:
                        collab.status = "offline"
                        break
            self.current_room = None
            self.current_user = None
    
    def get_active_users(self, room_id: str) -> List[Collaborator]:
        """获取在线用户"""
        room = self.rooms.get(room_id)
        if room:
            return [c for c in room.collaborators if c.status == "online"]
        return []
    
    def update_cursor_position(self, position: int):
        """更新光标位置"""
        if self.current_room and self.current_user:
            room = self.rooms.get(self.current_room)
            if room:
                for collab in room.collaborators:
                    if collab.id == self.current_user:
                        collab.cursor_position = position
                        collab.last_active = datetime.now()
                        break

class AnnotationManager:
    """批注管理器"""
    
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.annotations = []
    
    def add_annotation(
        self,
        annotation_type: str,
        content: str,
        author: str,
        position: Dict
    ) -> Annotation:
        """添加批注"""
        annotation = Annotation(
            id=str(uuid.uuid4()),
            type=annotation_type,
            content=content,
            author=author,
            created_at=datetime.now(),
            position=position
        )
        
        self.annotations.append(annotation)
        return annotation
    
    def add_reply(
        self,
        annotation_id: str,
        content: str,
        author: str
    ) -> bool:
        """添加回复"""
        for ann in self.annotations:
            if ann.id == annotation_id:
                ann.replies.append({
                    "id": str(uuid.uuid4()),
                    "content": content,
                    "author": author,
                    "created_at": datetime.now().isoformat()
                })
                return True
        return False
    
    def resolve_annotation(self, annotation_id: str) -> bool:
        """标记为已解决"""
        for ann in self.annotations:
            if ann.id == annotation_id:
                ann.resolved = True
                return True
        return False
    
    def get_unresolved(self) -> List[Annotation]:
        """获取未解决的批注"""
        return [a for a in self.annotations if not a.resolved]

class RealTimeSync:
    """实时同步"""
    
    def __init__(self):
        self.pending_changes = []
        self.last_sync = None
    
    def add_change(
        self,
        change_type: str,
        target: str,
        data: Dict
    ):
        """添加变更"""
        self.pending_changes.append({
            "type": change_type,
            "target": target,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_changes(self) -> List[Dict]:
        """获取变更列表"""
        return self.pending_changes.copy()
    
    def clear_changes(self):
        """清除已处理的变更"""
        self.pending_changes = []

class PresenceIndicator:
    """在线状态指示"""
    
    @staticmethod
    def get_status_color(status: str) -> str:
        """获取状态颜色"""
        colors = {
            "online": "🟢",
            "away": "🟡",
            "offline": "⚫"
        }
        return colors.get(status, "⚫")
    
    @staticmethod
    def render_user_list(
        collaborators: List[Collaborator],
        show_avatar: bool = True
    ) -> str:
        """渲染用户列表"""
        items = []
        for collab in collaborators:
            status_icon = PresenceIndicator.get_status_color(collab.status)
            if show_avatar:
                items.append(f"{status_icon} {collab.avatar} {collab.name}")
            else:
                items.append(f"{status_icon} {collab.name}")
        
        return "\n".join(items)

class ConflictResolver:
    """冲突解决"""
    
    RESOLUTION_STRATEGIES = {
        "last_write": "last_write",
        "first_write": "first_write",
        "manual": "manual",
        "merge": "merge"
    }
    
    def __init__(self, strategy: str = "last_write"):
        self.strategy = strategy
    
    def resolve(self, changes: List[Dict]) -> Dict:
        """解决冲突"""
        if not changes:
            return {}
        
        if self.strategy == "last_write":
            # 使用最后一次写入
            return changes[-1]["data"]
        elif self.strategy == "first_write":
            return changes[0]["data"]
        elif self.strategy == "merge":
            return self._merge_changes(changes)
        
        return changes[-1]["data"]
    
    def _merge_changes(self, changes: List[Dict]) -> Dict:
        """合并变更"""
        merged = {}
        for change in changes:
            merged.update(change.get("data", {}))
        return merged

def render_collaboration_ui():
    """渲染协作UI"""
    st.subheader("👥 实时协作")
    
    # 协作房间
    tab1, tab2, tab3 = st.tabs(["🏠 房间", "💬 批注", "👤 用户"])
    
    with tab1:
        st.write("**协作房间管理**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ 创建房间", use_container_width=True):
                st.info("创建新的协作房间，邀请他人加入")
                
                with st.form("create_room"):
                    room_name = st.text_input("房间名称")
                    owner_name = st.text_input("你的名字", value="创作者")
                    
                    if st.form_submit_button("创建"):
                        manager = CollaborationManager()
                        room = manager.create_room(room_name, "project_1", owner_name)
                        st.success(f"房间创建成功！邀请码: **{room.invite_code}**")
        
        with col2:
            invite_code = st.text_input("输入邀请码")
            
            if st.button("🚪 加入房间", use_container_width=True):
                manager = CollaborationManager()
                room = manager.join_room(invite_code, "访客")
                
                if room:
                    st.success(f"成功加入房间: {room.name}")
                else:
                    st.error("邀请码无效或房间已关闭")
    
    with tab2:
        st.write("**批注与评论**")
        
        # 批注类型
        annotation_types = {
            "comment": "💬 评论",
            "suggestion": "💡 建议",
            "todo": "✅ 待办",
            "question": "❓ 问题",
        }
        
        selected_type = st.selectbox(
            "批注类型",
            options=list(annotation_types.keys()),
            format_func=lambda x: annotation_types[x]
        )
        
        content = st.text_area("批注内容")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            panel_select = st.selectbox("关联面板", range(1, 21), index=0)
        with col2:
            st.write("")  # 占位
            if st.button("📝 添加批注"):
                if content:
                    st.success("批注已添加")
                else:
                    st.warning("请输入批注内容")
        
        # 显示批注列表
        st.divider()
        st.write("**批注列表**")
        
        with st.expander("💬 评论 #1", expanded=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write("这个场景的氛围很好，建议加强光影效果")
            with col2:
                st.write("小明\n10:30")
            st.button("✅ 标记已解决", key="resolve_1")
            st.button("💬 回复", key="reply_1")
    
    with tab3:
        st.write("**在线用户**")
        
        # 示例在线用户
        users = [
            {"name": "小明", "avatar": "👨", "status": "online", "role": "owner"},
            {"name": "小红", "avatar": "👩", "status": "online", "role": "editor"},
            {"name": "阿杰", "avatar": "🧑", "status": "away", "role": "viewer"},
        ]
        
        for user in users:
            status_icon = "🟢" if user["status"] == "online" else "🟡"
            st.write(f"{status_icon} {user['avatar']} **{user['name']}** ({user['role']})")
        
        # 权限管理
        st.divider()
        st.write("**权限设置**")
        
        role_options = {
            "owner": "👑 所有者",
            "editor": "✏️ 编辑者",
            "viewer": "👁️ 观看者",
        }
        
        for user in users[1:]:  # 不包括自己
            st.selectbox(
                f"{user['name']} 的权限",
                options=list(role_options.keys()),
                format_func=lambda x: role_options[x],
                key=f"role_{user['name']}"
            )

def render_presence_indicator(collaborators: List[Dict]):
    """渲染在线状态指示器"""
    online_count = sum(1 for c in collaborators if c.get("status") == "online")
    
    st.write(f"**在线用户 ({online_count})**")
    
    cols = st.columns(min(5, online_count))
    for i, collab in enumerate([c for c in collaborators if c.get("status") == "online"][:5]):
        with cols[i]:
            st.avatar(collab.get("avatar", "👤"), size="sm")
