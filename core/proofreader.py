"""
智能校对与语法检查系统 v23
错别字检测、语法优化、标点修正、表达润色
"""

import streamlit as st
import re
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class ErrorType(Enum):
    """错误类型"""
    TYPO = "typo"           # 错别字
    GRAMMAR = "grammar"     # 语法错误
    PUNCTUATION = "punct"    # 标点错误
    EXPRESSION = "express"   # 表达不当
    REDUNDANCY = "redundant" # 冗余重复
    INCONSISTENCY = "inconsist"  # 不一致
    CLARITY = "clarity"      # 表意不清
    FORMAT = "format"         # 格式问题

class Severity(Enum):
    """严重程度"""
    CRITICAL = 3  # 严重错误
    WARNING = 2   # 警告
    SUGGESTION = 1  # 建议

@dataclass
class TextError:
    """文本错误"""
    error_type: ErrorType
    severity: Severity
    original: str
    suggestion: str
    reason: str
    position: Tuple[int, int]  # (start, end) 位置
    examples: List[str] = field(default_factory=list)

@dataclass
class CorrectionReport:
    """校对报告"""
    original_text: str
    corrected_text: str
    errors: List[TextError]
    stats: Dict = field(default_factory=dict)
    
    def get_summary(self) -> str:
        """获取摘要"""
        critical = len([e for e in self.errors if e.severity == Severity.CRITICAL])
        warnings = len([e for e in self.errors if e.severity == Severity.WARNING])
        suggestions = len([e for e in self.errors if e.severity == Severity.SUGGESTION])
        
        return f"发现 {critical} 处严重错误，{warnings} 处警告，{suggestions} 处建议"

class ChineseTypoDatabase:
    """中文错别字数据库"""
    
    # 常见错别字映射
    COMMON_TYPOS = {
        # 形近字错误
        "己": "已", "已": "己",
        "大": "太", "太": "大",
        "人": "入", "入": "人",
        "土": "士", "士": "土",
        "干": "于", "于": "干",
        "日": "曰", "曰": "日",
        "今": "令", "令": "今",
        "又": "叉", "叉": "又",
        "折": "拆", "拆": "折",
        "末": "未", "未": "末",
        "候": "侯", "侯": "候",
        "戌": "戍", "戍": "戌",
        "戉": "戊", "戊": "戉",
        
        # 常见词组错误
        "年轻": "年青",
        "表达": "表明",
        "其他": "其它",
        "好像": "好似",
        "那里": "哪里",
        "这么": "这么",
        "可以": "可以",
        
        # 易混淆词
        "的": "地", "地": "的",
        "做": "作",
        "像": "象",
        "在": "再",
        
        # 常见错字
        "时候": "时侯",
        "已经": "已经",
        "什么": "什末",
        "为什么": "为什末",
    }
    
    # 正确词汇（用于检测错误）
    CORRECT_WORDS = set([
        "时候", "已经", "什么", "为什么", "这么", "那里", "可以",
        "因为", "所以", "但是", "而且", "或者", "如果", "虽然",
        "只是", "还是", "以及", "关于", "通过", "进行", "作为",
        "自己", "我们", "他们", "你们", "这个", "那个", "一个",
        "没有", "不是", "就是", "都是", "有些", "所有", "各种",
    ])
    
    @classmethod
    def check_word(cls, word: str) -> Optional[str]:
        """检查词汇是否正确，返回正确形式或None"""
        # 检查是否是常见错字
        if word in cls.COMMON_TYPOS:
            correct = cls.COMMON_TYPOS[word]
            # 确保返回的是正确形式
            if correct in cls.CORRECT_WORDS or correct in [
                "已", "太", "入", "士", "于", "日", "令", "叉", "拆", "未", "侯", "戍", "戊"
            ]:
                return correct
        return None

class GrammarRules:
    """语法规则库"""
    
    # 主谓宾不匹配规则
    SUBJECT_VERB_RULES = [
        # 数量不一致
        (r"(\d+)个\w+都', '动词了", "数量词后的动词"),
        (r"我\s*和\s*(\w+)\s*都\s*是", "并列主语"),
    ]
    
    # 介词使用错误
    PREPOSITION_RULES = [
        ("在...上/下/里", "表示地点时用\"在\"，表示时间时用\"当\""),
        ("对...感兴趣", "固定搭配"),
        ("跟...有关", "固定搭配"),
    ]
    
    # 常用搭配
    COLLOCATION_RULES = {
        "产生": ["影响", "变化", "问题", "效果", "感情"],
        "发生": ["事情", "变化", "事故", "情况"],
        "发展": ["经济", "事业", "关系", "水平"],
        "提高": ["水平", "能力", "效率", "质量"],
        "增加": ["数量", "内容", "功能", "难度"],
        "改善": ["生活", "关系", "条件", "环境"],
        "解决": ["问题", "困难", "矛盾", "麻烦"],
        "克服": ["困难", "障碍", "挑战", "恐惧"],
    }

class TextProofreader:
    """文本校对器"""
    
    def __init__(self):
        self.typo_db = ChineseTypoDatabase()
        self.grammar_rules = GrammarRules()
        self.custom_rules: List[Callable] = []
    
    def add_custom_rule(self, rule: Callable):
        """添加自定义规则"""
        self.custom_rules.append(rule)
    
    def proofread(self, text: str) -> CorrectionReport:
        """校对文本"""
        errors = []
        
        # 1. 错别字检测
        errors.extend(self._check_typos(text))
        
        # 2. 语法错误检测
        errors.extend(self._check_grammar(text))
        
        # 3. 标点错误检测
        errors.extend(self._check_punctuation(text))
        
        # 4. 冗余检测
        errors.extend(self._check_redundancy(text))
        
        # 5. 不一致检测
        errors.extend(self._check_inconsistency(text))
        
        # 6. 表意不清检测
        errors.extend(self._check_clarity(text))
        
        # 7. 表达润色建议
        errors.extend(self._check_expression(text))
        
        # 生成修正文本
        corrected_text = self._apply_corrections(text, errors)
        
        # 统计信息
        stats = self._generate_stats(errors)
        
        return CorrectionReport(
            original_text=text,
            corrected_text=corrected_text,
            errors=errors,
            stats=stats
        )
    
    def _check_typos(self, text: str) -> List[TextError]:
        """检测错别字"""
        errors = []
        
        # 检测常见的错别字模式
        typo_patterns = [
            # 时侯 -> 时候
            (r"时侯", "时候", "\"时侯\"应为\"时候\""),
            # 年青 -> 年轻
            (r"年青(?![人])", "年轻", "\"年青\"应为\"年轻\""),
            # 什末 -> 什么
            (r"什末", "什么", "\"什末\"应为\"什么\""),
            # 为什末 -> 为什么
            (r"为什末", "为什么", "\"为什末\"应为\"为什么\""),
            # 这木 -> 这么
            (r"这木", "这么", "\"这木\"应为\"这么\""),
            # 那木 -> 那么
            (r"那木", "那么", "\"那木\"应为\"那么\""),
            # 己经 -> 已经
            (r"己经", "已经", "\"己经\"应为\"已经\""),
            # 那里 -> 哪里 (在疑问句中)
            (r"(哪里|那个|哪些)\?(?:不是|应该是)", "语气确认", "反问句中的\"哪里\"应为\"那里\""),
        ]
        
        for pattern, replacement, reason in typo_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                errors.append(TextError(
                    error_type=ErrorType.TYPO,
                    severity=Severity.WARNING,
                    original=match.group(),
                    suggestion=replacement,
                    reason=reason,
                    position=(match.start(), match.end()),
                    examples=["正确用法：" + text[:match.start()] + replacement + text[match.end():]]
                ))
        
        return errors
    
    def _check_grammar(self, text: str) -> List[TextError]:
        """检测语法错误"""
        errors = []
        
        # 主谓不一致
        grammar_patterns = [
            # 一个...都...动词了（主谓不一致）
            (r"一个[^，。,]+?[都|也]\s*说\s*了", "主谓不一致", "\"一个...都...\"后应使用名词或形容词"),
            # 的地得混用
            (r"(\w+)的(\w+)", "的-de", "检测\"的\"的使用"),
            (r"(\w+)地(\w+)", "地-de", "检测\"地\"的使用"),
            (r"(\w+)得(\w+)", "得-de", "检测\"得\"的使用"),
        ]
        
        # 检测"得"的使用错误
        de_patterns = [
            # 动词+得+副词（正确）
            (r"说得\s+很\s+好", "正确", ""),
            (r"做得\s+非常\s+认真", "正确", ""),
            # 动词+的+名词（错误）
            (r"做\s*的\s*事", "正确", ""),
            (r"说\s*的\s*话", "正确", ""),
        ]
        
        # 重复用词
        repeat_pattern = r"(\w{2,})\1{2,}"
        matches = list(re.finditer(repeat_pattern, text))
        for match in matches:
            word = match.group()
            # 允许的重复（如"好好"）
            if word not in ["好好", "常常", "慢慢", "轻轻"]:
                errors.append(TextError(
                    error_type=ErrorType.REDUNDANCY,
                    severity=Severity.WARNING,
                    original=word,
                    suggestion=word[0],
                    reason=f"检测到重复词汇\"{word}\"，可能需要精简",
                    position=(match.start(), match.end())
                ))
        
        return errors
    
    def _check_punctuation(self, text: str) -> List[TextError]:
        """检测标点错误"""
        errors = []
        
        # 连续标点
        punct_pattern = r"[，。,!?]{3,}"
        matches = list(re.finditer(punct_pattern, text))
        for match in matches:
            errors.append(TextError(
                error_type=ErrorType.PUNCTUATION,
                severity=Severity.SUGGESTION,
                original=match.group(),
                suggestion=match.group()[0],
                reason="连续标点符号应精简",
                position=(match.start(), match.end())
            ))
        
        # 句末缺少标点
        sentences = re.split(r"[。！？.!?]", text)
        for i, sent in enumerate(sentences[:-1]):  # 最后一个不需要
            stripped = sent.strip()
            if stripped and len(stripped) > 10 and not stripped.endswith((",", "，", ":", "：")):
                # 检查下一句是否以标点开头
                pass  # 简化处理
        
        # 引号不匹配
        quote_count_open = text.count("\"") + text.count(""") + text.count("「")
        quote_count_close = text.count("\"") + text.count(""") + text.count("」")
        if quote_count_open != quote_count_close:
            errors.append(TextError(
                error_type=ErrorType.PUNCTUATION,
                severity=Severity.WARNING,
                original="引号",
                suggestion="引号",
                reason="引号数量不匹配",
                position=(0, 0)
            ))
        
        return errors
    
    def _check_redundancy(self, text: str) -> List[TextError]:
        """检测冗余"""
        errors = []
        
        # 常见冗余词组
        redundant_patterns = [
            (r"十分\s*非常", "非常", "\"十分非常\"语义重复"),
            (r"非常\s*十分", "十分", "\"非常十分\"语义重复"),
            (r"大概\s*可能", "可能", "\"大概可能\"语义重复"),
            (r"基本\s*上", "基本", "\"基本上\"可简化为\"基本\""),
            (r"其实\s*际上", "实际", "\"实际上\"可简化为\"实际\""),
            (r"首先\s*第一", "首先", "\"首先第一\"语义重复"),
            (r"而且\s*还", "而且", "\"而且还\"可简化为\"而且\""),
            (r"因为\s*由于", "因为", "\"因为由于\"语义重复"),
        ]
        
        for pattern, replacement, reason in redundant_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                errors.append(TextError(
                    error_type=ErrorType.REDUNDANCY,
                    severity=Severity.SUGGESTION,
                    original=match.group(),
                    suggestion=replacement,
                    reason=reason,
                    position=(match.start(), match.end())
                ))
        
        return errors
    
    def _check_inconsistency(self, text: str) -> List[TextError]:
        """检测不一致"""
        errors = []
        
        # 人称不一致（简化版）
        pronouns = ["我", "你", "他", "她", "它", "我们", "你们", "他们", "她们"]
        
        # 检测第三人称转换
        third_person = ["他", "她", "它", "他们", "她们", "它们"]
        for pron in third_person:
            if text.count(pron) > 1:
                # 简单检查是否混用他/她
                if "他" in text and "她" in text:
                    errors.append(TextError(
                        error_type=ErrorType.INCONSISTENCY,
                        severity=Severity.SUGGESTION,
                        original="他/她混用",
                        suggestion="统一人称",
                        reason="检测到\"他\"和\"她\"混用，可能造成指代不清",
                        position=(0, 0)
                    ))
                    break
        
        return errors
    
    def _check_clarity(self, text: str) -> List[TextError]:
        """检测表意不清"""
        errors = []
        
        # 过长句子
        sentences = re.split(r"[。！？]", text)
        for i, sent in enumerate(sentences):
            if len(sent) > 100:
                errors.append(TextError(
                    error_type=ErrorType.CLARITY,
                    severity=Severity.SUGGESTION,
                    original=sent[:20] + "...",
                    suggestion="拆分句子",
                    reason=f"句子过长（{len(sent)}字），建议拆分为多个短句",
                    position=(0, 0)
                ))
        
        # 指代不清
        vague_patterns = [
            (r"这个\s*这个", "指代不清", "连续的\"这个\"可能造成指代不清"),
            (r"那个\s*那个", "指代不清", "连续的\"那个\"可能造成指代不清"),
        ]
        
        for pattern, error_type, reason in vague_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                errors.append(TextError(
                    error_type=ErrorType.CLARITY,
                    severity=Severity.WARNING,
                    original=match.group(),
                    suggestion=match.group().replace("这个这个", "这个").replace("那个那个", "那个"),
                    reason=reason,
                    position=(match.start(), match.end())
                ))
        
        return errors
    
    def _check_expression(self, text: str) -> List[TextError]:
        """表达润色建议"""
        errors = []
        
        # 生硬表达
        stiff_patterns = [
            (r"非常\s*重要", "至关重要", "更生动的表达"),
            (r"非常\s*困难", "困难重重", "更形象的表达"),
            (r"非常\s*高兴", "欣喜若狂", "更有感染力的表达"),
            (r"看了\s*一下", "看了一眼", "更规范的动作描述"),
            (r"吃了\s*一下", "尝了一口", "更规范的动作描述"),
        ]
        
        for pattern, replacement, reason in stiff_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                errors.append(TextError(
                    error_type=ErrorType.EXPRESSION,
                    severity=Severity.SUGGESTION,
                    original=match.group(),
                    suggestion=replacement,
                    reason=reason,
                    position=(match.start(), match.end())
                ))
        
        return errors
    
    def _apply_corrections(self, text: str, errors: List[TextError]) -> str:
        """应用修正"""
        corrected = text
        # 按位置从后往前修正（避免位置偏移）
        sorted_errors = sorted(errors, key=lambda e: e.position[0], reverse=True)
        
        for error in sorted_errors:
            if error.position[0] != error.position[1]:  # 有效位置
                corrected = corrected[:error.position[0]] + error.suggestion + corrected[error.position[1]:]
        
        return corrected
    
    def _generate_stats(self, errors: List[TextError]) -> Dict:
        """生成统计"""
        return {
            "total_errors": len(errors),
            "critical": len([e for e in errors if e.severity == Severity.CRITICAL]),
            "warnings": len([e for e in errors if e.severity == Severity.WARNING]),
            "suggestions": len([e for e in errors if e.severity == Severity.SUGGESTION]),
            "by_type": {et.value: len([e for e in errors if e.error_type == et]) for et in ErrorType}
        }

class ProofreaderUI:
    """校对器UI"""
    
    def __init__(self, proofreader: TextProofreader):
        self.proofreader = proofreader
    
    def render(self):
        """渲染UI"""
        st.subheader("✍️ 智能校对")
        
        # 输入区域
        input_text = st.text_area(
            "输入需要校对的文本",
            value="这里有时侯我会想起年青时候的故事，什末原因呢？可能是因为十分非常怀念吧。",
            height=200,
            key="proofread_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            check_button = st.button("🔍 开始校对", type="primary", use_container_width=True)
        with col2:
            auto_fix = st.checkbox("自动修正", value=True)
        
        if check_button and input_text:
            with st.spinner("校对中..."):
                report = self.proofreader.proofread(input_text)
            
            # 显示统计
            st.divider()
            st.subheader("📊 校对结果")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("总错误", report.stats.get("total_errors", 0))
            with col2:
                st.metric("严重", report.stats.get("critical", 0))
            with col3:
                st.metric("警告", report.stats.get("warnings", 0))
            with col4:
                st.metric("建议", report.stats.get("suggestions", 0))
            
            # 错误详情
            if report.errors:
                st.divider()
                st.subheader("📝 错误详情")
                
                for i, error in enumerate(report.errors):
                    severity_icon = {
                        Severity.CRITICAL: "🔴",
                        Severity.WARNING: "🟡",
                        Severity.SUGGESTION: "🟢"
                    }.get(error.severity, "⚪")
                    
                    error_icon = {
                        ErrorType.TYPO: "🔤",
                        ErrorType.GRAMMAR: "📐",
                        ErrorType.PUNCTUATION: "💬",
                        ErrorType.EXPRESSION: "💭",
                        ErrorType.REDUNDANCY: "📋",
                        ErrorType.INCONSISTENCY: "⚖️",
                        ErrorType.CLARITY: "❓",
                        ErrorType.FORMAT: "📄",
                    }.get(error.error_type, "📌")
                    
                    with st.expander(f"{severity_icon}{error_icon} {error.original} → {error.suggestion}"):
                        st.write(f"**错误类型:** {error.error_type.value}")
                        st.write(f"**严重程度:** {error.severity.name}")
                        st.write(f"**修正建议:** {error.suggestion}")
                        st.write(f"**原因:** {error.reason}")
            
            # 修正后的文本
            st.divider()
            st.subheader("✨ 修正后文本")
            
            if auto_fix:
                st.text_area(
                    "修正结果",
                    value=report.corrected_text,
                    height=200,
                    key="proofread_output",
                    disabled=True
                )
                
                # 对比视图
                if report.corrected_text != input_text:
                    with st.expander("📋 修改对比", expanded=False):
                        st.write("**原文:**")
                        st.info(input_text)
                        st.write("**修正后:**")
                        st.success(report.corrected_text)
            else:
                st.info("取消勾选\"自动修正\"后可查看手动修正建议")
            
            # 复制按钮
            if auto_fix and report.corrected_text:
                if st.button("📋 复制修正后文本"):
                    st.code(report.corrected_text, language=None)
                    st.success("已生成代码，可复制使用")
        
        # 校对设置
        st.divider()
        with st.expander("⚙️ 校对设置", expanded=False):
            enable_typo = st.checkbox("错别字检测", value=True)
            enable_grammar = st.checkbox("语法检查", value=True)
            enable_punct = st.checkbox("标点检查", value=True)
            enable_style = st.checkbox("表达润色", value=True)
            
            st.write("**严格程度:**")
            strictness = st.slider("从宽松到严格", 1, 3, 2)
            strictness_labels = {1: "宽松（仅显示严重错误）", 2: "标准（显示警告和建议）", 3: "严格（显示所有问题）"}
            st.caption(strictness_labels.get(strictness, "标准"))

# 全局实例
proofreader = TextProofreader()

def get_proofreader() -> TextProofreader:
    """获取校对器"""
    return proofreader
