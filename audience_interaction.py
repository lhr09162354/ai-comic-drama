# -*- coding: utf-8 -*-
"""
观众互动系统 - 投票/分支选择/实时弹幕/观众决策影响剧情
v28 新增功能
"""
import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class AudienceInteractionSystem:
    """观众互动系统"""
    
    def __init__(self):
        # 互动类型
        self.interaction_types = {
            "vote": {
                "name": "剧情投票",
                "icon": "🗳️",
                "description": "让观众投票决定剧情走向"
            },
            "branch": {
                "name": "分支选择",
                "icon": "🔀",
                "description": "观众选择不同的剧情分支"
            },
            "barrage": {
                "name": "实时弹幕",
                "icon": "💬",
                "description": "观众发送实时弹幕评论"
            },
            "prediction": {
                "name": "剧情预测",
                "icon": "🔮",
                "description": "观众预测后续剧情发展"
            },
            "challenge": {
                "name": "互动挑战",
                "icon": "🎯",
                "description": "发起观众参与的挑战任务"
            }
        }
        
        # 投票预设
        self.vote_presets = {
            "character_fate": {
                "name": "角色命运投票",
                "question": "你认为主角应该如何选择？",
                "options": [
                    {"text": "坚守原则", "votes": 0, "percentage": 0},
                    {"text": "灵活变通", "votes": 0, "percentage": 0},
                    {"text": "寻求妥协", "votes": 0, "percentage": 0}
                ],
                "deadline": None
            },
            "plot_direction": {
                "name": "剧情走向投票",
                "question": "你希望剧情如何发展？",
                "options": [
                    {"text": "悲剧收场", "votes": 0, "percentage": 0},
                    {"text": "喜剧收场", "votes": 0, "percentage": 0},
                    {"text": "开放式结局", "votes": 0, "percentage": 0}
                ],
                "deadline": None
            },
            "ship_wars": {
                "name": "CP投票",
                "question": "你支持哪对CP？",
                "options": [
                    {"text": "官配", "votes": 0, "percentage": 0},
                    {"text": "逆CP", "votes": 0, "percentage": 0},
                    {"text": "单身搞事业", "votes": 0, "percentage": 0}
                ],
                "deadline": None
            }
        }
        
        # 弹幕样式
        self.barrage_styles = {
            "top": {"position": "top", "speed": "slow", "color": "#FFFFFF"},
            "center": {"position": "center", "speed": "medium", "color": "#FFD700"},
            "bottom": {"position": "bottom", "speed": "fast", "color": "#00CED1"}
        }
        
    def create_vote(self, preset_key: str, custom_question: str = None) -> Dict:
        """创建投票"""
        preset = self.vote_presets.get(preset_key, self.vote_presets["character_fate"]).copy()
        
        if custom_question:
            preset["question"] = custom_question
            
        # 重置投票
        for option in preset["options"]:
            option["votes"] = 0
            option["percentage"] = 0
            
        return {
            "vote_id": f"vote_{random.randint(1000, 9999)}",
            "preset_key": preset_key,
            "name": preset["name"],
            "question": preset["question"],
            "options": preset["options"],
            "total_votes": 0,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "viewers_participated": 0
        }
    
    def submit_vote(self, vote: Dict, option_index: int) -> Dict:
        """提交投票"""
        if option_index < len(vote["options"]):
            vote["options"][option_index]["votes"] += 1
            vote["total_votes"] += 1
            vote["viewers_participated"] += 1
            
            # 重新计算百分比
            for option in vote["options"]:
                if vote["total_votes"] > 0:
                    option["percentage"] = option["votes"] / vote["total_votes"] * 100
                else:
                    option["percentage"] = 0
                    
        return vote
    
    def create_branch(self, branch_point: Dict) -> List[Dict]:
        """创建分支剧情"""
        branches = []
        
        for i, option in enumerate(branch_point.get("options", [])):
            branch = {
                "branch_id": f"branch_{i+1}",
                "option_text": option.get("text", f"选项{i+1}"),
                "narrative": option.get("narrative", ""),
                "consequences": option.get("consequences", []),
                "selected_count": 0,
                "stats": {
                    "engagement": random.randint(50, 100),
                    "retention": random.uniform(0.6, 0.9)
                }
            }
            branches.append(branch)
            
        return branches
    
    def generate_barrage(self, text: str, user: str = "匿名用户") -> Dict:
        """生成弹幕"""
        style_key = random.choice(list(self.barrage_styles.keys()))
        style = self.barrage_styles[style_key]
        
        return {
            "barrage_id": f"barrage_{random.randint(10000, 99999)}",
            "user": user,
            "text": text,
            "position": style["position"],
            "speed": style["speed"],
            "color": style["color"],
            "timestamp": datetime.now().isoformat(),
            "likes": random.randint(0, 100),
            "is_highlighted": random.random() > 0.9
        }
    
    def create_prediction(self, prediction_type: str) -> Dict:
        """创建剧情预测"""
        prediction_templates = {
            "killer": {
                "question": "谁是真正的幕后黑手？",
                "options": ["角色A", "角色B", "角色C", "另有其人"]
            },
            "ending": {
                "question": "故事会如何结局？",
                "options": ["大团圆", "悲剧", "开放式", "反转"]
            },
            "relationship": {
                "question": "角色之间的关系会如何发展？",
                "options": ["在一起", "错过", "敌对", "成长"]
            }
        }
        
        template = prediction_templates.get(prediction_type, prediction_templates["ending"])
        
        return {
            "prediction_id": f"pred_{random.randint(1000, 9999)}",
            "type": prediction_type,
            "question": template["question"],
            "options": [{"text": opt, "count": 0} for opt in template["options"]],
            "participants": 0,
            "correct_answer": None,
            "status": "active"
        }
    
    def create_challenge(self, challenge_type: str) -> Dict:
        """创建互动挑战"""
        challenges = {
            "caption": {
                "name": "弹幕配台词",
                "description": "为图片配上搞笑或感人的台词",
                "rewards": {"coins": 50, "badges": ["脑洞达人"]}
            },
            "story_continue": {
                "name": "剧情接龙",
                "description": "续写接下来的剧情发展",
                "rewards": {"coins": 100, "badges": ["故事大王"]}
            },
            "character_photo": {
                "name": "角色cosplay",
                "description": "上传角色cosplay照片",
                "rewards": {"coins": 200, "badges": ["cos之星"]}
            },
            "meme": {
                "name": "表情包创作",
                "description": "创作剧中角色的表情包",
                "rewards": {"coins": 80, "badges": ["斗图大师"]}
            }
        }
        
        challenge = challenges.get(challenge_type, challenges["caption"])
        
        return {
            "challenge_id": f"chal_{random.randint(1000, 9999)}",
            "type": challenge_type,
            "name": challenge["name"],
            "description": challenge["description"],
            "rewards": challenge["rewards"],
            "submissions": [],
            "top_submissions": [],
            "deadline": None,
            "status": "active"
        }


class ViewerDecisionTracker:
    """观众决策追踪"""
    
    def __init__(self):
        self.decisions = {}
        self.decision_history = []
        
    def record_decision(self, viewer_id: str, decision: Dict) -> None:
        """记录观众决策"""
        if viewer_id not in self.decisions:
            self.decisions[viewer_id] = []
            
        decision_entry = {
            "decision_id": f"dec_{len(self.decision_history)}",
            "timestamp": datetime.now().isoformat(),
            **decision
        }
        
        self.decisions[viewer_id].append(decision_entry)
        self.decision_history.append(decision_entry)
        
    def get_viewer_profile(self, viewer_id: str) -> Dict:
        """获取观众画像"""
        viewer_decisions = self.decisions.get(viewer_id, [])
        
        return {
            "viewer_id": viewer_id,
            "total_decisions": len(viewer_decisions),
            "participation_rate": len(viewer_decisions) / max(1, len(self.decision_history)) * 100,
            "preferred_choices": self._analyze_preferences(viewer_decisions),
            "engagement_level": self._calculate_engagement(viewer_decisions),
            "influence_score": len(viewer_decisions) * 10
        }
    
    def _analyze_preferences(self, decisions: List[Dict]) -> Dict:
        """分析观众偏好"""
        choices = [d.get("choice") for d in decisions]
        
        return {
            "most_common_choice": max(set(choices), default="未选择") if choices else "未选择",
            "choice_diversity": len(set(choices)),
            "risk_taking": random.uniform(0.3, 0.8)  # 简化计算
        }
    
    def _calculate_engagement(self, decisions: List[Dict]) -> str:
        """计算参与度"""
        count = len(decisions)
        if count >= 20:
            return "超级粉丝"
        elif count >= 10:
            return "活跃观众"
        elif count >= 5:
            return "普通观众"
        else:
            return "轻度观众"
    
    def get_plot_impact(self) -> Dict:
        """获取剧情影响统计"""
        total_decisions = len(self.decision_history)
        
        choice_counts = {}
        for decision in self.decision_history:
            choice = decision.get("choice", "unknown")
            choice_counts[choice] = choice_counts.get(choice, 0) + 1
            
        return {
            "total_decisions": total_decisions,
            "choice_distribution": choice_counts,
            "most_popular_choice": max(choice_counts.items(), key=lambda x: x[1])[0] if choice_counts else None,
            "engagement_rate": min(total_decisions / 100, 1.0) * 100
        }


class InteractiveStoryEngine:
    """互动剧情引擎"""
    
    def __init__(self):
        self.story_branches = {}
        self.branch_history = []
        
    def create_interactive_story(self, base_story: Dict, num_branches: int = 3) -> Dict:
        """创建互动剧情"""
        story = {
            "story_id": f"story_{random.randint(1000, 9999)}",
            "title": base_story.get("title", "互动故事"),
            "chapters": [],
            "total_branches": 0,
            "viewers参与": 0
        }
        
        # 为每个章节创建分支点
        for chapter in base_story.get("chapters", [])[:5]:
            branch_point = self._create_branch_point(chapter, num_branches)
            story["chapters"].append(branch_point)
            story["total_branches"] += len(branch_point["options"])
            
        return story
    
    def _create_branch_point(self, chapter: Dict, num_options: int) -> Dict:
        """创建分支点"""
        branch_point = {
            "chapter_num": chapter.get("chapter_num", 1),
            "chapter_title": chapter.get("chapter_title", ""),
            "branch_point_id": f"bp_{random.randint(1000, 9999)}",
            "description": "主角面临一个重要选择...",
            "options": [],
            "result_narrative": {}
        }
        
        option_templates = [
            {"text": "勇敢面对", "consequence": "获得成长，但付出代价"},
            {"text": "谨慎行事", "consequence": "更安全，但可能错过机会"},
            {"text": "寻求帮助", "consequence": "建立关系，获得支持"},
            {"text": "另辟蹊径", "consequence": "创新方案，结果不确定"}
        ]
        
        for i in range(min(num_options, len(option_templates))):
            template = option_templates[i]
            branch = {
                "option_id": f"opt_{i+1}",
                "text": template["text"],
                "consequence": template["consequence"],
                "selected_count": random.randint(10, 100),
                "leading_to": f"chapter_{random.randint(1, 10)}",
                "stats": {
                    "excitement": random.uniform(0.7, 1.0),
                    "safety": random.uniform(0.5, 0.9),
                    "romance": random.uniform(0.2, 0.8)
                }
            }
            branch_point["options"].append(branch)
            
        return branch_point
    
    def calculate_popular_path(self, story_id: str) -> List[str]:
        """计算最受欢迎路径"""
        popular_path = []
        
        for branch_point in self.story_branches.get(story_id, {}).get("chapters", []):
            # 找出选择最多的选项
            options = branch_point.get("options", [])
            if options:
                most_popular = max(options, key=lambda x: x.get("selected_count", 0))
                popular_path.append(most_popular.get("text", ""))
                
        return popular_path
    
    def generate_branch_statistics(self, branch_point: Dict) -> Dict:
        """生成分支统计"""
        options = branch_point.get("options", [])
        total_selections = sum(opt.get("selected_count", 0) for opt in options)
        
        stats = {
            "total_selections": total_selections,
            "options": []
        }
        
        for opt in options:
            count = opt.get("selected_count", 0)
            percentage = count / total_selections * 100 if total_selections > 0 else 0
            
            stats["options"].append({
                "text": opt.get("text", ""),
                "count": count,
                "percentage": percentage,
                "result_preview": opt.get("consequence", "")
            })
            
        # 排序
        stats["options"].sort(key=lambda x: x["count"], reverse=True)
        
        return stats


def render_interaction_system_tab(st, state):
    """渲染观众互动系统页面"""
    st.header("💬 观众互动系统")
    
    # 初始化
    if "interaction_system" not in state:
        state.interaction_system = AudienceInteractionSystem()
    if "decision_tracker" not in state:
        state.decision_tracker = ViewerDecisionTracker()
    if "interactive_engine" not in state:
        state.interactive_engine = InteractiveStoryEngine()
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗳️ 投票", "🔀 分支", "💬 弹幕", "🔮 预测", "🎯 挑战"
    ])
    
    with tab1:
        render_vote_system(st, state)
        
    with tab2:
        render_branch_system(st, state)
        
    with tab3:
        render_barrage_system(st, state)
        
    with tab4:
        render_prediction_system(st, state)
        
    with tab5:
        render_challenge_system(st, state)
    
    return state


def render_vote_system(st, state):
    """渲染投票系统"""
    system = state.interaction_system
    
    st.subheader("🗳️ 剧情投票")
    
    # 创建投票
    st.write("**✨ 创建新投票**")
    
    vote_col1, vote_col2 = st.columns(2)
    
    with vote_col1:
        vote_type = st.selectbox(
            "投票类型",
            list(system.vote_presets.keys()),
            format_func=lambda x: system.vote_presets[x]["name"],
            key="vote_type_select"
        )
        
    with vote_col2:
        custom_question = st.text_input("自定义问题（可选）", key="vote_custom_question")
    
    if st.button("🚀 创建投票", key="create_vote_btn"):
        vote = system.create_vote(vote_type, custom_question if custom_question else None)
        st.session_state.current_vote = vote
        st.success(f"✅ 投票已创建！ID: {vote['vote_id']}")
    
    # 显示当前投票
    if "current_vote" in st.session_state:
        vote = st.session_state.current_vote
        
        st.write("---")
        st.write(f"**📋 {vote['name']}**")
        st.write(f"问题：{vote['question']}")
        st.write(f"状态：{vote['status']} | 总投票：{vote['total_votes']}")
        
        # 投票选项
        for i, option in enumerate(vote["options"]):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                progress = option["percentage"]
                st.progress(progress / 100, text=f"{option['text']} ({option['votes']}票, {option['percentage']:.1f}%)")
                
            with col2:
                if st.button("投票", key=f"vote_opt_{i}"):
                    vote = system.submit_vote(vote, i)
                    st.session_state.current_vote = vote
                    st.rerun()
    
    # 历史投票
    st.write("---")
    st.write("**📜 历史投票**")
    
    presets = list(system.vote_presets.keys())
    for preset_key in presets[:3]:
        preset = system.vote_presets[preset_key]
        with st.expander(f"📊 {preset['name']}"):
            st.write(f"问题：{preset['question']}")
            for opt in preset["options"]:
                st.write(f"- {opt['text']}")


def render_branch_system(st, state):
    """渲染分支系统"""
    engine = state.interactive_engine
    
    st.subheader("🔀 分支剧情")
    
    # 创建互动故事
    st.write("**🎬 创建互动剧情**")
    
    story_title = st.text_input("故事标题", "我的互动漫剧", key="branch_story_title")
    num_branches = st.slider("每个节点选项数", 2, 4, 3, key="branch_count_slider")
    
    if st.button("✨ 生成互动剧情", key="generate_branch_btn"):
        base_story = {
            "title": story_title,
            "chapters": [
                {"chapter_num": i, "chapter_title": f"第{i}章"}
                for i in range(1, 6)
            ]
        }
        
        story = engine.create_interactive_story(base_story, num_branches)
        st.session_state.interactive_story = story
        st.success(f"✅ 互动剧情已生成！共 {story['total_branches']} 个分支")
    
    # 显示分支剧情
    if "interactive_story" in st.session_state:
        story = st.session_state.interactive_story
        
        st.write("---")
        st.write(f"**📖 {story['title']}**")
        st.write(f"分支数：{story['total_branches']} | 参与观众：{story['viewers参与']}")
        
        for chapter in story["chapters"]:
            with st.expander(f"📕 第{chapter['chapter_num']}章：{chapter['branch_point_id']}"):
                st.write(f"**分支点描述：** {chapter['description']}")
                
                # 显示选项
                stats = engine.generate_branch_statistics(chapter)
                st.write(f"**总选择数：** {stats['total_selections']}")
                
                for opt in stats["options"]:
                    st.write(f"\n📌 **{opt['text']}** ({opt['count']}票, {opt['percentage']:.1f}%)")
                    st.write(f"   后果：{opt['result_preview']}")


def render_barrage_system(st, state):
    """渲染弹幕系统"""
    system = state.interaction_system
    
    st.subheader("💬 实时弹幕")
    
    # 弹幕样式
    style_col1, style_col2 = st.columns(2)
    
    with style_col1:
        barrage_position = st.selectbox(
            "弹幕位置",
            ["top", "center", "bottom"],
            format_func=lambda x: {"top": "顶部", "center": "中部", "bottom": "底部"}.get(x, x),
            key="barrage_position"
        )
        
    with style_col2:
        barrage_color = st.color_picker("弹幕颜色", "#FFFFFF", key="barrage_color")
    
    # 发送弹幕
    st.write("**✏️ 发送弹幕**")
    
    barrage_col1, barrage_col2 = st.columns([4, 1])
    
    with barrage_col1:
        barrage_text = st.text_input("弹幕内容", placeholder="说点什么...", key="barrage_text_input")
        
    with barrage_col2:
        st.write("")  # 占位
        if st.button("🚀 发送", key="send_barrage_btn"):
            if barrage_text:
                barrage = system.generate_barrage(barrage_text)
                st.session_state.barrages = st.session_state.get("barrages", [])
                st.session_state.barrages.append(barrage)
                st.success("弹幕已发送！")
    
    # 显示弹幕
    st.write("---")
    st.write("**📺 弹幕预览**")
    
    barrages = st.session_state.get("barrages", [])
    
    if barrages:
        # 模拟弹幕滚动效果
        for barrage in barrages[-10:]:
            emoji = "🎬" if barrage["is_highlighted"] else "💭"
            st.markdown(f"<span style='color:{barrage['color']}'>{emoji} {barrage['user']}: {barrage['text']}</span>", unsafe_allow_html=True)
    else:
        st.info("暂无弹幕，快来发送第一条吧！")
    
    # 弹幕模板
    st.write("---")
    st.write("**💡 快速弹幕**")
    
    templates = [
        "太精彩了！", "哈哈哈", "这是什么神剧情",
        "心疼角色", "催更催更！", "磕到了磕到了"
    ]
    
    for i in range(0, len(templates), 3):
        cols = st.columns(3)
        for j, template in enumerate(templates[i:i+3]):
            with cols[j]:
                if st.button(template, key=f"template_{i+j}"):
                    barrage = system.generate_barrage(template)
                    st.session_state.barrages = st.session_state.get("barrages", [])
                    st.session_state.barrages.append(barrage)
                    st.rerun()


def render_prediction_system(st, state):
    """渲染预测系统"""
    system = state.interaction_system
    
    st.subheader("🔮 剧情预测")
    
    # 创建预测
    st.write("**✨ 创建预测**")
    
    pred_col1, pred_col2 = st.columns(2)
    
    with pred_col1:
        pred_type = st.selectbox(
            "预测类型",
            ["killer", "ending", "relationship"],
            format_func=lambda x: {"killer": "谁是凶手", "ending": "结局预测", "relationship": "感情走向"}.get(x, x),
            key="pred_type_select"
        )
        
    with pred_col2:
        include_rewards = st.checkbox("设置奖励", True, key="pred_rewards")
    
    if st.button("🎯 创建预测", key="create_pred_btn"):
        prediction = system.create_prediction(pred_type)
        st.session_state.current_prediction = prediction
        st.success(f"✅ 预测已创建！")
    
    # 显示当前预测
    if "current_prediction" in st.session_state:
        pred = st.session_state.current_prediction
        
        st.write("---")
        st.write(f"**📋 {pred['question']}**")
        st.write(f"参与人数：{pred['participants']} | 状态：{pred['status']}")
        
        for i, option in enumerate(pred["options"]):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                percentage = option["count"] / max(1, pred["participants"]) * 100 if pred["participants"] > 0 else 0
                st.progress(percentage / 100, text=f"{option['text']} ({option['count']}票)")
                
            with col2:
                if st.button("预测", key=f"pred_opt_{i}"):
                    option["count"] += 1
                    pred["participants"] += 1
                    st.rerun()
    
    # 历史预测
    st.write("---")
    st.write("**📜 历史预测结果**")
    
    past_predictions = [
        {"question": "谁是幕后黑手？", "answer": "角色A", "accuracy": 85},
        {"question": "故事结局是？", "answer": "大团圆", "accuracy": 92}
    ]
    
    for pred in past_predictions:
        with st.expander(f"✅ {pred['question']}"):
            st.write(f"正确答案：{pred['answer']}")
            st.write(f"预测准确率：{pred['accuracy']}%")


def render_challenge_system(st, state):
    """渲染挑战系统"""
    system = state.interaction_system
    
    st.subheader("🎯 互动挑战")
    
    # 可用挑战
    challenges = ["caption", "story_continue", "character_photo", "meme"]
    challenge_names = ["弹幕配台词", "剧情接龙", "角色cosplay", "表情包创作"]
    
    challenge_col1, challenge_col2 = st.columns(2)
    
    for i, (challenge, name) in enumerate(zip(challenges, challenge_names)):
        with challenge_col1 if i % 2 == 0 else challenge_col2:
            if st.button(f"🎮 {name}", key=f"challenge_btn_{i}"):
                challenge_data = system.create_challenge(challenge)
                st.session_state.current_challenge = challenge_data
                st.rerun()
    
    # 当前挑战
    if "current_challenge" in st.session_state:
        challenge = st.session_state.current_challenge
        
        st.write("---")
        st.write(f"**🏆 {challenge['name']}**")
        st.write(f"描述：{challenge['description']}")
        st.write(f"奖励：金币{challenge['rewards']['coins']} | 勋章：{challenge['rewards']['badges'][0]}")
        
        # 参与挑战
        submission = st.text_area("提交作品", height=100, key="challenge_submission")
        
        if st.button("📤 提交", key="submit_challenge_btn"):
            if submission:
                challenge["submissions"].append({
                    "user": "当前用户",
                    "content": submission,
                    "timestamp": datetime.now().isoformat()
                })
                st.success("✅ 作品已提交！")
    
    # 挑战榜单
    st.write("---")
    st.write("**🏅 挑战榜单**")
    
    leaderboard = [
        {"rank": 1, "user": "漫剧达人", "score": 1500, "badges": ["脑洞达人", "故事大王"]},
        {"rank": 2, "user": "追剧狂人", "score": 1200, "badges": ["cos之星"]},
        {"rank": 3, "user": "弹幕教主", "score": 1000, "badges": ["斗图大师"]}
    ]
    
    for entry in leaderboard:
        st.write(f"**#{entry['rank']} {entry['user']}** | 积分：{entry['score']}")
        st.write(f"勋章：{', '.join(entry['badges'])}")


# v35: 兼容别名
def render_audience_interaction_page():
    """兼容 page 命名约定"""
    import streamlit as st_local
    render_interaction_system_tab(st_local, st_local.session_state)
