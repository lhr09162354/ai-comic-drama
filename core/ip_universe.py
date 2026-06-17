# -*- coding: utf-8 -*-
"""
IP联动系统 - 角色跨作品联动/宇宙观构建/彩蛋系统
v28 新增功能
"""
import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class IPUniverse:
    """IP宇宙系统"""
    
    def __init__(self):
        # 已创建的角色数据库
        self.characters_db = {}
        
        # 宇宙设定
        self.universe_settings = {
            "main": {
                "name": "主宇宙",
                "description": "AI漫剧的主线故事宇宙",
                "genres": ["都市", "奇幻", "科幻"],
                "connected_works": []
            },
            "alternate": {
                "name": "平行宇宙",
                "description": "同一角色的不同可能性",
                "genres": ["悬疑", "恐怖"],
                "connected_works": []
            },
            "prequel": {
                "name": "前传宇宙",
                "description": "主线故事前的历史",
                "genres": ["历史", "战争"],
                "connected_works": []
            },
            "spin_off": {
                "name": "衍生宇宙",
                "description": "配角或支线的独立故事",
                "genres": ["喜剧", "爱情"],
                "connected_works": []
            }
        }
        
    def create_character_universe(self, character: Dict, works: List[Dict]) -> Dict:
        """为角色创建跨作品宇宙"""
        universe = {
            "character_id": character.get("id"),
            "character_name": character.get("name"),
            "universe_id": f"universe_{character.get('id')}",
            "main_work": works[0] if works else None,
            "alternate_versions": self._generate_alternate_versions(character),
            "connected_characters": self._find_connections(character, works),
            "timeline": self._build_timeline(works),
            "easter_eggs": []
        }
        
        self._populate_easter_eggs(universe)
        
        return universe
    
    def _generate_alternate_versions(self, character: Dict) -> List[Dict]:
        """生成角色的平行版本"""
        versions = [
            {
                "version_id": f"{character.get('id')}_alt1",
                "title": "黑化版本",
                "description": "角色走向黑暗面的版本",
                "traits": ["冷酷", "腹黑", "强大"],
                "key_difference": "选择了复仇而非宽恕"
            },
            {
                "version_id": f"{character.get('id')}_alt2",
                "title": "和平版本",
                "description": "没有经历冲突的版本",
                "traits": ["温和", "乐观", "善良"],
                "key_difference": "出生在和平年代"
            },
            {
                "version_id": f"{character.get('id')}_alt3",
                "title": "未来版本",
                "description": "多年后的角色",
                "traits": ["睿智", "沉稳", "孤独"],
                "key_difference": "成为领导者但失去重要之人"
            }
        ]
        
        return versions
    
    def _find_connections(self, character: Dict, works: List[Dict]) -> List[Dict]:
        """查找角色关联"""
        connections = []
        
        for work in works:
            if work.get("characters"):
                for char in work["characters"]:
                    if char.get("id") != character.get("id"):
                        connections.append({
                            "character_id": char.get("id"),
                            "character_name": char.get("name"),
                            "relationship": random.choice(["挚友", "对手", "恋人", "导师", "战友"]),
                            "first_meet": work.get("title"),
                            "connection_type": "direct" if random.random() > 0.5 else "indirect"
                        })
                        
        return connections[:5]
    
    def _build_timeline(self, works: List[Dict]) -> List[Dict]:
        """构建时间线"""
        timeline = []
        
        for i, work in enumerate(sorted(works, key=lambda x: x.get("timeline_order", i))):
            timeline.append({
                "event_id": f"event_{i+1}",
                "title": work.get("title", f"事件{i+1}"),
                "year": 2020 + i,
                "description": work.get("summary", ""),
                "importance": "major" if i % 2 == 0 else "minor"
            })
            
        return timeline
    
    def _populate_easter_eggs(self, universe: Dict) -> None:
        """填充彩蛋"""
        universe["easter_eggs"] = [
            {
                "egg_id": "egg_1",
                "name": "幸运数字",
                "description": "角色总是出现在7号场景",
                "hidden_in": ["所有作品"]
            },
            {
                "egg_id": "egg_2",
                "name": "经典台词",
                "description": "平行版本会说对方的经典台词",
                "hidden_in": ["第2版", "第3版"]
            }
        ]

class CrossWorkLinker:
    """跨作品联动"""
    
    def __init__(self):
        self.link_templates = {
            "crossover": {
                "name": "跨界联动",
                "description": "不同作品的角色相遇",
                "mechanics": ["角色穿越", "平行世界相遇", "梦境联动"]
            },
            "reference": {
                "name": "致敬引用",
                "description": "在作品中引用其他作品",
                "mechanics": ["台词致敬", "场景还原", "物品出现"]
            },
            "collaboration": {
                "name": "合作剧情",
                "description": "多个角色共同完成的任务",
                "mechanics": ["组队任务", "对抗BOSS", "交换身份"]
            },
            "legacy": {
                "name": "传承联动",
                "description": "角色的后代或徒弟登场",
                "mechanics": ["师徒关系", "血脉传承", "遗物继承"]
            }
        }
        
    def create_crossover_event(self, works: List[Dict], event_type: str) -> Dict:
        """创建跨界联动事件"""
        event = {
            "event_id": f"event_{random.randint(1000, 9999)}",
            "type": event_type,
            "name": self._generate_event_name(event_type),
            "description": "",
            "participants": [],
            "plot_points": [],
            "rewards": {}
        }
        
        # 选择参与者
        for work in works[:3]:
            if work.get("main_character"):
                event["participants"].append(work["main_character"])
        
        # 生成剧情点
        event["plot_points"] = self._generate_plot_points(event_type, event["participants"])
        
        # 设置奖励
        event["rewards"] = {
            "unlock_content": ["限定皮肤", "隐藏剧情"],
            "achievement": "宇宙探索者",
            "bonus": "理解度+20%"
        }
        
        return event
    
    def _generate_event_name(self, event_type: str) -> str:
        """生成事件名称"""
        names = {
            "crossover": [
                "宇宙大乱斗", "英雄集结", "跨维度相遇", "最强对决"
            ],
            "reference": [
                "致敬之夜", "经典重现", "彩蛋搜寻", "回忆杀"
            ],
            "collaboration": [
                "团队挑战", "协作任务", "共建任务", "联合作战"
            ],
            "legacy": [
                "传承时刻", "师徒情深", "血脉觉醒", "遗物守护"
            ]
        }
        
        return random.choice(names.get(event_type, names["crossover"]))
    
    def _generate_plot_points(self, event_type: str, participants: List[Dict]) -> List[Dict]:
        """生成剧情点"""
        plot_points = []
        
        # 开场
        plot_points.append({
            "point_id": "intro",
            "title": "意外相遇",
            "description": "参与者们因为某种原因聚集在一起",
            "duration": 3
        })
        
        # 发展
        plot_points.append({
            "point_id": "conflict",
            "title": "冲突产生",
            "description": "不同背景的角色产生摩擦或共同目标",
            "duration": 5
        })
        
        # 高潮
        plot_points.append({
            "point_id": "climax",
            "title": "携手作战",
            "description": "角色们团结一致面对挑战",
            "duration": 8
        })
        
        # 结尾
        plot_points.append({
            "point_id": "ending",
            "title": "新的羁绊",
            "description": "联动结束，角色获得新的关系或成长",
            "duration": 2
        })
        
        return plot_points
    
    def link_characters(self, char1: Dict, char2: Dict, relationship: str) -> Dict:
        """建立角色关联"""
        return {
            "link_id": f"link_{char1.get('id')}_{char2.get('id')}",
            "character_1": char1.get("name"),
            "character_2": char2.get("name"),
            "relationship": relationship,
            "link_type": self._determine_link_type(relationship),
            "connection_events": [],
            "shared_memories": [],
            "crossover_potential": random.uniform(0.7, 1.0)
        }
    
    def _determine_link_type(self, relationship: str) -> str:
        """确定关联类型"""
        positive = ["挚友", "恋人", "导师", "战友", "搭档"]
        negative = ["对手", "仇人", "陌生人"]
        
        if relationship in positive:
            return "positive"
        elif relationship in negative:
            return "negative"
        return "neutral"

class EasterEggSystem:
    """彩蛋系统"""
    
    def __init__(self):
        self.egg_categories = {
            "character": {
                "name": "角色彩蛋",
                "examples": ["前世今生", "平行版本", "致敬角色"]
            },
            "scene": {
                "name": "场景彩蛋",
                "examples": ["经典场景还原", "隐藏地点", "细节暗示"]
            },
            "dialogue": {
                "name": "台词彩蛋",
                "examples": ["经典台词引用", "谐音梗", "双关语"]
            },
            "item": {
                "name": "物品彩蛋",
                "examples": ["关键道具", "收藏品", "纪念品"]
            },
            "audio": {
                "name": "音频彩蛋",
                "examples": ["BGM彩蛋", "音效暗示", "角色主题曲"]
            },
            "visual": {
                "name": "视觉彩蛋",
                "examples": ["海报暗藏", "分镜细节", "色彩暗示"]
            }
        }
        
        self.egg_templates = {
            "callback": "致敬{}的经典场景",
            "foreshadowing": "为{}埋下的伏笔",
            "celebration": "庆祝{}的特殊时刻",
            "tribute": "致敬{}的经典角色"
        }
        
    def create_easter_egg(self, egg_type: str, reference: str, hidden_in: str) -> Dict:
        """创建彩蛋"""
        template = random.choice(list(self.egg_templates.values()))
        
        egg = {
            "egg_id": f"egg_{random.randint(10000, 99999)}",
            "category": egg_type,
            "name": template.format(reference),
            "description": self._get_description(egg_type),
            "reference": reference,
            "hidden_in": hidden_in,
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "discovered_count": 0,
            "hint": self._generate_hint(egg_type, reference)
        }
        
        return egg
    
    def _get_description(self, egg_type: str) -> str:
        """获取彩蛋描述"""
        descriptions = {
            "character": "发现隐藏角色的真实身份",
            "scene": "找到经典场景的还原细节",
            "dialogue": "注意到台词中的致敬元素",
            "item": "收集到具有特殊意义的物品",
            "audio": "听出BGM中的隐藏信息",
            "visual": "发现画面中的微妙细节"
        }
        return descriptions.get(egg_type, "")
    
    def _generate_hint(self, egg_type: str, reference: str) -> str:
        """生成彩蛋提示"""
        hints = {
            "character": "关注角色的{}时刻",
            "scene": "注意场景中的{}细节",
            "dialogue": "仔细聆听角色的{}台词",
            "item": "寻找{}相关的物品",
            "audio": "留意BGM中的{}元素",
            "visual": "观察画面{}位置"
        }
        
        hint_template = hints.get(egg_type, hints["character"])
        return hint_template.format(reference[:2] if len(reference) > 2 else reference)
    
    def track_discovery(self, egg_id: str, viewer_id: str) -> Dict:
        """追踪彩蛋发现"""
        return {
            "egg_id": egg_id,
            "viewer_id": viewer_id,
            "discovered_at": datetime.now().isoformat(),
            "time_spent": random.randint(10, 300),  # 秒
            "reward": {
                "coins": 50,
                "badge": "彩蛋猎人",
                "unlock": "隐藏剧情"
            }
        }
    
    def generate_egg_quest(self, theme: str, num_eggs: int = 5) -> Dict:
        """生成彩蛋任务"""
        quest = {
            "quest_id": f"quest_{random.randint(1000, 9999)}",
            "theme": theme,
            "name": f"寻找{theme}彩蛋",
            "description": f"在作品中找到{num_eggs}个{theme}相关的彩蛋",
            "eggs": [],
            "rewards": {
                "coins": num_eggs * 100,
                "badge": f"{theme}达人",
                "unlock_content": f"限定{theme}内容"
            },
            "deadline": None,
            "status": "active"
        }
        
        egg_types = list(self.egg_categories.keys())
        for i in range(num_eggs):
            egg_type = random.choice(egg_types)
            egg = self.create_easter_egg(
                egg_type,
                f"{theme}_{i+1}",
                f"第{i+1}章节"
            )
            quest["eggs"].append(egg)
            
        return quest

class UniverseNavigator:
    """宇宙导航器"""
    
    def __init__(self):
        self.explored_content = {}
        self.unlock_requirements = {
            "alternate_universe": {"understanding": 80, "achievements": 5},
            "secret_ending": {"understanding": 95, "easter_eggs": 10},
            "bonus_content": {"understanding": 60, "re_watches": 3}
        }
        
    def track_exploration(self, viewer_id: str, content_id: str, depth: str = "surface") -> Dict:
        """追踪探索深度"""
        if viewer_id not in self.explored_content:
            self.explored_content[viewer_id] = []
            
        exploration = {
            "content_id": content_id,
            "depth": depth,
            "explored_at": datetime.now().isoformat(),
            "time_spent": random.randint(60, 600),
            "interactions": random.randint(5, 20)
        }
        
        self.explored_content[viewer_id].append(exploration)
        
        return {
            "exploration": exploration,
            "unlocked_content": self._check_unlocks(viewer_id)
        }
    
    def _check_unlocks(self, viewer_id: str) -> List[str]:
        """检查解锁内容"""
        unlocked = []
        viewer_content = self.explored_content.get(viewer_id, [])
        
        # 检查解锁条件
        if len(viewer_content) >= 10:
            unlocked.append("隐藏花絮")
        if sum(c.get("interactions", 0) for c in viewer_content) >= 100:
            unlocked.append("导演评论音轨")
        if any(c.get("depth") == "deep" for c in viewer_content):
            unlocked.append("平行结局")
            
        return unlocked
    
    def get_viewer_universe_progress(self, viewer_id: str) -> Dict:
        """获取观众宇宙探索进度"""
        viewer_content = self.explored_content.get(viewer_id, [])
        
        return {
            "viewer_id": viewer_id,
            "total_explored": len(viewer_content),
            "deep_explorations": sum(1 for c in viewer_content if c.get("depth") == "deep"),
            "total_interactions": sum(c.get("interactions", 0) for c in viewer_content),
            "unlocked_content": self._check_unlocks(viewer_id),
            "next_unlock": self._get_next_unlock_requirement(viewer_id)
        }
    
    def _get_next_unlock_requirement(self, viewer_id: str) -> Optional[Dict]:
        """获取下一个解锁条件"""
        viewer_content = self.explored_content.get(viewer_id, [])
        current_count = len(viewer_content)
        
        requirements = [
            {"name": "隐藏花絮", "requirement": 10, "current": current_count},
            {"name": "导演评论音轨", "requirement": 20, "current": current_count},
            {"name": "平行结局", "requirement": 30, "current": current_count}
        ]
        
        for req in requirements:
            if current_count < req["requirement"]:
                return req
                
        return None

def render_ip_universe_tab(st, state):
    """渲染IP宇宙系统页面"""
    st.header("🌌 IP宇宙系统")
    
    # 初始化
    if "ip_universe" not in state:
        state.ip_universe = IPUniverse()
    if "cross_linker" not in state:
        state.cross_linker = CrossWorkLinker()
    if "easter_eggs" not in state:
        state.easter_eggs = EasterEggSystem()
    if "navigator" not in state:
        state.navigator = UniverseNavigator()
    
    # 标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🌍 宇宙构建", "🔗 跨作联动", "🥚 彩蛋系统", "🧭 宇宙导航"])
    
    with tab1:
        render_universe_builder(st, state)
        
    with tab2:
        render_crosswork_linker(st, state)
        
    with tab3:
        render_easter_egg_system(st, state)
        
    with tab4:
        render_universe_navigator(st, state)
    
    return state

def render_universe_builder(st, state):
    """渲染宇宙构建器"""
    universe = state.ip_universe
    
    st.subheader("🌍 IP宇宙构建器")
    
    # 创建宇宙
    st.write("**✨ 创建角色宇宙**")
    
    char_name = st.text_input("角色名称", key="universe_char_name")
    char_genre = st.selectbox(
        "作品类型",
        ["都市", "奇幻", "科幻", "悬疑", "历史"],
        key="universe_char_genre"
    )
    
    if st.button("🚀 创建宇宙", key="create_universe_btn"):
        if char_name:
            character = {"id": random.randint(1, 1000), "name": char_name}
            works = [
                {"title": f"{char_name}的主线故事", "summary": "主线剧情", "main_character": character},
                {"title": f"{char_name}的外传", "summary": "番外故事", "characters": [character]}
            ]
            
            char_universe = universe.create_character_universe(character, works)
            st.session_state.current_universe = char_universe
            st.success(f"✅ {char_name}的IP宇宙已创建！")
    
    # 显示当前宇宙
    if "current_universe" in st.session_state:
        uni = st.session_state.current_universe
        
        st.write("---")
        st.write(f"**🌌 {uni['character_name']}的宇宙**")
        st.write(f"宇宙ID：{uni['universe_id']}")
        
        # 时间线
        with st.expander("📅 时间线"):
            for event in uni["timeline"]:
                st.write(f"**{event['year']}** - {event['title']}")
                st.caption(event['description'])
        
        # 平行版本
        with st.expander("🔄 平行版本"):
            for version in uni["alternate_versions"]:
                st.write(f"**{version['title']}**：{version['description']}")
                st.write(f"特征：{', '.join(version['traits'])}")
                st.caption(f"关键差异：{version['key_difference']}")
        
        # 关联角色
        with st.expander("🤝 关联角色"):
            for conn in uni["connected_characters"]:
                st.write(f"**{conn['character_name']}** ({conn['relationship']})")
                st.caption(f"首次登场：{conn['first_meet']}")

def render_crosswork_linker(st, state):
    """渲染跨作联动"""
    linker = state.cross_linker
    
    st.subheader("🔗 跨作品联动")
    
    # 联动类型
    link_col1, link_col2 = st.columns(2)
    
    with link_col1:
        link_type = st.selectbox(
            "联动类型",
            list(linker.link_templates.keys()),
            format_func=lambda x: linker.link_templates[x]["name"],
            key="link_type_select"
        )
        st.caption(linker.link_templates[link_type]["description"])
        
    with link_col2:
        num_participants = st.slider("参与角色数", 2, 5, 3, key="link_participants")
    
    # 创建联动
    if st.button("🎯 创建联动事件", key="create_link_btn"):
        works = [{"title": f"作品{i}", "main_character": {"id": i, "name": f"角色{i}"}} for i in range(num_participants)]
        event = linker.create_crossover_event(works, link_type)
        st.session_state.current_event = event
        st.success(f"✅ 联动事件已创建！")
    
    # 显示联动事件
    if "current_event" in st.session_state:
        event = st.session_state.current_event
        
        st.write("---")
        st.write(f"**🏆 {event['name']}**")
        st.write(f"类型：{event['type']} | 参与者：{len(event['participants'])}")
        
        # 剧情点
        for point in event["plot_points"]:
            with st.expander(f"📍 {point['title']} ({point['duration']}分钟)"):
                st.write(point['description'])
        
        # 奖励
        with st.expander("🎁 联动奖励"):
            st.write(f"解锁内容：{', '.join(event['rewards']['unlock_content'])}")
            st.write(f"成就：{event['rewards']['achievement']}")

def render_easter_egg_system(st, state):
    """渲染彩蛋系统"""
    eggs = state.easter_eggs
    
    st.subheader("🥚 彩蛋系统")
    
    # 创建彩蛋
    st.write("**✨ 创建彩蛋**")
    
    egg_col1, egg_col2, egg_col3 = st.columns(3)
    
    with egg_col1:
        egg_category = st.selectbox(
            "彩蛋类型",
            list(eggs.egg_categories.keys()),
            format_func=lambda x: eggs.egg_categories[x]["name"],
            key="egg_category_select"
        )
        
    with egg_col2:
        egg_reference = st.text_input("关联内容", key="egg_reference")
        
    with egg_col3:
        egg_difficulty = st.select_slider("难度", ["easy", "medium", "hard"], value="medium")
    
    if st.button("🥚 创建彩蛋", key="create_egg_btn"):
        egg = eggs.create_easter_egg(egg_category, egg_reference, "所有章节")
        st.session_state.current_egg = egg
        st.success("✅ 彩蛋已创建！")
    
    # 显示彩蛋
    if "current_egg" in st.session_state:
        egg = st.session_state.current_egg
        
        st.write("---")
        st.write(f"**🥚 {egg['name']}**")
        st.write(f"类型：{eggs.egg_categories[egg['category']]['name']}")
        st.write(f"难度：{egg['difficulty']} | 发现次数：{egg['discovered_count']}")
        st.write(f"提示：{egg['hint']}")
    
    # 彩蛋任务
    st.write("---")
    st.write("**🎯 彩蛋任务**")
    
    quest = eggs.generate_egg_quest("主线剧情", 5)
    
    if st.button("📜 发起彩蛋任务", key="egg_quest_btn"):
        st.session_state.current_quest = quest
        st.rerun()
    
    if "current_quest" in st.session_state:
        q = st.session_state.current_quest
        
        st.write(f"**{q['name']}**")
        st.write(q['description'])
        st.write(f"奖励：金币{q['rewards']['coins']} | 勋章：{q['rewards']['badge']}")
        
        for egg in q["eggs"]:
            with st.expander(f"🥚 {egg['name']}"):
                st.write(egg['description'])
                st.write(f"难度：{egg['difficulty']}")

def render_universe_navigator(st, state):
    """渲染宇宙导航"""
    nav = state.navigator
    
    st.subheader("🧭 宇宙导航器")
    
    # 查看探索进度
    st.write("**📊 探索进度**")
    
    if st.button("🔍 查看我的进度", key="view_progress_btn"):
        progress = nav.get_viewer_universe_progress("current_user")
        st.session_state.universe_progress = progress
        st.rerun()
    
    if "universe_progress" in st.session_state:
        prog = st.session_state.universe_progress
        
        st.write("**当前进度：**")
        st.write(f"- 已探索内容：{prog['total_explored']}")
        st.write(f"- 深度探索：{prog['deep_explorations']}")
        st.write(f"- 总互动数：{prog['total_interactions']}")
        
        if prog["unlocked_content"]:
            st.success(f"已解锁：{', '.join(prog['unlocked_content'])}")
        
        if prog["next_unlock"]:
            next_req = prog["next_unlock"]
            progress_pct = next_req["current"] / next_req["requirement"] * 100
            st.progress(progress_pct / 100, text=f"解锁「{next_req['name']}」: {next_req['current']}/{next_req['requirement']}")
    
    # 解锁内容
    st.write("---")
    st.write("**🎁 可解锁内容**")
    
    unlocks = [
        {"name": "隐藏花絮", "requirement": "探索10个内容", "unlocked": False},
        {"name": "导演评论音轨", "requirement": "互动100次", "unlocked": False},
        {"name": "平行结局", "requirement": "完成1次深度探索", "unlocked": False},
        {"name": "全部角色故事", "requirement": "解锁全部彩蛋", "unlocked": False}
    ]
    
    for unlock in unlocks:
        status = "✅" if unlock["unlocked"] else "🔒"
        st.write(f"{status} **{unlock['name']}** - {unlock['requirement']}")


# v35: 兼容别名
def render_ip_universe_page():
    """兼容 page 命名约定"""
    import streamlit as st_local
    render_ip_universe_tab(st_local, st_local.session_state)
