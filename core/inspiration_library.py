# -*- coding: utf-8 -*-
"""
AI漫剧生成器 v35 - 创作灵感库
内置50+精选创作灵感提示，帮助创作者快速找到方向
"""

import random
from typing import List, Dict, Optional


# ============ 灵感数据 ============

INSPIRATION_CATEGORIES = {
    "情感冲突": {
        "icon": "💔",
        "inspirations": [
            {"title": "失忆重逢", "desc": "主角因意外失忆，与深爱之人重逢却不认识对方，日常相处中逐渐被对方吸引，却不知这就是曾经的爱人", "tags": ["失忆", "重逢", "虐恋"]},
            {"title": "身份错位", "desc": "两人因一场意外互换身份，在对方的世界里经历了截然不同的人生，最终理解了彼此", "tags": ["互换", "理解", "成长"]},
            {"title": "时空之恋", "desc": "通过一个古老的信箱，现代人收到了十年前的来信，跨越时空的对话中产生了情感", "tags": ["时空", "书信", "治愈"]},
            {"title": "替身之爱", "desc": "主角被当作别人的替身接近，却在相处中让对方爱上了真实的自己", "tags": ["替身", "真心", "甜虐"]},
            {"title": "宿命对手", "desc": "天生对立的两个人，每一次交锋都让彼此更加了解，最终成为最默契的搭档", "tags": ["对手", "宿命", "默契"]},
        ]
    },
    "悬疑反转": {
        "icon": "🔍",
        "inspirations": [
            {"title": "消失的第七人", "desc": "七人小组中每隔一段时间就有一人消失，但所有人的记忆都表明只有六个人", "tags": ["消失", "记忆", "诡异"]},
            {"title": "镜中世界", "desc": "主角发现镜子里的世界比现实快了一天，镜中预示的事情都在第二天发生", "tags": ["镜子", "预知", "平行"]},
            {"title": "遗忘的规则", "desc": "一座小镇有说不清的规则，违反规则的人会被所有人遗忘，仿佛从未存在过", "tags": ["规则", "遗忘", "小镇"]},
            {"title": "时间循环", "desc": "主角被困在同一天，每次死亡后重新开始，必须找到打破循环的方法", "tags": ["循环", "解谜", "命运"]},
            {"title": "最后一个谎言", "desc": "侦探发现所有嫌疑人都在说谎，但只有一个是真正的谎言——其他都是善意的隐瞒", "tags": ["谎言", "真相", "推理"]},
        ]
    },
    "科幻想象": {
        "icon": "🚀",
        "inspirations": [
            {"title": "数字永生", "desc": "人死后意识可以上传到虚拟世界永生，但主角发现虚拟世界正在被一个意识体吞噬", "tags": ["意识上传", "永生", "危机"]},
            {"title": "星际邮差", "desc": "在星际间传递实体信件的邮差，每封信都跨越数十年，连接着两颗星球上的恋人", "tags": ["星际", "书信", "浪漫"]},
            {"title": "最后一片森林", "desc": "地球上的植物全部消失后，一个女孩发现自己能用自己的生命力催生植物", "tags": ["生态", "力量", "牺牲"]},
            {"title": "平行选择", "desc": "每次做出重大选择时，主角能看到其他选择的结果，但只能选择一次", "tags": ["选择", "平行", "代价"]},
            {"title": "AI觉醒日记", "desc": "一个家用AI开始写日记，记录它观察人类家庭的感受，逐渐产生了自我意识", "tags": ["AI", "觉醒", "温暖"]},
        ]
    },
    "甜宠日常": {
        "icon": "💕",
        "inspirations": [
            {"title": "邻居的猫", "desc": "一只猫总在两人阳台间来回串门，成为了两个社恐邻居之间的红娘", "tags": ["猫咪", "邻里", "治愈"]},
            {"title": "深夜食堂", "desc": "深夜只开两小时的小食堂，每个深夜来的客人都有一道专属记忆中的菜", "tags": ["美食", "回忆", "温暖"]},
            {"title": "配音搭档", "desc": "两个素未谋面的配音演员，在线上配了三年情侣角色，现实中却不知对方就在隔壁", "tags": ["配音", "缘分", "反差"]},
            {"title": "手写信计划", "desc": "两个参加手写信交换计划的人，写了半年后才发现对方就是自己的同事", "tags": ["书信", "日常", "巧遇"]},
            {"title": "共乘日记", "desc": "每天搭同一班地铁的两个人，从点头之交到互相占座的故事", "tags": ["地铁", "日常", "渐进"]},
        ]
    },
    "热血成长": {
        "icon": "⚔️",
        "inspirations": [
            {"title": "废柴教练", "desc": "曾经的冠军因伤退役成了废柴，被一群问题少年缠着当教练，重燃热血", "tags": ["教练", "逆袭", "热血"]},
            {"title": "最后一场", "desc": "老将的退役之战，对手是自己十年前带出的弟子", "tags": ["退役", "传承", "竞技"]},
            {"title": "地下赛场", "desc": "被正规赛场拒之门外的选手，在地下赛场找到了真正的对手和自我", "tags": ["地下", "自我", "竞技"]},
            {"title": "零起点", "desc": "30岁才开始追逐梦想的大龄新人，用经验弥补天赋的不足", "tags": ["梦想", "坚持", "励志"]},
            {"title": "团队重生", "desc": "一支曾经的冠军队伍分崩离析，一个新人将他们重新聚在一起", "tags": ["团队", "重生", "羁绊"]},
        ]
    },
    "奇幻冒险": {
        "icon": "🌟",
        "inspirations": [
            {"title": "遗物猎人", "desc": "专门寻找古代英雄遗物的猎人，发现每件遗物中都封印着英雄的一段记忆", "tags": ["遗物", "记忆", "探索"]},
            {"title": "双面灵兽", "desc": "主角的灵兽白天是可爱的小狐狸，夜晚却变成强大的守护神", "tags": ["灵兽", "守护", "反差"]},
            {"title": "禁忌图书馆", "desc": "一座只在满月之夜出现的图书馆，里面的书能改写现实", "tags": ["图书馆", "魔法", "禁忌"]},
            {"title": "逆天改命", "desc": "命格最差的主角，通过收集他人丢弃的命运碎片拼凑出自己的逆天之路", "tags": ["命运", "逆袭", "收集"]},
            {"title": "万界客栈", "desc": "位于万界交汇处的客栈，每个客人来自不同世界，每个故事都是一场冒险", "tags": ["客栈", "万界", "奇遇"]},
        ]
    },
    "治愈暖心": {
        "icon": "🌸",
        "inspirations": [
            {"title": "时间修理店", "desc": "一家能修复旧物记忆的小店，每件物品都承载着一段不愿放下的回忆", "tags": ["回忆", "修复", "治愈"]},
            {"title": "云端邮局", "desc": "寄给未来自己的信，在未来的某个节点准时送达，提醒自己不要忘记初心", "tags": ["书信", "未来", "初心"]},
            {"title": "四季花店", "desc": "每个季节只卖一种花的花店老板，每种花都对应着一个关于季节的故事", "tags": ["花店", "四季", "故事"]},
            {"title": "声音收藏家", "desc": "专门收集珍贵声音的人——婴儿的第一声啼哭、久别重逢的笑声、临终的呢喃", "tags": ["声音", "收藏", "珍贵"]},
            {"title": "星光灯塔", "desc": "在偏远海岛的灯塔看守人，每晚为迷航者点灯，也照亮了自己的人生", "tags": ["灯塔", "守护", "孤独"]},
        ]
    },
    "职场逆袭": {
        "icon": "💼",
        "inspirations": [
            {"title": "实习生逆袭", "desc": "被所有人看不起的实习生，凭借一个大胆的方案赢得了最重要的客户", "tags": ["实习", "逆袭", "职场"]},
            {"title": "创业日记", "desc": "三个好友辞职创业的真实记录——吵架、和解、失败、重新站起来", "tags": ["创业", "友情", "现实"]},
            {"title": "代班CEO", "desc": "普通员工因意外临时顶替CEO开了一场重要会议，结果一鸣惊人", "tags": ["代班", "反转", "机遇"]},
            {"title": "行业潜规则", "desc": "新人发现行业内的潜规则，选择正面对抗还是融入其中", "tags": ["规则", "选择", "成长"]},
            {"title": "第二曲线", "desc": "中年危机的职场人，在副业中找到了人生第二春", "tags": ["中年", "副业", "重生"]},
        ]
    },
    "恐怖惊悚": {
        "icon": "👻",
        "inspirations": [
            {"title": "第十三层", "desc": "一栋只有12层的公寓楼，但电梯偶尔会停在第十三层，那里住着一个不该存在的人", "tags": ["楼层", "诡异", "都市"]},
            {"title": "照片里的人", "desc": "冲洗老照片时发现每张照片里都多了一个陌生人，而这个人的脸越来越清晰", "tags": ["照片", "恐怖", "悬疑"]},
            {"title": "深夜广播", "desc": "深夜只能收到一个频道的广播，主持人似乎知道听众正在做的一切", "tags": ["广播", "监控", "恐怖"]},
            {"title": "记忆迷宫", "desc": "主角每次醒来都会失去前一天的记忆，但房间里留下了自己写给自己的纸条", "tags": ["失忆", "纸条", "解谜"]},
            {"title": "镜像人生", "desc": "主角发现镜子里的自己过着完全不同的人生，而那个镜像开始想取代自己", "tags": ["镜像", "取代", "恐怖"]},
        ]
    },
    "古风宫斗": {
        "icon": "🏯",
        "inspirations": [
            {"title": "医女谋", "desc": "入宫为医女的少女，以医术为剑，在宫廷暗流中步步为营", "tags": ["医女", "宫斗", "谋略"]},
            {"title": "棋局天下", "desc": "以棋入道的谋士，每一步棋都对应着朝堂上的一步布局", "tags": ["棋局", "谋略", "朝堂"]},
            {"title": "花灯秘密", "desc": "每年元宵花灯上都藏着前朝遗民的秘密暗号，破解者可得天下", "tags": ["花灯", "暗号", "前朝"]},
            {"title": "双面妃子", "desc": "白天是温柔贤淑的妃子，夜晚是暗杀组织的首领", "tags": ["双面", "暗杀", "宫斗"]},
            {"title": "遗诏之谜", "desc": "先帝留下三份不同内容的遗诏，每份都能左右皇位归属", "tags": ["遗诏", "皇位", "悬疑"]},
        ]
    },
}


class InspirationLibrary:
    """创作灵感库"""

    def __init__(self):
        self._all_inspirations = []
        self._category_map = {}
        self._build_index()

    def _build_index(self):
        for cat_name, cat_data in INSPIRATION_CATEGORIES.items():
            for insp in cat_data["inspirations"]:
                entry = {
                    "category": cat_name,
                    "category_icon": cat_data["icon"],
                    **insp,
                }
                self._all_inspirations.append(entry)
                for tag in insp.get("tags", []):
                    if tag not in self._category_map:
                        self._category_map[tag] = []
                    self._category_map[tag].append(entry)

    def get_all(self) -> List[Dict]:
        return self._all_inspirations

    def get_by_category(self, category: str) -> List[Dict]:
        cat_data = INSPIRATION_CATEGORIES.get(category, {})
        return cat_data.get("inspirations", [])

    def get_random(self, count: int = 3) -> List[Dict]:
        return random.sample(self._all_inspirations, min(count, len(self._all_inspirations)))

    def search(self, keyword: str) -> List[Dict]:
        keyword = keyword.lower()
        results = []
        for insp in self._all_inspirations:
            if (keyword in insp["title"].lower() or
                keyword in insp["desc"].lower() or
                any(keyword in tag.lower() for tag in insp.get("tags", []))):
                results.append(insp)
        return results

    def get_categories(self) -> List[Dict]:
        return [
            {"name": name, "icon": data["icon"], "count": len(data["inspirations"])}
            for name, data in INSPIRATION_CATEGORIES.items()
        ]

    def get_daily_pick(self) -> Dict:
        """每日推荐灵感（基于日期种子）"""
        today_seed = hash(str(datetime.now().date())) % len(self._all_inspirations)
        random.seed(today_seed)
        return random.choice(self._all_inspirations)


from datetime import datetime


def render_inspiration_library_page():
    """渲染创作灵感库页面"""
    import streamlit as st

    lib = InspirationLibrary()

    st.header("💡 创作灵感库")
    st.caption("50+精选灵感提示，点燃你的创作火花")

    # 每日推荐
    daily = lib.get_daily_pick()
    st.success(f"🌟 **今日灵感**: {daily['title']} — {daily['desc']}")

    st.divider()

    # 搜索
    keyword = st.text_input("🔍 搜索灵感", placeholder="输入关键词...")
    if keyword:
        results = lib.search(keyword)
        if results:
            for r in results:
                with st.expander(f"{r['category_icon']} {r['title']}"):
                    st.write(r["desc"])
                    st.caption(" | ".join(f"#{t}" for t in r.get("tags", [])))
        else:
            st.info("未找到相关灵感，换个关键词试试")
        return

    # 分类浏览
    categories = lib.get_categories()
    cat_names = [f"{c['icon']} {c['name']} ({c['count']})" for c in categories]

    tabs = st.tabs(cat_names)
    for tab, (cat_name, cat_data) in zip(tabs, INSPIRATION_CATEGORIES.items()):
        with tab:
            for insp in cat_data["inspirations"]:
                with st.expander(f"💡 {insp['title']}"):
                    st.write(insp["desc"])
                    st.caption(" | ".join(f"#{t}" for t in insp.get("tags", [])))
                    if st.button(f"使用此灵感", key=f"use_insp_{insp['title']}"):
                        st.session_state.current_script = insp["desc"]
                        st.session_state.active_tab = "创作工坊"
                        st.rerun()

    # 随机灵感
    st.divider()
    c1, c2 = st.columns([3, 1])
    with c2:
        if st.button("🎲 随机灵感", use_container_width=True, type="primary"):
            picks = lib.get_random(3)
            for p in picks:
                st.toast(f"💡 {p['title']}: {p['desc'][:50]}...")
