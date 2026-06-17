"""
多语言本地化系统
支持多种语言输出，拓展海外市场
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional

class MultiLanguageSystem:
    """多语言本地化系统"""
    
    # 支持的语言列表
    LANGUAGES = {
        "zh": {"name": "中文", "native": "中文", "flag": "🇨🇳"},
        "en": {"name": "英语", "native": "English", "flag": "🇺🇸"},
        "ja": {"name": "日语", "native": "日本語", "flag": "🇯🇵"},
        "ko": {"name": "韩语", "native": "한국어", "flag": "🇰🇷"},
        "es": {"name": "西班牙语", "native": "Español", "flag": "🇪🇸"},
        "fr": {"name": "法语", "native": "Français", "flag": "🇫🇷"},
        "de": {"name": "德语", "native": "Deutsch", "flag": "🇩🇪"},
        "pt": {"name": "葡萄牙语", "native": "Português", "flag": "🇵🇹"},
        "ru": {"name": "俄语", "native": "Русский", "flag": "🇷🇺"},
        "ar": {"name": "阿拉伯语", "native": "العربية", "flag": "🇸🇦"},
        "hi": {"name": "印地语", "native": "हिन्दी", "flag": "🇮🇳"},
        "th": {"name": "泰语", "native": "ไทย", "flag": "🇹🇭"},
        "vi": {"name": "越南语", "native": "Tiếng Việt", "flag": "🇻🇳"},
        "id": {"name": "印尼语", "native": "Bahasa Indonesia", "flag": "🇮🇩"},
    }
    
    def __init__(self):
        self.translation_cache = {}
    
    def render(self):
        """渲染多语言系统界面"""
        st.subheader("🌐 多语言本地化系统")
        
        # 语言选择
        col1, col2, col3 = st.columns(3)
        
        with col1:
            source_lang = st.selectbox(
                "源语言",
                list(self.LANGUAGES.keys()),
                format_func=lambda x: f"{self.LANGUAGES[x]['flag']} {self.LANGUAGES[x]['name']}",
                index=0,
                help="选择要翻译的内容源语言"
            )
        
        with col2:
            target_langs = st.multiselect(
                "目标语言",
                [k for k in self.LANGUAGES.keys() if k != source_lang],
                default=["en"],
                format_func=lambda x: f"{self.LANGUAGES[x]['flag']} {self.LANGUAGES[x]['name']}",
                help="选择要翻译成的目标语言（可多选）"
            )
        
        with col3:
            quality_level = st.select_slider(
                "翻译质量",
                options=["快速", "标准", "高精度"],
                value="标准",
                help="高精度会保留更多语境和情感"
            )
        
        # 内容输入
        tab1, tab2 = st.tabs(["📝 文本翻译", "📄 批量翻译"])
        
        with tab1:
            self._render_single_translation(source_lang, target_langs, quality_level)
        
        with tab2:
            self._render_batch_translation(source_lang, target_langs, quality_level)
    
    def _render_single_translation(self, source_lang, target_langs, quality):
        """单文本翻译界面"""
        source_text = st.text_area(
            "输入内容",
            height=150,
            placeholder="输入要翻译的剧本、对白或描述...",
            key="source_text_single"
        )
        
        if st.button("🌍 开始翻译", type="primary"):
            if source_text and target_langs:
                results = self._translate_text(source_text, source_lang, target_langs, quality)
                self._display_translation_results(results)
            else:
                st.warning("请输入内容并选择目标语言")
    
    def _render_batch_translation(self, source_lang, target_langs, quality):
        """批量翻译界面"""
        st.info("💡 批量翻译适合多个剧本或大量内容的统一翻译")
        
        uploaded_file = st.file_uploader(
            "上传剧本文件",
            type=['txt', 'json'],
            help="支持 .txt 和 .json 格式"
        )
        
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            st.text_area("文件内容预览", value=content[:500], height=100, disabled=True)
            
            if st.button("🚀 批量翻译", type="primary"):
                if target_langs:
                    results = self._batch_translate(content, source_lang, target_langs, quality)
                    self._display_batch_results(results)
                else:
                    st.warning("请选择目标语言")
    
    def _translate_text(self, text: str, source: str, targets: List[str], quality: str) -> Dict:
        """翻译文本"""
        results = {}
        
        for target in targets:
            # 模拟翻译（实际使用翻译API）
            translated = self._simulate_translation(text, source, target, quality)
            results[target] = {
                "original": text,
                "translated": translated,
                "language": self.LANGUAGES[target]["name"],
                "quality": quality,
                "char_count": len(translated),
                "timestamp": datetime.now().isoformat()
            }
        
        return results
    
    def _batch_translate(self, content: str, source: str, targets: List[str], quality: str) -> Dict:
        """批量翻译"""
        # 按行或段落分割
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        
        results = {}
        for target in targets:
            translations = []
            for line in lines:
                translated = self._simulate_translation(line, source, target, quality)
                translations.append({
                    "original": line,
                    "translated": translated
                })
            
            results[target] = {
                "items": translations,
                "total_lines": len(translations),
                "language": self.LANGUAGES[target]["name"],
                "timestamp": datetime.now().isoformat()
            }
        
        return results
    
    def _simulate_translation(self, text: str, source: str, target: str, quality: str) -> str:
        """模拟翻译（实际项目中替换为真实翻译API）"""
        # 这里应该调用真实的翻译API
        # 暂时返回原文 + 语言标记作为占位
        lang_name = self.LANGUAGES[target]["name"]
        
        if target == "en":
            # 简单的中文转英文模拟
            translations = {
                "爱": "love", "恨": "hate", "哭": "cry", "笑": "laugh",
                "死": "die", "活": "live", "杀": "kill", "救": "save",
                "朋友": "friend", "敌人": "enemy", "家人": "family",
                "我": "I", "你": "you", "他": "he", "她": "she",
                "我们": "we", "他们": "they", "是": "is", "有": "have"
            }
            result = text
            for cn, en in translations.items():
                result = result.replace(cn, en)
            return result
        else:
            return f"[{lang_name}] {text}"
    
    def _display_translation_results(self, results: Dict):
        """展示翻译结果"""
        st.success(f"✅ 翻译完成！共 {len(results)} 个语言版本")
        
        for lang_code, result in results.items():
            lang_info = self.LANGUAGES[lang_code]
            with st.expander(f"{lang_info['flag']} {lang_info['name']} ({result['char_count']}字)"):
                st.text_area(
                    f"{lang_info['native']}",
                    value=result["translated"],
                    height=150,
                    key=f"result_{lang_code}",
                    label_visibility="collapsed"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📋 复制{lang_info['name']}", key=f"copy_{lang_code}"):
                        st.info("已复制到剪贴板")
                
                with col2:
                    if st.button(f"💾 下载{lang_info['name']}", key=f"download_{lang_code}"):
                        self._download_translation(result, lang_code)
    
    def _display_batch_results(self, results: Dict):
        """展示批量翻译结果"""
        st.success("✅ 批量翻译完成！")
        
        for lang_code, result in results.items():
            lang_info = self.LANGUAGES[lang_code]
            
            with st.expander(f"📄 {lang_info['flag']} {lang_info['name']} ({result['total_lines']}条)"):
                for i, item in enumerate(result["items"][:10]):  # 只显示前10条
                    st.write(f"**原文 {i+1}:** {item['original']}")
                    st.write(f"**译文 {i+1}:** {item['translated']}")
                    st.divider()
                
                if result["total_lines"] > 10:
                    st.info(f"还有 {result['total_lines'] - 10} 条内容...")
                
                # 下载全部
                if st.button(f"📥 下载全部{lang_info['name']}翻译", key=f"batch_download_{lang_code}"):
                    self._download_batch_translation(result, lang_code)
    
    def _download_translation(self, result: Dict, lang_code: str):
        """下载单条翻译"""
        st.info(f"下载 {self.LANGUAGES[lang_code]['name']} 翻译文件...")
    
    def _download_batch_translation(self, result: Dict, lang_code: str):
        """下载批量翻译"""
        st.info(f"下载 {self.LANGUAGES[lang_code]['name']} 批量翻译文件...")
    
    def get_supported_languages(self) -> List[Dict]:
        """获取支持的语言列表"""
        return [
            {"code": code, "name": info["name"], "native": info["native"]}
            for code, info in self.LANGUAGES.items()
        ]

class LocaleManager:
    """本地化管理器"""
    
    def __init__(self):
        self.locales = {}
        self._init_default_locales()
    
    def _init_default_locales(self):
        """初始化默认本地化字符串"""
        self.locales = {
            "zh": {
                "app_name": "AI漫剧生成器",
                "generate": "生成剧本",
                "preview": "预览漫剧",
                "download": "下载",
                "settings": "设置"
            },
            "en": {
                "app_name": "AI Comic Drama Generator",
                "generate": "Generate Script",
                "preview": "Preview",
                "download": "Download",
                "settings": "Settings"
            },
            "ja": {
                "app_name": "AI漫画ドラマ生成",
                "generate": "脚本生成",
                "preview": "プレビュー",
                "download": "ダウンロード",
                "settings": "設定"
            }
        }
    
    def get_text(self, key: str, locale: str = "zh") -> str:
        """获取本地化文本"""
        return self.locales.get(locale, {}).get(key, key)
    
    def add_locale(self, locale: str, strings: Dict):
        """添加新的本地化"""
        self.locales[locale] = strings
    
    def export_locale(self, locale: str) -> str:
        """导出本地化文件"""
        return json.dumps(self.locales.get(locale, {}), ensure_ascii=False, indent=2)

def render_multi_language_system():
    """入口函数"""
    system = MultiLanguageSystem()
    system.render()
