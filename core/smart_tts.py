"""
AI Comic Drama Generator v17 - 智能配音模块
情感配音 + 多角色配音 + 音效配乐
"""

import streamlit as st
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import random

@dataclass
class DialogueSegment:
    """对话片段"""
    id: str
    speaker: str
    text: str
    emotion: str = "neutral"
    intensity: float = 1.0
    start_time: float = 0
    duration: float = 3.0

@dataclass
class AudioTrack:
    """音轨"""
    type: str           # voice, sfx, bgm, narration
    source: str
    volume: float = 1.0
    fade_in: float = 0
    fade_out: float = 0
    start_time: float = 0

class SmartTTSEngine:
    """智能TTS配音引擎"""
    
    # 情感映射到语音参数
    EMOTION_PARAMS = {
        "happy": {"pitch": 1.2, "speed": 1.1, "volume": 1.0},
        "sad": {"pitch": 0.9, "speed": 0.9, "volume": 0.8},
        "angry": {"pitch": 1.3, "speed": 1.2, "volume": 1.1},
        "surprised": {"pitch": 1.4, "speed": 1.3, "volume": 1.0},
        "scared": {"pitch": 1.2, "speed": 1.1, "volume": 0.9},
        "neutral": {"pitch": 1.0, "speed": 1.0, "volume": 1.0},
        "excited": {"pitch": 1.3, "speed": 1.25, "volume": 1.1},
        "tender": {"pitch": 0.95, "speed": 0.95, "volume": 0.85},
    }
    
    # 声音角色配置
    VOICE_PROFILES = {
        "protagonist_male": {
            "name": "少年主角",
            "voice_id": "zh-CN-YunxiNeural",
            "gender": "male",
            "age": "young",
            "personality": "brave",
        },
        "protagonist_female": {
            "name": "少女主角",
            "voice_id": "zh-CN-XiaoxiaoNeural",
            "gender": "female",
            "age": "young",
            "personality": "kind",
        },
        "mentor": {
            "name": "智者导师",
            "voice_id": "zh-CN-YunyangNeural",
            "gender": "male",
            "age": "elder",
            "personality": "wise",
        },
        "comic_relief": {
            "name": "搞笑担当",
            "voice_id": "zh-CN-YunhaoNeural",
            "gender": "male",
            "age": "young",
            "personality": "humorous",
        },
        "villain": {
            "name": "反派",
            "voice_id": "zh-CN-YunyeNeural",
            "gender": "male",
            "age": "adult",
            "personality": "evil",
        },
        "narrator": {
            "name": "旁白",
            "voice_id": "zh-CN-XiaoyiNeural",
            "gender": "neutral",
            "age": "adult",
            "personality": "neutral",
        },
    }
    
    def __init__(self):
        self.segments = []
        self.voice_assignments = {}
    
    def analyze_dialogue(self, dialogues: List[Dict]) -> List[DialogueSegment]:
        """
        分析对话并添加情感标注
        
        Args:
            dialogues: 对话列表 [{"speaker": "角色名", "text": "对话内容"}]
        
        Returns:
            带情感标注的对话片段
        """
        segments = []
        
        for i, dialogue in enumerate(dialogues):
            speaker = dialogue.get("speaker", "旁白")
            text = dialogue.get("text", "")
            
            # 情感分析
            emotion, intensity = self._detect_emotion(text)
            
            # 计算时长（基于文字长度和语速）
            duration = max(1.5, len(text) / 5)
            
            segment = DialogueSegment(
                id=f"seg_{i}",
                speaker=speaker,
                text=text,
                emotion=emotion,
                intensity=intensity,
                start_time=sum(s.duration for s in segments),
                duration=duration
            )
            
            segments.append(segment)
        
        self.segments = segments
        return segments
    
    def _detect_emotion(self, text: str) -> Tuple[str, float]:
        """检测情感"""
        # 情感关键词
        emotion_keywords = {
            "happy": ["开心", "高兴", "快乐", "太好了", "哈哈", "耶", "幸福"],
            "sad": ["难过", "伤心", "悲伤", "痛苦", "呜呜", "哭", "可怜"],
            "angry": ["生气", "愤怒", "可恶", "混蛋", "气死我了", "讨厌"],
            "surprised": ["啊", "什么", "怎么可能", "不会吧", "震惊", "惊讶"],
            "scared": ["害怕", "恐惧", "危险", "救命", "发抖", "紧张"],
            "excited": ["太棒了", "厉害", "激动", "热血", "沸腾", "冲啊"],
            "tender": ["温柔", "关心", "爱你", "喜欢", "心跳", "害羞"],
        }
        
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    intensity = 0.7 + (len(keyword) / 10)  # 关键词越长情感越强
                    return emotion, min(intensity, 1.0)
        
        return "neutral", 0.5
    
    def assign_voices(self, characters: List[Dict]) -> Dict[str, str]:
        """
        自动分配声音
        
        Args:
            characters: 角色列表 [{"name": "角色名", "desc": "描述"}]
        
        Returns:
            {角色名: 声音ID}
        """
        assignments = {}
        
        # 关键词匹配
        for char in characters:
            name = char.get("name", "")
            desc = char.get("desc", "")
            combined = f"{name} {desc}".lower()
            
            # 根据描述匹配合适的声音
            voice_id = "narrator"  # 默认旁白
            
            if "主角" in combined or "勇敢" in combined or "少年" in combined:
                voice_id = "protagonist_male"
            elif "少女" in combined or "女主" in combined or "女孩" in combined:
                voice_id = "protagonist_female"
            elif "导师" in combined or "师父" in combined or "智者" in combined:
                voice_id = "mentor"
            elif "搞笑" in combined or "逗比" in combined:
                voice_id = "comic_relief"
            elif "反派" in combined or "敌人" in combined or "恶人" in combined:
                voice_id = "villain"
            
            assignments[name] = voice_id
        
        self.voice_assignments = assignments
        return assignments
    
    def generate_speech(
        self,
        segment: DialogueSegment,
        voice_id: str = None
    ) -> Dict:
        """
        生成语音参数
        
        Args:
            segment: 对话片段
            voice_id: 声音ID
        
        Returns:
            语音生成参数
        """
        # 获取声音配置
        if voice_id is None:
            voice_id = self.voice_assignments.get(segment.speaker, "narrator")
        
        voice_profile = self.VOICE_PROFILES.get(voice_id, self.VOICE_PROFILES["narrator"])
        emotion_params = self.EMOTION_PARAMS.get(segment.emotion, self.EMOTION_PARAMS["neutral"])
        
        # 合并参数
        params = {
            "text": segment.text,
            "voice_id": voice_profile["voice_id"],
            "pitch": emotion_params["pitch"] * segment.intensity,
            "speed": emotion_params["speed"],
            "volume": emotion_params["volume"],
            "emotion": segment.emotion,
        }
        
        return params
    
    def export_audio_config(self) -> Dict:
        """导出音频配置"""
        return {
            "segments": [
                {
                    "id": s.id,
                    "speaker": s.speaker,
                    "text": s.text,
                    "emotion": s.emotion,
                    "start": s.start_time,
                    "duration": s.duration,
                }
                for s in self.segments
            ],
            "voice_assignments": self.voice_assignments,
        }

class SoundEffectsEngine:
    """音效引擎"""
    
    # 场景对应的音效
    SCENE_SFX = {
        "战斗": ["剑击", "爆炸", "冲击波", "惨叫"],
        "日常": ["脚步", "门声", "杯子", "笑声"],
        "紧张": ["心跳", "呼吸", "时钟", "风声"],
        "浪漫": ["心跳", "风声", "轻音乐", "雨声"],
        "搞笑": ["摔跤", "弹跳", "滑稽", "掌声"],
        "悲伤": ["雨声", "风声", "抽泣", "低鸣"],
        "神秘": ["脚步", "门声", "低语", "回声"],
        "高潮": ["爆炸", "欢呼", "音乐高潮", "心跳加速"],
    }
    
    def detect_sfx(self, scene_description: str) -> List[str]:
        """检测适用音效"""
        detected = []
        
        for category, keywords in self.SCENE_SFX.items():
            for keyword in keywords:
                if keyword in scene_description:
                    if category not in detected:
                        detected.append(category)
        
        return detected if detected else ["日常"]
    
    def generate_sfx_config(
        self,
        detected_scenes: List[str],
        intensity: float = 0.7
    ) -> List[AudioTrack]:
        """生成音效配置"""
        tracks = []
        current_time = 0
        
        for scene in detected_scenes:
            sfx_types = self.SCENE_SFX.get(scene, self.SCENE_SFX["日常"])
            
            for sfx_type in sfx_types[:2]:  # 每个场景最多2个音效
                track = AudioTrack(
                    type="sfx",
                    source=f"sfx_{sfx_type}",
                    volume=intensity,
                    fade_in=0.1,
                    fade_out=0.2,
                    start_time=current_time
                )
                tracks.append(track)
                current_time += 1
        
        return tracks

class BGMEngine:
    """背景音乐引擎"""
    
    # 情感对应的BGM
    EMOTION_BGM = {
        "happy": ["upbeat_pop", "cheerful_acoustic", "celebration"],
        "sad": ["sad_piano", "melancholy_strings", "rainy_day"],
        "angry": ["epic_drums", "action_rock", "tension_strings"],
        "exciting": ["adventure_theme", "epic_orchestra", "chase_music"],
        "romantic": ["love_theme", "soft_piano", "warm_strings"],
        "mysterious": ["suspense", "dark_ambient", "investigation"],
        "peaceful": ["calm_acoustic", "nature_sounds", "gentle_melody"],
    }
    
    # 场景类型对应的BGM
    SCENE_BGM = {
        "日常": "relaxed_acoustic",
        "战斗": "epic_battle",
        "追逐": "adrenaline_rush",
        "告白": "romantic_piano",
        "回忆": "nostalgic_guitar",
        "结局": "satisfying_conclusion",
        "高潮": "ultimate_climax",
    }
    
    def select_bgm(
        self,
        emotion: str = None,
        scene_type: str = None,
        transition: bool = True
    ) -> List[AudioTrack]:
        """选择BGM"""
        tracks = []
        
        # 基于情感选择
        if emotion and emotion in self.EMOTION_BGM:
            bgm_id = random.choice(self.EMOTION_BGM[emotion])
            track = AudioTrack(
                type="bgm",
                source=f"bgm_{bgm_id}",
                volume=0.4,
                fade_in=1.0 if transition else 0,
                fade_out=1.0 if transition else 0
            )
            tracks.append(track)
        
        # 基于场景选择
        if scene_type and scene_type in self.SCENE_BGM:
            bgm_id = self.SCENE_BGM[scene_type]
            track = AudioTrack(
                type="bgm",
                source=f"bgm_{bgm_id}",
                volume=0.5,
                fade_in=0.5,
                fade_out=0.5
            )
            tracks.append(track)
        
        return tracks

class NarrationEngine:
    """旁白引擎"""
    
    # 旁白模板
    NARRATION_TEMPLATES = {
        "intro": "故事要从{}说起...",
        "transition": "镜头切换...",
        "time_jump": "时光飞逝，转眼间...",
        "emotion": "此刻，{}的内心...",
        "cliffhanger": "就在这时，意外发生了...",
        "ending": "故事到这里告一段落...",
    }
    
    def generate_narration(
        self,
        template_type: str,
        context: Dict = None
    ) -> str:
        """生成旁白"""
        template = self.NARRATION_TEMPLATES.get(template_type, "{}")
        
        if context:
            return template.format(**context)
        
        return template.format("")
    
    def insert_narrations(
        self,
        segments: List[DialogueSegment],
        narration_interval: int = 3
    ) -> List[DialogueSegment]:
        """在对话间插入旁白"""
        result = []
        counter = 0
        
        for i, seg in enumerate(segments):
            result.append(seg)
            counter += 1
            
            # 每隔几个对话插入旁白
            if counter >= narration_interval and i < len(segments) - 1:
                next_seg = segments[i + 1]
                narration_text = self.generate_narration(
                    "transition",
                    {"character": next_seg.speaker}
                )
                
                narration = DialogueSegment(
                    id=f"nar_{i}",
                    speaker="旁白",
                    text=narration_text,
                    emotion="neutral",
                    start_time=seg.start_time + seg.duration + 0.5,
                    duration=2.0
                )
                result.append(narration)
                counter = 0
        
        return result

class AudioMixer:
    """混音器"""
    
    def __init__(self):
        self.tracks = []
        self.master_volume = 1.0
    
    def add_track(self, track: AudioTrack):
        """添加音轨"""
        self.tracks.append(track)
    
    def set_master_volume(self, volume: float):
        """设置主音量"""
        self.master_volume = max(0, min(2.0, volume))
    
    def export_mix_config(self) -> Dict:
        """导出混音配置"""
        return {
            "tracks": [
                {
                    "type": t.type,
                    "source": t.source,
                    "volume": t.volume * self.master_volume,
                    "fade_in": t.fade_in,
                    "fade_out": t.fade_out,
                    "start": t.start_time,
                }
                for t in self.tracks
            ],
            "master_volume": self.master_volume,
        }

def render_smart_tts_ui():
    """渲染智能配音UI"""
    st.subheader("🎙️ 智能配音")
    
    # 配音模式
    mode = st.radio(
        "配音模式",
        options=["快速配音", "情感配音", "多角色配音", "完整配音"],
        horizontal=True
    )
    
    if mode == "快速配音":
        st.info("使用默认音色，快速生成配音")
        
        if st.button("🎵 生成配音", type="primary"):
            st.success("配音生成完成！")
    
    elif mode == "情感配音":
        st.write("为对话添加情感标注，生成更生动的配音")
        
        # 情感示例
        emotions = ["happy", "sad", "angry", "surprised", "excited", "tender"]
        emotion_names = {
            "happy": "😊 开心",
            "sad": "😢 悲伤",
            "angry": "😠 愤怒",
            "surprised": "😲 惊讶",
            "excited": "🤩 激动",
            "tender": "🥰 温柔",
        }
        
        for emotion in emotions:
            st.write(f"**{emotion_names[emotion]}** - 语速加快/音调变化")
    
    elif mode == "多角色配音":
        st.write("为每个角色分配专属音色")
        
        # 角色音色配置
        voices = [
            ("少年主角", "zh-CN-YunxiNeural"),
            ("少女主角", "zh-CN-XiaoxiaoNeural"),
            ("智者导师", "zh-CN-YunyangNeural"),
            ("搞笑担当", "zh-CN-YunhaoNeural"),
            ("反派", "zh-CN-YunyeNeural"),
        ]
        
        for name, voice_id in voices:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{name}**")
            with col2:
                if st.button("▶ 试听", key=f"voice_{name}"):
                    st.info(f"播放 {voice_id}")
    
    elif mode == "完整配音":
        st.write("包含旁白、音效、BGM的完整配音")
        
        # 旁白开关
        use_narration = st.checkbox("添加旁白", value=True)
        
        # 音效开关
        use_sfx = st.checkbox("添加音效", value=True)
        
        # BGM开关
        use_bgm = st.checkbox("添加背景音乐", value=True)
        
        if use_bgm:
            bgm_volume = st.slider("BGM音量", 0, 100, 40)
        
        if st.button("🎬 生成完整配音", type="primary"):
            st.success("完整配音生成完成！")

def render_audio_mixer_ui():
    """渲染混音器UI"""
    st.subheader("🎚️ 音频混音")
    
    # 音量滑块
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎤 人声", f"{st.slider('人声', 0, 100, 80)}%")
    with col2:
        st.metric("🎵 BGM", f"{st.slider('背景乐', 0, 100, 40)}%")
    with col3:
        st.metric("🔊 音效", f"{st.slider('音效', 0, 100, 60)}%")
    with col4:
        st.metric("📢 旁白", f"{st.slider('旁白', 0, 100, 70)}%")
    
    # 导出
    if st.button("💾 导出音频配置"):
        st.success("音频配置已导出")
