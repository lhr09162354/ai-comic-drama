"""故事弧模板系统 - 结构化叙事框架"""

import json
import config

# ============ 故事弧模板 ============

STORY_ARCS = {
    "三幕式": {
        "icon": "🎭",
        "description": "经典西方三幕式：建置→对抗→解决",
        "structure": [
            {"act": "第一幕：建置", "ratio": 0.25, "prompt": "介绍主角的日常世界，建立角色性格和观众的情感连接，然后用一个激励事件打破平衡，迫使主角踏上旅程"},
            {"act": "第二幕：对抗", "ratio": 0.50, "prompt": "主角面对一系列越来越难的障碍和敌人，经历挫折和成长。中点处有一个重大转折，之后危机不断升级，直至最低谷"},
            {"act": "第三幕：解决", "ratio": 0.25, "prompt": "主角在最黑暗的时刻找到了内在力量，完成最终对决，解决核心冲突，世界恢复新的平衡"},
        ],
    },
    "起承转合": {
        "icon": "🎋",
        "description": "东方四段式：起→承→转→合",
        "structure": [
            {"act": "起：开篇", "ratio": 0.20, "prompt": "以一个引人入胜的场景开头，交代世界和角色，暗示潜在的矛盾"},
            {"act": "承：发展", "ratio": 0.30, "prompt": "沿着开篇的方向逐步深入，角色关系展开，矛盾逐渐明朗化，积蓄力量"},
            {"act": "转：转折", "ratio": 0.30, "prompt": "出乎意料的转折打破之前的预期，角色面临根本性的选择或危机，故事方向急转直下"},
            {"act": "合：收束", "ratio": 0.20, "prompt": "所有线索汇聚，冲突得到解决，留下余韵和思考的空间"},
        ],
    },
    "英雄之旅": {
        "icon": "⚔️",
        "description": "坎贝尔英雄之旅：12阶段浓缩版",
        "structure": [
            {"act": "召唤与启程", "ratio": 0.20, "prompt": "主角在平凡世界收到冒险召唤，起初抗拒，最终在导师引导下跨入未知世界"},
            {"act": "试炼与盟友", "ratio": 0.35, "prompt": "主角经历一系列试炼，结识盟友和敌人，进入最深处的洞穴面对最大的恐惧"},
            {"act": "转变与回归", "ratio": 0.25, "prompt": "主角获得关键奖励或启示，经历死亡与重生，带着蜕变开始回归之旅"},
            {"act": "归来与新生", "ratio": 0.20, "prompt": "主角带着新的力量回到日常世界，用所学解决最终危机，世界因主角的蜕变而改变"},
        ],
    },
    "悬疑解谜": {
        "icon": "🔍",
        "description": "层层剥开真相的悬疑结构",
        "structure": [
            {"act": "谜面", "ratio": 0.15, "prompt": "呈现一个看似不可能的谜题或案件，设置关键悬念，吸引读者"},
            {"act": "调查", "ratio": 0.30, "prompt": "主角展开调查，发现线索但每个线索又引出新的疑问，误导性信息让真相更扑朔迷离"},
            {"act": "反转", "ratio": 0.30, "prompt": "一个颠覆性的发现彻底改变了之前的认知，看似无关的线索突然串联起来"},
            {"act": "揭秘", "ratio": 0.25, "prompt": "主角在关键时刻揭开真相，一切谜团有了合理解释，但真相可能比想象更复杂"},
        ],
    },
    "恋爱升温": {
        "icon": "💕",
        "description": "从相遇到心动的恋爱递进",
        "structure": [
            {"act": "初遇", "ratio": 0.20, "prompt": "两个性格不同的人因为一个偶然事件相遇，第一印象可能是误解或冲突"},
            {"act": "靠近", "ratio": 0.30, "prompt": "被迫共处或共同经历某些事情，逐渐发现对方意想不到的一面，好感暗生"},
            {"act": "心动", "ratio": 0.25, "prompt": "一个关键时刻让感情升温，但因误解或外部阻力产生了矛盾和犹豫"},
            {"act": "告白", "ratio": 0.25, "prompt": "克服内心障碍，勇敢表达心意，两人在甜蜜或感人的场景中走到一起"},
        ],
    },
    "逆袭成长": {
        "icon": "🔥",
        "description": "从弱到强的热血逆袭之路",
        "structure": [
            {"act": "低谷", "ratio": 0.20, "prompt": "主角处于最低点，被轻视、被打败、失去一切，但内心不甘的火种未灭"},
            {"act": "磨砺", "ratio": 0.30, "prompt": "主角在困境中找到出路，刻苦修炼或学习，获得关键的成长和力量提升"},
            {"act": "反击", "ratio": 0.25, "prompt": "主角在关键时刻展现出蜕变后的实力，让所有轻视者震惊，但最强的敌人还在前方"},
            {"act": "登顶", "ratio": 0.25, "prompt": "最终决战中主角爆发全部力量，战胜曾经不可逾越的对手，站在新的巅峰"},
        ],
    },
}

def get_arc_prompt(arc_name: str, total_pages: int, theme: str, genre: str) -> str:
    """根据故事弧模板生成增强版prompt
    
    Args:
        arc_name: 故事弧名称
        total_pages: 总页数
        theme: 用户创意
        genre: 题材类型
    
    Returns:
        增强后的prompt字符串
    """
    arc = STORY_ARCS.get(arc_name)
    if not arc:
        return theme

    parts = []
    parts.append(f"故事框架：{arc_name}（{arc['description']}）")
    parts.append(f"总页数：{total_pages}页")
    parts.append(f"题材：{genre}")
    parts.append(f"创意：{theme}")
    parts.append("")
    parts.append("请按以下结构分配剧情：")

    for i, act in enumerate(arc["structure"]):
        act_pages = max(1, round(total_pages * act["ratio"]))
        parts.append(f"【{act['act']}】约{act_pages}页：{act['prompt']}")

    parts.append("")
    parts.append("要求：严格按照以上结构分配页数和剧情节奏，确保每个阶段的关键情节点都有体现。")

    return "\n".join(parts)

def apply_arc_to_script(script: dict, arc_name: str) -> dict:
    """给已生成的剧本添加故事弧标签（不修改内容，只添加结构注释）"""
    arc = STORY_ARCS.get(arc_name)
    if not arc or not script.get("pages"):
        return script

    total = len(script["pages"])
    current_page = 0

    for act in arc["structure"]:
        act_pages = max(1, round(total * act["ratio"]))
        end_page = min(current_page + act_pages, total)
        for pi in range(current_page, end_page):
            if pi < len(script["pages"]):
                script["pages"][pi]["act"] = act["act"]
        current_page = end_page

    script["story_arc"] = arc_name
    return script

def get_arc_summary(arc_name: str) -> str:
    """获取故事弧摘要"""
    arc = STORY_ARCS.get(arc_name)
    if not arc:
        return ""
    parts = [f"{arc['icon']} {arc_name}：{arc['description']}"]
    for act in arc["structure"]:
        parts.append(f"  • {act['act']}（约{int(act['ratio']*100)}%）")
    return "\n".join(parts)
