# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 互动系统增强
投票、问答、猜剧情等新互动形式
"""

import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# ============ 互动类型 ============

@dataclass
class VoteOption:
    """投票选项"""
    text: str
    votes: int = 0
    percentage: float = 0.0


@dataclass
class VoteEvent:
    """投票事件"""
    title: str
    question: str
    options: List[VoteOption] = field(default_factory=list)
    is_active: bool = True
    total_votes: int = 0
    created_at: str = ""


@dataclass
class QuizQuestion:
    """问答题目"""
    question: str
    options: List[str]
    correct_index: int
    explanation: str = ""


@dataclass
class PlotGuess:
    """猜剧情"""
    description: str
    options: List[str]
    answer_index: int
    hint: str = ""


class InteractionPlusSystem:
    """互动系统增强"""

    def __init__(self):
        self._votes: List[VoteEvent] = []
        self._quizzes: List[QuizQuestion] = []
        self._plot_guesses: List[PlotGuess] = []

    # ============ 投票系统 ============

    def create_vote(self, title: str, question: str, option_texts: List[str]) -> VoteEvent:
        options = [VoteOption(text=t) for t in option_texts]
        vote = VoteEvent(
            title=title, question=question, options=options,
            created_at=datetime.now().isoformat()
        )
        self._votes.append(vote)
        return vote

    def cast_vote(self, vote_index: int, option_index: int) -> VoteEvent:
        vote = self._votes[vote_index]
        vote.options[option_index].votes += 1
        vote.total_votes = sum(o.votes for o in vote.options)
        for o in vote.options:
            o.percentage = round(o.votes / vote.total_votes * 100, 1) if vote.total_votes > 0 else 0
        return vote

    def get_active_votes(self) -> List[VoteEvent]:
        return [v for v in self._votes if v.is_active]

    # ============ 问答系统 ============

    def add_quiz(self, question: str, options: List[str], correct_index: int, explanation: str = ""):
        q = QuizQuestion(question=question, options=options, correct_index=correct_index, explanation=explanation)
        self._quizzes.append(q)

    def get_quizzes(self) -> List[QuizQuestion]:
        return self._quizzes

    def check_answer(self, quiz_index: int, selected_index: int) -> Dict:
        quiz = self._quizzes[quiz_index]
        correct = selected_index == quiz.correct_index
        return {
            "correct": correct,
            "explanation": quiz.explanation if quiz.explanation else ("回答正确！" if correct else "回答错误。"),
            "correct_answer": quiz.options[quiz.correct_index],
        }

    # ============ 猜剧情 ============

    def create_plot_guess(self, description: str, options: List[str], answer_index: int, hint: str = ""):
        guess = PlotGuess(description=description, options=options, answer_index=answer_index, hint=hint)
        self._plot_guesses.append(guess)

    def get_plot_guesses(self) -> List[PlotGuess]:
        return self._plot_guesses

    def reveal_answer(self, guess_index: int) -> Dict:
        guess = self._plot_guesses[guess_index]
        return {
            "answer": guess.options[guess.answer_index],
            "hint": guess.hint,
        }


# ============ 预设互动数据 ============

PRESET_VOTES = [
    {"title": "下一话剧情走向", "question": "主角接下来会做什么选择？", "options": ["勇往直前", "暂且退让", "寻求帮助", "独自承受"]},
    {"title": "CP投票", "question": "你最磕哪一对？", "options": ["青梅竹马组", "欢喜冤家组", "命中注定组", "暗恋情深组"]},
    {"title": "角色人气", "question": "你最喜欢哪个角色？", "options": ["主角", "男二号", "反派", "神秘人"]},
]

PRESET_QUIZZES = [
    {"question": "漫画中常用的分格方式「コマ」源自哪种语言？", "options": ["中文", "日语", "英语", "法语"], "correct": 1, "explanation": "「コマ」是日语词汇，源自汉字「駒」，原指棋子，后用于漫画分格"},
    {"question": "以下哪种不是漫画常见的叙事节奏？", "options": ["起承转合", "倒叙插叙", "意识流", "随机跳跃"], "correct": 3, "explanation": "随机跳跃不是有效的叙事节奏，好的漫画都需要有节奏感"},
    {"question": "对话框中锯齿状边框通常表示什么？", "options": ["内心独白", "电子通讯", "愤怒/激动", "回忆"], "correct": 2, "explanation": "锯齿状边框通常表示角色情绪激动或愤怒"},
]

PRESET_PLOT_GUESSES = [
    {"description": "神秘人救了主角后消失了，他到底是谁？", "options": ["未来的主角", "男主的父亲", "平行世界的来客", "AI化身"], "answer": 0, "hint": "想想故事的时间线暗示"},
    {"description": "女主突然获得的特殊能力来自哪里？", "options": ["天生觉醒", "神秘遗物", "某人的托付", "一场实验的副作用"], "answer": 2, "hint": "注意前几章那个消失的人"},
]


def render_interaction_plus_page():
    """渲染互动系统增强页面"""
    import streamlit as st

    system = InteractionPlusSystem()

    # 加载预设
    for pv in PRESET_VOTES:
        system.create_vote(pv["title"], pv["question"], pv["options"])
    for pq in PRESET_QUIZZES:
        system.add_quiz(pq["question"], pq["options"], pq["correct"], pq.get("explanation", ""))
    for pg in PRESET_PLOT_GUESSES:
        system.create_plot_guess(pg["description"], pg["options"], pg["answer"], pg.get("hint", ""))

    st.header("🎮 互动系统增强")
    st.caption("投票、问答、猜剧情——让观众参与创作")

    tab1, tab2, tab3, tab4 = st.tabs(["🗳️ 投票", "❓ 问答", "🔮 猜剧情", "➕ 创建互动"])

    # 投票
    with tab1:
        st.subheader("🗳️ 观众投票")
        votes = system.get_active_votes()
        for i, vote in enumerate(votes):
            with st.expander(f"📊 {vote.title}"):
                st.write(f"**{vote.question}**")
                for j, opt in enumerate(vote.options):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.progress(opt.percentage / 100 if vote.total_votes > 0 else 0,
                                   text=f"{opt.text} ({opt.percentage}%)")
                    with c2:
                        if st.button("投票", key=f"vote_{i}_{j}", use_container_width=True):
                            system.cast_vote(i, j)
                            st.toast(f"已投票: {opt.text}")

    # 问答
    with tab2:
        st.subheader("❓ 漫画知识问答")
        quizzes = system.get_quizzes()
        for i, quiz in enumerate(quizzes):
            st.write(f"**Q{i+1}: {quiz.question}**")
            selected = st.radio("选择答案", quiz.options, key=f"quiz_{i}")
            if st.button(f"提交答案", key=f"quiz_submit_{i}"):
                selected_idx = quiz.options.index(selected)
                result = system.check_answer(i, selected_idx)
                if result["correct"]:
                    st.success(f"✅ {result['explanation']}")
                else:
                    st.error(f"❌ 正确答案是: {result['correct_answer']}。{result['explanation']}")

    # 猜剧情
    with tab3:
        st.subheader("🔮 猜剧情")
        guesses = system.get_plot_guesses()
        for i, guess in enumerate(guesses):
            st.write(f"**{guess.description}**")
            selected = st.radio("你的猜测", guess.options, key=f"guess_{i}")
            if st.button(f"揭晓答案", key=f"guess_reveal_{i}"):
                result = system.reveal_answer(i)
                st.info(f"💡 提示: {result['hint']}")
                st.success(f"答案: {result['answer']}")

    # 创建互动
    with tab4:
        st.subheader("➕ 创建新互动")
        interaction_type = st.selectbox("互动类型", ["投票", "问答", "猜剧情"])

        if interaction_type == "投票":
            vote_title = st.text_input("投票标题", key="new_vote_title")
            vote_question = st.text_input("投票问题", key="new_vote_question")
            vote_options = st.text_area("选项(每行一个)", key="new_vote_options")
            if st.button("创建投票", type="primary", use_container_width=True):
                if vote_title and vote_question and vote_options:
                    opts = [o.strip() for o in vote_options.strip().split("\n") if o.strip()]
                    system.create_vote(vote_title, vote_question, opts)
                    st.success(f"投票「{vote_title}」已创建！")
                else:
                    st.warning("请填写所有字段")

        elif interaction_type == "问答":
            quiz_q = st.text_input("问题", key="new_quiz_q")
            quiz_opts = st.text_area("选项(每行一个)", key="new_quiz_opts")
            quiz_answer = st.number_input("正确答案序号(从0开始)", 0, 10, 0, key="new_quiz_answer")
            quiz_explain = st.text_input("解释", key="new_quiz_explain")
            if st.button("创建问答", type="primary", use_container_width=True):
                if quiz_q and quiz_opts:
                    opts = [o.strip() for o in quiz_opts.strip().split("\n") if o.strip()]
                    system.add_quiz(quiz_q, opts, quiz_answer, quiz_explain)
                    st.success("问答已创建！")

        else:
            guess_desc = st.text_input("剧情描述", key="new_guess_desc")
            guess_opts = st.text_area("选项(每行一个)", key="new_guess_opts")
            guess_answer = st.number_input("正确答案序号(从0开始)", 0, 10, 0, key="new_guess_answer")
            guess_hint = st.text_input("提示", key="new_guess_hint")
            if st.button("创建猜剧情", type="primary", use_container_width=True):
                if guess_desc and guess_opts:
                    opts = [o.strip() for o in guess_opts.strip().split("\n") if o.strip()]
                    system.create_plot_guess(guess_desc, opts, guess_answer, guess_hint)
                    st.success("猜剧情已创建！")
