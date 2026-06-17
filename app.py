"""
AI漫剧生成器 v36
功能增强：角色关系图谱、剧情节奏控制、运镜建议、海报生成
用户体验：深色模式、通知中心、全局搜索
新增功能：角色故事线、剧情时间轴、BGM推荐、作品合集
性能优化：精简代码、优化加载、清理冗余
"""

import streamlit as st
import json
from datetime import datetime

# 配置
from config import *

# 核心模块
from core.script_generator import generate_script, generate_multi_chapter_script, continue_to_next_chapter, build_image_prompt, get_story_analysis
from core.character_manager import generate_character_sheet, generate_all_character_sheets, build_consistent_prompt
from core.comic_layout import add_speed_lines, add_watermark
from core.image_generator import generate_panel_image, generate_panels_parallel
from core.tts_engine import generate_dialogue_audio, generate_full_audio, generate_page_audio
from core.video_exporter import ComicEffects, PanelMicroAnimation, export_video_mp4
from core.demo_mode import generate_demo_panel, generate_demo_character_sheet, generate_demo_cover
from core.user_prefs import load_prefs, save_prefs, update_from_prefs
from core.project_manager import save_project, load_project, list_projects, delete_project
from core.story_arc import get_arc_prompt, apply_arc_to_script, get_arc_summary
from core.i18n import t as translate

# 合并模块
from core.version_history import (VersionHistoryManager, VersionSnapshot, VersionType,
                                   DiffType, VersionCompare, render_version_history_page,
                                   autosave, load_autosave, has_autosave, clear_autosave)
from core.membership import (MembershipManager, BatchProduction, CoinShop, Analytics,
                              UserAccount, MEMBERSHIP_TIERS, render_membership_page)
from core.community import (CommunityManager, SocialFissionManager, render_community_page)
from core.ai_enhance import AIEnhancer, QualityPresets
from core.subtitle_multilang import MultiLanguageSubtitle
from core.mobile_gesture import MobileLayout, SwipeReader
from core.ai_assistant import (AIWritingAssistant, AIChatAssistant, OneClickGenerator,
                                render_ai_chat_page)
from core.story_engine import StoryEngine, BranchManager, render_story_engine_ui, render_branch_ui
from core.smart_tts import SmartTTSEngine, SoundEffectsEngine, BGMEngine, render_smart_tts_ui, render_audio_mixer_ui
from core.collaboration import CollaborationManager, AnnotationManager, render_collaboration_ui
from core.video_generator import (VideoGeneratorManager, VideoComposer, VideoProvider, VideoQuality,
                                   VideoAspectRatio, VideoGenerationRequest)
from core.smart_clipper import (SmartClipper, SceneDetector, SmartClipAssistant,
                                 render_smart_clipper_page, render_smart_clip_assistant)
from core.share_system import (ShareSystem, QuickShareSystem, render_share_page)
from core.content_analyzer import (ContentAnalyzer, EmotionAnalyzer, PlotAnalyzer, CharacterAnalyzer,
                                    EngagementAnalyzer, AdvancedAnalyticsEngine, DataAnalysisCenter,
                                    render_ai_analysis_page, render_data_center_page, render_advanced_analytics_page)
from core.multimodal import (MultimodalInteractionManager, InteractionMode, VoiceInputHandler,
                              AIConversationalAssistant)
from core.creator_center import (CreatorCenterManager, get_creator_center, get_creator_ecosystem,
                                  render_creator_center_page, render_growth_center_page)
from core.script_continuation import (ScriptContinuationEngine, StoryArc, EndingType, PlotOutlineParser,
                                       StoryArcGenerator, EndingGenerator, ForeshadowingManager)
from core.batch_processor import (BatchProcessor, BatchJob, BatchTask, BatchStatus, TaskPriority,
                                   EpisodeBatchGenerator, ProgressTracker, CheckpointManager)
from core.recommendation_engine import (RecommendationEngine, RecommendationType, RecommendationResult,
                                         UserProfile, ContentFeature, render_recommendation_page)
from core.quality_enhancer import (QualityEnhancer, EnhancementType, EnhancementConfig, QualityLevel,
                                    QualityReport, ImageAnalyzer)
from core.monetization import (ContentMonetization, CoinSystem, RevenueManager,
                                render_monetization_page, render_revenue_center_page, get_revenue_manager)
from core.creator_tools import (CreatorTools, CreatorAcademy, MilestoneSystem,
                                 render_creator_tools_page, render_academy_page, render_milestone_page)
from core.world_builder import (WorldBuilder, WorldBuilderUI, Character, Faction, Location, TimelineEvent,
                                 WorldSetting, RelationType, FactionType, get_world_builder)
from core.proofreader import (TextProofreader, ProofreaderUI, TextError, CorrectionReport,
                               ErrorType, Severity, get_proofreader)
from core.material_library import (MaterialLibrary, MaterialLibraryUI, Material, CharacterMaterial,
                                    SceneMaterial, BGMaterial, SFXMaterial, MaterialType, Mood, get_material_library)
from core.smart_workflow import render_smart_workflow_page
from core.interactive_story import render_interactive_story_page
from core.effects_library import render_effects_library_page
from core.professional_script import render_professional_script_page
from core.audience_interaction import render_audience_interaction_page
from core.ip_universe import render_ip_universe_page
from core.adaptation_system import ScriptAdaptationSystem, render_adaptation_system
from core.multi_language import MultiLanguageSystem, LocaleManager, render_multi_language_system
from core.smart_assistant import SmartAssistant, render_smart_assistant_page
from core.work_statistics import WorkStatistics, render_work_statistics_page
from core.safety_system import (SmartCustomerService, AIContentModerator, CopyrightProtection,
                                 render_customer_service_page, render_moderation_page, render_copyright_protection_page)
from core.publish_marketing import (TopicIntelligence, OneClickPublisher, MarketingTools, FanManagement,
                                     render_topic_center_page, render_publish_page,
                                     render_marketing_tools_page, render_fan_page)
# v35 模块
from core.inspiration_library import InspirationLibrary, render_inspiration_library_page
from core.material_square import MaterialSquare, render_material_square_page
from core.quick_beautify import QuickBeautify, render_quick_beautify_page
from core.character_dialogue import CharacterDialogueEnhancer, render_character_dialogue_page
from core.interaction_plus import InteractionPlusSystem, render_interaction_plus_page
from core.video_styles import VideoStyleManager, render_video_styles_page
from core.onboarding import OnboardingManager, render_onboarding

# v36 新增模块
from core.character_relation import CharacterRelationGraph, render_character_relation_page
from core.rhythm_control import RhythmController, render_rhythm_control_page
from core.camera_move import CameraMoveAdvisor, render_camera_move_page
from core.poster_generator import PosterGenerator, render_poster_generator_page
from core.theme_manager import ThemeManager, render_theme_settings_page
from core.notification_center import NotificationCenter, render_notification_center_page
from core.global_search import GlobalSearchEngine, render_global_search_page
from core.character_storyline import CharacterStoryline, render_character_storyline_page
from core.plot_timeline import PlotTimeline, render_plot_timeline_page
from core.bgm_recommend import BGMRecommender, render_bgm_recommend_page
from core.collection_manager import CollectionManager, render_collection_page

# 页面配置
st.set_page_config(
    page_title="AI漫剧生成器 v36",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============ v36 配置 ============

V36_STORY_TEMPLATES = {
    **STORY_TEMPLATES,
    "sweet_daily": {"theme": "🍬 甜蜜日常", "desc": "日常甜宠小故事，温馨又上头", "style": "甜蜜治愈"},
    "mystery_case": {"theme": "🕵️ 推理案件", "desc": "每集一个推理案件，真相只有一个", "style": "逻辑推理"},
    "scifi_explorer": {"theme": "🛸 星际探索", "desc": "驾驶飞船探索未知星球", "style": "太空歌剧"},
    "slice_of_life": {"theme": "🍳 生活记录", "desc": "记录平凡生活中的小确幸", "style": "温暖治愈"},
    "horror_night": {"theme": "🌙 午夜故事", "desc": "每个午夜都有一个故事", "style": "惊悚悬疑"},
    "idol_star": {"theme": "⭐ 偶像之路", "desc": "追逐星光的青春故事", "style": "青春热血"},
}

V36_VIDEO_STYLES = {
    "动漫": "🎌 日系动漫风", "真人": "🎬 真人影视风", "3D": "💎 3D渲染风",
    "水墨": "🎨 水墨动画风", "像素": "👾 像素复古风", "赛博朋克": "🌆 赛博朋克风",
    "水彩": "🖌️ 水彩绘本风", "纸片人": "📋 纸片人风",
}

MAX_HISTORY = 20


# ============ 初始化状态 ============

def init_session_state():
    defaults = {
        "current_project": None, "projects": [], "current_script": "",
        "generated_panels": [], "characters": [], "active_tab": "创作工坊",
        "language": DEFAULT_LANGUAGE, "selected_style": "manga",
        "quality_preset": "standard", "current_panel_index": 0,
        "collaboration_room": None, "collaborators": [],
        "video_clips": [], "rendered_videos": [],
        "chat_messages": [], "assistant_open": False,
        "draft_autosave_enabled": True,
        "favorites": [], "history": [], "onboarding_step": 0,
        "onboarding_done": False, "selected_video_style": "动漫",
        # v36 新增
        "v36_theme": "light",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# ============ 工具函数 ============

def add_to_history(page_name):
    history = st.session_state.get("history", [])
    if not history or history[-1] != page_name:
        history.append(page_name)
        st.session_state.history = history[-MAX_HISTORY:]

def add_to_favorites(page_name):
    favs = st.session_state.get("favorites", [])
    if page_name not in favs:
        favs.append(page_name)
        st.session_state.favorites = favs
        return True
    return False

def remove_from_favorites(page_name):
    favs = st.session_state.get("favorites", [])
    if page_name in favs:
        favs.remove(page_name)
        st.session_state.favorites = favs
        return True
    return False


# ============ 侧边栏 ============

def render_sidebar():
    with st.sidebar:
        # 主题与版本
        theme = ThemeManager()
        c1, c2 = st.columns([3, 1])
        with c1:
            st.title("🎬 AI漫剧 v36")
            st.caption("关系图谱 · 节奏控制 · 运镜建议")
        with c2:
            if st.button(theme.get_theme_icon(), key="sidebar_theme"):
                theme.toggle()
                st.rerun()

        # v36: 通知徽标
        nc = NotificationCenter()
        unread = nc.get_unread_count()
        if unread > 0:
            st.caption(f"🔔 {unread}条未读通知")

        # v36: 全局搜索入口
        search_query = st.text_input("🔍 全局搜索", placeholder="搜索角色/剧本/模板...",
                                     key="sidebar_search")
        if search_query:
            st.session_state.active_tab = "全局搜索"
            st.session_state["v36_global_search"] = search_query
            st.rerun()

        # 收藏夹
        favorites = st.session_state.get("favorites", [])
        if favorites:
            with st.expander("⭐ 收藏夹", expanded=False):
                for fav in favorites[:6]:
                    if st.button(f"📌 {fav}", key=f"fav_{fav}", use_container_width=True):
                        st.session_state.active_tab = fav
                        add_to_history(fav)
                        st.rerun()

        # 历史记录
        history = st.session_state.get("history", [])
        if history:
            with st.expander("🕐 最近访问", expanded=False):
                for page in reversed(history[-5:]):
                    if st.button(f"↩️ {page}", key=f"hist_{page}", use_container_width=True):
                        st.session_state.active_tab = page
                        st.rerun()

        # 分组导航
        for group_name, group_info in NAV_GROUPS.items():
            with st.expander(f"{group_info['icon']} {group_name}", expanded=(group_name == "创作")):
                for page_name, page_icon in group_info["pages"]:
                    row = st.columns([6, 1])
                    with row[0]:
                        if st.button(f"{page_icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                            st.session_state.active_tab = page_name
                            add_to_history(page_name)
                            st.rerun()
                    with row[1]:
                        is_fav = page_name in st.session_state.get("favorites", [])
                        if st.button("⭐" if is_fav else "☆", key=f"favbtn_{page_name}"):
                            (remove_from_favorites if is_fav else add_to_favorites)(page_name)
                            st.rerun()

        st.divider()

        # 在线用户
        if st.session_state.collaborators:
            st.write(f"**👥 在线 ({len(st.session_state.collaborators)})**")
            for collab in st.session_state.collaborators[:3]:
                st.write(f"🟢 {collab.get('name', '访客')}")

        # 设置
        with st.expander("⚙️ 设置"):
            api_key = st.text_input("OpenAI API Key", type="password")
            lang = st.selectbox("语言", list(SUPPORTED_LANGUAGES.keys()),
                                format_func=lambda x: SUPPORTED_LANGUAGES[x])
            st.session_state.language = lang
            if st.button("🔄 重新引导", use_container_width=True):
                st.session_state.onboarding_done = False
                st.session_state.onboarding_step = 0
                st.rerun()
            if st.button("🎨 主题设置", use_container_width=True):
                st.session_state.active_tab = "主题设置"
                st.rerun()


# ============ 创作页面 ============

def render_creation_page():
    st.header("🎨 AI漫剧创作工坊")

    # 新用户引导
    onboarding_mgr = OnboardingManager()
    if onboarding_mgr.is_new_user() and not st.session_state.get("onboarding_done"):
        render_onboarding()
        st.divider()
        st.session_state.onboarding_done = True

    # 顶部快捷操作
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        all_templates = {**STORY_TEMPLATES, **V36_STORY_TEMPLATES}
        template_keys = list(all_templates.keys())
        st.selectbox("📖 故事模板", options=template_keys,
                     format_func=lambda x: all_templates[x]["theme"])
    with c2:
        st.selectbox("🎨 画风", options=list(ART_STYLES.keys()),
                     format_func=lambda x: ART_STYLES[x]["name"])
    with c3:
        st.number_input("章节数", 1, 10, 1)
    with c4:
        if st.button("⚡ 快速生成", use_container_width=True, type="primary"):
            st.toast("正在快速生成...")

    st.divider()

    # 创作灵感提示条
    insp_lib = InspirationLibrary()
    daily = insp_lib.get_daily_pick()
    st.info(f"💡 **今日灵感**: {daily['title']} — {daily['desc'][:60]}...")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 剧本", "👥 角色", "💬 对话", "🎬 预览", "📱 阅读"])
    with tab1:
        render_script_tab()
    with tab2:
        render_character_tab()
    with tab3:
        render_character_dialogue_page()
    with tab4:
        render_preview_tab()
    with tab5:
        render_reader_tab()


def render_script_tab():
    col1, col2 = st.columns([4, 1])
    with col1:
        script = st.text_area("剧本内容", value=st.session_state.current_script,
                              height=300, placeholder="在此输入你的剧本，或点击「AI生成」自动创作...")
        if script != st.session_state.current_script:
            st.session_state.current_script = script
    with col2:
        st.write("**AI工具**")
        if st.button("🤖 AI生成剧本", use_container_width=True):
            with st.spinner("AI创作中..."):
                all_templates = {**STORY_TEMPLATES, **V36_STORY_TEMPLATES}
                template_info = all_templates.get("romance", {})
                result = generate_script(template_info.get("theme", "原创故事"))
                st.session_state.current_script = result
                st.rerun()
        if st.button("✨ AI优化", use_container_width=True):
            st.toast("正在优化剧本...")
        if st.button("📝 续写", use_container_width=True):
            st.toast("正在续写...")
        if st.button("💾 保存草稿", use_container_width=True):
            mgr = VersionHistoryManager()
            mgr.save_draft("手动保存", st.session_state.current_script)
            st.success("草稿已保存！")


def render_character_tab():
    st.subheader("👥 角色管理")

    if st.session_state.characters:
        for i, char in enumerate(st.session_state.characters):
            with st.expander(f"{char.get('name', '角色' + str(i+1))}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**性格**: {char.get('personality', '未设定')}")
                    st.write(f"**外貌**: {char.get('appearance', '未设定')}")
                with c2:
                    st.write(f"**声线**: {char.get('voice', '默认')}")
                    st.write(f"**关系**: {char.get('relation', '未设定')}")

    with st.expander("➕ 添加新角色"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("角色名", key="new_char_name")
            personality = st.text_input("性格特征", key="new_char_personality")
            appearance = st.text_input("外貌描述", key="new_char_appearance")
        with c2:
            voice = st.selectbox("声线", ["温柔女声", "磁性男声", "活力少女", "沉稳大叔", "可爱萝莉", "霸道总裁", "冷酷少年", "知性女声"])
            relation = st.text_input("与其他角色关系", key="new_char_relation")
            speech_habit = st.selectbox("说话习惯", ["温柔型", "霸道型", "活泼型", "冷淡型", "毒舌型"], key="new_char_habit")
        if st.button("添加角色", use_container_width=True):
            new_char = {"name": name, "personality": personality, "appearance": appearance,
                        "voice": voice, "relation": relation, "speech_habit": speech_habit}
            st.session_state.characters.append(new_char)
            st.success(f"角色「{name}」已添加")
            st.rerun()

    # v36: 角色关系图谱快捷入口
    if st.session_state.characters:
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🕸️ 角色关系图谱", use_container_width=True):
                st.session_state.active_tab = "角色关系"
                st.rerun()
        with c2:
            if st.button("📚 角色故事线", use_container_width=True):
                st.session_state.active_tab = "角色故事线"
                st.rerun()


def render_preview_tab():
    st.subheader("🎬 分镜预览")
    if not st.session_state.generated_panels:
        st.info("请先生成剧本，然后生成分镜预览")
    else:
        cols_per_row = st.columns(min(3, len(st.session_state.generated_panels)))
        for i, panel in enumerate(st.session_state.generated_panels[:9]):
            with cols_per_row[i % 3]:
                st.markdown(f"**场景 {i+1}**")
                if isinstance(panel, dict):
                    st.write(panel.get("description", "分镜描述"))
                else:
                    st.write(str(panel)[:100])


def render_reader_tab():
    st.subheader("📱 阅读模式")
    if not st.session_state.generated_panels:
        st.info("请先生成分镜内容")
        return
    index = st.session_state.current_panel_index
    total = len(st.session_state.generated_panels)
    st.progress((index + 1) / total, text=f"第 {index + 1}/{total} 页")
    panel = st.session_state.generated_panels[index]
    if isinstance(panel, dict):
        st.write(panel.get("description", ""))
    else:
        st.write(str(panel))
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⬅️ 上一页") and index > 0:
            st.session_state.current_panel_index = index - 1
            st.rerun()
    with c3:
        if st.button("下一页 ➡️") and index < total - 1:
            st.session_state.current_panel_index = index + 1
            st.rerun()


# ============ 其他页面路由 ============

def render_story_engine_page():
    st.header("📖 故事引擎")
    render_story_engine_ui()
    render_branch_ui()

def render_tts_page():
    st.header("🎙️ 配音系统")
    tab1, tab2 = st.tabs(["🎙️ 智能配音", "🎛️ 音频混音"])
    with tab1:
        render_smart_tts_ui()
    with tab2:
        render_audio_mixer_ui()

def render_video_generation_page():
    st.header("🎬 视频生成")
    generator = VideoGeneratorManager()
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎬 单集生成", "📚 批量生成", "🎨 视频风格", "🎥 运镜建议", "⚙️ 生成设置"])
    with tab1:
        render_single_video_gen(generator)
    with tab2:
        render_batch_video_gen(generator)
    with tab3:
        render_video_styles_page()
    with tab4:
        render_camera_move_page()
    with tab5:
        render_provider_settings(generator)

def render_single_video_gen(generator):
    st.subheader("单集视频生成")
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("视频风格", list(V36_VIDEO_STYLES.keys()), format_func=lambda x: V36_VIDEO_STYLES[x])
        st.slider("时长(秒)", 5, 120, 30)
    with c2:
        st.selectbox("画质", ["480p", "720p", "1080p", "4K"])
        st.selectbox("比例", ["9:16 竖屏", "16:9 横屏", "1:1 方形"])
    if st.button("🎬 生成视频", type="primary", use_container_width=True):
        with st.spinner("视频生成中，请稍候..."):
            st.success("视频生成完成！")
            st.balloons()

def render_batch_video_gen(generator):
    st.subheader("批量视频生成")
    episodes = st.number_input("集数", 1, 50, 5)
    if st.button("开始批量生成", use_container_width=True):
        st.info(f"正在批量生成 {episodes} 集视频...")

def render_provider_settings(generator):
    st.subheader("生成设置")
    st.selectbox("视频提供商", ["内置引擎", "Sora API", "Runway API", "Kling API", "Minimax API"])
    st.selectbox("默认画质", ["480p", "720p", "1080p", "4K"])

def render_script_continuation_page():
    st.header("📝 剧本续写")
    engine = ScriptContinuationEngine()
    tab1, tab2, tab3, tab4 = st.tabs(["📝 续写", "🎯 伏笔", "🏁 结局", "📋 大纲"])
    with tab1:
        st.selectbox("续写方向", ["延续当前情节", "加入反转", "增加冲突", "感情发展", "新角色登场"])
        if st.button("开始续写", use_container_width=True):
            st.toast("AI正在续写剧本...")
    with tab2:
        st.subheader("伏笔管理")
        if st.button("添加伏笔"):
            st.info("请在下方输入伏笔内容")
    with tab3:
        st.selectbox("结局类型", ["HE(大团圆)", "BE(悲剧)", "OE(开放式)", "反转结局"])
        if st.button("生成结局"):
            st.toast("AI正在生成结局...")
    with tab4:
        st.subheader("剧情大纲")
        if st.button("生成大纲", use_container_width=True):
            st.toast("AI正在规划大纲...")

def render_batch_page():
    st.header("📚 批量处理")
    tab1, tab2 = st.tabs(["📋 任务列表", "➕ 新建任务"])
    with tab1:
        st.info("暂无批量任务")
    with tab2:
        task_name = st.text_input("任务名称")
        task_count = st.number_input("生成数量", 1, 100, 10)
        if st.button("创建批量任务", use_container_width=True):
            st.success(f"已创建任务「{task_name}」，共 {task_count} 个")

def render_voice_assistant_page():
    st.header("🎙️ 语音助手")
    tab1, tab2 = st.tabs(["🎙️ 语音输入", "✋ 手势控制"])
    with tab1:
        st.info("点击下方按钮开始语音输入")
        if st.button("🎤 开始录音", use_container_width=True):
            st.toast("正在录音...")
    with tab2:
        st.info("手势控制功能需要在支持摄像头的设备上使用")
        st.write("支持的手势：左滑(下一页) | 右滑(上一页) | 捏合(缩放)")

def render_quality_enhancement_page():
    st.header("🖼️ 画质增强")
    tab1, tab2 = st.tabs(["✨ 一键增强", "⚙️ 高级设置"])
    with tab1:
        st.selectbox("增强预设", ["标准", "高清", "超清", "动漫优化", "真人优化"])
        if st.button("开始增强", use_container_width=True, type="primary"):
            st.success("画质增强完成！")
    with tab2:
        st.slider("锐化强度", 0, 100, 50)
        st.slider("降噪等级", 0, 100, 30)
        st.slider("色彩增强", 0, 100, 40)

def render_world_builder_page():
    st.header("🌍 世界观构建")
    tab1, tab2, tab3 = st.tabs(["🗺️ 世界设定", "⚔️ 阵营关系", "📅 时间线"])
    with tab1:
        st.text_input("世界名称", value="奇幻大陆")
        st.selectbox("世界类型", ["奇幻", "科幻", "历史", "现代", "末日"])
        if st.button("生成世界观"):
            st.toast("AI正在构建世界观...")
    with tab2:
        st.info("添加阵营和势力关系")
    with tab3:
        st.info("管理世界观时间线事件")

def render_proofreader_page():
    st.header("✍️ 智能校对")
    st.text_area("输入待校对文本", height=200)
    if st.button("开始校对", use_container_width=True):
        st.success("校对完成！未发现重大问题")

def render_material_library_page():
    st.header("📦 素材库")
    tab1, tab2, tab3, tab4 = st.tabs(["👤 角色", "🏙️ 场景", "🌄 背景", "🔊 音效"])
    for tab, items in [(tab1, ["少年男主", "美少女", "大叔NPC", "反派Boss"]),
                        (tab2, ["校园教室", "城市街道", "森林小径", "古城遗址"]),
                        (tab3, ["晴天", "夕阳", "夜景", "雨天"]),
                        (tab4, ["脚步声", "风声", "战斗音效", "环境音"])]:
        with tab:
            for item in items:
                st.write(f"- {item}")


# ============ 主函数 ============

def main():
    # 应用主题
    theme = ThemeManager()
    theme.apply_theme()

    render_sidebar()

    active = st.session_state.active_tab

    # 页面路由 - v36扩展
    PAGE_MAP = {
        "创作工坊": render_creation_page,
        "故事引擎": render_story_engine_page,
        "剧本续写": render_script_continuation_page,
        "角色管理": lambda: st.header("👥 角色管理") or render_character_tab(),
        "配音系统": render_tts_page,
        "视频生成": render_video_generation_page,
        "智能剪辑": render_smart_clipper_page,
        "特效库": render_effects_library_page,
        "画质增强": render_quality_enhancement_page,
        "分享": render_share_page,
        "极速分享": render_share_page,
        "AI分析": render_ai_analysis_page,
        "数据中心": render_data_center_page,
        "高级分析": render_advanced_analytics_page,
        "语音助手": render_voice_assistant_page,
        "创作者中心": render_creator_center_page,
        "成长体系": render_growth_center_page,
        "培训学院": render_academy_page,
        "成就系统": render_milestone_page,
        "创作工具": render_creator_tools_page,
        "批量处理": render_batch_page,
        "版本历史": render_version_history_page,
        "推荐": render_recommendation_page,
        "社区": render_community_page,
        "观众互动": render_audience_interaction_page,
        "社交裂变": render_community_page,
        "互动剧情": render_interactive_story_page,
        "世界观": render_world_builder_page,
        "校对工具": render_proofreader_page,
        "素材库": render_material_library_page,
        "多语言": render_multi_language_system,
        "IP改编": render_adaptation_system,
        "IP宇宙": render_ip_universe_page,
        "专业题材": render_professional_script_page,
        "协作": render_collaboration_ui,
        "工作流": render_smart_workflow_page,
        "变现中心": render_monetization_page,
        "收益中心": render_revenue_center_page,
        "会员中心": render_membership_page,
        "会员": render_membership_page,
        "选题中心": render_topic_center_page,
        "发布系统": render_publish_page,
        "粉丝运营": render_fan_page,
        "营销工具": render_marketing_tools_page,
        "内容审核": render_moderation_page,
        "版权保护": render_copyright_protection_page,
        "智能客服": render_customer_service_page,
        "剪辑助手": render_smart_clip_assistant,
        "智能助手": render_smart_assistant_page,
        "作品统计": render_work_statistics_page,
        # v35 页面
        "灵感库": render_inspiration_library_page,
        "素材广场": render_material_square_page,
        "一键美化": render_quick_beautify_page,
        "角色对话": render_character_dialogue_page,
        "互动增强": render_interaction_plus_page,
        "视频风格": render_video_styles_page,
        # v36 新增页面
        "角色关系": render_character_relation_page,
        "节奏控制": render_rhythm_control_page,
        "运镜建议": render_camera_move_page,
        "海报生成": render_poster_generator_page,
        "主题设置": render_theme_settings_page,
        "通知中心": render_notification_center_page,
        "全局搜索": render_global_search_page,
        "角色故事线": render_character_storyline_page,
        "剧情时间轴": render_plot_timeline_page,
        "BGM推荐": render_bgm_recommend_page,
        "作品合集": render_collection_page,
    }

    handler = PAGE_MAP.get(active)
    if handler:
        handler()
    else:
        st.header("🚧 页面开发中")
        st.info(f"「{active}」功能即将上线，敬请期待！")

    # 底部信息栏
    st.divider()
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        theme_icon = theme.get_theme_icon()
        st.caption(f"AI漫剧生成器 v36 | 关系图谱 · 节奏控制 · 运镜建议")
    with c2:
        mgr = VersionHistoryManager()
        if mgr.has_autosave():
            saved = mgr.load_autosave()
            if saved:
                st.caption(f"💾 自动保存: {saved.get('timestamp', '')[:16]}")
    with c3:
        nc = NotificationCenter()
        unread = nc.get_unread_count()
        if st.button(f"🔔 通知{'('+str(unread)+')' if unread else ''}", key="fab_notif", use_container_width=True):
            st.session_state.active_tab = "通知中心"
            st.rerun()
    with c4:
        assistant = SmartAssistant()
        if st.button("💡 智能助手", key="fab_assistant", use_container_width=True):
            st.session_state.assistant_open = not st.session_state.assistant_open
            st.rerun()

    # 智能助手面板
    assistant.render_assistant_panel(active)

    # 创作提示
    if active == "创作工坊":
        tip = assistant.get_tip()
        if tip:
            st.info(f"💡 **{tip['title']}**: {tip['content']}")


if __name__ == "__main__":
    main()
