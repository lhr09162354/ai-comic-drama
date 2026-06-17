"""
智能素材库系统 v23
角色素材、场景素材、配乐素材、特效素材、模板素材
"""

import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class MaterialType(Enum):
    """素材类型"""
    CHARACTER = "character"     # 角色素材
    SCENE = "scene"           # 场景素材
    BGM = "bgm"              # 背景音乐
    SFX = "sfx"              # 音效
    EFFECT = "effect"         # 特效
    TEMPLATE = "template"     # 模板
    FONT = "font"             # 字体
    STICKER = "sticker"       # 贴纸
    VECTOR = "vector"         # 矢量素材

class SceneCategory(Enum):
    """场景分类"""
    INDOOR = "indoor"         # 室内
    OUTDOOR = "outdoor"       # 户外
    FANTASY = "fantasy"       # 奇幻
    SCI_FI = "sci_fi"         # 科幻
    HISTORICAL = "historical" # 历史
    MODERN = "modern"         # 现代
    SCHOOL = "school"         # 校园
    URBAN = "urban"          # 都市

class Mood(Enum):
    """情绪分类"""
    HAPPY = "happy"           # 开心
    SAD = "sad"              # 悲伤
    TENSE = "tense"          # 紧张
    ROMANTIC = "romantic"    # 浪漫
    EPIC = "epic"            # 史诗
    MYSTERIOUS = "mysterious" # 神秘
    FUNNY = "funny"          # 搞笑
    PEACEFUL = "peaceful"    # 平静

@dataclass
class Material:
    """素材基类"""
    id: str = ""
    name: str = ""
    material_type: MaterialType = MaterialType.CHARACTER
    tags: List[str] = field(default_factory=list)
    category: str = ""
    description: str = ""
    thumbnail: str = ""
    preview_url: str = ""
    source_url: str = ""
    license: str = "CC0"  # CC0, CC-BY, Commercial
    author: str = ""
    download_count: int = 0
    favorite_count: int = 0
    rating: float = 4.0
    created_at: datetime = field(default_factory=datetime.now)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

@dataclass
class CharacterMaterial(Material):
    """角色素材"""
    pose: str = ""            # 姿势
    expression: str = ""      # 表情
    outfit: str = ""          # 服装
    age_group: str = ""       # 年龄层
    gender: str = ""          # 性别
    style: str = ""           # 画风
    has_color: bool = True
    has_transparent: bool = False

    def __post_init__(self):
        self.material_type = MaterialType.CHARACTER

@dataclass
class SceneMaterial(Material):
    """场景素材"""
    scene_category: SceneCategory = SceneCategory.MODERN
    has_foreground: bool = True
    has_background: bool = True
    has_transparent: bool = False
    perspective: str = "front"  # front, side, top, 3d
    time_of_day: str = "day"  # day, night, dawn, dusk
    weather: str = "clear"    # clear, rainy, snowy, cloudy

    def __post_init__(self):
        self.material_type = MaterialType.SCENE

@dataclass
class BGMaterial(Material):
    """背景音乐素材"""
    duration: int = 0         # 秒
    bpm: int = 0             # 节拍
    mood: Mood = Mood.HAPPY
    instruments: List[str] = field(default_factory=list)
    has_loop: bool = True
    has_intro: bool = False

    def __post_init__(self):
        self.material_type = MaterialType.BGM

@dataclass
class SFXMaterial(Material):
    """音效素材"""
    duration: int = 0
    sfx_category: str = ""    # battle, nature, ui, human, etc.
    has_variations: int = 1

    def __post_init__(self):
        self.material_type = MaterialType.SFX

@dataclass
class TemplateMaterial(Material):
    """模板素材"""
    template_category: str = ""  # layout, style, story, etc.
    panels_count: int = 0
    color_scheme: str = ""
    is_animation: bool = False

    def __post_init__(self):
        self.material_type = MaterialType.TEMPLATE

class MaterialLibrary:
    """素材库"""
    
    def __init__(self):
        self.materials: Dict[str, Material] = {}
        self.collections: Dict[str, List[str]] = {}  # collection_id -> material_ids
        self.favorites: Dict[str, List[str]] = {}  # user_id -> material_ids
        self.download_history: List[Dict] = []
        
        # 初始化示例素材
        self._init_sample_materials()
    
    def _init_sample_materials(self):
        """初始化示例素材"""
        # 角色素材
        for i in range(10):
            char = CharacterMaterial(
                id=f"char_{i+1}",
                name=f"角色素材 {i+1}",
                tags=["免费", "通用", "站立"],
                description=f"高清角色立绘素材 {i+1}",
                pose=["standing", "sitting", "running"][i % 3],
                expression=["happy", "serious", "surprised"][i % 3],
                outfit=["casual", "formal", "fantasy"][i % 3],
                rating=4.0 + (i % 10) * 0.1
            )
            self.materials[char.id] = char
        
        # 场景素材
        for i in range(12):
            scene = SceneMaterial(
                id=f"scene_{i+1}",
                name=f"场景 {i+1}",
                tags=["免费", "室内", "温馨"],
                description=f"精美场景素材 {i+1}",
                scene_category=SceneCategory(list(SceneCategory)[i % 8]),
                time_of_day=["day", "night", "dusk"][i % 3],
                weather=["clear", "rainy"][i % 2],
                rating=4.2 + (i % 10) * 0.08
            )
            self.materials[scene.id] = scene
        
        # BGM素材
        moods = [Mood.HAPPY, Mood.SAD, Mood.TENSE, Mood.ROMANTIC, Mood.EPIC, Mood.MYSTERIOUS]
        for i, mood in enumerate(moods):
            bgm = BGMaterial(
                id=f"bgm_{i+1}",
                name=f"{mood.value} 背景音乐 {i+1}",
                tags=["免费", "原创", mood.value],
                description=f"适合{mood.value}场景的背景音乐",
                duration=random.randint(60, 180),
                bpm=random.randint(60, 140),
                mood=mood,
                instruments=["钢琴", "吉他", "弦乐", "电子"][i % 4].split(),
                rating=4.5 + (i % 5) * 0.1
            )
            self.materials[bgm.id] = bgm
        
        # 音效素材
        categories = ["战斗", "自然", "UI", "人物", "机械", "魔法"]
        for i, cat in enumerate(categories):
            sfx = SFXMaterial(
                id=f"sfx_{i+1}",
                name=f"{cat}音效包",
                tags=["免费", "音效", cat],
                description=f"精选{cat}类音效素材",
                duration=random.randint(1, 10),
                sfx_category=cat,
                has_variations=random.randint(3, 8),
                rating=4.3 + (i % 10) * 0.07
            )
            self.materials[sfx.id] = sfx
    
    def search(self, query: str = "", material_type: Optional[MaterialType] = None,
               tags: Optional[List[str]] = None, limit: int = 20) -> List[Material]:
        """搜索素材"""
        results = []
        
        for mat in self.materials.values():
            # 类型过滤
            if material_type and mat.material_type != material_type:
                continue
            
            # 标签过滤
            if tags:
                if not any(tag in mat.tags for tag in tags):
                    continue
            
            # 关键词搜索
            if query:
                query_lower = query.lower()
                if (query_lower not in mat.name.lower() and 
                    query_lower not in mat.description.lower() and
                    not any(query_lower in tag.lower() for tag in mat.tags)):
                    continue
            
            results.append(mat)
        
        # 排序：优先按评分，其次按下载量
        results.sort(key=lambda x: (x.rating, x.download_count), reverse=True)
        
        return results[:limit]
    
    def get_by_type(self, material_type: MaterialType) -> List[Material]:
        """按类型获取素材"""
        return [m for m in self.materials.values() if m.material_type == material_type]
    
    def get_hot(self, material_type: Optional[MaterialType] = None, limit: int = 10) -> List[Material]:
        """获取热门素材"""
        materials = self.get_by_type(material_type) if material_type else list(self.materials.values())
        return sorted(materials, key=lambda x: x.download_count, reverse=True)[:limit]
    
    def get_recommendations(self, user_id: str, material_type: Optional[MaterialType] = None, limit: int = 6) -> List[Material]:
        """获取推荐素材（基于历史）"""
        # 简化版：随机推荐
        materials = self.get_by_type(material_type) if material_type else list(self.materials.values())
        return random.sample(materials, min(limit, len(materials)))
    
    def add_to_favorites(self, user_id: str, material_id: str) -> bool:
        """添加收藏"""
        if user_id not in self.favorites:
            self.favorites[user_id] = []
        if material_id not in self.favorites[user_id]:
            self.favorites[user_id].append(material_id)
            self.materials[material_id].favorite_count += 1
            return True
        return False
    
    def remove_from_favorites(self, user_id: str, material_id: str) -> bool:
        """取消收藏"""
        if user_id in self.favorites and material_id in self.favorites[user_id]:
            self.favorites[user_id].remove(material_id)
            self.materials[material_id].favorite_count = max(0, self.materials[material_id].favorite_count - 1)
            return True
        return False
    
    def get_favorites(self, user_id: str) -> List[Material]:
        """获取收藏列表"""
        if user_id not in self.favorites:
            return []
        return [self.materials[mid] for mid in self.favorites[user_id] if mid in self.materials]
    
    def record_download(self, user_id: str, material_id: str):
        """记录下载"""
        if material_id in self.materials:
            self.materials[material_id].download_count += 1
            self.download_history.append({
                "user_id": user_id,
                "material_id": material_id,
                "timestamp": datetime.now()
            })
    
    def create_collection(self, collection_id: str, name: str, material_ids: List[str] = None):
        """创建素材集"""
        self.collections[collection_id] = material_ids or []
    
    def add_to_collection(self, collection_id: str, material_id: str):
        """添加素材到集"""
        if collection_id not in self.collections:
            self.collections[collection_id] = []
        if material_id not in self.collections[collection_id]:
            self.collections[collection_id].append(material_id)

class MaterialLibraryUI:
    """素材库UI"""
    
    def __init__(self, library: MaterialLibrary):
        self.library = library
    
    def render_material_card(self, material: Material, cols=None):
        """渲染素材卡片"""
        if cols:
            with cols:
                return self._render_card_content(material)
        else:
            return self._render_card_content(material)
    
    def _render_card_content(self, material: Material) -> bool:
        """渲染卡片内容，返回是否被选中"""
        with st.container():
            # 缩略图区域
            st.image(f"https://picsum.photos/200/150?random={material.id}", use_container_width=True)
            
            # 素材信息
            st.write(f"**{material.name}**")
            st.caption(f"⭐ {material.rating:.1f} | 📥 {material.download_count}")
            
            # 标签
            tag_str = " ".join([f"#{t}" for t in material.tags[:3]])
            st.caption(tag_str)
            
            # 操作按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾", key=f"dl_{material.id}", use_container_width=True):
                    self.library.record_download("current_user", material.id)
                    st.success("已下载!")
                    return True
            with col2:
                if st.button("❤️", key=f"fav_{material.id}", use_container_width=True):
                    self.library.add_to_favorites("current_user", material.id)
                    st.success("已收藏!")
                    return True
        
        return False
    
    def render_search_bar(self):
        """渲染搜索栏"""
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            query = st.text_input("🔍 搜索素材", placeholder="输入关键词...", key="material_search")
        with col2:
            sort_by = st.selectbox("排序", ["评分", "下载量", "最新"], key="material_sort")
        with col3:
            filter_license = st.selectbox("许可", ["全部", "免费", "商用"], key="material_license")
        
        return query, sort_by, filter_license
    
    def render_filter_panel(self):
        """渲染筛选面板"""
        with st.expander("🔽 筛选条件", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**类型**")
                type_filter = st.multiselect(
                    "素材类型",
                    [t.value for t in MaterialType],
                    default=[]
                )
            
            with col2:
                st.write("**标签**")
                tag_filter = st.multiselect(
                    "热门标签",
                    ["免费", "原创", "高清", "商用", "热门"],
                    default=[]
                )
            
            with col3:
                st.write("**排序**")
                sort_filter = st.radio(
                    "排序方式",
                    ["评分优先", "下载量优先", "最新优先"]
                )
        
        return type_filter, tag_filter, sort_filter
    
    def render_character_materials(self):
        """渲染角色素材"""
        st.subheader("👥 角色素材")
        
        chars = self.library.get_by_type(MaterialType.CHARACTER)
        if not chars:
            st.info("暂无角色素材")
            return
        
        cols = st.columns(5)
        for i, char in enumerate(chars[:10]):
            self.render_material_card(char, cols[i % 5])
    
    def render_scene_materials(self):
        """渲染场景素材"""
        st.subheader("🏠 场景素材")
        
        scenes = self.library.get_by_type(MaterialType.SCENE)
        if not scenes:
            st.info("暂无场景素材")
            return
        
        cols = st.columns(4)
        for i, scene in enumerate(scenes[:8]):
            self.render_material_card(scene, cols[i % 4])
    
    def render_bgm_materials(self):
        """渲染BGM素材"""
        st.subheader("🎵 背景音乐")
        
        bgms = self.library.get_by_type(MaterialType.BGM)
        if not bgms:
            st.info("暂无BGM素材")
            return
        
        cols = st.columns(3)
        for i, bgm in enumerate(bgms):
            with cols[i % 3]:
                st.write(f"🎵 **{bgm.name}**")
                st.caption(f"⏱️ {bgm.duration}秒 | 🎯 {bgm.mood.value}")
                st.caption(f"⭐ {bgm.rating:.1f} | 📥 {bgm.download_count}")
                
                if st.button("▶️ 试听", key=f"play_{bgm.id}", use_container_width=True):
                    st.info(f"正在播放: {bgm.name}")
                
                if st.button("💾 下载", key=f"dlbgm_{bgm.id}", use_container_width=True):
                    self.library.record_download("current_user", bgm.id)
                    st.success("已下载!")
    
    def render_sfx_materials(self):
        """渲染音效素材"""
        st.subheader("🔊 音效素材")
        
        sfxs = self.library.get_by_type(MaterialType.SFX)
        if not sfxs:
            st.info("暂无音效素材")
            return
        
        cols = st.columns(3)
        for i, sfx in enumerate(sfxs):
            with cols[i % 3]:
                with st.container():
                    st.write(f"🔊 **{sfx.name}**")
                    st.caption(f"📁 {sfx.sfx_category} | 🎯 {sfx.has_variations}种变体")
                    st.caption(f"⭐ {sfx.rating:.1f} | 📥 {sfx.download_count}")
                    
                    if st.button("🔊 试听", key=f"sfxplay_{sfx.id}"):
                        st.info(f"正在播放: {sfx.name}")
                    
                    if st.button("💾 下载", key=f"sfxdl_{sfx.id}"):
                        self.library.record_download("current_user", sfx.id)
                        st.success("已下载!")
    
    def render_favorites(self):
        """渲染收藏"""
        st.subheader("❤️ 我的收藏")
        
        favorites = self.library.get_favorites("current_user")
        
        if not favorites:
            st.info("暂无收藏，快去发现喜欢的素材吧!")
            return
        
        cols = st.columns(4)
        for i, mat in enumerate(favorites):
            with cols[i % 4]:
                self.render_material_card(mat)
                if st.button("❌ 取消收藏", key=f"unfav_{mat.id}"):
                    self.library.remove_from_favorites("current_user", mat.id)
                    st.rerun()
    
    def render_hot_materials(self):
        """渲染热门素材"""
        st.subheader("🔥 热门素材")
        
        hot = self.library.get_hot(limit=6)
        
        cols = st.columns(6)
        for i, mat in enumerate(hot):
            with cols[i % 6]:
                st.write(f"**{i+1}.** {mat.name}")
                st.caption(f"📥 {mat.download_count}")
    
    def render_full_ui(self):
        """渲染完整UI"""
        st.subheader("📚 素材库 v23")
        
        # 搜索栏
        query, sort_by, filter_license = self.render_search_bar()
        
        # 类型标签
        tabs = st.tabs(["全部", "👥 角色", "🏠 场景", "🎵 BGM", "🔊 音效", "❤️ 收藏"])
        
        with tabs[0]:
            # 全部素材
            materials = self.library.search(query=query)
            
            if not materials:
                st.info("没有找到匹配的素材")
            else:
                cols = st.columns(5)
                for i, mat in enumerate(materials[:20]):
                    self.render_material_card(mat, cols[i % 5])
        
        with tabs[1]:
            self.render_character_materials()
        
        with tabs[2]:
            self.render_scene_materials()
        
        with tabs[3]:
            self.render_bgm_materials()
        
        with tabs[4]:
            self.render_sfx_materials()
        
        with tabs[5]:
            self.render_favorites()
        
        # 热门素材
        st.divider()
        self.render_hot_materials()
        
        # 上传素材
        st.divider()
        with st.expander("⬆️ 上传素材", expanded=False):
            st.write("**上传你的原创素材**")
            
            col1, col2 = st.columns(2)
            with col1:
                upload_name = st.text_input("素材名称")
                upload_type = st.selectbox("素材类型", [t.value for t in MaterialType])
                upload_tags = st.text_input("标签（用逗号分隔）")
            
            with col2:
                upload_desc = st.text_area("素材描述")
                upload_license = st.selectbox("授权类型", ["CC0", "CC-BY", "商用"])
            
            uploaded_file = st.file_uploader("上传文件", type=["png", "jpg", "mp3", "wav"])
            
            if st.button("上传素材", type="primary"):
                st.success("素材上传成功!")
                st.info("审核通过后将显示在素材库中")

# 全局实例
material_library = MaterialLibrary()

def get_material_library() -> MaterialLibrary:
    """获取素材库"""
    return material_library
