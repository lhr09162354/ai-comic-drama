"""
AI剧本改编系统
支持小说、漫画、IP内容转换为剧本格式
"""

import streamlit as st
import json
import re
from datetime import datetime

class ScriptAdaptationSystem:
    """剧本改编系统"""
    
    def __init__(self):
        self.adaptation_types = {
            "小说改编": self._adapt_novel,
            "漫画改编": self._adapt_comic,
            "IP衍生": self._adapt_ip,
            "真实故事": self._adapt_true_story
        }
        self.genres = ["都市", "古言", "玄幻", "悬疑", "科幻", "校园", "职场", "穿越", "甜宠", "虐恋"]
    
    def render(self):
        """渲染改编系统界面"""
        st.subheader("🎬 AI剧本改编系统")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            adaptation_type = st.selectbox(
                "改编类型",
                list(self.adaptation_types.keys()),
                help="选择内容来源类型"
            )
            
            genre = st.selectbox("目标题材", self.genres)
            
            source_content = st.text_area(
                "原始内容",
                height=200,
                placeholder="粘贴小说章节、故事大纲或IP描述...",
                help="输入要改编的原始内容"
            )
        
        with col2:
            target_episodes = st.slider("目标集数", 1, 50, 12)
            
            style = st.selectbox(
                "改编风格",
                ["忠实原著", "适当改编", "大胆创新"]
            )
            
            target_length = st.selectbox(
                "每集时长",
                ["3-5分钟（短剧）", "10-15分钟（短剧）", "45分钟（网剧）"]
            )
        
        if st.button("🚀 开始改编", type="primary"):
            if source_content:
                with st.spinner("AI正在分析并改编剧本..."):
                    result = self._process_adaptation(
                        source_content, 
                        adaptation_type, 
                        genre,
                        target_episodes,
                        style,
                        target_length
                    )
                    self._display_result(result)
            else:
                st.warning("请输入原始内容")
    
    def _process_adaptation(self, content, ad_type, genre, episodes, style, length):
        """处理改编流程"""
        # 提取关键元素
        elements = self._extract_elements(content)
        
        # 生成改编方案
        plan = self._generate_plan(elements, genre, episodes, style)
        
        # 生成剧本大纲
        outline = self._generate_outline(elements, plan, episodes)
        
        # 生成人物设定
        characters = self._extract_characters(elements)
        
        return {
            "type": ad_type,
            "genre": genre,
            "episodes": episodes,
            "style": style,
            "length": length,
            "elements": elements,
            "plan": plan,
            "outline": outline,
            "characters": characters,
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_elements(self, content):
        """提取内容关键元素"""
        # 识别主要人物
        names = re.findall(r'[\u4e00-\u9fa5]{2,4}(?:说|道|问|答|笑|道|叹|怒|惊)', content)
        
        # 识别场景
        scenes = re.findall(r'在(.+?)[，,。]', content)
        
        # 识别情节关键词
        keywords = self._extract_keywords(content)
        
        return {
            "title": self._extract_title(content),
            "main_characters": list(set(names))[:5],
            "scenes": list(set(scenes))[:10],
            "keywords": keywords,
            "tone": self._analyze_tone(content)
        }
    
    def _extract_title(self, content):
        """提取标题"""
        lines = content.strip().split('\n')
        for line in lines[:3]:
            if len(line) <= 20 and len(line) >= 2:
                return line.strip()
        return "未命名作品"
    
    def _extract_keywords(self, content):
        """提取关键词"""
        emotion_words = ["爱", "恨", "情", "仇", "杀", "救", "死", "活", "梦", "醒"]
        theme_words = ["权", "谋", "爱", "恨", "义", "利", "欲", "念"]
        
        emotion_count = sum(content.count(w) for w in emotion_words)
        theme_count = sum(content.count(w) for w in theme_words)
        
        if emotion_count > theme_count:
            return ["情感", "成长", "救赎"]
        else:
            return ["权谋", "复仇", "逆袭"]
    
    def _analyze_tone(self, content):
        """分析内容基调"""
        happy_words = ["甜", "笑", "喜", "欢", "爱"]
        sad_words = ["泪", "哭", "悲", "伤", "痛"]
        tense_words = ["杀", "死", "血", "战", "斗"]
        
        happy = sum(content.count(w) for w in happy_words)
        sad = sum(content.count(w) for w in sad_words)
        tense = sum(content.count(w) for w in tense_words)
        
        if happy > sad and happy > tense:
            return "轻松治愈"
        elif sad > happy:
            return "虐心催泪"
        else:
            return "紧张刺激"
    
    def _generate_plan(self, elements, genre, episodes, style):
        """生成改编方案"""
        plan = {
            "narrative_arc": self._generate_arc(episodes),
            "pacing": self._calculate_pacing(episodes, style),
            "conflict_points": self._generate_conflicts(episodes),
            "emotional_curve": self._generate_emotion_curve(episodes),
            "twist_points": self._generate_twists(episodes, style)
        }
        return plan
    
    def _generate_arc(self, episodes):
        """生成叙事弧线"""
        midpoint = episodes // 2
        return {
            "act1_end": episodes // 4,  # 建置
            "act2_start": episodes // 4,
            "midpoint": midpoint,  # 中点转折
            "act2_end": episodes * 3 // 4,
            "act3_start": episodes * 3 // 4,
            "climax": episodes - 1,
            "resolution": episodes
        }
    
    def _calculate_pacing(self, episodes, style):
        """计算节奏"""
        if style == "忠实原著":
            return {"episodes_per_chapter": 1.5, "scene_density": "中"}
        elif style == "适当改编":
            return {"episodes_per_chapter": 1.2, "scene_density": "中高"}
        else:
            return {"episodes_per_chapter": 1.0, "scene_density": "高"}
    
    def _generate_conflicts(self, episodes):
        """生成冲突点"""
        conflicts = []
        for i in range(min(5, episodes)):
            episode = (i + 1) * episodes // 5
            conflicts.append({
                "episode": episode,
                "type": ["情感冲突", "利益冲突", "身份冲突", "误会冲突"][i % 4],
                "description": f"第{episode}集冲突点"
            })
        return conflicts
    
    def _generate_emotion_curve(self, episodes):
        """生成情感曲线"""
        import math
        curve = []
        for i in range(episodes):
            # 使用正弦函数生成起伏曲线
            value = 50 + 30 * math.sin((i / episodes) * 2 * math.pi)
            curve.append(int(value))
        return curve
    
    def _generate_twists(self, episodes, style):
        """生成反转点"""
        if style == "忠实原著":
            return [{"episode": episodes // 2, "type": "小反转"}]
        elif style == "适当改编":
            return [
                {"episode": episodes // 3, "type": "小反转"},
                {"episode": episodes // 2, "type": "中反转"}
            ]
        else:
            return [
                {"episode": episodes // 4, "type": "小反转"},
                {"episode": episodes // 2, "type": "大反转"},
                {"episode": episodes * 3 // 4, "type": "身份揭露"}
            ]
    
    def _generate_outline(self, elements, plan, episodes):
        """生成剧集大纲"""
        outline = []
        for i in range(episodes):
            episode = i + 1
            
            # 确定本集重点
            if episode == 1:
                focus = "世界观+主角登场"
            elif episode == plan["midpoint"]:
                focus = "中点转折"
            elif episode == plan["climax"]:
                focus = "高潮对决"
            elif episode == plan["resolution"]:
                focus = "圆满收尾"
            else:
                focus = f"情节推进{episode % 3 + 1}"
            
            outline.append({
                "episode": episode,
                "title": f"第{episode}集",
                "focus": focus,
                "duration": "10-15分钟",
                "key_scenes": [f"场景{i+1}", f"场景{i+2}"]
            })
        return outline
    
    def _extract_characters(self, elements):
        """提取人物设定"""
        characters = []
        for i, name in enumerate(elements.get("main_characters", [])[:4]):
            role = ["主角", "配角", "反派", "助攻"][i]
            characters.append({
                "name": name.replace("说", "").replace("道", ""),
                "role": role,
                "archetype": ["英雄", "智者", "恋人", "挑战者"][i],
                "arc": f"{role}成长弧线"
            })
        return characters
    
    def _adapt_novel(self, content, *args):
        """小说改编"""
        return self._process_adaptation(content, "小说改编", *args)
    
    def _adapt_comic(self, content, *args):
        """漫画改编"""
        return self._process_adaptation(content, "漫画改编", *args)
    
    def _adapt_ip(self, content, *args):
        """IP衍生"""
        return self._process_adaptation(content, "IP衍生", *args)
    
    def _adapt_true_story(self, content, *args):
        """真实故事改编"""
        return self._process_adaptation(content, "真实故事改编", *args)
    
    def _display_result(self, result):
        """展示改编结果"""
        st.success("✅ 改编完成！")
        
        # 标签页展示
        tabs = st.tabs(["📋 改编概览", "📖 剧集大纲", "👥 人物设定", "📊 改编方案"])
        
        with tabs[0]:
            st.json({
                "标题": result["elements"]["title"],
                "改编类型": result["type"],
                "目标题材": result["genre"],
                "总集数": result["episodes"],
                "改编风格": result["style"],
                "内容基调": result["elements"]["tone"],
                "核心关键词": result["elements"]["keywords"]
            })
        
        with tabs[1]:
            for ep in result["outline"]:
                with st.expander(f"第{ep['episode']}集: {ep['focus']}"):
                    st.write(f"⏱ {ep['duration']}")
                    st.write(f"🎬 关键场景: {', '.join(ep['key_scenes'])}")
        
        with tabs[2]:
            for char in result["characters"]:
                st.write(f"**{char['name']}** ({char['role']})")
                st.write(f"   人设: {char['archetype']} | {char['arc']}")
        
        with tabs[3]:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**叙事弧线**")
                st.json(result["plan"]["narrative_arc"])
            
            with col2:
                st.write("**节奏方案**")
                st.json(result["plan"]["pacing"])
            
            st.write("**冲突点**")
            st.json(result["plan"]["conflict_points"])
            
            st.write("**反转设计**")
            st.json(result["plan"]["twist_points"])
    
    def export_script(self, result):
        """导出剧本"""
        return json.dumps(result, ensure_ascii=False, indent=2)

def render_adaptation_system():
    """入口函数"""
    system = ScriptAdaptationSystem()
    system.render()
