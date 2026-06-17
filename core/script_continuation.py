"""
智能剧本续写引擎
根据大纲自动扩展剧情，生成多种结局分支
"""
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class StoryArc(Enum):
    """故事弧线类型"""
    HERO_JOURNEY = "hero_journey"           # 英雄之旅
    FALL_AND_REDEMPTION = "fall_redemption"  # 堕落与救赎
    RAGS_TO_RICHES = "rags_to_riches"        # 麻雀变凤凰
    TRAGEDY = "tragedy"                      # 悲剧
    COMEDY = "comedy"                        # 喜剧
    REBIRTH = "rebirth"                      # 重生
    VENGEANCE = "vengeance"                  # 复仇
    MYSTERY = "mystery"                      # 悬疑

class EndingType(Enum):
    """结局类型"""
    HAPPY = "happy"                          # 圆满结局
    BITTERSWEET = "bittersweet"              # 苦乐参半
    TRAGIC = "tragic"                        # 悲剧结局
    OPEN = "open"                            # 开放式结局
    SURPRISE = "surprise"                    # 反转型结局
    CYCLICAL = "cyclical"                    # 首尾呼应型

@dataclass
class PlotNode:
    """剧情节点"""
    id: str
    title: str
    description: str
    characters: List[str] = field(default_factory=list)
    emotion: str = "neutral"
    tension_level: int = 5  # 1-10
    duration: str = "medium"  # short/medium/long
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)

@dataclass
class StoryBranch:
    """故事分支"""
    id: str
    name: str
    plot_points: List[PlotNode]
    ending_type: EndingType
    probability: float = 1.0  # 该分支被选中的概率
    unlock_conditions: List[str] = field(default_factory=list)

@dataclass
class ContinuationResult:
    """续写结果"""
    original_outline: str
    generated_plot: str
    branch_name: str
    ending_type: EndingType
    new_characters: List[Dict] = field(default_factory=list)
    foreshadowing_elements: List[str] = field(default_factory=list)
    character_development: Dict[str, str] = field(default_factory=dict)

class PlotOutlineParser:
    """剧情大纲解析器"""
    
    def __init__(self):
        self.patterns = {
            'chapter': r'第[一二三四五六七八九十百千\d]+[章节集部]|Chapter\s*\d+|Episode\s*\d+',
            'scene': r'场景\d+|Scene\s*\d+',
            'character': r'【([^】]+)】|\[([^\]]+)\]|角色[：:]\s*([^\n]+)',
            'emotion': r'情感[：:]\s*([^\n]+)|情绪[：:]\s*([^\n]+)',
            'tension': r'张力[：:]\s*(\d+)|冲突[：:]\s*([^\n]+)',
        }
    
    def parse(self, outline: str) -> List[PlotNode]:
        """解析大纲为剧情节点列表"""
        nodes = []
        lines = outline.strip().split('\n')
        
        current_node = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检测章节/场景标记
            if re.search(self.patterns['chapter'], line):
                if current_node:
                    nodes.append(current_node)
                node_id = f"node_{len(nodes)}"
                current_node = PlotNode(
                    id=node_id,
                    title=line,
                    description="",
                    tension_level=5
                )
            elif re.search(self.patterns['scene'], line):
                if current_node:
                    nodes.append(current_node)
                node_id = f"node_{len(nodes)}"
                current_node = PlotNode(
                    id=node_id,
                    title=line,
                    description="",
                    tension_level=5
                )
            else:
                # 解析角色
                char_match = re.search(self.patterns['character'], line)
                if char_match:
                    chars = [g for g in char_match.groups() if g]
                    if current_node and chars:
                        current_node.characters.extend(chars)
                
                # 解析情感
                emotion_match = re.search(self.patterns['emotion'], line)
                if emotion_match and current_node:
                    emotion = emotion_match.group(1)
                    current_node.emotion = emotion
                
                # 解析张力
                tension_match = re.search(self.patterns['tension'], line)
                if tension_match and current_node:
                    tension = tension_match.group(1)
                    if tension:
                        current_node.tension_level = min(10, max(1, int(tension)))
                
                # 添加到描述
                if current_node:
                    current_node.description += line + "\n"
        
        if current_node:
            nodes.append(current_node)
        
        return nodes if nodes else [PlotNode(
            id="node_0",
            title="开场",
            description=outline,
            tension_level=5
        )]

class StoryArcGenerator:
    """故事弧线生成器"""
    
    def __init__(self):
        self.arc_templates = {
            StoryArc.HERO_JOURNEY: {
                'phases': ['平凡世界', '冒险召唤', '跨越门槛', '考验与盟友', '最深处的洞穴', '严峻考验', '获得奖赏', '归来之路', '重生'],
                'tension_curve': [2, 3, 5, 6, 7, 8, 6, 4, 7],
                'typical_ending': EndingType.HAPPY
            },
            StoryArc.FALL_AND_REDEMPTION: {
                'phases': ['巅峰时刻', '堕落', '沉沦', '触底', '觉醒', '赎罪', '救赎'],
                'tension_curve': [7, 8, 6, 3, 4, 6, 8],
                'typical_ending': EndingType.BITTERSWEET
            },
            StoryArc.TRAGEDY: {
                'phases': ['美好时光', '隐藏缺陷', '缺陷暴露', '试图改正', '越陷越深', '无法挽回', '毁灭'],
                'tension_curve': [5, 6, 7, 6, 8, 9, 10],
                'typical_ending': EndingType.TRAGIC
            },
            StoryArc.COMEDY: {
                'phases': ['困境', '尝试解决', '弄巧成拙', '更大的困境', '意外转折', '圆满解决'],
                'tension_curve': [4, 5, 6, 7, 5, 3],
                'typical_ending': EndingType.HAPPY
            },
            StoryArc.VENGEANCE: {
                'phases': ['伤害', '悲痛', '计划', '行动', '接近目标', '冲突', '复仇完成'],
                'tension_curve': [3, 5, 6, 7, 8, 9, 7],
                'typical_ending': EndingType.BITTERSWEET
            },
            StoryArc.REBIRTH: {
                'phases': ['绝望', '死亡象征', '内心转变', '新生活'],
                'tension_curve': [8, 9, 5, 3],
                'typical_ending': EndingType.HAPPY
            },
            StoryArc.MYSTERY: {
                'phases': ['案件发生', '调查开始', '线索发现', '误导信息', '真相浮现', '最终揭示'],
                'tension_curve': [4, 5, 6, 7, 8, 9],
                'typical_ending': EndingType.SURPRISE
            },
        }
    
    def generate_arc(
        self, 
        arc_type: StoryArc,
        num_episodes: int = 5
    ) -> List[Dict]:
        """根据弧线类型生成结构化剧情"""
        template = self.arc_templates.get(arc_type)
        if not template:
            return []
        
        phases = template['phases']
        tension_curve = template['tension_curve']
        
        # 根据集数调整
        episodes = []
        phase_idx = 0
        tension_idx = 0
        
        for i in range(num_episodes):
            # 计算当前阶段和张力
            if phase_idx < len(phases):
                phase = phases[phase_idx]
            else:
                phase = phases[-1]
            
            if tension_idx < len(tension_curve):
                tension = tension_curve[tension_idx]
            else:
                tension = tension_curve[-1]
            
            episodes.append({
                'episode': i + 1,
                'phase': phase,
                'tension': tension,
                'title': f"第{i+1}集：{phase}"
            })
            
            # 更新索引
            phase_idx = min(phase_idx + 1, len(phases) - 1)
            tension_idx = min(tension_idx + 1, len(tension_curve) - 1)
        
        return episodes
    
    def get_available_arcs(self) -> List[Dict]:
        """获取所有可用的故事弧线"""
        return [
            {
                'type': arc.value,
                'name': self._get_arc_name(arc),
                'description': self._get_arc_description(arc),
                'typical_ending': self.arc_templates[arc]['typical_ending'].value
            }
            for arc in StoryArc
        ]
    
    def _get_arc_name(self, arc: StoryArc) -> str:
        names = {
            StoryArc.HERO_JOURNEY: "英雄之旅",
            StoryArc.FALL_AND_REDEMPTION: "堕落与救赎",
            StoryArc.RAGS_TO_RICHES: "麻雀变凤凰",
            StoryArc.TRAGEDY: "悲剧",
            StoryArc.COMEDY: "喜剧",
            StoryArc.REBIRTH: "重生",
            StoryArc.VENGEANCE: "复仇",
            StoryArc.MYSTERY: "悬疑"
        }
        return names.get(arc, arc.value)
    
    def _get_arc_description(self, arc: StoryArc) -> str:
        descs = {
            StoryArc.HERO_JOURNEY: "经典英雄成长故事，从平凡走向伟大",
            StoryArc.FALL_AND_REDEMPTION: "角色经历堕落，最终找到救赎之路",
            StoryArc.RAGS_TO_RICHES: "从卑微起点到成功巅峰的逆袭故事",
            StoryArc.TRAGEDY: "主人公因缺陷走向毁灭的悲剧命运",
            StoryArc.COMEDY: "轻松幽默，问题最终圆满解决",
            StoryArc.REBIRTH: "经历绝望后获得重生的转变故事",
            StoryArc.VENGEANCE: "因伤害踏上复仇之路的故事",
            StoryArc.MYSTERY: "层层谜团，最终真相大白"
        }
        return descs.get(arc, "")

class EndingGenerator:
    """结局生成器"""
    
    def __init__(self):
        self.ending_templates = {
            EndingType.HAPPY: {
                'keywords': ['圆满', '幸福', '成功', '团聚', '和解'],
                'typical_elements': ['英雄凯旋', '有情人终成眷属', '家人团聚', '梦想实现'],
                'tension_pattern': [7, 6, 4, 2, 1]
            },
            EndingType.BITTERSWEET: {
                'keywords': ['遗憾', '代价', '失去', '成长', '释然'],
                'typical_elements': ['牺牲换来和平', '遗憾但释然', '虽败犹荣', '物是人非'],
                'tension_pattern': [8, 9, 7, 5, 4]
            },
            EndingType.TRAGIC: {
                'keywords': ['牺牲', '毁灭', '失去', '绝望', '无奈'],
                'typical_elements': ['英雄陨落', '阴谋得逞', '无力回天', '命运的捉弄'],
                'tension_pattern': [7, 8, 9, 10, 10]
            },
            EndingType.OPEN: {
                'keywords': ['未知', '延续', '悬而未决', '未来', '可能性'],
                'typical_elements': ['故事未完待续', '命运未知', '新的开始', '伏笔揭晓'],
                'tension_pattern': [6, 6, 7, 6, 5]
            },
            EndingType.SURPRISE: {
                'keywords': ['反转', '真相', '意外', '揭露', '震撼'],
                'typical_elements': ['真凶现身', '身份揭露', '卧底反转', '隐藏关系曝光'],
                'tension_pattern': [5, 6, 7, 9, 8]
            },
            EndingType.CYCLICAL: {
                'keywords': ['呼应', '轮回', '轮回', '开始', '结束'],
                'typical_elements': ['首尾呼应', '时间轮回', '命运循环', '故事重现'],
                'tension_pattern': [6, 7, 6, 5, 6]
            }
        }
    
    def generate_ending(
        self,
        ending_type: EndingType,
        story_context: Dict,
        num_episodes: int = 3
    ) -> str:
        """生成结局内容"""
        template = self.ending_templates.get(ending_type)
        if not template:
            return ""
        
        ending_content = []
        
        # 生成结局铺垫（倒数第2集）
        if num_episodes >= 2:
            ending_content.append(self._generate_ending_setup(ending_type, template))
        
        # 生成高潮（倒数第1集）
        ending_content.append(self._generate_climax(ending_type, template, story_context))
        
        # 生成结局（最后一集）
        ending_content.append(self._generate_resolution(ending_type, template))
        
        return '\n\n'.join(ending_content)
    
    def _generate_ending_setup(self, ending_type: EndingType, template: Dict) -> str:
        """生成结局铺垫"""
        setups = {
            EndingType.HAPPY: "经过漫长的旅程，主角终于看到了胜利的曙光。所有努力即将得到回报...",
            EndingType.BITTERSWEET: "胜利就在眼前，但代价已经付出。有人选择离开，带着遗憾...",
            EndingType.TRAGIC: "命运的车轮开始转动，一切都在朝着无法挽回的方向发展...",
            EndingType.OPEN: "故事似乎要结束了，但新的谜团正在浮现...",
            EndingType.SURPRISE: "就在一切看似明朗之时，一个意外的发现打破了一切...",
            EndingType.CYCLICAL: "故事似乎回到了原点，但一切已经不同..."
        }
        return setups.get(ending_type, "")
    
    def _generate_climax(self, ending_type: EndingType, template: Dict, context: Dict) -> str:
        """生成高潮"""
        keywords = template['keywords']
        protagonist = context.get('protagonist', '主角')
        
        climaxes = {
            EndingType.HAPPY: f"{protagonist}克服了最后的障碍，胜利的欢呼声响彻云霄！",
            EndingType.BITTERSWEET: f"最终对决来临，{protagonist}必须在理想和现实之间做出选择...",
            EndingType.TRAGIC: f"命运无情地降临，{protagonist}拼尽全力却无法改变结局...",
            EndingType.OPEN: f"当所有人以为故事结束时，真相才刚刚开始浮现...",
            EndingType.SURPRISE: f"那个一直被信任的人，竟然是...",
            EndingType.CYCLICAL: f"时间倒流，一切重新开始，但记忆依然存在..."
        }
        return climaxes.get(ending_type, "")
    
    def _generate_resolution(self, ending_type: EndingType, template: Dict) -> str:
        """生成结局"""
        elements = template['typical_elements']
        resolution = elements[0] if elements else ""
        
        resolutions = {
            EndingType.HAPPY: f"结局：{resolution}。所有人都得到了幸福的归宿。",
            EndingType.BITTERSWEET: f"结局：{resolution}。虽然不完美，但这就是成长。",
            EndingType.TRAGIC: f"结局：{resolution}。故事在遗憾中落幕。",
            EndingType.OPEN: f"结局：{resolution}。故事还在继续...",
            EndingType.SURPRISE: f"结局：{resolution}。所有人都震惊了。",
            EndingType.CYCLICAL: f"结局：{resolution}。一切都在轮回中延续。"
        }
        return resolutions.get(ending_type, "")

class ForeshadowingManager:
    """伏笔管理系统"""
    
    def __init__(self):
        self.foreshadowing_patterns = [
            {
                'type': 'character',
                'pattern': r'(提到了|暗示了|出现了|隐藏着).*?(秘密|身份|过去)',
                'example': '配角不经意提到主角的神秘过去'
            },
            {
                'type': 'object',
                'pattern': r'(一件|一个|一枚).*?(物品|信物|证物)',
                'example': '某个重要物品在第一集出现'
            },
            {
                'type': 'relationship',
                'pattern': r'(似乎|好像|可能).*?(认识|熟悉|有关系)',
                'example': '两个角色之间的微妙关系'
            },
            {
                'type': 'prophecy',
                'pattern': r'(预言|预言|预示|命运的)',
                'example': '某个关于命运的预言'
            },
            {
                'type': 'mystery',
                'pattern': r'(谜团|真相|秘密|隐藏)',
                'example': '某个未解之谜'
            }
        ]
    
    def generate_foreshadowing(
        self,
        num_items: int = 5,
        story_theme: str = ""
    ) -> List[Dict]:
        """生成伏笔列表"""
        foreshadowings = []
        
        base_templates = [
            {
                'title': '神秘的信物',
                'description': f'一件带有特殊标记的物品，在关键时刻发挥作用',
                'reveal_point': '中后期'
            },
            {
                'title': '隐藏的关系',
                'description': f'看似无关的两个角色，实际上有着不为人知的联系',
                'reveal_point': '中期'
            },
            {
                'title': '命运的预言',
                'description': f'关于故事走向的神秘预示',
                'reveal_point': '结局'
            },
            {
                'title': '过去的创伤',
                'description': f'角色努力隐藏的过去经历',
                'reveal_point': '角色弧线高潮'
            },
            {
                'title': '隐藏的反派',
                'description': f'幕后操控一切的神秘人物',
                'reveal_point': '后期反转'
            }
        ]
        
        for i in range(min(num_items, len(base_templates))):
            template = base_templates[i]
            foreshadowings.append({
                'id': f'fs_{i+1}',
                'title': template['title'],
                'description': template['description'],
                'reveal_point': template['reveal_point'],
                'status': 'unrevealed'
            })
        
        return foreshadowings
    
    def generate_reveal_script(
        self,
        foreshadowing: Dict,
        story_context: Dict
    ) -> str:
        """生成伏笔揭示的剧本片段"""
        reveals = {
            '神秘的信物': '当主角拿出那件物品时，所有人都震惊了——这就是失散多年的证物！',
            '隐藏的关系': '"原来...你是我一直在找的人！"真相终于大白。',
            '命运的预言': '预言成真的那一刻，所有人都陷入了沉默。',
            '过去的创伤': '当伤疤被揭开，主角终于面对了那个不愿提起的过去。',
            '隐藏的反派': '"这一切的幕后黑手，竟然是你！"震惊的真相浮出水面。'
        }
        return reveals.get(foreshadowing.get('title', ''), '')

class ScriptContinuationEngine:
    """剧本续写引擎 - 主控制器"""
    
    def __init__(self):
        self.parser = PlotOutlineParser()
        self.arc_generator = StoryArcGenerator()
        self.ending_generator = EndingGenerator()
        self.foreshadowing_manager = ForeshadowingManager()
    
    def continue_script(
        self,
        original_outline: str,
        target_arc: str = "hero_journey",
        num_episodes: int = 5,
        ending_type: str = "happy",
        add_foreshadowing: bool = True,
        language: str = "zh"
    ) -> ContinuationResult:
        """
        续写剧本
        
        Args:
            original_outline: 原始大纲
            target_arc: 目标故事弧线
            num_episodes: 目标集数
            ending_type: 结局类型
            add_foreshadowing: 是否添加伏笔
            language: 语言
            
        Returns:
            ContinuationResult: 续写结果
        """
        # 解析原始大纲
        plot_nodes = self.parser.parse(original_outline)
        
        # 生成故事弧线
        try:
            arc_type = StoryArc(target_arc)
        except ValueError:
            arc_type = StoryArc.HERO_JOURNEY
        
        arc_structure = self.arc_generator.generate_arc(arc_type, num_episodes)
        
        # 生成结局
        try:
            end_type = EndingType(ending_type)
        except ValueError:
            end_type = EndingType.HAPPY
        
        story_context = {
            'protagonist': plot_nodes[0].characters[0] if plot_nodes and plot_nodes[0].characters else '主角',
            'theme': plot_nodes[0].description[:50] if plot_nodes else ''
        }
        
        ending_content = self.ending_generator.generate_ending(
            end_type, story_context, num_episodes
        )
        
        # 生成伏笔
        foreshadowing = []
        if add_foreshadowing:
            foreshadowing = self.foreshadowing_manager.generate_foreshadowing(
                num_items=5,
                story_theme=story_context['theme']
            )
        
        # 生成续写内容
        continuation = self._generate_continuation_content(
            plot_nodes, arc_structure, ending_content, foreshadowing, language
        )
        
        # 提取新角色
        new_characters = self._extract_new_characters(arc_structure, foreshadowing)
        
        # 生成角色发展
        character_development = self._generate_character_development(
            plot_nodes, arc_structure
        )
        
        return ContinuationResult(
            original_outline=original_outline,
            generated_plot=continuation,
            branch_name=f"{arc_type.value}_{ending_type}",
            ending_type=end_type,
            new_characters=new_characters,
            foreshadowing_elements=[f['title'] for f in foreshadowing],
            character_development=character_development
        )
    
    def _generate_continuation_content(
        self,
        plot_nodes: List[PlotNode],
        arc_structure: List[Dict],
        ending_content: str,
        foreshadowing: List[Dict],
        language: str
    ) -> str:
        """生成完整的续写内容"""
        content_parts = []
        
        # 生成剧情结构
        content_parts.append("# 续写剧情结构\n")
        content_parts.append(f"## 目标集数：{len(arc_structure)}集\n")
        
        for episode in arc_structure:
            content_parts.append(f"### {episode['title']}")
            content_parts.append(f"- 阶段：{episode['phase']}")
            content_parts.append(f"- 张力值：{episode['tension']}/10")
            content_parts.append("")
        
        # 添加伏笔
        if foreshadowing:
            content_parts.append("\n## 伏笔设置")
            for fs in foreshadowing:
                content_parts.append(f"- **{fs['title']}**：{fs['description']}（揭示点：{fs['reveal_point']}）")
        
        # 添加结局
        if ending_content:
            content_parts.append("\n## 结局内容\n")
            content_parts.append(ending_content)
        
        return '\n'.join(content_parts)
    
    def _extract_new_characters(
        self,
        arc_structure: List[Dict],
        foreshadowing: List[Dict]
    ) -> List[Dict]:
        """提取需要新增的角色"""
        characters = []
        
        # 基于故事弧线推断角色类型
        if any('考验' in e.get('phase', '') for e in arc_structure):
            characters.append({
                'name': '导师角色',
                'role': 'mentor',
                'description': '在关键时刻给予主角指导和帮助'
            })
        
        if any('考验与盟友' in e.get('phase', '') for e in arc_structure):
            characters.append({
                'name': '盟友角色',
                'role': 'ally',
                'description': '与主角并肩作战的伙伴'
            })
        
        if any('最深处的洞穴' in e.get('phase', '') for e in arc_structure):
            characters.append({
                'name': '守护者角色',
                'role': 'guardian',
                'description': '守护关键事物或信息的角色'
            })
        
        # 基于伏笔生成角色
        for fs in foreshadowing:
            if '隐藏的反派' in fs.get('title', ''):
                characters.append({
                    'name': '神秘反派',
                    'role': 'antagonist',
                    'description': '隐藏在幕后的真正敌人'
                })
        
        return characters
    
    def _generate_character_development(
        self,
        plot_nodes: List[PlotNode],
        arc_structure: List[Dict]
    ) -> Dict[str, str]:
        """生成角色发展轨迹"""
        development = {}
        
        for node in plot_nodes:
            for char in node.characters:
                if char not in development:
                    development[char] = ""
                
                # 基于剧情节点生成发展
                if node.tension_level > 7:
                    development[char] += f"在高压情境下展现内心挣扎；"
                elif node.tension_level < 4:
                    development[char] += f"展现轻松一面和成长；"
        
        return development
    
    def generate_branch_options(
        self,
        outline: str,
        num_branches: int = 3
    ) -> List[StoryBranch]:
        """生成故事分支选项"""
        branches = []
        
        ending_options = [
            (EndingType.HAPPY, "圆满结局", "主角成功实现目标"),
            (EndingType.BITTERSWEET, "苦乐参半", "成功但付出代价"),
            (EndingType.TRAGIC, "悲剧结局", "主角命运多舛")
        ]
        
        arc_options = [
            StoryArc.HERO_JOURNEY,
            StoryArc.FALL_AND_REDEMPTION,
            StoryArc.VENGEANCE
        ]
        
        for i in range(min(num_branches, len(ending_options))):
            ending, name, desc = ending_options[i]
            arc = arc_options[i] if i < len(arc_options) else arc_options[0]
            
            branch = StoryBranch(
                id=f"branch_{i+1}",
                name=name,
                plot_points=[],
                ending_type=ending,
                probability=1.0 / num_branches
            )
            branches.append(branch)
        
        return branches
    
    def get_available_options(self) -> Dict:
        """获取所有可用选项"""
        return {
            'story_arcs': self.arc_generator.get_available_arcs(),
            'ending_types': [
                {'type': e.value, 'name': self._get_ending_name(e)}
                for e in EndingType
            ]
        }
    
    def _get_ending_name(self, ending: EndingType) -> str:
        names = {
            EndingType.HAPPY: "圆满结局",
            EndingType.BITTERSWEET: "苦乐参半",
            EndingType.TRAGIC: "悲剧结局",
            EndingType.OPEN: "开放式结局",
            EndingType.SURPRISE: "反转型结局",
            EndingType.CYCLICAL: "首尾呼应型"
        }
        return names.get(ending, ending.value)
