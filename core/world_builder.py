"""
故事世界观构建系统 v23
角色关系图谱、故事时间线、势力分布、背景设定
"""

import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum

class RelationType(Enum):
    """关系类型"""
    FAMILY = "家族"
    FRIEND = "朋友"
    ENEMY = "敌人"
    LOVE = "恋人"
    MENTOR = "导师"
    RIVAL = "对手"
    PARTNER = "伙伴"
    STRANGER = "陌生人"
    SIBLING = "兄妹"
    PARENT = "父母"
    MASTER = "师徒"
    LOVER = "情人"
    SPOUSE = "配偶"

class FactionType(Enum):
    """势力类型"""
    KINGDOM = "王国"
    GUILD = "公会"
    SECT = "门派"
    TRIAD = "黑帮"
    CORPORATION = "企业"
    ORGANIZATION = "组织"
    FAMILY = "家族"
    CLAN = "氏族"
    RELIGION = "宗教"
    TRIBE = "部落"

@dataclass
class Character:
    """角色"""
    id: str
    name: str
    title: str = ""  # 称号
    description: str = ""
    personality: str = ""
    appearance: str = ""
    background: str = ""
    abilities: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)  # 角色ID -> 关系类型
    faction_id: Optional[str] = None
    position: str = ""  # 职位/身份
    status: str = "alive"  # alive, dead, missing, unknown
    avatar_color: str = "#4A90D9"

@dataclass
class Faction:
    """势力"""
    id: str
    name: str
    faction_type: FactionType
    description: str = ""
    leader_id: Optional[str] = None
    members: List[str] = field(default_factory=list)  # 角色ID列表
    headquarters: str = ""  # 总部
    territory: str = ""  # 领地/势力范围
    strength: int = 50  # 实力等级 1-100
    alignment: str = "neutral"  # good, evil, neutral
    resources: Dict[str, int] = field(default_factory=dict)  # 资源

@dataclass
class TimelineEvent:
    """时间线事件"""
    id: str
    title: str
    description: str
    timestamp: str  # 故事内时间
    year: int  # 故事内年份
    month: int = 1
    day: int = 1
    involved_characters: List[str] = field(default_factory=list)  # 角色ID
    involved_factions: List[str] = field(default_factory=list)  # 势力ID
    importance: str = "normal"  # minor, normal, major, critical
    event_type: str = "story"  # story, battle, political, personal, world

@dataclass
class Location:
    """地点"""
    id: str
    name: str
    description: str = ""
    location_type: str = "city"  # city, village, dungeon, wilderness, building
    parent_id: Optional[str] = None  # 上级地点
    controlled_by: Optional[str] = None  # 势力ID
    characters: List[str] = field(default_factory=list)  # 常驻角色
    significance: str = "normal"  # normal, important, key, legendary

class WorldSetting:
    """世界观设定"""
    
    def __init__(self):
        self.title = ""
        self.genre = ""
        self.setting_time = ""  # 故事背景时代
        self.setting_place = ""  # 故事背景地点
        self.description = ""
        self.theme = ""  # 主题
        self.tone = ""  # 基调
        self.rules: List[str] = []  # 世界规则
        self.lore: List[str] = []  # 世界观知识

class WorldBuilder:
    """世界观构建器"""
    
    def __init__(self):
        self.world = WorldSetting()
        self.characters: Dict[str, Character] = {}
        self.factions: Dict[str, Faction] = {}
        self.locations: Dict[str, Location] = {}
        self.timeline: List[TimelineEvent] = []
        self.relationship_matrix: Dict[Tuple[str, str], str] = {}  # (角色1, 角色2) -> 关系描述
    
    def add_character(self, name: str, **kwargs) -> Character:
        """添加角色"""
        char_id = f"char_{len(self.characters) + 1}"
        char = Character(id=char_id, name=name, **kwargs)
        self.characters[char_id] = char
        return char
    
    def add_faction(self, name: str, faction_type: FactionType, **kwargs) -> Faction:
        """添加势力"""
        faction_id = f"faction_{len(self.factions) + 1}"
        faction = Faction(id=faction_id, name=name, faction_type=faction_type, **kwargs)
        self.factions[faction_id] = faction
        return faction
    
    def add_location(self, name: str, **kwargs) -> Location:
        """添加地点"""
        loc_id = f"loc_{len(self.locations) + 1}"
        loc = Location(id=loc_id, name=name, **kwargs)
        self.locations[loc_id] = loc
        return loc
    
    def add_timeline_event(self, title: str, year: int, **kwargs) -> TimelineEvent:
        """添加时间线事件"""
        event_id = f"event_{len(self.timeline) + 1}"
        event = TimelineEvent(id=event_id, title=title, year=year, **kwargs)
        self.timeline.append(event)
        self.timeline.sort(key=lambda x: (x.year, x.month, x.day))
        return event
    
    def set_relationship(self, char1_id: str, char2_id: str, relation_type: RelationType, description: str = ""):
        """设置角色关系"""
        self.characters[char1_id].relationships[char2_id] = relation_type.value
        self.characters[char2_id].relationships[char1_id] = relation_type.value
        if description:
            self.relationship_matrix[(char1_id, char2_id)] = description
    
    def get_relationship(self, char1_id: str, char2_id: str) -> Optional[str]:
        """获取角色关系"""
        if char1_id in self.characters and char2_id in self.characters[char1_id].relationships:
            return self.characters[char1_id].relationships[char2_id]
        return None
    
    def get_characters_by_faction(self, faction_id: str) -> List[Character]:
        """获取某势力的所有角色"""
        return [c for c in self.characters.values() if c.faction_id == faction_id]
    
    def get_characters_by_relationship(self, char_id: str, relation_type: str) -> List[Character]:
        """获取具有特定关系的角色"""
        char = self.characters.get(char_id)
        if not char:
            return []
        return [self.characters[c_id] for c_id, rel in char.relationships.items() 
                if rel == relation_type and c_id in self.characters]
    
    def generate_family_tree(self, root_char_id: str) -> Dict:
        """生成家族树"""
        def build_tree(char_id: str, visited: Set[str]) -> Dict:
            if char_id in visited:
                return {"id": char_id, "name": self.characters[char_id].name, "loop": True}
            visited.add(char_id)
            
            char = self.characters.get(char_id)
            if not char:
                return {}
            
            node = {
                "id": char.id,
                "name": char.name,
                "title": char.title,
                "children": []
            }
            
            # 查找子女关系
            for other_id, relation in char.relationships.items():
                if relation in ["子女", "child"] and other_id not in visited:
                    node["children"].append(build_tree(other_id, visited.copy()))
            
            return node
        
        return build_tree(root_char_id, set())
    
    def generate_conflict_map(self) -> List[Dict]:
        """生成势力冲突图"""
        conflicts = []
        faction_list = list(self.factions.values())
        
        for i, f1 in enumerate(faction_list):
            for f2 in faction_list[i+1:]:
                # 根据alignment判断敌对关系
                if (f1.alignment == "good" and f2.alignment == "evil") or \
                   (f1.alignment == "evil" and f2.alignment == "good"):
                    conflicts.append({
                        "faction1": f1.name,
                        "faction2": f2.name,
                        "type": "敌对",
                        "strength": random.randint(50, 100)
                    })
                elif f1.alignment == f2.alignment == "neutral":
                    conflicts.append({
                        "faction1": f1.name,
                        "faction2": f2.name,
                        "type": "竞争",
                        "strength": random.randint(20, 60)
                    })
        
        return conflicts

    def export_to_dict(self) -> Dict:
        """导出为字典"""
        return {
            "world": {
                "title": self.world.title,
                "genre": self.world.genre,
                "setting_time": self.world.setting_time,
                "setting_place": self.world.setting_place,
                "description": self.world.description,
                "theme": self.world.theme,
                "tone": self.world.tone,
                "rules": self.world.rules,
                "lore": self.world.lore,
            },
            "characters": {k: {
                "id": v.id,
                "name": v.name,
                "title": v.title,
                "description": v.description,
                "personality": v.personality,
                "appearance": v.appearance,
                "background": v.background,
                "abilities": v.abilities,
                "relationships": v.relationships,
                "faction_id": v.faction_id,
                "status": v.status,
                "avatar_color": v.avatar_color,
            } for k, v in self.characters.items()},
            "factions": {k: {
                "id": v.id,
                "name": v.name,
                "type": v.faction_type.value,
                "description": v.description,
                "leader_id": v.leader_id,
                "strength": v.strength,
                "alignment": v.alignment,
            } for k, v in self.factions.items()},
            "locations": {k: {
                "id": v.id,
                "name": v.name,
                "description": v.description,
                "type": v.location_type,
            } for k, v in self.locations.items()},
            "timeline_count": len(self.timeline),
        }

class WorldBuilderUI:
    """世界观构建器UI"""
    
    def __init__(self, world_builder: WorldBuilder):
        self.builder = world_builder
    
    def render_world_setting(self):
        """渲染世界观设置"""
        st.subheader("🌍 世界观设定")
        
        with st.expander("基础设定", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                self.builder.world.title = st.text_input("故事标题", value=self.builder.world.title)
                self.builder.world.genre = st.selectbox(
                    "类型",
                    ["奇幻", "科幻", "都市", "校园", "历史", "武侠", "悬疑", "恋爱", "冒险", "其他"],
                    index=0 if not self.builder.world.genre else ["奇幻", "科幻", "都市", "校园", "历史", "武侠", "悬疑", "恋爱", "冒险", "其他"].index(self.builder.world.genre) if self.builder.world.genre in ["奇幻", "科幻", "都市", "校园", "历史", "武侠", "悬疑", "恋爱", "冒险", "其他"] else 0
                )
                self.builder.world.setting_time = st.text_input("时代背景", value=self.builder.world.setting_time)
            
            with col2:
                self.builder.world.setting_place = st.text_input("地点背景", value=self.builder.world.setting_place)
                self.builder.world.theme = st.text_input("主题", value=self.builder.world.theme)
                self.builder.world.tone = st.selectbox(
                    "基调",
                    ["热血", "治愈", "黑暗", "轻松", "感人", "悬疑", "浪漫", "史诗"],
                    index=0
                )
            
            self.builder.world.description = st.text_area("世界观描述", value=self.builder.world.description, height=100)
        
        with st.expander("世界规则与知识", expanded=False):
            rule = st.text_input("添加世界规则")
            if st.button("添加规则") and rule:
                self.builder.world.rules.append(rule)
                st.success("规则已添加")
            
            for i, rule in enumerate(self.builder.world.rules):
                st.write(f"📜 {rule}")
                if st.button("删除", key=f"del_rule_{i}"):
                    self.builder.world.rules.pop(i)
                    st.rerun()
    
    def render_character_manager(self):
        """渲染角色管理器"""
        st.subheader("👥 角色管理")
        
        tab1, tab2, tab3 = st.tabs(["角色列表", "添加角色", "关系管理"])
        
        with tab1:
            if not self.builder.characters:
                st.info("暂无角色，请先添加")
            else:
                for char in self.builder.characters.values():
                    with st.expander(f"{char.name} ({char.title or '无称号'})"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**身份:** {char.position or '未设定'}")
                            st.write(f"**状态:** {char.status}")
                            st.write(f"**性格:** {char.personality or '未设定'}")
                            st.write(f"**简介:** {char.description[:50] if char.description else '无'}...")
                            
                            if char.relationships:
                                st.write("**关系:**")
                                for target_id, relation in char.relationships.items():
                                    target = self.builder.characters.get(target_id)
                                    if target:
                                        st.write(f"  - {target.name}: {relation}")
                        
                        with col2:
                            if st.button("删除", key=f"del_char_{char.id}"):
                                del self.builder.characters[char.id]
                                st.rerun()
        
        with tab2:
            st.write("**添加新角色**")
            name = st.text_input("角色名")
            title = st.text_input("称号")
            position = st.text_input("身份/职位")
            personality = st.text_input("性格特点")
            description = st.text_area("角色描述")
            
            col1, col2 = st.columns(2)
            with col1:
                status = st.selectbox("状态", ["alive", "dead", "missing", "unknown"])
                color = st.color_picker("标识颜色", "#4A90D9")
            
            with col2:
                faction_options = ["无"] + [f"{f.id}: {f.name}" for f in self.builder.factions.values()]
                faction_choice = st.selectbox("所属势力", faction_options)
                faction_id = faction_choice.split(":")[0] if faction_choice != "无" else None
            
            if st.button("添加角色", type="primary"):
                char = self.builder.add_character(
                    name=name,
                    title=title,
                    position=position,
                    personality=personality,
                    description=description,
                    status=status,
                    avatar_color=color,
                    faction_id=faction_id if faction_id != "无" else None
                )
                if faction_id and faction_id != "无":
                    self.builder.factions.get(faction_id.split(":")[0], Faction("","",FactionType.ORGANIZATION)).members.append(char.id)
                st.success(f"角色 {name} 已添加!")
                st.rerun()
        
        with tab3:
            st.write("**设置角色关系**")
            if len(self.builder.characters) < 2:
                st.warning("需要至少2个角色才能设置关系")
            else:
                char_options = [(cid, char.name) for cid, char in self.builder.characters.items()]
                char1_id = st.selectbox("角色1", [c[0] for c in char_options], format_func=lambda x: dict(char_options)[x])
                char2_id = st.selectbox("角色2", [c[0] for c in char_options], format_func=lambda x: dict(char_options)[x])
                
                relation = st.selectbox("关系类型", [r.value for r in RelationType])
                
                if st.button("确认关系"):
                    self.builder.set_relationship(char1_id, char2_id, RelationType(relation))
                    st.success("关系已设置!")
                    st.rerun()
    
    def render_faction_manager(self):
        """渲染势力管理器"""
        st.subheader("⚔️ 势力管理")
        
        tab1, tab2 = st.tabs(["势力列表", "添加势力"])
        
        with tab1:
            if not self.builder.factions:
                st.info("暂无势力，请先添加")
            else:
                for faction in self.builder.factions.values():
                    with st.expander(f"{faction.name} ({faction.faction_type.value})"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**类型:** {faction.faction_type.value}")
                            st.write(f"**实力:** {faction.strength}/100")
                            st.write(f"**立场:** {faction.alignment}")
                            st.write(f"**描述:** {faction.description[:50] if faction.description else '无'}...")
                            
                            # 成员
                            members = self.builder.get_characters_by_faction(faction.id)
                            if members:
                                st.write(f"**成员 ({len(members)}):**")
                                for m in members:
                                    st.write(f"  - {m.name}")
                        
                        with col2:
                            if st.button("删除", key=f"del_faction_{faction.id}"):
                                del self.builder.factions[faction.id]
                                st.rerun()
        
        with tab2:
            st.write("**添加新势力**")
            name = st.text_input("势力名称")
            faction_type = st.selectbox("势力类型", [f.value for f in FactionType])
            alignment = st.selectbox("立场", ["good", "evil", "neutral"])
            strength = st.slider("实力等级", 1, 100, 50)
            description = st.text_area("势力描述")
            
            if st.button("添加势力", type="primary"):
                faction = self.builder.add_faction(
                    name=name,
                    faction_type=FactionType(faction_type),
                    alignment=alignment,
                    strength=strength,
                    description=description
                )
                st.success(f"势力 {name} 已添加!")
                st.rerun()
    
    def render_timeline(self):
        """渲染时间线"""
        st.subheader("📅 故事时间线")
        
        # 添加事件
        with st.expander("添加事件", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("事件标题")
                year = st.number_input("年份", 1, 9999, 1)
                month = st.number_input("月份", 1, 12, 1)
                day = st.number_input("日期", 1, 31, 1)
            
            with col2:
                importance = st.selectbox("重要程度", ["minor", "normal", "major", "critical"])
                event_type = st.selectbox("事件类型", ["story", "battle", "political", "personal", "world"])
            
            description = st.text_area("事件描述")
            
            # 涉及角色
            if self.builder.characters:
                char_names = st.multiselect("涉及角色", list(self.builder.characters.keys()), 
                                           format_func=lambda x: self.builder.characters[x].name)
            else:
                char_names = []
            
            if st.button("添加事件", type="primary"):
                self.builder.add_timeline_event(
                    title=title,
                    year=year,
                    month=month,
                    day=day,
                    description=description,
                    importance=importance,
                    event_type=event_type,
                    involved_characters=char_names
                )
                st.success("事件已添加!")
                st.rerun()
        
        # 显示时间线
        st.divider()
        st.write("**事件列表**")
        
        if not self.builder.timeline:
            st.info("暂无事件")
        else:
            # 按年份分组显示
            years = sorted(set(e.year for e in self.builder.timeline))
            
            for year in years:
                year_events = [e for e in self.builder.timeline if e.year == year]
                with st.expander(f"📆 {year}年 ({len(year_events)}个事件)"):
                    for event in year_events:
                        importance_icon = {"minor": "📌", "normal": "📍", "major": "🔶", "critical": "🔥"}.get(event.importance, "📍")
                        type_icon = {"story": "📖", "battle": "⚔️", "political": "🏛️", "personal": "💬", "world": "🌍"}.get(event.event_type, "📖")
                        
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"**{importance_icon}{type_icon} {event.title}**")
                            st.caption(f"{event.month}月{event.day}日 | {event.importance}")
                            if event.description:
                                st.write(event.description[:80] + "..." if len(event.description) > 80 else event.description)
                            
                            # 涉及角色
                            if event.involved_characters:
                                names = [self.builder.characters.get(cid, Character(cid, "未知")).name 
                                        for cid in event.involved_characters if cid in self.builder.characters]
                                if names:
                                    st.write(f"**涉及:** {', '.join(names)}")
                        with col2:
                            if st.button("删除", key=f"del_event_{event.id}"):
                                self.builder.timeline.remove(event)
                                st.rerun()
    
    def render_relationship_map(self):
        """渲染关系图谱"""
        st.subheader("🔗 角色关系图谱")
        
        if len(self.builder.characters) < 2:
            st.info("至少需要2个角色才能生成关系图谱")
            return
        
        # 关系统计
        relation_counts = {}
        for char in self.builder.characters.values():
            for rel in char.relationships.values():
                relation_counts[rel] = relation_counts.get(rel, 0) + 1
        
        if relation_counts:
            st.write("**关系分布:**")
            cols = st.columns(len(relation_counts))
            for idx, (rel, count) in enumerate(relation_counts.items()):
                with cols[idx % len(relation_counts)]:
                    st.metric(rel, count)
        
        # 关系矩阵
        st.divider()
        st.write("**关系矩阵:**")
        
        char_list = list(self.builder.characters.values())
        
        # 表头
        header = " | " + " | ".join([c.name[:5] for c in char_list]) + " |"
        separator = "|---" * (len(char_list) + 1) + "|"
        
        table = [header, separator]
        
        for char1 in char_list:
            row = f"| **{char1.name[:5]}**"
            for char2 in char_list:
                if char1.id == char2.id:
                    row += " | - "
                else:
                    rel = self.builder.get_relationship(char1.id, char2.id)
                    if rel:
                        rel_emoji = {"家族": "👨‍👩‍👧", "朋友": "🤝", "敌人": "⚔️", "恋人": "💕", 
                                   "导师": "👨‍🏫", "对手": "🏋️", "伙伴": "🧑‍🤝‍🧑"}.get(rel, "•")
                        row += f" | {rel_emoji}{rel}"
                    else:
                        row += " | · "
            row += " |"
            table.append(row)
        
        for line in table:
            st.markdown(line)
        
        # 冲突图
        st.divider()
        st.write("**势力冲突图:**")
        
        conflicts = self.builder.generate_conflict_map()
        if conflicts:
            for conflict in conflicts[:5]:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"{conflict['faction1']} ⚔️ {conflict['faction2']}")
                with col2:
                    st.write(f"类型: {conflict['type']}")
                with col3:
                    st.write(f"强度: {conflict['strength']}")
        else:
            st.info("暂无冲突关系")
    
    def render_location_manager(self):
        """渲染地点管理器"""
        st.subheader("📍 地点管理")
        
        tab1, tab2 = st.tabs(["地点列表", "添加地点"])
        
        with tab1:
            if not self.builder.locations:
                st.info("暂无地点")
            else:
                for loc in self.builder.locations.values():
                    with st.expander(f"📍 {loc.name}"):
                        st.write(f"**类型:** {loc.location_type}")
                        st.write(f"**重要性:** {loc.significance}")
                        st.write(f"**描述:** {loc.description or '无'}")
        
        with tab2:
            name = st.text_input("地点名称")
            loc_type = st.selectbox("类型", ["city", "village", "dungeon", "wilderness", "building"])
            significance = st.selectbox("重要性", ["normal", "important", "key", "legendary"])
            description = st.text_area("描述")
            
            if st.button("添加地点"):
                self.builder.add_location(name=name, location_type=loc_type, 
                                        significance=significance, description=description)
                st.success(f"地点 {name} 已添加!")
                st.rerun()
    
    def render_full_ui(self):
        """渲染完整UI"""
        st.subheader("🌍 世界观构建器 v23")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🌍 世界设定", "👥 角色", "⚔️ 势力", "🔗 关系图", "📅 时间线", "📍 地点"
        ])
        
        with tab1:
            self.render_world_setting()
        
        with tab2:
            self.render_character_manager()
        
        with tab3:
            self.render_faction_manager()
        
        with tab4:
            self.render_relationship_map()
        
        with tab5:
            self.render_timeline()
        
        with tab6:
            self.render_location_manager()
        
        st.divider()
        
        # 导出
        if st.button("📤 导出世界观数据"):
            data = self.builder.export_to_dict()
            st.json(data)
            st.success("世界观数据已导出")

# 全局实例
world_builder = WorldBuilder()

def get_world_builder() -> WorldBuilder:
    """获取世界观构建器"""
    return world_builder
