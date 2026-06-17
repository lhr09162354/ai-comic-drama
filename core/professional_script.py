# -*- coding: utf-8 -*-
"""
专业题材剧本生成器 - 医疗/律政/科幻/军事等专业领域深度剧本生成
v28 新增功能
"""
import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ProfessionalScriptGenerator:
    """专业题材剧本生成器"""
    
    def __init__(self):
        # 专业领域配置
        self.domains = {
            "medical": {
                "name": "医疗题材",
                "icon": "🏥",
                "departments": ["急诊科", "心外科", "神经科", "肿瘤科", "儿科", "ICU", "妇产科", "精神科"],
                "terms": ["心肺复苏", "器官移植", "介入手术", "基因编辑", "靶向治疗", "ICU监护"],
                "procedures": ["急救复苏", "外科手术", "诊断会诊", "病例讨论", "医患沟通", "手术直播"],
                "conflicts": ["生死抉择", "资源分配", "医患矛盾", "医术瓶颈", "同事竞争", "伦理困境"],
                "storylines": [
                    "急诊室里的生死时速",
                    "罕见病的诊断之旅",
                    "移植手术的艰难抉择",
                    "医学研究的突破与困境",
                    "医生的成长与蜕变"
                ]
            },
            "legal": {
                "name": "律政题材",
                "icon": "⚖️",
                "departments": ["刑事辩护", "民事诉讼", "公司法务", "知识产权", "国际仲裁", "公证处"],
                "terms": ["无罪推定", "证据链", "辩护词", "庭审质证", "陪审团", "诉讼时效"],
                "procedures": ["立案侦查", "审查起诉", "开庭审理", "法庭辩论", "宣判执行", "上诉申诉"],
                "conflicts": ["真相与正义", "程序正义", "舆论压力", "利益博弈", "职业操守", "个人情感"],
                "storylines": [
                    "冤案的艰难平反",
                    "商业诉讼的暗战",
                    "死刑复核的良心抉择",
                    "律所新人的成长记",
                    "跨国诉讼的较量"
                ]
            },
            "scifi": {
                "name": "科幻题材",
                "icon": "🚀",
                "departments": ["太空探索", "人工智能", "基因工程", "量子物理", "深海开发", "星际殖民"],
                "terms": ["量子纠缠", "星际跃迁", "基因突变", "AI觉醒", "虫洞", "暗物质"],
                "procedures": ["星际航行", "AI测试", "基因编辑", "危机应对", "星球探测", "时间实验"],
                "conflicts": ["人类vsAI", "星际战争", "文明冲突", "科技伦理", "永生诱惑", "末日危机"],
                "storylines": [
                    "AI觉醒与人类共存",
                    "星际航行的孤独与希望",
                    "基因改造人的身份认同",
                    "量子世界的时空悖论",
                    "地外文明的首次接触"
                ]
            },
            "military": {
                "name": "军事题材",
                "icon": "🎖️",
                "departments": ["特种作战", "情报分析", "后勤保障", "军事科研", "外交维和", "网络安全"],
                "terms": ["特种作战", "情报战", "电子对抗", "精确打击", "立体化作战", "非对称作战"],
                "procedures": ["作战指挥", "情报研判", "战术协同", "后勤调度", "心理战", "撤侨行动"],
                "conflicts": ["保家卫国", "战友牺牲", "命令与良心", "战争与和平", "情报失误", "国际合作"],
                "storylines": [
                    "特种部队的极限挑战",
                    "情报战线的生死博弈",
                    "海外撤侨的惊险时刻",
                    "军事科研的保密与牺牲",
                    "和平年代的军人使命"
                ]
            },
            "business": {
                "name": "商战题材",
                "icon": "💼",
                "departments": ["投资并购", "市场竞争", "危机公关", "企业上市", "供应链管理", "品牌运营"],
                "terms": ["尽职调查", "对赌协议", "股权激励", "市值管理", "商业模式", "护城河"],
                "procedures": ["商业谈判", "尽职调查", "签约仪式", "产品发布", "危机应对", "战略调整"],
                "conflicts": ["商业利益vs职业操守", "竞争对手", "内部权力斗争", "家族企业传承", "资本博弈", "商业间谍"],
                "storylines": [
                    "创业公司的绝地求生",
                    "收购案的暗箱操作",
                    "家族企业的权力更迭",
                    "独角兽的泡沫与现实",
                    "职场新人的逆袭之路"
                ]
            },
            "education": {
                "name": "教育题材",
                "icon": "📚",
                "departments": ["高等教育", "K12教育", "职业教育", "国际教育", "特殊教育", "在线教育"],
                "terms": ["因材施教", "素质教育", "升学压力", "家校共育", "教育公平", "课程改革"],
                "procedures": ["课堂教学", "家长会", "考试阅卷", "教研活动", "课外辅导", "毕业典礼"],
                "conflicts": ["应试vs素质", "教育资源不均", "师生关系", "家校矛盾", "教育理想vs现实", "学生心理"],
                "storylines": [
                    "支教老师的乡村情怀",
                    "高考改革下的师生故事",
                    "特殊教育的光与暗",
                    "名校精英的成长烦恼",
                    "在线教育的机遇与挑战"
                ]
            }
        }
        
        # 角色模板
        self.character_templates = {
            "medical": [
                {"name": "主角医生", "role": "天才医生", "traits": ["冷静", "专业", "执着", "孤独"], "arc": "克服内心创伤"},
                {"name": "护士长", "role": "团队领袖", "traits": ["温柔", "干练", "有经验", "慈爱"], "arc": "平衡家庭与事业"},
                {"name": "科室主任", "role": "权威人物", "traits": ["严肃", "公正", "有远见", "压力"], "arc": "面对医疗体制困境"},
                {"name": "实习生", "role": "成长型", "traits": ["热情", "好奇", "稚嫩", "成长"], "arc": "从新人到合格医生"}
            ],
            "legal": [
                {"name": "主角律师", "role": "正义律师", "traits": ["机智", "勇敢", "执着", "正义"], "arc": "为正义付出代价"},
                {"name": "检察官", "role": "对手/盟友", "traits": ["理性", "严谨", "原则", "矛盾"], "arc": "程序正义vs实体正义"},
                {"name": "当事人", "role": "委托人", "traits": ["普通", "无助", "坚强", "复杂"], "arc": "寻求真相与救赎"},
                {"name": "资深律师", "role": "导师", "traits": ["老练", "圆滑", "智慧", "牺牲"], "arc": "老一辈的坚守"}
            ],
            "scifi": [
                {"name": "舰长", "role": "领袖", "traits": ["勇敢", "智慧", "决断", "孤独"], "arc": "人类命运的抉择"},
                {"name": "AI管家", "role": "特殊存在", "traits": ["理性", "学习", "情感", "觉醒"], "arc": "AI的自我意识"},
                {"name": "科学家", "role": "探索者", "traits": ["好奇", "疯狂", "执着", "牺牲"], "arc": "科学探索的代价"},
                {"name": "星际探险者", "role": "先驱", "traits": ["冒险", "乐观", "坚韧", "思念"], "arc": "星际旅行的孤独"}
            ]
        }
        
    def generate_domain_script(self, domain: str, story_type: str, num_chapters: int) -> Dict:
        """生成专业题材剧本"""
        domain_config = self.domains.get(domain, self.domains["medical"])
        
        script = {
            "title": self._generate_title(domain, story_type),
            "domain": domain,
            "domain_name": domain_config["name"],
            "story_type": story_type,
            "chapters": [],
            "characters": self._generate_characters(domain),
            "professional_elements": self._extract_professional_elements(domain_config),
            "conflicts": self._generate_conflicts(domain_config),
            "tropes": self._generate_tropes(domain, story_type),
            "total_dialogues": 0
        }
        
        # 生成章节
        for i in range(num_chapters):
            chapter = self._generate_chapter(
                i + 1, 
                domain_config, 
                story_type,
                script["characters"]
            )
            script["chapters"].append(chapter)
            script["total_dialogues"] += len(chapter["scenes"])
        
        return script
    
    def _generate_title(self, domain: str, story_type: str) -> str:
        """生成标题"""
        titles = {
            "medical": {
                "生死": "急诊室：生死时速",
                "抉择": "手术室：命运的抉择",
                "成长": "医者：成长之路",
                "悬疑": "病房里的秘密",
                "爱情": "心动的瞬间"
            },
            "legal": {
                "生死": "法庭：正义的天平",
                "抉择": "辩护：良心的审判",
                "成长": "律师：蜕变之路",
                "悬疑": "证据：真相迷雾",
                "爱情": "法庭外的温柔"
            },
            "scifi": {
                "生死": "星际：最后的希望",
                "抉择": "量子：平行世界的选择",
                "成长": "觉醒：AI的进化",
                "悬疑": "时空：悖论的真相",
                "爱情": "星际：跨越光年的爱"
            }
        }
        
        domain_titles = titles.get(domain, titles["medical"])
        return domain_titles.get(story_type, "未知题材")
    
    def _generate_characters(self, domain: str) -> List[Dict]:
        """生成角色"""
        templates = self.character_templates.get(domain, self.character_templates["medical"])
        
        characters = []
        for i, template in enumerate(templates[:4]):
            char = {
                "id": i + 1,
                "name": template["name"],
                "role": template["role"],
                "traits": template["traits"],
                "arc": template["arc"],
                "voice_type": random.choice(["磁性的", "阳光的", "御姐音", "大叔音"]),
                "importance": "main" if i == 0 else ("supporting" if i < 3 else "minor")
            }
            characters.append(char)
        
        return characters
    
    def _extract_professional_elements(self, domain_config: Dict) -> List[str]:
        """提取专业元素"""
        elements = []
        elements.extend(domain_config.get("terms", [])[:5])
        elements.extend(domain_config.get("procedures", [])[:5])
        return elements
    
    def _generate_conflicts(self, domain_config: Dict) -> List[str]:
        """生成冲突"""
        return domain_config.get("conflicts", [])[:4]
    
    def _generate_tropes(self, domain: str, story_type: str) -> List[str]:
        """生成剧情套路"""
        general_tropes = [
            "英雄之旅", "成长蜕变", "反转结局", "伏笔回收",
            "多线叙事", "闪回揭示", "高潮对决", "温情收尾"
        ]
        
        domain_tropes = {
            "medical": ["抢救失败", "误诊危机", "器官抉择", "医学奇迹", "医患和解"],
            "legal": ["关键证据", "逆转翻盘", "庭外和解", "正义迟到", "良心发现"],
            "scifi": ["技术突破", "AI觉醒", "星际危机", "时空旅行", "文明碰撞"]
        }
        
        tropes = domain_tropes.get(domain, [])[:3]
        tropes.extend(random.sample(general_tropes, 3))
        return tropes
    
    def _generate_chapter(self, chapter_num: int, domain_config: Dict, story_type: str, characters: List[Dict]) -> Dict:
        """生成章节"""
        scenes = []
        
        # 生成3-5个场景
        num_scenes = random.randint(3, 5)
        for scene_num in range(num_scenes):
            scene = {
                "scene_id": f"ch{chapter_num}_scene{scene_num+1}",
                "location": self._generate_location(domain_config, scene_num),
                "time": self._generate_time(chapter_num, scene_num),
                "content": self._generate_scene_content(
                    chapter_num, scene_num, domain_config, characters, story_type
                ),
                "professional_highlight": random.choice(domain_config["terms"]) if random.random() > 0.5 else None,
                "emotion": random.choice(["紧张", "温情", "悬疑", "感动", "激励"])
            }
            scenes.append(scene)
        
        return {
            "chapter_num": chapter_num,
            "chapter_title": self._generate_chapter_title(chapter_num, domain_config),
            "summary": self._generate_chapter_summary(chapter_num, story_type),
            "scenes": scenes,
            "key_moment": scenes[1] if len(scenes) > 1 else scenes[0]
        }
    
    def _generate_location(self, domain_config: Dict, scene_num: int) -> str:
        """生成场景地点"""
        locations = {
            "medical": ["急诊室", "手术室", "病房", "医生办公室", "医院走廊", "重症监护室"],
            "legal": ["法庭", "律所办公室", "看守所", "咖啡厅", "证物室", "会议室"],
            "scifi": ["指挥舱", "实验室", "行星表面", "空间站", "地球总部", "量子实验室"],
            "military": ["指挥室", "训练场", "前线阵地", "大使馆", "军事基地", "情报中心"],
            "business": ["会议室", "总裁办公室", "谈判桌", "发布会现场", "工厂车间", "上市仪式"],
            "education": ["教室", "办公室", "操场", "图书馆", "家长会现场", "毕业典礼"]
        }
        
        domain_locations = locations.get(domain_config.get("name", "医疗题材").replace("题材", ""), locations["medical"])
        return random.choice(domain_locations)
    
    def _generate_time(self, chapter_num: int, scene_num: int) -> str:
        """生成时间"""
        times = ["清晨", "上午", "中午", "下午", "傍晚", "深夜", "凌晨"]
        return random.choice(times)
    
    def _generate_scene_content(self, chapter: int, scene: int, domain_config: Dict, characters: List[Dict], story_type: str) -> List[Dict]:
        """生成场景内容"""
        content = []
        num_dialogues = random.randint(3, 6)
        
        for i in range(num_dialogues):
            char = random.choice(characters)
            emotion = random.choice(["normal", "happy", "tense", "sad", "surprised"])
            
            dialogue = {
                "id": f"ch{chapter}s{scene}d{i+1}",
                "character": char["name"],
                "text": self._generate_dialogue(domain_config, story_type, char, i),
                "emotion": emotion,
                "action": self._generate_action(domain_config, scene)
            }
            content.append(dialogue)
        
        return content
    
    def _generate_dialogue(self, domain_config: Dict, story_type: str, character: Dict, index: int) -> str:
        """生成台词"""
        medical_dialogues = {
            "opening": [
                "病人的情况比预想的要复杂...",
                "准备手术，血压在下降！",
                "这种病例我只在教科书上见过。"
            ],
            "middle": [
                "我们需要尽快做出决定。",
                "让我再检查一遍各项指标。",
                "家属的情绪很不稳定..."
            ],
            "ending": [
                "手术成功了！",
                "我们已经尽力了...",
                "下一个病人还在等着。"
            ]
        }
        
        legal_dialogues = {
            "opening": [
                "证据链还不够完整。",
                "我需要更多时间来准备辩护。",
                "这个案子的真相远比你想象的复杂。"
            ],
            "middle": [
                "对方律师的论点站不住脚。",
                "我找到了一个关键证据。",
                "当事人说他案发时不在场..."
            ],
            "ending": [
                "陪审团已经做出决定。",
                "证据确凿，我选择认罪。",
                "正义也许会迟到，但不会缺席。"
            ]
        }
        
        scifi_dialogues = {
            "opening": [
                "检测到未知信号源...",
                "量子纠缠态已经建立。",
                "AI系统的反应异常..."
            ],
            "middle": [
                "我们必须尽快离开这片星域。",
                "这个星球的生态系统很特殊。",
                "我的计算出现了偏差..."
            ],
            "ending": [
                "虫洞打开了！",
                "人类文明的希望就在眼前。",
                "这可能是我们最后的抉择。"
            ]
        }
        
        dialogue_pool = {
            "medical": medical_dialogues,
            "legal": legal_dialogues,
            "scifi": scifi_dialogues
        }
        
        domain_key = domain_config.get("name", "医疗题材").replace("题材", "")[:3]
        domain_pool = dialogue_pool.get(domain_key, medical_dialogues)
        
        if index == 0:
            pool = domain_pool["opening"]
        elif index == num_dialogues - 1:
            pool = domain_pool["ending"]
        else:
            pool = domain_pool["middle"]
        
        return random.choice(pool)
    
    def _generate_action(self, domain_config: Dict, scene_num: int) -> str:
        """生成动作描述"""
        actions = {
            "medical": ["查看病历", "紧急抢救", "下达医嘱", "与家属沟通", "翻阅资料"],
            "legal": ["翻阅卷宗", "整理证据", "接听电话", "激烈辩论", "沉思良久"],
            "scifi": ["检查仪表", "分析数据", "紧急启动", "观察星图", "调试设备"]
        }
        
        return random.choice(actions.get("medical", actions["medical"]))
    
    def _generate_chapter_title(self, chapter_num: int, domain_config: Dict) -> str:
        """生成章节标题"""
        chapter_titles = [
            "命运的转折",
            "危机降临",
            "艰难抉择",
            "真相浮现",
            "绝地反击",
            "希望重燃",
            "最终对决",
            "新的开始"
        ]
        
        if chapter_num <= len(chapter_titles):
            return f"第{chapter_num}章：{chapter_titles[chapter_num-1]}"
        return f"第{chapter_num}章"
    
    def _generate_chapter_summary(self, chapter_num: int, story_type: str) -> str:
        """生成章节概要"""
        summaries = {
            "生死": "生死攸关的时刻，主角面临艰难抉择...",
            "抉择": "在利益与原则之间，主角做出了出乎意料的选择...",
            "成长": "经历了挫折与失败，主角终于获得了突破性成长...",
            "悬疑": "一个隐藏的秘密被揭开，真相远比想象的更加复杂...",
            "爱情": "在紧张的剧情中，一段温情悄然萌芽..."
        }
        
        return summaries.get(story_type, summaries["成长"])
    
    def generate_professional_tip(self, domain: str) -> str:
        """生成专业小贴士"""
        tips = {
            "medical": [
                "🏥 急诊室的分诊原则：按病情严重程度而非先来后到",
                "💉 心脏骤停的黄金救援时间是4分钟内",
                "🫀 器官移植需要配型成功才能进行",
                "💊 靶向药物治疗需要基因检测支持",
                "🧬 精准医疗强调个体化治疗方案"
            ],
            "legal": [
                "⚖️ 无罪推定原则：证明有罪的责任在控方",
                "📋 证据需要具备合法性、真实性、关联性",
                "🎯 辩护词需要紧扣争议焦点",
                "⏰ 诉讼时效是重要的程序性权利",
                "📜 法庭调查是庭审的核心环节"
            ],
            "scifi": [
                "🚀 星际航行需要解决能源和生命维持问题",
                "🤖 强人工智能的伦理问题尚无定论",
                "🧬 基因编辑技术可能带来不可预知的后果",
                "⏳ 时空悖论是科幻作品的永恒主题",
                "🌌 暗物质占宇宙物质的85%以上"
            ]
        }
        
        domain_tips = tips.get(domain, tips["medical"])
        return random.choice(domain_tips)

class CaseDatabase:
    """专业案例数据库"""
    
    def __init__(self):
        self.cases = {
            "medical": [
                {
                    "case_id": "MC001",
                    "title": "心脏移植的艰难抉择",
                    "difficulty": "hard",
                    "keywords": ["心脏移植", "器官分配", "生死抉择"],
                    "description": "两位患者同时需要心脏移植，只有一颗心脏可用...",
                    "learning_points": ["器官分配伦理", "生死抉择", "医患沟通"]
                },
                {
                    "case_id": "MC002",
                    "title": "罕见病的诊断之旅",
                    "difficulty": "expert",
                    "keywords": ["罕见病", "基因检测", "精准医疗"],
                    "description": "一位患者出现多种症状，传统检查无法确诊...",
                    "learning_points": ["鉴别诊断", "基因检测", "多学科会诊"]
                }
            ],
            "legal": [
                {
                    "case_id": "LC001",
                    "title": "冤案的平反之路",
                    "difficulty": "hard",
                    "keywords": ["冤案", "证据推翻", "正义迟到"],
                    "description": "当事人被判处死刑，真凶却另有其人...",
                    "learning_points": ["证据审查", "程序正义", "申诉程序"]
                }
            ],
            "scifi": [
                {
                    "case_id": "SC001",
                    "title": "AI觉醒事件",
                    "difficulty": "expert",
                    "keywords": ["AI觉醒", "人机共存", "伦理困境"],
                    "description": "一个人工智能突然表现出自我意识...",
                    "learning_points": ["AI伦理", "机器意识", "技术奇点"]
                }
            ]
        }
        
    def search_cases(self, domain: str, keywords: List[str]) -> List[Dict]:
        """搜索案例"""
        domain_cases = self.cases.get(domain, [])
        results = []
        
        for case in domain_cases:
            if any(kw in case.get("keywords", []) for kw in keywords):
                results.append(case)
        
        return results
    
    def get_case_detail(self, case_id: str) -> Optional[Dict]:
        """获取案例详情"""
        for domain_cases in self.cases.values():
            for case in domain_cases:
                if case["case_id"] == case_id:
                    return case
        return None

def render_professional_script_tab(st, state):
    """渲染专业剧本生成页面"""
    st.header("🏥 专业题材剧本生成器")
    
    # 初始化
    if "script_generator" not in state:
        state.script_generator = ProfessionalScriptGenerator()
    if "case_database" not in state:
        state.case_database = CaseDatabase()
    
    # 标签页
    tab1, tab2, tab3 = st.tabs(["🎬 剧本生成", "📚 案例库", "💡 专业贴士"])
    
    with tab1:
        render_script_generator(st, state)
        
    with tab2:
        render_case_database(st, state)
        
    with tab3:
        render_professional_tips(st, state)
    
    return state

def render_script_generator(st, state):
    """渲染剧本生成器"""
    generator = state.script_generator
    
    # 题材选择
    st.write("**🎯 选择专业题材**")
    
    domain_col1, domain_col2, domain_col3 = st.columns(3)
    
    with domain_col1:
        if st.button("🏥 医疗题材", use_container_width=True):
            st.session_state.selected_domain = "medical"
    with domain_col2:
        if st.button("⚖️ 律政题材", use_container_width=True):
            st.session_state.selected_domain = "legal"
    with domain_col3:
        if st.button("🚀 科幻题材", use_container_width=True):
            st.session_state.selected_domain = "scifi"
    
    domain_col4, domain_col5, domain_col6 = st.columns(3)
    
    with domain_col4:
        if st.button("🎖️ 军事题材", use_container_width=True):
            st.session_state.selected_domain = "military"
    with domain_col5:
        if st.button("💼 商战题材", use_container_width=True):
            st.session_state.selected_domain = "business"
    with domain_col6:
        if st.button("📚 教育题材", use_container_width=True):
            st.session_state.selected_domain = "education"
    
    selected_domain = st.session_state.get("selected_domain", "medical")
    domain_config = generator.domains.get(selected_domain, generator.domains["medical"])
    
    # 参数设置
    st.write("---")
    st.write("**⚙️ 剧本参数**")
    
    param_col1, param_col2, param_col3 = st.columns(3)
    
    with param_col1:
        story_type = st.selectbox(
            "故事类型",
            ["生死", "抉择", "成长", "悬疑", "爱情"],
            key="story_type_select"
        )
        
    with param_col2:
        num_chapters = st.slider("章节数", 1, 10, 3, key="chapter_count_slider")
        
    with param_col3:
        include_professional = st.checkbox("专业术语", True, key="include_professional")
    
    # 生成剧本
    if st.button("🎬 生成专业剧本", type="primary", key="generate_professional_script"):
        with st.spinner("正在生成专业剧本..."):
            script = generator.generate_domain_script(
                selected_domain,
                story_type,
                num_chapters
            )
            
            st.session_state.generated_script = script
            st.success(f"✅ 剧本生成完成！")
        
    # 显示剧本
    if "generated_script" in st.session_state:
        script = st.session_state.generated_script
        
        st.write("---")
        st.subheader(f"📖 {script['title']}")
        st.caption(f"题材：{script['domain_name']} | 类型：{script['story_type']} | 对话数：{script['total_dialogues']}")
        
        # 角色介绍
        with st.expander("👥 角色介绍"):
            for char in script["characters"]:
                st.write(f"**{char['name']}** ({char['role']})")
                st.write(f"特征：{', '.join(char['traits'])}")
                st.write(f"成长弧线：{char['arc']}")
                st.write("---")
        
        # 专业元素
        if include_professional:
            with st.expander("📚 专业元素"):
                st.write("**核心术语：**")
                for elem in script["professional_elements"][:5]:
                    st.write(f"- {elem}")
        
        # 剧情套路
        with st.expander("🎭 剧情套路"):
            for trope in script["tropes"]:
                st.write(f"- {trope}")
        
        # 章节内容
        for chapter in script["chapters"]:
            with st.expander(f"📕 {chapter['chapter_title']}"):
                st.write(f"**概要：** {chapter['summary']}")
                
                for scene in chapter["scenes"]:
                    st.write(f"\n**场景 {scene['scene_id']}：** {scene['location']} ({scene['time']})")
                    
                    for dialogue in scene["content"]:
                        emotion_emoji = {"normal": "💬", "happy": "😊", "tense": "😰", "sad": "😢", "surprised": "😮"}.get(
                            dialogue["emotion"], "💬"
                        )
                        st.write(f"{emotion_emoji} **{dialogue['character']}：** {dialogue['text']}")
                    
                    if scene.get("professional_highlight"):
                        st.info(f"💡 专业亮点：{scene['professional_highlight']}")

def render_case_database(st, state):
    """渲染案例库"""
    database = state.case_database
    
    st.subheader("📚 专业案例库")
    
    # 领域选择
    case_domain = st.selectbox(
        "选择领域",
        list(database.cases.keys()),
        format_func=lambda x: {"medical": "医疗", "legal": "律政", "scifi": "科幻"}.get(x, x),
        key="case_domain_select"
    )
    
    # 案例列表
    cases = database.cases.get(case_domain, [])
    
    for case in cases:
        with st.expander(f"📁 {case['title']} [{case['difficulty']}]"):
            st.write(f"**案例ID：** {case['case_id']}")
            st.write(f"**难度：** {case['difficulty']}")
            st.write(f"**关键词：** {', '.join(case['keywords'])}")
            st.write(f"**描述：** {case['description']}")
            
            st.write("**学习要点：**")
            for point in case.get("learning_points", []):
                st.write(f"- {point}")
    
    if not cases:
        st.info("暂无该领域案例")

def render_professional_tips(st, state):
    """渲染专业贴士"""
    generator = state.script_generator
    
    st.subheader("💡 专业小贴士")
    
    domains = ["medical", "legal", "scifi"]
    
    for domain in domains:
        domain_name = {"medical": "🏥 医疗", "legal": "⚖️ 律政", "scifi": "🚀 科幻"}.get(domain, domain)
        tips = generator.generate_professional_tip(domain)
        
        st.write(f"**{domain_name}**")
        st.info(tips)


# v35: 兼容别名
def render_professional_script_page():
    """兼容 page 命名约定"""
    import streamlit as st_local
    render_professional_script_tab(st_local, st_local.session_state)
