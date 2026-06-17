"""剧本生成模块 v11 - 角色成长弧线·多视角叙事·主题深化"""

import json
import os
import random
from openai import OpenAI
import config

# ============ v11 核心：角色成长弧线系统 ============

class CharacterGrowthArc:
    """角色成长弧线 - 记录角色在故事中的变化"""
    
    GROWTH_TYPES = {
        "觉醒": {
            "描述": "从普通人成长为觉醒者",
            "起点": "平凡、不自信",
            "转折点": "遭遇重大事件",
            "终点": "觉醒力量、找到自我",
            "关键词": ["觉醒", "成长", "蜕变", "力量"]
        },
        "救赎": {
            "描述": "从迷失到重新找回方向",
            "起点": "迷茫、堕落或犯错",
            "转折点": "遇到关键人物或事件",
            "终点": "找回初心、获得救赎",
            "关键词": ["救赎", "迷失", "初心", "回归"]
        },
        "羁绊": {
            "描述": "从孤僻到建立深厚羁绊",
            "起点": "封闭内心、独自承受",
            "转折点": "遇到能够理解自己的人",
            "终点": "敞开心扉、建立羁绊",
            "关键词": ["羁绊", "友情", "信任", "陪伴"]
        },
        "抉择": {
            "描述": "在艰难抉择中成长",
            "起点": "面临两难选择",
            "转折点": "做出牺牲或选择",
            "终点": "承担责任、获得成长",
            "关键词": ["抉择", "牺牲", "责任", "勇气"]
        },
        "和解": {
            "描述": "与过去和解、放下执念",
            "起点": "心怀怨恨或执念",
            "转折点": "理解真相或对方",
            "终点": "放下执念、获得平静",
            "关键词": ["和解", "放下", "释然", "理解"]
        },
        "传承": {
            "描述": "将所学传递给下一代",
            "起点": "独自掌握某种能力",
            "转折点": "遇到需要培养的人",
            "终点": "传承精神、薪火相传",
            "关键词": ["传承", "教导", "信任", "延续"]
        }
    }
    
    @classmethod
    def get_growth_for_character(cls, personality: str, role: str = "主角") -> dict:
        """根据性格和角色确定成长弧线"""
        personality_lower = personality.lower()
        
        # 根据性格匹配成长类型
        if any(kw in personality_lower for kw in ["平凡", "普通", "软弱", "胆怯"]):
            return cls.GROWTH_TYPES["觉醒"]
        elif any(kw in personality_lower for kw in ["迷茫", "叛逆", "堕落"]):
            return cls.GROWTH_TYPES["救赎"]
        elif any(kw in personality_lower for kw in ["孤僻", "冷漠", "独立"]):
            return cls.GROWTH_TYPES["羁绊"]
        elif any(kw in personality_lower for kw in ["犹豫", "善良", "天真"]):
            return cls.GROWTH_TYPES["抉择"]
        elif any(kw in personality_lower for kw in ["怨恨", "执着", "固执"]):
            return cls.GROWTH_TYPES["和解"]
        elif any(kw in personality_lower for kw in ["导师", "长辈", "智慧"]):
            return cls.GROWTH_TYPES["传承"]
        else:
            return cls.GROWTH_TYPES["觉醒"]  # 默认觉醒弧线
    
    @classmethod
    def generate_growth_constraint(cls, characters: list) -> str:
        """生成角色成长约束"""
        constraints = []
        for char in characters:
            role = char.get("role", "配角")
            if role in ["主角", "核心角色"]:
                growth = cls.get_growth_for_character(char.get("personality", ""), role)
                constraints.append(f"- {char['name']}：{growth['描述']}")
        return "\n".join(constraints) if constraints else ""

# ============ v11 核心：多视角叙事系统 ============

class MultiPerspectiveNarrative:
    """多视角叙事 - 同一事件从不同角色的视角呈现"""
    
    @classmethod
    def generate_multi_perspective_hint(cls) -> str:
        """生成多视角叙事提示"""
        return """
【多视角叙事要求】
- 关键场景可以从2-3个角色的视角分别呈现
- 每个视角展现不同的信息和情感
- 通过视角切换增加信息量和悬念
- 视角切换时要有明确的过渡标识
"""
    
    @classmethod
    def should_use_multi_perspective(cls, story_type: str) -> bool:
        """判断是否适合多视角叙事"""
        multi_perspective_types = [
            "悬疑推理", "热血冒险", "恋爱日常", "奇幻魔法", "科幻未来"
        ]
        return story_type in multi_perspective_types
    
    @classmethod
    def structure_multi_perspective_scene(cls, panels: list, characters: list) -> list:
        """构建多视角分镜"""
        if len(characters) < 2 or len(panels) < 3:
            return panels
        
        # 选择两个主要角色作为视角
        main_chars = [c["name"] for c in characters[:2]]
        
        structured = []
        for i, panel in enumerate(panels):
            structured.append(panel)
            # 在第2个分镜后，可以切换视角
            if i == 1 and len(characters) >= 2:
                panel["perspective_shift"] = True
                panel["new_perspective"] = main_chars[1]
                panel["perspective_note"] = f"【{main_chars[1]}视角】"
        
        return structured

# ============ v11 核心：主题深化系统 ============

class ThemeDeepening:
    """主题深化 - 为故事赋予更深层的意义"""
    
    THEMES = {
        "成长与蜕变": {
            "核心问题": "人如何突破自我？",
            "探讨角度": ["勇气", "选择", "牺牲", "坚持"],
            "金句类型": "真正的强大，是敢于面对恐惧的自己"
        },
        "爱与羁绊": {
            "核心问题": "爱意味着什么？",
            "探讨角度": ["亲情", "友情", "爱情", "博爱"],
            "金句类型": "真正的羁绊，是即使分离也心心相印"
        },
        "正义与抉择": {
            "核心问题": "什么是真正的正义？",
            "探讨角度": ["规则", "道德", "牺牲", "代价"],
            "金句类型": "正义的代价，往往是沉重的"
        },
        "真相与谎言": {
            "核心问题": "真相一定是最重要的吗？",
            "探讨角度": ["真相", "谎言", "善意", "保护"],
            "金句类型": "有些谎言，是温柔的守护"
        },
        "过去与未来": {
            "核心问题": "人应该活在过去还是未来？",
            "探讨角度": ["回忆", "放下", "希望", "前行"],
            "金句类型": "过去无法改变，但未来可以创造"
        },
        "孤独与陪伴": {
            "核心问题": "人为何害怕孤独？",
            "探讨角度": ["独处", "陪伴", "理解", "共鸣"],
            "金句类型": "最深的孤独，是不被理解的灵魂"
        }
    }
    
    @classmethod
    def get_theme_for_story(cls, story_type: str) -> dict:
        """根据故事类型推荐主题"""
        theme_map = {
            "热血冒险": "成长与蜕变",
            "恋爱日常": "爱与羁绊",
            "悬疑推理": "真相与谎言",
            "奇幻魔法": "成长与蜕变",
            "科幻未来": "过去与未来",
            "治愈日常": "孤独与陪伴",
            "逆袭成长": "成长与蜕变",
        }
        theme_name = theme_map.get(story_type, "成长与蜕变")
        return cls.THEMES.get(theme_name, cls.THEMES["成长与蜕变"])
    
    @classmethod
    def generate_theme_constraint(cls, story_type: str) -> str:
        """生成主题深化约束"""
        theme = cls.get_theme_for_story(story_type)
        return f"""
【主题深化要求】
- 核心主题：{theme['核心问题']}
- 探讨角度：{"、".join(theme['探讨角度'])}
- 在关键场景融入主题思考
- 可用金句升华主题："{theme['金句类型']}"
"""

# ============ v11 核心：对话张力系统 ============

class DialogueTension:
    """对话张力 - 让对话更有戏剧性"""
    
    TENSION_TYPES = {
        "对峙": {
            "特点": "双方立场对立，言语交锋激烈",
            "表现形式": ["反问", "质问", "反驳", "威胁"],
            "节奏": "快节奏，句句紧逼"
        },
        "试探": {
            "特点": "双方在试探对方底线",
            "表现形式": ["暗示", "旁敲侧击", "反话", "沉默"],
            "节奏": "慢节奏，意味深长"
        },
        "坦白": {
            "特点": "一方终于说出真心话",
            "表现形式": ["倾诉", "告白", "道歉", "表白"],
            "节奏": "先慢后快，情绪爆发"
        },
        "误会": {
            "特点": "双方信息不对等，产生误解",
            "表现形式": ["猜疑", "质问", "辩解", "澄清"],
            "节奏": "先快后慢，悬念铺垫"
        }
    }
    
    @classmethod
    def get_tension_for_scene(cls, emotion: str) -> str:
        """根据情感选择对话张力类型"""
        tension_map = {
            "紧张": "对峙",
            "高潮": "对峙",
            "悬疑": "试探",
            "浪漫": "试探",
            "悲伤": "坦白",
            "搞笑": "误会",
        }
        return tension_map.get(emotion, "对峙")
    
    @classmethod
    def generate_tension_hint(cls, emotion: str) -> str:
        """生成对话张力提示"""
        tension_type = cls.get_tension_for_scene(emotion)
        tension = cls.TENSION_TYPES.get(tension_type, cls.TENSION_TYPES["对峙"])
        return f"【对话张力】{tension['特点']}，节奏：{tension['节奏']}"

# ============ v10 核心：情感曲线系统（保留）============

class EmotionCurve:
    """情感曲线设计器 - 让故事有起伏有节奏"""
    
    # 情感类型映射
    EMOTION_TYPES = {
        "tension": "紧张",
        "warmth": "温馨", 
        "excitement": "兴奋",
        "sadness": "悲伤",
        "humor": "搞笑",
        "romance": "浪漫",
        "mystery": "悬疑",
        "climax": "高潮",
        "resolution": "释然",
    }
    
    @classmethod
    def design_curve(cls, total_pages: int) -> list:
        """
        设计故事的情感曲线
        返回每页的情感类型列表
        """
        if total_pages <= 3:
            return cls._short_story_curve(total_pages)
        elif total_pages <= 6:
            return cls._medium_story_curve(total_pages)
        else:
            return cls._long_story_curve(total_pages)
    
    @classmethod
    def _short_story_curve(cls, pages: int) -> list:
        """短篇：铺垫→冲突→高潮→收尾"""
        base = ["温馨", "紧张", "高潮", "温馨"]
        return base[:pages]
    
    @classmethod
    def _medium_story_curve(cls, pages: int) -> list:
        """中篇：起→承→转→合的多次循环"""
        curve = []
        rhythm = ["温馨", "紧张", "搞笑", "紧张", "高潮", "温馨", "悬念", "高潮", "释然"]
        for i in range(pages):
            curve.append(rhythm[i % len(rhythm)])
        return curve
    
    @classmethod
    def _long_story_curve(cls, pages: int) -> list:
        """长篇：多幕高潮设计"""
        curve = []
        phases = [
            ("温馨", "紧张"),  # 开场
            ("搞笑", "紧张"),  # 发展1
            ("悬疑", "浪漫"),  # 发展2
            ("紧张", "高潮"),  # 高潮1
            ("悲伤", "温馨"),  # 低谷
            ("悬念", "高潮"),  # 最终高潮
            ("释然",),         # 收尾
        ]
        for phase in phases:
            curve.extend(phase)
        return curve[:pages]
    
    @classmethod
    def get_emotion_description(cls, emotion: str) -> str:
        """获取情感的氛围描述"""
        descriptions = {
            "紧张": "压迫感十足，音乐节奏加快",
            "温馨": "柔和光效，背景音乐舒缓",
            "搞笑": "夸张表情，动作变形，配欢快音效",
            "悲伤": "冷色调，眼泪特写，雨声",
            "浪漫": "柔光，花瓣飘落，心跳音效",
            "悬疑": "阴影，神秘音效，镜头推近",
            "高潮": "爆发特效，光芒四射，震撼音效",
            "释然": "阳光，音乐渐强，微笑",
            "兴奋": "明亮色调，动作快节奏",
        }
        return descriptions.get(emotion, "普通氛围")

# ============ v10 核心：伏笔与呼应系统 ============

class ForeshadowingSystem:
    """伏笔埋设与呼应系统"""
    
    def __init__(self):
        self.foreshadows = []  # 埋下的伏笔
        self.callbacks = []    # 后续呼应
    
    def add_foreshadow(self, panel: dict, tag: str, hint: str):
        """埋设伏笔"""
        self.foreshadows.append({
            "panel": panel,
            "tag": tag,          # 伏笔标签
            "hint": hint,        # 暗示内容
            "is_fulfilled": False
        })
    
    def add_callback(self, panel: dict, tag: str, payoff: str):
        """添加呼应"""
        self.callbacks.append({
            "panel": panel,
            "tag": tag,
            "payoff": payoff
        })
        # 标记伏笔已被呼应
        for fs in self.foreshadows:
            if fs["tag"] == tag and not fs["is_fulfilled"]:
                fs["is_fulfilled"] = True
                break
    
    def generate_foreshadow_hint(self) -> str:
        """生成伏笔提示词给AI"""
        return """
【伏笔设计要求】
- 在故事前期埋设1-2个小伏笔
- 伏笔要自然融入剧情，不刻意
- 在故事后期呼应伏笔，形成闭环
- 伏笔类型：人物小习惯、神秘物品、意外事件、角色过去
"""
    
    def integrate_foreshadowing(self, script: dict) -> dict:
        """将伏笔系统融入剧本"""
        # 随机选择一个伏笔类型
        foreshadow_type = random.choice([
            "人物小习惯",
            "神秘物品", 
            "意外事件",
            "角色过去",
            "关键台词"
        ])
        
        # 在脚本中标记伏笔位置（由调用方处理）
        if len(script.get("pages", [])) >= 3:
            # 在第1-2页埋下伏笔
            foreshadow_page = random.randint(1, min(2, len(script["pages"]) - 1))
            if "foreshadow_hint" not in script:
                script["foreshadow_hint"] = {
                    "type": foreshadow_type,
                    "foreshadow_at": f"第{foreshadow_page}页",
                    "resolve_at": f"第{len(script['pages'])}页"
                }
        
        return script

# ============ v10 核心：角色对话差异化系统 ============

class DialogueStyleSystem:
    """角色对话风格差异化 - 让每个角色说话都有自己的特色"""
    
    DIALOGUE_STYLES = {
        "阳光型": {
            "说话特点": "开朗活泼，使用感叹词多",
            "常用词汇": ["太好了", "加油", "没问题", "交给我吧"],
            "语气助词": ["呀", "哦", "呢", "哈"]
        },
        "高冷型": {
            "说话特点": "简短有力，不拖泥带水",
            "常用词汇": ["...", "无聊", "随便", "无所谓"],
            "语气助词": ["。", "——"]
        },
        "腹黑型": {
            "说话特点": "话里有话，阴阳怪气",
            "常用词汇": ["哎呀", "真巧", "有意思", "你说是吧"],
            "语气助词": ["呢", "哦~", "呵"]
        },
        "热血型": {
            "说话特点": "充满干劲，声音大",
            "常用词汇": ["绝对不会", "一定要", "绝不允许"],
            "语气助词": ["！", "啊", "啦"]
        },
        "温柔型": {
            "说话特点": "轻声细语，关心他人",
            "常用词汇": ["没关系", "辛苦了", "没事的", "要加油哦"],
            "语气助词": ["~", "呢", "的哦"]
        },
        "傲娇型": {
            "说话特点": "嘴硬心软，否认三连",
            "常用词汇": ["才不是", "不是因为你", "哼"],
            "语气助词": ["啦", "哼", "啊"]
        },
        "搞笑型": {
            "说话特点": "冷笑话多，跑题达人",
            "常用词汇": ["等等", "话说", "说起来", "对了"],
            "语气助词": ["...", "啊这", "嗯？"]
        },
        "神秘型": {
            "说话特点": "意味深长，话说一半",
            "常用词汇": ["有些事", "时候到了", "真相是"],
            "语气助词": ["...", "~"]
        }
    }
    
    @classmethod
    def get_style_for_character(cls, personality: str) -> str:
        """根据性格确定对话风格"""
        personality_lower = personality.lower()
        
        if any(kw in personality_lower for kw in ["开朗", "活泼", "阳光", "乐观"]):
            return "阳光型"
        elif any(kw in personality_lower for kw in ["冷漠", "高冷", "冷酷", "冷淡"]):
            return "高冷型"
        elif any(kw in personality_lower for kw in ["腹黑", "心机", "狡猾"]):
            return "腹黑型"
        elif any(kw in personality_lower for kw in ["热血", "正义", "勇敢"]):
            return "热血型"
        elif any(kw in personality_lower for kw in ["温柔", "体贴", "善良"]):
            return "温柔型"
        elif any(kw in personality_lower for kw in ["傲娇", "别扭"]):
            return "傲娇型"
        elif any(kw in personality_lower for kw in ["搞笑", "幽默", "逗比"]):
            return "搞笑型"
        elif any(kw in personality_lower for kw in ["神秘", "高深", "深沉"]):
            return "神秘型"
        else:
            return "阳光型"  # 默认
    
    @classmethod
    def generate_dialogue_constraint(cls) -> str:
        """生成对话风格约束词"""
        styles_text = []
        for name, style in cls.DIALOGUE_STYLES.items():
            styles_text.append(f"- {name}：{style['说话特点']}")
        return "\n".join(styles_text)

# ============ v10 核心：旁白增强系统 ============

class NarrationSystem:
    """增强的旁白系统 - 内心独白、场景描述、氛围烘托"""
    
    NARRATION_TYPES = {
        "场景描述": {
            "用途": "交代时间、地点、环境",
            "句式": "【时间】在【地点】，...",
            "示例": "【黄昏·天台】夕阳将整座城市染成橘红色"
        },
        "内心独白": {
            "用途": "展现角色内心想法",
            "句式": "（内心：...）",
            "示例": "（内心：为什么...会是他？）"
        },
        "氛围烘托": {
            "用途": "营造情绪氛围",
            "句式": "旁白：...",
            "示例": "旁白：空气中弥漫着不安的气息..."
        },
        "时间跳跃": {
            "用途": "转场过渡",
            "句式": "【数小时后】/【第二天】",
            "示例": "【与此同时·某处】"
        },
        "关键解读": {
            "用途": "补充信息、增加深度",
            "句式": "※...※",
            "示例": "※他不知道，这个选择将改变一切※"
        }
    }
    
    @classmethod
    def generate_narration_constraint(cls) -> str:
        """生成旁白使用规则"""
        rules = []
        for name, info in cls.NARRATION_TYPES.items():
            rules.append(f"- {name}：{info['用途']}，使用{info['句式']}")
        return "\n".join(rules)

# ============ v10 剧本生成提示词 ============

V11_SCRIPT_PROMPT = """你是一个专业的漫画编剧，擅长创作有深度、有情感共鸣的故事。

【v11核心能力】
1. **情感曲线设计**：故事要有起伏，紧张与温馨交替，最后推向高潮
2. **角色成长弧线**：主角要有明显的成长变化（觉醒/救赎/羁绊/抉择/和解/传承）
3. **主题深化**：故事要有深层主题（成长/爱/正义/真相/过去未来/孤独）
4. **伏笔与呼应**：埋设小伏笔并在后续情节中呼应，增加故事深度
5. **角色差异化对话**：每个角色说话风格要独特，符合性格设定
6. **增强旁白系统**：结合内心独白、场景描述、氛围烘托
7. **对话张力**：根据情感选择合适的对话张力类型（对峙/试探/坦白/误会）

【角色成长弧线】
{growth_constraints}

【主题深化】
{theme_constraint}

【情感曲线要求】
情感顺序参考（可根据故事调整）：
- 温馨开场 → 引入矛盾 → 搞笑缓解 → 紧张升级 → 高潮爆发 → 温馨收尾
- 或：悬疑铺垫 → 真相揭露 → 危机降临 → 绝地反击 → 圆满结局

【伏笔设计】
- 每篇至少埋设1个小伏笔
- 伏笔要自然（人物习惯、神秘物品、关键台词等）
- 在故事后期呼应，形成闭环

【角色对话差异化】
{dialogue_styles}

【对话张力】
{tension_hint}

【旁白系统】
{narration_rules}

【输出格式 - 严格JSON】
{{
  "title": "漫画标题",
  "synopsis": "一句话简介",
  "theme": "本篇主题（如：成长与蜕变）",
  "theme_question": "核心问题（如：人如何突破自我？）",
  "emotion_curve": ["温馨", "紧张", "搞笑", "高潮", "温馨"],
  "foreshadow_hint": "本篇埋设的伏笔描述",
  "characters": [
    {{
      "name": "角色名",
      "role": "主角/配角",
      "visual_description": "详细外貌描述（用于AI生图保持一致）",
      "personality": "性格简述",
      "dialogue_style": "对话风格（阳光型/高冷型/腹黑型等）",
      "growth_arc": "角色成长弧线（如：觉醒/救赎等）"
    }}
  ],
  "pages": [
    {{
      "page_number": 1,
      "emotion": "本页情感基调",
      "emotion_note": "情感说明（如：建立温馨氛围）",
      "growth_moment": "是否有关键成长时刻（true/false）",
      "panels": [
        {{
          "panel_number": 1,
          "scene_description": "详细的场景画面描述",
          "characters_in_scene": ["角色1"],
          "camera_angle": "特写/中景/远景/俯视/仰视",
          "inner_thought": "内心独白（可选）",
          "narration": "旁白/场景描述（可选）",
          "dialogues": [
            {{
              "speaker": "角色1",
              "text": "对话内容",
              "style_note": "符合角色性格的说话方式",
              "tension_type": "对话张力类型"
            }}
          ],
          "sound_effects": ["轰！"],
          "foreshadow": true/false,
          "foreshadow_detail": "伏笔细节（如埋下某物/某句话）",
          "callback": true/false,
          "callback_detail": "伏笔呼应细节",
          "perspective_shift": true/false,
          "new_perspective": "切换到的新视角角色"
        }}
      ]
    }}
  ]
}}

【关键要求】
1. 严格按JSON格式输出，不要输出任何其他内容
2. 每页2-4个分镜
3. 角色外貌描述必须一致（用于AI保持一致）
4. 对话要符合角色性格和对话风格
5. 主角至少有一次明确的成长时刻
6. 在关键场景融入主题思考
7. 最后一页要有收束感，给读者满足的结局
8. 如果埋了伏笔，在回收伏笔的panel标注 "callback": true

用户要求：
- 主题：{theme}
- 风格：{style}
- 页数：{pages}页
- 角色参考：{character_hints}
- 额外要求：{extra}
"""

# ============ 多章节剧本提示词（v10增强版）============

V10_CHAPTER_SCRIPT_PROMPT = """你是一个专业的漫画编剧。请生成一部**多章节连载**的完整漫画剧本。

【v10增强功能】
1. 每章有独立的情感曲线，整体有更大的情感弧线
2. 章节之间埋设悬念，形成钩子效应
3. 角色在多章中有成长和变化
4. 每章结尾有强悬念

【情感设计】
- 单章情感曲线：开场→发展→小高潮→悬念
- 整体情感弧线：引入期→对抗期→高潮期→解决期

【伏笔系统】
- 章节内伏笔：单章内埋设和回收
- 跨章节伏笔：第一章埋下的伏笔在后续章节回收

【角色成长】
- 主角在第一章到最后一章要有明显成长
- 角色关系随章节发展变化

输出格式：
{{
  "title": "漫画标题",
  "synopsis": "整体故事简介",
  "total_chapters": 总章节数,
  "overall_emotion_arc": ["引入", "发展", "高潮", "解决"],
  "main_foreshadow": "贯穿全篇的主线伏笔",
  "characters": [...],
  "chapters": [
    {{
      "chapter_number": 1,
      "chapter_title": "第1章标题",
      "chapter_synopsis": "本章简介",
      "chapter_emotion_curve": ["温馨", "紧张", "高潮"],
      "chapter_foreshadow": "本章埋设的伏笔",
      "pages": [...]
    }}
  ]
}}

用户要求：
- 主题：{theme}
- 风格：{style}
- 总章节：{chapters}章，每章{pages}页
- 总页数：约{total_pages}页
- 角色参考：{character_hints}
- 额外要求：{extra}
"""

def generate_script(
    theme: str, 
    style: str = "热血冒险", 
    pages: int = 3,
    extra: str = "无", 
    character_hints: str = "自由发挥"
) -> dict:
    """v10生成漫剧剧本 - 增强版"""
    client = get_client()
    
    # 生成情感曲线
    emotion_curve = EmotionCurve.design_curve(pages)
    emotion_curve_str = " → ".join(emotion_curve)
    
    # 获取对话风格和旁白规则
    dialogue_styles = DialogueStyleSystem.generate_dialogue_constraint()
    narration_rules = NarrationSystem.generate_narration_constraint()
    
    # v11 新增：生成角色成长约束和主题约束
    theme_constraint = ThemeDeepening.generate_theme_constraint(style)
    tension_hint = DialogueTension.generate_tension_hint("紧张")  # 默认紧张
    
    prompt = V11_SCRIPT_PROMPT.format(
        theme=theme,
        style=style,
        pages=pages,
        character_hints=character_hints,
        extra=extra,
        dialogue_styles=dialogue_styles,
        narration_rules=narration_rules,
        emotion_curve_str=emotion_curve_str,
        growth_constraints="主角需要有明确的成长变化",
        theme_constraint=theme_constraint,
        tension_hint=tension_hint
    )
    
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": "你是一个专业的漫画编剧，擅长创作有深度有情感共鸣的故事。请严格按照JSON格式输出。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=8192,
    )
    
    content = response.choices[0].message.content.strip()
    
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    try:
        script = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"剧本解析失败: {e}\n原始输出: {content[:500]}")
    
    # v11 整合系统
    script = EmotionCurve.design_curve(pages)
    script = ForeshadowingSystem().integrate_foreshadowing(script)
    
    # v11 新增：为角色添加成长弧线分析
    script["character_growth_analysis"] = analyze_character_growth(script)
    
    _validate_script(script)
    return script

def analyze_character_growth(script: dict) -> list:
    """分析角色的成长弧线"""
    analysis = []
    characters = script.get("characters", [])
    
    for char in characters:
        role = char.get("role", "配角")
        if role in ["主角", "核心角色"]:
            personality = char.get("personality", "")
            growth_arc = char.get("growth_arc", "")
            growth = CharacterGrowthArc.get_growth_for_character(personality, role)
            
            analysis.append({
                "character": char.get("name"),
                "role": role,
                "growth_type": growth_arc or list(CharacterGrowthArc.GROWTH_TYPES.keys())[0],
                "growth_description": growth["描述"],
                "start_state": growth["起点"],
                "turning_point": growth["转折点"],
                "end_state": growth["终点"]
            })
    
    return analysis

def generate_multi_chapter_script(
    theme: str, 
    style: str = "热血冒险", 
    chapters: int = 2,
    pages_per_chapter: int = 4,
    extra: str = "无",
    character_hints: str = "自由发挥"
) -> dict:
    """v10生成多章节剧本"""
    client = get_client()
    
    total_pages = chapters * pages_per_chapter
    
    prompt = V10_CHAPTER_SCRIPT_PROMPT.format(
        theme=theme,
        style=style,
        chapters=chapters,
        pages=pages_per_chapter,
        total_pages=total_pages,
        character_hints=character_hints,
        extra=extra
    )
    
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": "你是一个专业的漫画编剧，擅长创作多章节连载故事。请严格按照JSON格式输出。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=16384,
    )
    
    content = response.choices[0].message.content.strip()
    
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    try:
        script = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"剧本解析失败: {e}\n原始输出: {content[:500]}")
    
    _validate_multi_chapter_script(script)
    return script

def continue_to_next_chapter(
    current_script: dict,
    chapter_number: int,
    style: str = "热血冒险",
    pages: int = 4
) -> dict:
    """续写到下一章（v10增强：包含伏笔呼应）"""
    client = get_client()
    
    # 提取已有剧情和伏笔
    existing_summary = f"已有 {chapter_number-1} 章"
    main_foreshadow = current_script.get("main_foreshadow", "")
    
    if current_script.get("chapters"):
        for ch in current_script["chapters"]:
            existing_summary += f"\n第{ch['chapter_number']}章「{ch['chapter_title']}」：{ch.get('chapter_synopsis', '')}"
    
    prompt = f"""根据已有剧情和主线伏笔，继续创作第{chapter_number}章。

主线伏笔（需要在后续章节中呼应）：
{main_foreshadow}

{existing_summary}

请生成第{chapter_number}章的内容，要求：
1. 承接上一章的悬念
2. 呼应主线伏笔（如果条件成熟）
3. 有独立的小高潮
4. 为后续章节埋下新伏笔
5. 严格按JSON格式输出

输出格式：
{{
  "chapter_number": {chapter_number},
  "chapter_title": "第{chapter_number}章标题",
  "chapter_synopsis": "本章简介",
  "chapter_emotion_curve": ["情感序列"],
  "chapter_foreshadow": "本章埋设的新伏笔（如果有）",
  "callback_main_foreshadow": true/false,
  "pages": [
    {{
      "page_number": 1,
      "emotion": "本页情感",
      "panels": [...]
    }}
  ]
}}
"""
    
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": "你是专业漫画编剧。请严格按JSON格式输出。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=8192,
    )
    
    content = response.choices[0].message.content.strip()
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    return json.loads(content)

def get_client():
    api_key = config.LLM_API_KEY
    base_url = config.LLM_BASE_URL
    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY 或切换到 Demo 模式")
    return OpenAI(api_key=api_key, base_url=base_url)

# ============ Demo 模式 ============

def generate_demo_script(
    theme: str, 
    style: str = "热血冒险", 
    pages: int = 3
) -> dict:
    """v10 Demo模式：生成预设剧本（包含情感曲线和伏笔）"""
    template = config.STORY_TEMPLATES.get(style, config.STORY_TEMPLATES["热血冒险"])
    
    # 设计情感曲线
    emotion_curve = EmotionCurve.design_curve(pages)
    
    # 构建角色
    characters = []
    for i, char_tmpl in enumerate(template["characters"]):
        dialogue_style = DialogueStyleSystem.get_style_for_character(char_tmpl["trait"])
        characters.append({
            "name": char_tmpl["name"],
            "visual_description": _demo_character_desc(style, i),
            "personality": char_tmpl["trait"],
            "dialogue_style": dialogue_style,
        })
    
    # 构建页面
    demo_scenes = _get_demo_scenes(style, pages)
    pages_data = []
    for p_idx in range(pages):
        emotion = emotion_curve[p_idx] if p_idx < len(emotion_curve) else "紧张"
        panels = []
        for s_idx, scene in enumerate(demo_scenes[p_idx] if p_idx < len(demo_scenes) else demo_scenes[-1]):
            panel = {
                "panel_number": s_idx + 1,
                "scene_description": scene["desc"],
                "characters_in_scene": scene["chars"],
                "camera_angle": scene["camera"],
                "inner_thought": scene.get("inner_thought"),
                "narration": scene.get("narration"),
                "dialogues": scene["dialogues"],
                "sound_effects": scene.get("sfx", []),
                "foreshadow": scene.get("foreshadow", False),
                "callback": scene.get("callback", False),
            }
            # 移除None值
            panel = {k: v for k, v in panel.items() if v is not None}
            panels.append(panel)
        
        pages_data.append({
            "page_number": p_idx + 1,
            "emotion": emotion,
            "emotion_note": EmotionCurve.get_emotion_description(emotion),
            "panels": panels,
        })
    
    return {
        "title": f"Demo: {theme[:20]}",
        "synopsis": template["description"],
        "emotion_curve": emotion_curve,
        "foreshadow_hint": "Demo故事的小彩蛋伏笔",
        "characters": characters,
        "pages": pages_data,
    }

def generate_demo_multi_chapter(
    theme: str, 
    style: str = "热血冒险", 
    chapters: int = 2, 
    pages_per_chapter: int = 3
) -> dict:
    """v10 Demo模式：生成多章节预设剧本"""
    all_chapters = []
    all_characters = []
    
    for ch_idx in range(chapters):
        ch_script = generate_demo_script(
            f"{theme} - 第{ch_idx+1}章", 
            style, 
            pages_per_chapter
        )
        chapter_data = {
            "chapter_number": ch_idx + 1,
            "chapter_title": f"第{ch_idx+1}章",
            "chapter_synopsis": f"第{ch_idx+1}章的故事",
            "chapter_emotion_curve": ch_script["emotion_curve"],
            "chapter_foreshadow": "本章小悬念" if ch_idx < chapters - 1 else None,
            "characters": ch_script["characters"],
            "pages": ch_script["pages"]
        }
        all_chapters.append(chapter_data)
        if ch_idx == 0:
            all_characters = ch_script["characters"]
    
    return {
        "title": f"Demo: {theme[:20]}",
        "synopsis": f"多章节连载漫画，共{chapters}章",
        "total_chapters": chapters,
        "overall_emotion_arc": ["引入", "发展", "高潮", "解决"],
        "main_foreshadow": "贯穿全篇的主线悬念",
        "characters": all_characters,
        "chapters": all_chapters
    }

# ============ 验证函数 ============

def _validate_script(script: dict):
    """验证剧本"""
    assert "title" in script, "剧本缺少 title 字段"
    assert "characters" in script, "剧本缺少 characters 字段"
    assert "pages" in script, "剧本缺少 pages 字段"
    assert len(script["pages"]) > 0, "剧本没有页面内容"

def _validate_multi_chapter_script(script: dict):
    """验证多章节剧本"""
    assert "title" in script, "剧本缺少 title 字段"
    assert "chapters" in script, "剧本缺少 chapters 字段"
    assert len(script["chapters"]) > 0, "剧本没有章节内容"
    
    for ch in script["chapters"]:
        assert "pages" in ch, f"第{ch.get('chapter_number', '?')}章缺少 pages"

# ============ 辅助函数 ============

def build_image_prompt(panel: dict, characters: list, style_key: str = "manga") -> str:
    """根据分镜信息构建AI生图的prompt"""
    style_prompt = config.STYLE_PROMPTS.get(style_key, config.STYLE_PROMPTS["manga"])
    
    char_descs = []
    for char_name in panel.get("characters_in_scene", []):
        for c in characters:
            if c["name"] == char_name:
                char_descs.append(f"{c['name']}: {c['visual_description']}")
                break
    
    char_text = "; ".join(char_descs) if char_descs else ""
    camera = panel.get("camera_angle", "")
    emotion = panel.get("emotion", "")
    
    prompt_parts = [
        style_prompt + ",",
        f"{camera} shot," if camera else "",
        panel.get("scene_description", ""),
        char_text,
        f"mood: {emotion}" if emotion else "",
        "high quality, detailed, masterpiece",
    ]
    
    return " ".join(p for p in prompt_parts if p).strip()

def get_story_analysis(script: dict) -> dict:
    """分析剧本的情感曲线和伏笔"""
    analysis = {
        "emotion_curve": script.get("emotion_curve", []),
        "foreshadow": script.get("foreshadow_hint", ""),
        "character_count": len(script.get("characters", [])),
        "page_count": len(script.get("pages", [])),
        "total_panels": sum(len(p.get("panels", [])) for p in script.get("pages", [])),
    }
    
    # 统计伏笔
    foreshadow_panels = []
    callback_panels = []
    for page in script.get("pages", []):
        for panel in page.get("panels", []):
            if panel.get("foreshadow"):
                foreshadow_panels.append(f"第{page['page_number']}页-{panel['panel_number']}格")
            if panel.get("callback"):
                callback_panels.append(f"第{page['page_number']}页-{panel['panel_number']}格")
    
    analysis["foreshadow_panels"] = foreshadow_panels
    analysis["callback_panels"] = callback_panels
    
    return analysis

# ============ Demo 数据 ============

def _demo_character_desc(style: str, index: int) -> str:
    """Demo角色外貌描述"""
    descs = {
        "热血冒险": [
            "黑发少年，红色夹克，左脸有小伤疤，目光坚定",
            "银发青年，黑色风衣，红色瞳孔，冷峻表情",
            "棕发少女，双马尾，绿色猎装，大弓",
        ],
        "恋爱日常": [
            "栗色长发女生，粉白校服裙，头发别着小发卡",
            "黑色短发男生，整齐校服，眼镜，温暖微笑",
        ],
        "悬疑推理": [
            "戴猎鹿帽的高瘦男人，深色大衣，锐利眼神",
            "短发干练女性，黑色西装，拿着笔记本",
        ],
        "奇幻魔法": [
            "白发精灵少年，蓝色法袍，水晶法杖，尖尖耳朵",
            "金色盔甲女骑士，红色披风，长剑，坚毅表情",
        ],
        "科幻未来": [
            "白色实验服的女科学家，短发，AR眼镜",
            "银色机甲AI人形，蓝色光纹，表情平静",
        ],
        "恐怖惊悚": [
            "苍白青年，旧校服，黑色眼圈，紧张表情",
            "黑影身影，看不清面容，两点红光",
        ],
        "搞笑日常": [
            "乱蓬蓬头发男生，歪扭校服，打瞌睡",
            "整洁班长，眼镜反光，嘴角抽搐",
            "天然呆少女，笑眯眯，衣服穿反",
        ],
        "古风仙侠": [
            "白衣修士，束发金冠，玉佩，清俊面容",
            "灰袍老者，白眉长须，拂尘，仙风道骨",
            "红衣妖女，狐耳，银发如瀑，妩媚笑容",
        ],
    }
    style_descs = descs.get(style, descs["热血冒险"])
    return style_descs[index % len(style_descs)]

def _get_demo_scenes(style: str, pages: int) -> list:
    """Demo场景数据 - v10增强：包含内心独白和伏笔"""
    all_scenes = {
        "热血冒险": [
            # Page 1 - 温馨开场 + 伏笔埋设
            [
                {"desc": "宁静小镇，阳光明媚，主角走在路上", "chars": ["主角"], "camera": "远景",
                 "dialogues": [{"speaker": "旁白", "text": "在这座平凡的小镇上..."}],
                 "narration": "【清晨·小镇】一切都很平静",
                 "inner_thought": "（今天好像有什么要发生...）",
                 "sfx": [], "emotion": "温馨", "foreshadow": True, "foreshadow_detail": "主角看向手腕上的旧伤疤"},
                {"desc": "天空裂开红光，巨大冲击波", "chars": ["主角"], "camera": "特写",
                 "dialogues": [{"speaker": "主角", "text": "这是...什么！"}],
                 "sfx": ["轰！！"], "emotion": "紧张"},
                {"desc": "主角手中出现发光纹路", "chars": ["主角"], "camera": "中景",
                 "dialogues": [{"speaker": "主角", "text": "身体...好热！"}],
                 "sfx": ["嗡——"], "emotion": "紧张"},
            ],
            # Page 2 - 冲突升级
            [
                {"desc": "废墟中宿敌现身", "chars": ["宿敌"], "camera": "仰视",
                 "dialogues": [{"speaker": "宿敌", "text": "你也觉醒了吗...有趣"}],
                 "narration": "【与此同时】命运的齿轮开始转动",
                 "sfx": [], "emotion": "紧张"},
                {"desc": "两人对峙，力量碰撞", "chars": ["主角", "宿敌"], "camera": "远景",
                 "dialogues": [{"speaker": "主角", "text": "我不会输给你！"}],
                 "sfx": ["砰！"], "emotion": "愤怒"},
                {"desc": "伙伴从侧翼冲出", "chars": ["伙伴"], "camera": "中景",
                 "dialogues": [{"speaker": "伙伴", "text": "久等了！"}, {"speaker": "主角", "text": "你来得好！"}],
                 "sfx": ["嗖！"], "emotion": "热血"},
            ],
            # Page 3 - 高潮 + 伏笔回收 + 悬念
            [
                {"desc": "主角释放全力一击", "chars": ["主角"], "camera": "仰视",
                 "dialogues": [{"speaker": "主角", "text": "这一击——为了所有人！"}],
                 "sfx": ["轰！！！"], "emotion": "高潮"},
                {"desc": "战斗结束，主角看向手腕", "chars": ["主角"], "camera": "特写",
                 "dialogues": [{"speaker": "旁白", "text": "那道旧伤疤，和今天的力量...有关联？"}],
                 "inner_thought": "（那个梦里的声音...是真实的吗）",
                 "sfx": [], "emotion": "悬念", "callback": True},  # 呼应第1页的伏笔
                {"desc": "远处，新的身影出现", "chars": [], "camera": "远景",
                 "dialogues": [{"speaker": "？？？", "text": "终于找到你了..."}],
                 "narration": "【未完待续】",
                 "sfx": [], "emotion": "悬念"},
            ],
        ],
        "恋爱日常": [
            # Page 1
            [
                {"desc": "樱花飘落的校园门口", "chars": ["女主角"], "camera": "中景",
                 "dialogues": [],
                 "narration": "【春天·校园】樱花盛开的季节",
                 "inner_thought": "（今天是转学生来的日子...）",
                 "sfx": [], "emotion": "浪漫"},
                {"desc": "男生捡起女生掉落的手帕", "chars": ["男主角"], "camera": "特写",
                 "dialogues": [{"speaker": "男主角", "text": "这个...是你的吧？"}, {"speaker": "女主角", "text": "啊...谢谢"}],
                 "sfx": [], "emotion": "温馨"},
                {"desc": "两人手指触碰，都红了脸", "chars": ["女主角", "男主角"], "camera": "特写",
                 "dialogues": [{"speaker": "旁白", "text": "心跳漏了一拍"}],
                 "sfx": ["咚"], "emotion": "浪漫"},
            ],
            # Page 2
            [
                {"desc": "雨天屋檐下等雨停", "chars": ["女主角", "男主角"], "camera": "中景",
                 "dialogues": [{"speaker": "女主角", "text": "雨...好像不打算停了"}, {"speaker": "男主角", "text": "那就再等等吧"}],
                 "sfx": ["哗——"], "emotion": "温馨"},
                {"desc": "男主披外套在女主肩上", "chars": ["女主角"], "camera": "特写",
                 "dialogues": [{"speaker": "女主角", "text": "...你不冷吗？"}, {"speaker": "男主角", "text": "我不冷"}],
                 "inner_thought": "（其实有点冷...但她好像很冷的样子）",
                 "sfx": [], "emotion": "浪漫"},
                {"desc": "雨后彩虹下相视而笑", "chars": ["女主角", "男主角"], "camera": "远景",
                 "dialogues": [],
                 "narration": "【雨后】有些东西悄悄发芽了",
                 "sfx": [], "emotion": "温馨"},
            ],
            # Page 3
            [
                {"desc": "几天后，女生在教室发呆", "chars": ["女主角"], "camera": "特写",
                 "dialogues": [],
                 "inner_thought": "（最近总是想起那天的他...）",
                 "sfx": [], "emotion": "浪漫"},
                {"desc": "男生出现，手里拿着什么东西", "chars": ["男主角"], "camera": "中景",
                 "dialogues": [{"speaker": "男主角", "text": "那个...上次的手帕，洗好了还你"}],
                 "sfx": [], "emotion": "温馨"},
                {"desc": "两人再次相视，樱花飘落", "chars": ["女主角", "男主角"], "camera": "远景",
                 "dialogues": [],
                 "narration": "【樱花树下】故事才刚刚开始",
                 "sfx": [], "emotion": "浪漫", "foreshadow": True, "foreshadow_detail": "背景中有人拍下了这一幕"},
            ],
        ],
    }
    
    # 通用场景模板
    generic = [
        [
            {"desc": "故事开始，主角登场", "chars": ["主角"], "camera": "中景",
             "dialogues": [{"speaker": "旁白", "text": "一切的起点..."}],
             "sfx": [], "emotion": "温馨"},
            {"desc": "意外事件发生", "chars": ["主角"], "camera": "特写",
             "dialogues": [{"speaker": "主角", "text": "这是怎么回事！"}],
             "sfx": ["轰！"], "emotion": "惊讶"},
            {"desc": "新角色带来转机", "chars": ["主角", "伙伴"], "camera": "远景",
             "dialogues": [{"speaker": "伙伴", "text": "需要帮忙吗？"}],
             "sfx": [], "emotion": "紧张"},
        ],
        [
            {"desc": "高潮对决", "chars": ["主角"], "camera": "仰视",
             "dialogues": [{"speaker": "主角", "text": "我不会放弃！"}],
             "sfx": ["砰！"], "emotion": "紧张"},
            {"desc": "胜利或突破", "chars": ["主角"], "camera": "中景",
             "dialogues": [{"speaker": "旁白", "text": "故事仍在继续..."}],
             "sfx": [], "emotion": "温馨"},
        ],
    ]
    
    scenes = all_scenes.get(style, generic)
    result = []
    for i in range(pages):
        result.append(scenes[i % len(scenes)])
    return result
