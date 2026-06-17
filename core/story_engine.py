"""
AI Comic Drama Generator v17 - AI故事引擎
智能剧情生成 + 分支故事 + 结构优化
"""

import streamlit as st
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random

@dataclass
class StoryBeat:
    """故事节拍"""
    id: str
    type: str           # setup, inciting, rising, climax, falling, resolution
    title: str
    description: str
    emotional_arc: str   # 情感弧线
    duration: int        # 预计格数
    dependencies: List[str] = field(default_factory=list)

@dataclass
class StoryBranch:
    """故事分支"""
    id: str
    parent_id: str
    name: str
    description: str
    divergence_point: str
    convergence_point: Optional[str] = None
    choices: List[Dict] = field(default_factory=list)
    beats: List[StoryBeat] = field(default_factory=list)

class StoryEngine:
    """AI故事引擎"""
    
    def __init__(self):
        self.story_arcs = {}
        self.beats = []
        self.branches = []
        self.characters = {}
    
    def generate_story(
        self,
        theme: str,
        characters: List[Dict],
        structure: str = "three_act",
        target_length: int = 50
    ) -> Dict:
        """
        生成完整故事
        
        Args:
            theme: 故事主题
            characters: 角色列表
            structure: 结构类型 (three_act/hero_journey/save_the_cat)
            target_length: 目标格数
        
        Returns:
            完整故事数据
        """
        story = {
            "theme": theme,
            "structure": structure,
            "acts": [],
            "beats": [],
            "branches": [],
            "characters": characters,
        }
        
        # 生成三幕结构
        if structure == "three_act":
            story["acts"] = self._generate_three_act(theme, characters, target_length)
        elif structure == "hero_journey":
            story["acts"] = self._generate_hero_journey(theme, characters, target_length)
        elif structure == "save_the_cat":
            story["acts"] = self._generate_save_the_cat(theme, characters, target_length)
        
        return story
    
    def _generate_three_act(self, theme: str, characters: List, target: int) -> List[Dict]:
        """生成三幕式结构"""
        act1_beats = max(5, target // 5)
        act2_beats = max(15, target // 2)
        act3_beats = target - act1_beats - act2_beats
        
        acts = [
            {
                "name": "第一幕：建置",
                "description": "介绍世界观和角色，建立故事基础",
                "beats": self._generate_act_beats("setup", act1_beats, theme)
            },
            {
                "name": "第二幕：对抗",
                "description": "主角面对挑战和冲突，情节升级",
                "beats": self._generate_act_beats("rising", act2_beats, theme)
            },
            {
                "name": "第三幕：解决",
                "description": "高潮和结局，问题得到解决",
                "beats": self._generate_act_beats("climax", act3_beats, theme)
            }
        ]
        
        return acts
    
    def _generate_hero_journey(self, theme: str, characters: List, target: int) -> List[Dict]:
        """生成英雄之旅结构"""
        stages = [
            ("平凡世界", "setup", target // 12),
            ("冒险召唤", "inciting", target // 12),
            ("拒绝召唤", "turning", target // 12),
            ("遇见导师", "rising", target // 12),
            ("跨越门槛", "rising", target // 10),
            ("考验盟友敌人", "rising", target // 8),
            ("接近洞穴", "rising", target // 8),
            ("最大考验", "climax", target // 6),
            ("奖励", "falling", target // 10),
            ("返回的路", "falling", target // 10),
            ("复活", "resolution", target // 8),
            ("满载而归", "resolution", target // 8),
        ]
        
        acts = []
        for name, beat_type, beats_count in stages:
            acts.append({
                "name": name,
                "description": self._get_stage_description(name),
                "beats": self._generate_act_beats(beat_type, beats_count, theme)
            })
        
        return acts
    
    def _generate_save_the_cat(self, theme: str, characters: List, target: int) -> List[Dict]:
        """生成救猫咪节拍表"""
        beats = [
            "开场画面",
            "主题陈述",
            "设定",
            "催化剂",
            "争论",
            "第二幕衔接",
            "B故事",
            "游戏",
            "中点",
            "坏人逼近",
            "一切皆失",
            "第三幕衔接",
            "最终画面",
        ]
        
        return [
            {
                "name": beat,
                "description": f"第{i+1}个节拍",
                "beats": self._generate_act_beats("beat", target // len(beats), theme)
            }
            for i, beat in enumerate(beats)
        ]
    
    def _generate_act_beats(self, beat_type: str, count: int, theme: str) -> List[Dict]:
        """生成节拍"""
        beats = []
        for i in range(count):
            beat = {
                "id": f"{beat_type}_{i}",
                "type": beat_type,
                "description": self._get_beat_description(beat_type, theme),
                "emotion": self._get_emotion_for_beat(beat_type),
                "scene_type": self._get_scene_type(beat_type),
            }
            beats.append(beat)
        return beats
    
    def _get_beat_description(self, beat_type: str, theme: str) -> str:
        """获取节拍描述"""
        descriptions = {
            "setup": [
                "介绍主角的日常生活",
                "展示主角的性格特点",
                "暗示主角的内心渴望",
                "建立故事的世界观",
                "引入配角角色",
            ],
            "rising": [
                "主角遭遇新的挑战",
                "关系出现新的发展",
                "意外事件打断计划",
                "角色获得新信息",
                "矛盾逐渐升级",
            ],
            "climax": [
                "主角面临最终抉择",
                "所有矛盾集中爆发",
                "真相终于大白",
                "角色关系发生巨变",
                "目标即将达成或失败",
            ],
            "falling": [
                "后果开始显现",
                "角色反思和成长",
                "新的平衡建立",
                "结局铺垫",
            ],
            "resolution": [
                "问题得到圆满解决",
                "角色获得内心平静",
                "展示新的日常生活",
                "留下温暖的结局画面",
            ],
        }
        
        options = descriptions.get(beat_type, descriptions["rising"])
        return random.choice(options)
    
    def _get_emotion_for_beat(self, beat_type: str) -> str:
        """获取情感类型"""
        emotions = {
            "setup": ["平静", "好奇", "期待"],
            "rising": ["紧张", "兴奋", "不安"],
            "climax": ["激动", "震惊", "紧张"],
            "falling": ["释然", "感慨", "温馨"],
            "resolution": ["满足", "温暖", "平静"],
        }
        return random.choice(emotions.get(beat_type, ["平静"]))
    
    def _get_scene_type(self, beat_type: str) -> str:
        """获取场景类型"""
        scenes = {
            "setup": ["日常", "对话", "介绍"],
            "rising": ["冲突", "追逐", "调查", "训练"],
            "climax": ["战斗", "告白", "抉择", "真相"],
            "falling": ["和好", "告别", "庆祝"],
            "resolution": ["温馨", "希望", "结束"],
        }
        return random.choice(scenes.get(beat_type, ["对话"]))
    
    def _get_stage_description(self, stage: str) -> str:
        """获取英雄之旅阶段描述"""
        descriptions = {
            "平凡世界": "在普通的世界里，主角过着平凡的生活，但内心有着不为人知的渴望",
            "冒险召唤": "一个契机出现，邀请主角踏上一段非凡的旅程",
            "拒绝召唤": "主角犹豫不决，外部或内部阻力让主角踌躇",
            "遇见导师": "一位智者或导师出现，给予主角启发和帮助",
            "跨越门槛": "主角正式踏出舒适区，进入冒险世界",
            "考验盟友敌人": "主角面对考验，遇到盟友，也遭遇敌人",
            "接近洞穴": "接近最终目标前的准备和深入",
            "最大考验": "最艰难的挑战，考验主角的成长",
            "奖励": "克服挑战后获得的奖励",
            "返回的路": "带着收获踏上归途",
            "复活": "最后的考验，主角的彻底蜕变",
            "满载而归": "带着智慧和成长回归",
        }
        return descriptions.get(stage, "")
    
    def add_branch_point(
        self,
        parent_beat_id: str,
        branch_name: str,
        choices: List[str]
    ) -> StoryBranch:
        """添加分支点"""
        branch = StoryBranch(
            id=f"branch_{len(self.branches)}",
            parent_id=parent_beat_id,
            name=branch_name,
            description=f"从{parent_beat_id}产生的分支",
            divergence_point=parent_beat_id,
            choices=[{"text": c, "selected": False} for c in choices]
        )
        self.branches.append(branch)
        return branch
    
    def select_branch_choice(self, branch_id: str, choice_index: int):
        """选择分支"""
        for branch in self.branches:
            if branch.id == branch_id:
                for i, choice in enumerate(branch.choices):
                    choice["selected"] = (i == choice_index)
                break
    
    def get_current_path(self) -> List[str]:
        """获取当前故事路径"""
        path = []
        for branch in self.branches:
            for choice in branch.choices:
                if choice.get("selected"):
                    path.append(f"{branch.name}: {choice['text']}")
        return path

class BranchManager:
    """分支故事管理器"""
    
    def __init__(self):
        self.stories = {}
        self.current_story_id = None
    
    def create_story(
        self,
        theme: str,
        characters: List[Dict],
        structure: str = "three_act"
    ) -> str:
        """创建分支故事"""
        story_id = f"story_{datetime.now().timestamp()}"
        
        engine = StoryEngine()
        story_data = engine.generate_story(theme, characters, structure)
        
        self.stories[story_id] = {
            "id": story_id,
            "theme": theme,
            "data": story_data,
            "branches": [],
            "selected_path": [],
            "created_at": datetime.now().isoformat(),
        }
        
        self.current_story_id = story_id
        return story_id
    
    def add_branch(
        self,
        story_id: str,
        point_id: str,
        options: List[Dict]
    ) -> str:
        """添加分支"""
        branch_id = f"branch_{len(self.stories[story_id]['branches'])}"
        
        self.stories[story_id]["branches"].append({
            "id": branch_id,
            "point": point_id,
            "options": options,
            "selected": None,
        })
        
        return branch_id
    
    def select_path(self, story_id: str, branch_id: str, option_index: int):
        """选择路径"""
        story = self.stories.get(story_id)
        if story:
            for branch in story["branches"]:
                if branch["id"] == branch_id:
                    branch["selected"] = option_index
                    story["selected_path"].append({
                        "branch": branch_id,
                        "choice": option_index
                    })
                    break
    
    def get_story_tree(self, story_id: str) -> Dict:
        """获取故事树"""
        story = self.stories.get(story_id, {})
        return {
            "theme": story.get("theme"),
            "branches": story.get("branches", []),
            "path": story.get("selected_path", []),
        }

class CharacterRelationshipGraph:
    """角色关系图"""
    
    def __init__(self):
        self.characters = {}
        self.relationships = []
    
    def add_character(self, char_id: str, name: str, role: str):
        """添加角色"""
        self.characters[char_id] = {
            "id": char_id,
            "name": name,
            "role": role,
            "traits": [],
        }
    
    def add_relationship(
        self,
        char1_id: str,
        char2_id: str,
        relation_type: str,
        strength: int = 5
    ):
        """添加关系"""
        self.relationships.append({
            "from": char1_id,
            "to": char2_id,
            "type": relation_type,
            "strength": strength,  # 1-10
            "events": [],
        })
    
    def update_relationship(
        self,
        char1_id: str,
        char2_id: str,
        event: str,
        delta: int
    ):
        """更新关系"""
        for rel in self.relationships:
            if (rel["from"] == char1_id and rel["to"] == char2_id) or \
               (rel["from"] == char2_id and rel["to"] == char1_id):
                rel["events"].append({"event": event, "delta": delta})
                rel["strength"] = max(1, min(10, rel["strength"] + delta))
                break
    
    def get_relationship(self, char1_id: str, char2_id: str) -> Optional[Dict]:
        """获取关系"""
        for rel in self.relationships:
            if (rel["from"] == char1_id and rel["to"] == char2_id) or \
               (rel["from"] == char2_id and rel["to"] == char1_id):
                return rel
        return None

def render_story_engine_ui():
    """渲染故事引擎UI"""
    st.subheader("📖 AI故事引擎")
    
    # 故事结构选择
    structure_options = {
        "three_act": "📚 三幕式结构",
        "hero_journey": "⚔️ 英雄之旅",
        "save_the_cat": "🐱 救猫咪节拍表",
    }
    
    selected_structure = st.selectbox(
        "选择故事结构",
        options=list(structure_options.keys()),
        format_func=lambda x: structure_options[x]
    )
    
    st.info(f"""
    **结构说明：**
    - 三幕式：经典叙事结构（建置→对抗→解决）
    - 英雄之旅：12阶段神话结构
    - 救猫咪：15个专业节拍
    """)
    
    # 目标长度
    target_panels = st.slider("目标格数", 20, 100, 50)
    
    # 生成按钮
    if st.button("🎬 生成故事大纲", type="primary"):
        engine = StoryEngine()
        
        characters = st.session_state.get("characters", [
            {"name": "小明", "desc": "勇敢的少年"},
            {"name": "小红", "desc": "聪明的少女"},
        ])
        
        with st.spinner("AI构思中..."):
            story = engine.generate_story(
                theme="热血冒险",
                characters=characters,
                structure=selected_structure,
                target_length=target_panels
            )
        
        st.success("故事大纲生成完成！")
        
        # 显示三幕结构
        st.divider()
        st.subheader("📊 故事结构")
        
        for i, act in enumerate(story.get("acts", []), 1):
            with st.expander(f"**第{i}幕: {act['name']}**", expanded=i==1):
                st.write(act.get("description", ""))
                
                beats = act.get("beats", [])
                if beats:
                    st.write(f"**共 {len(beats)} 个节拍**")
                    for beat in beats[:5]:
                        st.write(f"- {beat.get('description', '')}")
                    if len(beats) > 5:
                        st.info(f"还有 {len(beats) - 5} 个节拍...")

def render_branch_ui():
    """渲染分支故事UI"""
    st.subheader("🌳 分支故事")
    
    st.info("""
    **分支故事模式：**
    在关键节点创建分支，让观众选择故事走向
    """)
    
    # 创建分支
    if st.button("➕ 创建分支点", use_container_width=True):
        st.info("选择剧本中的一个场景，添加分支选项")
        
        # 示例分支点
        with st.expander("示例：主角遇到神秘人"):
            st.write("**场景：** 主角在森林中遇到一个神秘人")
            
            options = ["接受神秘人的任务", "拒绝并离开", "询问更多信息"]
            
            for i, opt in enumerate(options):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i+1}. {opt}")
                with col2:
                    if st.button("选择", key=f"opt_{i}"):
                        st.success(f"已选择：{opt}")

# 导入配置
try:
    from config import STORY_TEMPLATES, ART_STYLES
except:
    STORY_TEMPLATES = {}
    ART_STYLES = {}
