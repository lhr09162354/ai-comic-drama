# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 增强AI角色对话
增加情感表达、动作描写、场景氛围渲染
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


# ============ 对话增强数据 ============

EMOTION_EXPRESSIONS = {
    "开心": {
        "动作": ["嘴角上扬", "眼睛弯成月牙", "忍不住笑出声", "开心地转了一圈"],
        "语气": ["~", "！", "♪", "哈哈"],
        "氛围": ["阳光温暖", "微风拂面", "花香味飘来"],
    },
    "生气": {
        "动作": ["眉头紧锁", "拳头攥紧", "牙关咬紧", "猛地站起来"],
        "语气": ["！", "……！", "哼！", "你——！"],
        "氛围": ["空气凝固", "温度骤降", "暴风雨前的宁静"],
    },
    "悲伤": {
        "动作": ["低下了头", "眼眶泛红", "声音颤抖", "缓缓转过身去"],
        "语气": ["……", "啊……", "呜……", "（哽咽）"],
        "氛围": ["雨滴落在窗上", "灰暗的天空", "无人问津的角落"],
    },
    "紧张": {
        "动作": ["手心冒汗", "不自觉地后退一步", "攥紧衣角", "屏住呼吸"],
        "语气": ["……", "！", "？", "那个……"],
        "氛围": ["心跳加速", "空气稀薄", "时间仿佛静止"],
    },
    "惊讶": {
        "动作": ["瞪大了眼睛", "嘴巴微张", "下意识后退", "手上的东西掉落"],
        "语气": ["！？", "诶！？", "你说什么！？", "不会吧——"],
        "氛围": ["世界仿佛按了暂停键", "周围安静得可怕"],
    },
    "害羞": {
        "动作": ["脸颊泛红", "低下头不敢直视", "手指绞在一起", "声音越来越小"],
        "语气": ["……那个", "别看我啦……", "才、才不是呢！", "你、你说什么呢"],
        "氛围": ["脸上升起热气", "心跳声清晰可闻"],
    },
    "坚定": {
        "动作": ["目光坚定", "挺直腰背", "用力点头", "握紧拳头"],
        "语气": ["！", "一定！", "绝不会！", "我发誓！"],
        "氛围": ["光芒万丈", "信念的力量"],
    },
    "温柔": {
        "动作": ["微微弯起嘴角", "轻声说", "伸手轻抚", "目光柔和"],
        "语气": ["~", "呢", "哦~", "嗯……"],
        "氛围": ["月光如水", "暖意环绕", "轻柔的风"],
    },
}

# 对话场景模板
DIALOGUE_TEMPLATES = {
    "偶遇": [
        "在{location}的拐角，{char_a}和{char_b}不期而遇",
        "没想到会在{location}遇见你。",
        "命运还真是会开玩笑。",
    ],
    "对峙": [
        "{location}内气氛剑拔弩张，{char_a}和{char_b}相对而立",
        "今天，必须做个了断。",
        "你以为我怕你？",
    ],
    "告白": [
        "在{location}，{char_a}终于鼓起勇气",
        "有些话，不说出来，我怕以后再也没机会了。",
        "我喜欢你。一直，都喜欢着你。",
    ],
    "告别": [
        "{location}，夕阳西下，{char_a}站在{char_b}面前",
        "这可能是我们最后一次见面了。",
        "别忘了我，好吗？",
    ],
    "重逢": [
        "时隔{time}，在{location}再次相遇",
        "……是你吗？",
        "好久不见。",
    ],
    "争吵": [
        "{location}内，压抑许久的矛盾终于爆发",
        "你永远都是这样！从不考虑我的感受！",
        "那你呢？你又何曾理解过我！",
    ],
}

# 角色说话习惯模板
SPEECH_HABITS = {
    "温柔型": {
        "口头禅": ["嗯~", "好的呢", "没关系哦"],
        "称呼习惯": "喜欢用昵称",
        "特征": "说话总是很轻柔，句尾常带上语气的波浪线",
    },
    "霸道型": {
        "口头禅": ["哼", "闭嘴", "我说了算"],
        "称呼习惯": "喜欢叫对方全名",
        "特征": "话少但句句有力，从不解释自己",
    },
    "活泼型": {
        "口头禅": ["哇！", "太棒了！", "嘿嘿~"],
        "称呼习惯": "喜欢给人起外号",
        "特征": "说话语速快，经常使用感叹号，话题跳跃",
    },
    "冷淡型": {
        "口头禅": ["无所谓", "随便", "……"],
        "称呼习惯": "直呼其名或忽略称呼",
        "特征": "话极少，但一开口就是重点",
    },
    "毒舌型": {
        "口头禅": ["呵", "就这？", "别逗了"],
        "称呼习惯": "喜欢讽刺性称呼",
        "特征": "说话尖刻但其实很关心人，反差萌",
    },
}


@dataclass
class DialogueLine:
    """对话行"""
    character: str
    emotion: str = "平静"
    action: str = ""
    dialogue: str = ""
    atmosphere: str = ""
    inner_thought: str = ""  # 内心独白


class CharacterDialogueEnhancer:
    """AI角色对话增强器"""

    def __init__(self):
        pass

    def enhance_dialogue(self, character: Dict, emotion: str = "平静",
                         dialogue: str = "", scene: str = "") -> DialogueLine:
        """增强单句对话，添加动作描写和情感表达"""
        expressions = EMOTION_EXPRESSIONS.get(emotion, {})

        import random
        action = random.choice(expressions.get("动作", [""])) if expressions else ""
        atmosphere = random.choice(expressions.get("氛围", [""])) if expressions else ""

        return DialogueLine(
            character=character.get("name", "角色"),
            emotion=emotion,
            action=action,
            dialogue=dialogue,
            atmosphere=atmosphere,
            inner_thought="",
        )

    def generate_dialogue_scene(self, char_a: Dict, char_b: Dict,
                                 scene_type: str = "偶遇",
                                 location: str = "校园") -> List[DialogueLine]:
        """生成一组增强的对话场景"""
        import random
        template = DIALOGUE_TEMPLATES.get(scene_type, DIALOGUE_TEMPLATES["偶遇"])

        lines = []
        # 场景描写
        scene_desc = template[0].format(
            location=location, char_a=char_a.get("name", "A"), char_b=char_b.get("name", "B"),
            time="许久"
        )

        # 对话内容
        for i, line_text in enumerate(template[1:], 1):
            char = char_a if i % 2 == 1 else char_b
            emotion = "平静"
            if "怒" in line_text or "！" in line_text:
                emotion = "生气"
            elif "喜欢" in line_text or "温柔" in line_text:
                emotion = "害羞"

            enhanced = self.enhance_dialogue(char, emotion, line_text, scene_type)
            lines.append(enhanced)

        return lines

    def get_emotion_list(self) -> List[str]:
        return list(EMOTION_EXPRESSIONS.keys())

    def get_scene_types(self) -> List[str]:
        return list(DIALOGUE_TEMPLATES.keys())

    def get_speech_habits(self) -> Dict:
        return SPEECH_HABITS


def render_character_dialogue_page():
    """渲染增强AI角色对话页面"""
    import streamlit as st

    enhancer = CharacterDialogueEnhancer()

    st.header("💬 AI角色对话增强")
    st.caption("增加情感表达、动作描写，让角色更加鲜活")

    if not st.session_state.get("characters"):
        st.info("请先在「角色管理」中添加角色")
        return

    char_names = [c["name"] for c in st.session_state.characters]

    c1, c2 = st.columns(2)
    with c1:
        char_a_name = st.selectbox("角色A", char_names, key="dlg_char_a")
    with c2:
        char_b_name = st.selectbox("角色B", char_names, index=min(1, len(char_names) - 1), key="dlg_char_b")

    c3, c4 = st.columns(2)
    with c3:
        scene_type = st.selectbox("场景类型", enhancer.get_scene_types())
        location = st.text_input("场景地点", value="校园")
    with c4:
        emotion = st.selectbox("情感基调", enhancer.get_emotion_list())

    if st.button("🎭 生成增强对话", type="primary", use_container_width=True):
        char_a = next((c for c in st.session_state.characters if c["name"] == char_a_name), {})
        char_b = next((c for c in st.session_state.characters if c["name"] == char_b_name), {})

        lines = enhancer.generate_dialogue_scene(char_a, char_b, scene_type, location)

        for line in lines:
            st.markdown(f"**{line.character}** ({line.emotion})")
            if line.action:
                st.caption(f"🎬 *{line.action}*")
            if line.dialogue:
                st.write(f"「{line.dialogue}」")
            if line.atmosphere:
                st.caption(f"🌙 _{line.atmosphere}_")
            st.write("")  # 间距

    # 说话习惯参考
    with st.expander("📖 角色说话习惯参考"):
        for habit_name, habit_data in enhancer.get_speech_habits().items():
            st.write(f"**{habit_name}**")
            st.caption(f"口头禅: {' / '.join(habit_data['口头禅'])}")
            st.caption(f"特征: {habit_data['特征']}")
