"""
互动剧情引擎
观众投票决策，剧情走向由粉丝决定
"""
import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random

class InteractiveStoryEngine:
    """互动剧情引擎"""
    
    def __init__(self):
        self.story_modes = self._init_story_modes()
        self.vote_systems = self._init_vote_systems()
        
    def _init_story_modes(self) -> Dict:
        """初始化剧情模式"""
        return {
            "branching": {
                "name": "分支剧情",
                "description": "观众投票决定剧情走向",
                "icon": "🔀",
                "max_branches": 5
            },
            "multiple_ending": {
                "name": "多结局",
                "description": "根据累计选择解锁不同结局",
                "icon": "🎭",
                "endings": ["Happy", "BitterSweet", "Tragic", "Secret"]
            },
            "live_voting": {
                "name": "实时投票",
                "description": "直播过程中观众实时投票",
                "icon": "📺",
                "vote_interval": 30  # 秒
            },
            "weekly_decision": {
                "name": "周更决策",
                "description": "每周更新前投票决定下集内容",
                "icon": "📅",
                "vote_duration": 72  # 小时
            }
        }
    
    def _init_vote_systems(self) -> Dict:
        """初始化投票系统"""
        return {
            "single_choice": {
                "name": "单选投票",
                "description": "观众选择一个选项"
            },
            "rank_choice": {
                "name": "排序投票",
                "description": "观众对选项排序"
            },
            "score_voting": {
                "name": "评分投票",
                "description": "观众给选项打分 1-10"
            }
        }
    
    def create_branch_point(
        self,
        scene_id: str,
        description: str,
        options: List[Dict],
        vote_system: str = "single_choice"
    ) -> Dict:
        """创建分支节点"""
        return {
            "id": scene_id,
            "type": "branch_point",
            "description": description,
            "options": options,
            "vote_system": vote_system,
            "votes": {opt["id"]: 0 for opt in options},
            "created_at": datetime.now().isoformat()
        }
    
    def cast_vote(
        self,
        branch_id: str,
        option_id: str,
        user_id: str
    ) -> bool:
        """投票"""
        # 模拟投票
        return True
    
    def get_vote_results(self, branch_id: str) -> Dict:
        """获取投票结果"""
        total = random.randint(100, 1000)
        
        results = {}
        for i in range(4):
            votes = random.randint(10, total // 4)
            results[f"option_{i+1}"] = {
                "votes": votes,
                "percentage": f"{votes / total * 100:.1f}%"
            }
        
        return {
            "total_votes": total,
            "results": results,
            "leading_option": max(results, key=lambda x: results[x]["votes"]),
            "end_time": None
        }
    
    def calculate_narrative_impact(
        self,
        choice: Dict,
        character_states: Dict
    ) -> Dict:
        """计算选择对角色的影响"""
        impacts = {
            "relationship_change": random.uniform(-0.2, 0.3),
            "plot_progression": random.randint(5, 20),
            "mood_shift": random.choice(["lighter", "darker", "neutral"]),
            "foreshadowing": random.random() > 0.7
        }
        
        return impacts


class AudienceDecisionSystem:
    """观众决策系统"""
    
    def __init__(self):
        self.decisions = []
        self.decision_history = {}
        
    def create_decision_scene(
        self,
        title: str,
        context: str,
        choices: List[Dict]
    ) -> Dict:
        """创建决策场景"""
        decision_id = f"decision_{len(self.decisions) + 1}"
        
        decision = {
            "id": decision_id,
            "title": title,
            "context": context,
            "choices": choices,
            "participation": 0,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.decisions.append(decision)
        return decision
    
    def record_decision(
        self,
        decision_id: str,
        user_id: str,
        choice_id: str,
        reasoning: str = ""
    ) -> bool:
        """记录观众决策"""
        if decision_id not in self.decision_history:
            self.decision_history[decision_id] = []
        
        self.decision_history[decision_id].append({
            "user_id": user_id,
            "choice_id": choice_id,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        })
        
        # 更新参与度
        for d in self.decisions:
            if d["id"] == decision_id:
                d["participation"] += 1
                break
        
        return True
    
    def get_audience_preference(self) -> Dict:
        """分析观众偏好"""
        return {
            "favorite_genre": random.choice(["都市", "校园", "玄幻", "悬疑"]),
            "preferred_ending": random.choice(["甜", "虐", "悬疑", "反转"]),
            "pace_preference": random.choice(["快节奏", "慢热", "适中"]),
            "interaction_style": random.choice(["投票", "打赏解锁", "弹幕互动"])
        }


class LiveInteractionManager:
    """直播互动管理器"""
    
    def __init__(self):
        self.active_sessions = {}
        
    def start_live_session(
        self,
        story_id: str,
        duration: int = 3600
    ) -> Dict:
        """开始直播互动"""
        session_id = f"live_{story_id}_{int(datetime.now().timestamp())}"
        
        session = {
            "id": session_id,
            "story_id": story_id,
            "status": "live",
            "start_time": datetime.now().isoformat(),
            "duration": duration,
            "viewers": random.randint(500, 5000),
            "interactions": 0,
            "polls": [],
            "gifts": []
        }
        
        self.active_sessions[session_id] = session
        return session
    
    def create_live_poll(
        self,
        session_id: str,
        question: str,
        options: List[str],
        duration: int = 60
    ) -> Dict:
        """创建直播投票"""
        poll_id = f"poll_{len(self.active_sessions.get(session_id, {}).get('polls', [])) + 1}"
        
        poll = {
            "id": poll_id,
            "question": question,
            "options": [{"id": f"opt_{i}", "text": opt, "votes": 0} for i, opt in enumerate(options)],
            "duration": duration,
            "votes": 0,
            "created_at": datetime.now().isoformat()
        }
        
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["polls"].append(poll)
        
        return poll
    
    def submit_poll_vote(
        self,
        poll_id: str,
        option_id: str,
        user_id: str
    ) -> bool:
        """提交投票"""
        for session in self.active_sessions.values():
            for poll in session["polls"]:
                if poll["id"] == poll_id:
                    for opt in poll["options"]:
                        if opt["id"] == option_id:
                            opt["votes"] += 1
                            poll["votes"] += 1
                            return True
        return False
    
    def receive_gift(
        self,
        session_id: str,
        gift_type: str,
        user_id: str,
        quantity: int = 1
    ) -> Dict:
        """收到礼物"""
        gift_value = {
            "flower": 1,
            "heart": 5,
            "rocket": 50,
            "castle": 500
        }
        
        gift_record = {
            "user_id": user_id,
            "type": gift_type,
            "quantity": quantity,
            "value": gift_value.get(gift_type, 1) * quantity,
            "timestamp": datetime.now().isoformat()
        }
        
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["gifts"].append(gift_record)
        
        return gift_record


class ChoiceConsequenceTracker:
    """选择后果追踪器"""
    
    def __init__(self):
        self.consequence_map = {}
        
    def track_choice(
        self,
        user_id: str,
        story_id: str,
        choice_id: str,
        consequences: Dict
    ):
        """追踪选择后果"""
        key = f"{user_id}_{story_id}"
        
        if key not in self.consequence_map:
            self.consequence_map[key] = {
                "user_id": user_id,
                "story_id": story_id,
                "choices": [],
                "character_states": {},
                "relationship_states": {},
                "flags": []
            }
        
        self.consequence_map[key]["choices"].append({
            "choice_id": choice_id,
            "consequences": consequences,
            "timestamp": datetime.now().isoformat()
        })
        
        # 更新角色状态
        if "character_changes" in consequences:
            self.consequence_map[key]["character_states"].update(
                consequences["character_changes"]
            )
        
        # 设置剧情标记
        if "plot_flags" in consequences:
            self.consequence_map[key]["flags"].extend(consequences["plot_flags"])
    
    def get_story_state(self, user_id: str, story_id: str) -> Dict:
        """获取故事状态"""
        key = f"{user_id}_{story_id}"
        
        if key not in self.consequence_map:
            return {
                "choices_made": 0,
                "character_states": {},
                "relationship_states": {},
                "flags": []
            }
        
        return self.consequence_map[key]
    
    def calculate_ending_eligibility(self, user_id: str, story_id: str) -> List[str]:
        """计算可解锁结局"""
        state = self.get_story_state(user_id, story_id)
        
        eligible_endings = []
        
        # 根据标记判断结局
        flags = state.get("flags", [])
        
        if "heroic" in flags:
            eligible_endings.append("Heroic")
        if "romantic" in flags:
            eligible_endings.append("Romantic")
        if "tragic" in flags:
            eligible_endings.append("Tragic")
        if "secret_found" in flags:
            eligible_endings.append("Secret")
        
        return eligible_endings


class CommunityPredictionGame:
    """社区预测游戏"""
    
    def __init__(self):
        self.predictions = []
        
    def create_prediction(
        self,
        story_id: str,
        question: str,
        options: List[Dict],
        deadline: str
    ) -> Dict:
        """创建预测"""
        prediction_id = f"pred_{len(self.predictions) + 1}"
        
        prediction = {
            "id": prediction_id,
            "story_id": story_id,
            "question": question,
            "options": options,
            "deadline": deadline,
            "participants": 0,
            "bets": {},
            "status": "open"
        }
        
        self.predictions.append(prediction)
        return prediction
    
    def place_bet(
        self,
        prediction_id: str,
        user_id: str,
        option_id: str,
        points: int = 100
    ) -> bool:
        """下注"""
        for pred in self.predictions:
            if pred["id"] == prediction_id:
                pred["participants"] += 1
                pred["bets"][user_id] = {
                    "option_id": option_id,
                    "points": points,
                    "timestamp": datetime.now().isoformat()
                }
                return True
        return False
    
    def resolve_prediction(
        self,
        prediction_id: str,
        winning_option_id: str
    ) -> Dict:
        """结算预测"""
        for pred in self.predictions:
            if pred["id"] == prediction_id:
                pred["status"] = "resolved"
                pred["winning_option"] = winning_option_id
                
                # 计算奖励
                rewards = {}
                for user_id, bet in pred["bets"].items():
                    if bet["option_id"] == winning_option_id:
                        rewards[user_id] = bet["points"] * 2  # 猜中获得双倍
                
                return {
                    "prediction_id": prediction_id,
                    "winners": list(rewards.keys()),
                    "rewards": rewards,
                    "total_participants": pred["participants"]
                }
        
        return {}


def render_interactive_story_page():
    """渲染互动剧情页面"""
    st.title("🎭 互动剧情引擎")
    
    # 初始化
    if "story_engine" not in st.session_state:
        st.session_state.story_engine = InteractiveStoryEngine()
    
    if "decision_system" not in st.session_state:
        st.session_state.decision_system = AudienceDecisionSystem()
    
    if "live_manager" not in st.session_state:
        st.session_state.live_manager = LiveInteractionManager()
    
    if "choice_tracker" not in st.session_state:
        st.session_state.choice_tracker = ChoiceConsequenceTracker()
    
    if "prediction_game" not in st.session_state:
        st.session_state.prediction_game = CommunityPredictionGame()
    
    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔀 分支剧情", "📺 直播互动", "🎮 观众决策", "📊 预测游戏", "📈 数据分析"
    ])
    
    with tab1:
        st.subheader("🔀 分支剧情创作")
        
        # 剧情模式选择
        mode = st.selectbox(
            "选择剧情模式",
            list(st.session_state.story_engine.story_modes.keys()),
            format_func=lambda x: f"{st.session_state.story_engine.story_modes[x]['icon']} {st.session_state.story_engine.story_modes[x]['name']}"
        )
        
        mode_info = st.session_state.story_engine.story_modes[mode]
        st.info(f"**{mode_info['name']}**: {mode_info['description']}")
        
        # 创建分支节点
        with st.expander("➕ 创建分支节点", expanded=True):
            scene_id = st.text_input("场景ID", value=f"scene_{random.randint(1000, 9999)}")
            description = st.text_area("场景描述")
            
            st.write("**选项设置:**")
            options = []
            
            for i in range(3):
                col1, col2 = st.columns([3, 1])
                with col1:
                    opt_text = st.text_input(f"选项{i+1}", key=f"opt_{i}")
                with col2:
                    opt_weight = st.number_input("权重", 1, 10, 5, key=f"weight_{i}")
                
                if opt_text:
                    options.append({
                        "id": f"option_{i+1}",
                        "text": opt_text,
                        "weight": opt_weight
                    })
            
            vote_system = st.selectbox(
                "投票系统",
                list(st.session_state.story_engine.vote_systems.keys()),
                format_func=lambda x: st.session_state.story_engine.vote_systems[x]["name"]
            )
            
            if st.button("创建分支", type="primary"):
                if description and len(options) >= 2:
                    branch = st.session_state.story_engine.create_branch_point(
                        scene_id, description, options, vote_system
                    )
                    st.success(f"✅ 分支节点创建成功: {branch['id']}")
                    
                    # 显示预览
                    st.write("**预览:**")
                    st.write(f"📍 {description}")
                    for opt in options:
                        st.write(f"  • {opt['text']} (权重: {opt['weight']})")
                else:
                    st.warning("请填写场景描述和至少2个选项")
        
        # 现有分支
        st.divider()
        st.write("**📋 分支节点管理**")
        
        # 模拟已有分支
        sample_branches = [
            {
                "id": "scene_001",
                "description": "主角面临重大选择",
                "options": [
                    {"text": "接受任务", "votes": 156},
                    {"text": "拒绝并离开", "votes": 89},
                    {"text": "提出条件", "votes": 203}
                ]
            }
        ]
        
        for branch in sample_branches:
            with st.expander(f"📍 {branch['id']}"):
                st.write(f"**场景:** {branch['description']}")
                
                # 投票结果
                total = sum(opt["votes"] for opt in branch["options"])
                for opt in branch["options"]:
                    pct = opt["votes"] / total * 100 if total > 0 else 0
                    st.write(f"• {opt['text']}: {opt['votes']}票 ({pct:.1f}%)")
                    st.progress(pct / 100)
                
                if st.button("查看详情", key=f"view_{branch['id']}"):
                    st.json(branch)
    
    with tab2:
        st.subheader("📺 直播互动")
        
        # 开始直播
        with st.expander("🚀 开始直播会话", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                story_id = st.text_input("作品ID")
                duration = st.number_input("直播时长(分钟)", 30, 180, 60)
            
            with col2:
                auto_poll = st.checkbox("自动创建投票")
                gift_enabled = st.checkbox("启用礼物系统", value=True)
            
            if st.button("开始直播", type="primary"):
                session = st.session_state.live_manager.start_live_session(
                    story_id or "demo_story",
                    duration * 60
                )
                st.success(f"✅ 直播开始! Session: {session['id']}")
                st.info(f"👥 当前观众: {session['viewers']}")
        
        # 直播控制
        st.divider()
        
        if st.session_state.live_manager.active_sessions:
            session_id = list(st.session_state.live_manager.active_sessions.keys())[0]
            session = st.session_state.live_manager.active_sessions[session_id]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 观众", session["viewers"])
            
            with col2:
                st.metric("💬 互动", session["interactions"])
            
            with col3:
                st.metric("🎁 礼物", len(session["gifts"]))
            
            # 创建投票
            with st.expander("📊 创建投票"):
                question = st.text_input("问题")
                options = []
                
                opt1 = st.text_input("选项1")
                opt2 = st.text_input("选项2")
                opt3 = st.text_input("选项3(可选)")
                
                if opt1:
                    options.append(opt1)
                if opt2:
                    options.append(opt2)
                if opt3:
                    options.append(opt3)
                
                poll_duration = st.slider("投票时长(秒)", 10, 120, 60)
                
                if st.button("发起投票"):
                    if question and len(options) >= 2:
                        poll = st.session_state.live_manager.create_live_poll(
                            session_id, question, options, poll_duration
                        )
                        st.success(f"✅ 投票创建成功")
                        st.json(poll)
                    else:
                        st.warning("请填写问题至少2个选项")
            
            # 礼物系统
            if gift_enabled:
                st.write("**🎁 礼物系统**")
                
                col1, col2, col3, col4 = st.columns(4)
                
                gift_types = {
                    "flower": "🌸 花束",
                    "heart": "❤️ 爱心",
                    "rocket": "🚀 火箭",
                    "castle": "🏰 城堡"
                }
                
                for i, (gift_id, gift_name) in enumerate(gift_types.items()):
                    with [col1, col2, col3, col4][i]:
                        if st.button(gift_name):
                            st.info(f"收到 {gift_name}!")
        else:
            st.info("暂无活跃直播")
    
    with tab3:
        st.subheader("🎮 观众决策系统")
        
        # 创建决策场景
        with st.expander("➕ 创建决策场景"):
            title = st.text_input("场景标题")
            context = st.text_area("场景背景")
            
            st.write("**选项设置:**")
            choices = []
            
            for i in range(4):
                col1, col2 = st.columns([3, 1])
                with col1:
                    choice_text = st.text_area(f"选项{i+1}", height=60, key=f"choice_{i}")
                with col2:
                    impact = st.selectbox("影响", ["正向", "负向", "中性"], key=f"impact_{i}")
                
                if choice_text:
                    choices.append({
                        "id": f"choice_{i+1}",
                        "text": choice_text,
                        "impact": impact
                    })
            
            if st.button("创建决策", type="primary"):
                if title and context and len(choices) >= 2:
                    decision = st.session_state.decision_system.create_decision_scene(
                        title, context, choices
                    )
                    st.success(f"✅ 决策场景创建成功!")
                    st.json(decision)
        
        # 观众偏好分析
        st.divider()
        st.write("**📊 观众偏好分析**")
        
        prefs = st.session_state.decision_system.get_audience_preference()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**🎯 最爱题材:** {prefs['favorite_genre']}")
            st.write(f"**💕 偏好结局:** {prefs['preferred_ending']}")
        
        with col2:
            st.write(f"**⏱️ 节奏偏好:** {prefs['pace_preference']}")
            st.write(f"**🎮 互动风格:** {prefs['interaction_style']}")
    
    with tab4:
        st.subheader("📊 社区预测游戏")
        
        # 创建预测
        with st.expander("➕ 创建预测"):
            pred_question = st.text_input("预测问题")
            
            pred_options = []
            for i in range(3):
                opt = st.text_input(f"预测选项{i+1}", key=f"pred_opt_{i}")
                if opt:
                    pred_options.append({"id": f"pred_opt_{i+1}", "text": opt})
            
            bet_points = st.number_input("下注点数", 10, 1000, 100)
            
            if st.button("发布预测"):
                if pred_question and len(pred_options) >= 2:
                    prediction = st.session_state.prediction_game.create_prediction(
                        "demo_story",
                        pred_question,
                        pred_options,
                        datetime.now().isoformat()
                    )
                    st.success("✅ 预测发布成功!")
                    st.json(prediction)
        
        # 预测列表
        st.divider()
        st.write("**📋 进行中的预测**")
        
        # 模拟预测
        sample_predictions = [
            {
                "question": "主角下一集会做出什么选择?",
                "options": [
                    {"text": "接受挑战", "bets": 45, "total_bets": 120},
                    {"text": "拒绝", "bets": 35, "total_bets": 120},
                    {"text": "犹豫不决", "bets": 40, "total_bets": 120}
                ],
                "status": "open"
            }
        ]
        
        for pred in sample_predictions:
            with st.expander(f"❓ {pred['question']}"):
                total = sum(opt["total_bets"] for opt in pred["options"])
                
                for opt in pred["options"]:
                    pct = opt["bets"] / total * 100 if total > 0 else 0
                    st.write(f"**{opt['text']}** - {opt['bets']}人押注")
                    st.progress(pct / 100)
                
                if pred["status"] == "open":
                    selected = st.selectbox("选择押注", [o["text"] for o in pred["options"]])
                    if st.button("押注"):
                        st.success("押注成功!")
    
    with tab5:
        st.subheader("📈 互动数据分析")
        
        # 核心指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总互动数", "12.8万")
        
        with col2:
            st.metric("分支参与率", "78%")
        
        with col3:
            st.metric("直播峰值观众", "5.2万")
        
        with col4:
            st.metric("预测参与率", "65%")
        
        # 互动趋势
        st.write("**📊 互动趋势**")
        
        trend_data = {
            "日期": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
            "分支投票": [1200, 1350, 1100, 1500, 1800, 2200, 1600],
            "直播互动": [0, 0, 0, 0, 3500, 5200, 2800]
        }
        
        st.line_chart(trend_data)
        
        # 热门分支
        st.write("**🔥 最受欢迎分支**")
        
        hot_branches = [
            {"title": "主角选择职业道路", "participation": 2456, "engagement": 95},
            {"title": "感情线发展", "participation": 2189, "engagement": 92},
            {"title": "反派洗白决策", "participation": 1856, "engagement": 88}
        ]
        
        for branch in hot_branches:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"• {branch['title']}")
                with col2:
                    st.write(f"👥 {branch['participation']}")
                with col3:
                    st.write(f"🔥 {branch['engagement']}%")


if __name__ == "__main__":
    render_interactive_story_page()
