# -*- coding: utf-8 -*-
"""
多角色配音系统 - 多种音色、情感配音、角色语音管理
v27 新增功能
"""
import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

class MultiCharacterVoiceSystem:
    """多角色配音系统"""
    
    def __init__(self):
        # 音色库
        self.voice_profiles = {
            # 男声
            "磁性的": {
                "type": "male",
                "traits": ["低沉", "磁性", "成熟", "稳重"],
                "use_cases": ["男主角", "旁白", "反派"],
                "pitch_range": (60, 150),
                "speed": "slow"
            },
            "阳光的": {
                "type": "male",
                "traits": ["明亮", "活力", "年轻", "热血"],
                "use_cases": ["少年主角", "喜剧角色", "正面人物"],
                "pitch_range": (150, 250),
                "speed": "fast"
            },
            "成熟的": {
                "type": "male",
                "traits": ["深沉", "稳重", "睿智", "权威"],
                "use_cases": ["父亲", "导师", "领袖"],
                "pitch_range": (80, 160),
                "speed": "medium"
            },
            "反派腔": {
                "type": "male",
                "traits": ["阴险", "冷酷", "嘲讽", "危险"],
                "use_cases": ["反派", "阴谋家", "恶棍"],
                "pitch_range": (100, 180),
                "speed": "slow"
            },
            # 女声
            "甜美的": {
                "type": "female",
                "traits": ["温柔", "甜美", "亲切", "可爱"],
                "use_cases": ["女主角", "萝莉", "治愈系"],
                "pitch_range": (200, 350),
                "speed": "medium"
            },
            "御姐音": {
                "type": "female",
                "traits": ["成熟", "冷静", "知性", "优雅"],
                "use_cases": ["御姐角色", "女强人", "女王"],
                "pitch_range": (180, 300),
                "speed": "slow"
            },
            "少女音": {
                "type": "female",
                "traits": ["活泼", "俏皮", "元气", "天真"],
                "use_cases": ["少女", "元气角色", "萌系"],
                "pitch_range": (220, 380),
                "speed": "fast"
            },
            "神秘感": {
                "type": "female",
                "traits": ["神秘", "空灵", "冷淡", "疏离"],
                "use_cases": ["神秘角色", "反派", "女王"],
                "pitch_range": (160, 280),
                "speed": "slow"
            },
            # 特殊音色
            "大叔音": {
                "type": "male",
                "traits": ["沧桑", "粗犷", "豪放", "江湖"],
                "use_cases": ["江湖人士", "老兵", "硬汉"],
                "pitch_range": (70, 140),
                "speed": "slow"
            },
            "正太音": {
                "type": "male",
                "traits": ["稚嫩", "天真", "可爱", "活泼"],
                "use_cases": ["正太", "小男孩", "儿童"],
                "pitch_range": (280, 420),
                "speed": "fast"
            }
        }
        
        # 情感配音配置
        self.emotion_configs = {
            "normal": {"pitch_shift": 0, "speed_mult": 1.0, "volume": 1.0},
            "happy": {"pitch_shift": 50, "speed_mult": 1.1, "volume": 1.0},
            "sad": {"pitch_shift": -30, "speed_mult": 0.85, "volume": 0.9},
            "angry": {"pitch_shift": 20, "speed_mult": 1.3, "volume": 1.1},
            "fear": {"pitch_shift": 80, "speed_mult": 1.5, "volume": 0.95},
            "surprised": {"pitch_shift": 100, "speed_mult": 1.2, "volume": 1.0},
            "whisper": {"pitch_shift": -50, "speed_mult": 0.7, "volume": 0.6},
            "shout": {"pitch_shift": 30, "speed_mult": 1.4, "volume": 1.3},
            "laugh": {"pitch_shift": 60, "speed_mult": 1.1, "volume": 1.0},
            "cry": {"pitch_shift": -40, "speed_mult": 0.8, "volume": 0.85}
        }
        
    def get_voice_profile(self, voice_name: str) -> Dict:
        """获取音色配置"""
        return self.voice_profiles.get(voice_name, self.voice_profiles["磁性的"])
    
    def generate_voice_config(self, character: Dict) -> Dict:
        """为角色生成配音配置"""
        base_voice = character.get("preferred_voice", "磁性的")
        voice_profile = self.get_voice_profile(base_voice)
        
        return {
            "character_id": character.get("id"),
            "character_name": character.get("name"),
            "voice_type": base_voice,
            "voice_profile": voice_profile,
            "emotions": self.emotion_configs,
            "recommended_settings": {
                "pitch": voice_profile["pitch_range"][0],
                "speed": voice_profile["speed"],
                "volume": 1.0,
                "reverb": 0.2 if voice_profile["type"] == "female" else 0.1,
                "echo": 0.1
            }
        }
    
    def assign_voice_to_character(self, character: Dict, available_voices: List[str]) -> Dict:
        """为角色分配最合适的音色"""
        # 根据角色特征匹配合适音色
        character_traits = character.get("traits", [])
        character_type = character.get("type", "neutral")
        
        best_match = None
        best_score = 0
        
        for voice_name in available_voices:
            voice = self.voice_profiles.get(voice_name)
            if not voice:
                continue
                
            # 计算匹配度
            score = 0
            for trait in character_traits:
                if trait in voice["traits"]:
                    score += 2
                    
            if character_type in voice["use_cases"]:
                score += 3
                
            if score > best_score:
                best_score = score
                best_match = voice_name
                
        return {
            "character_id": character.get("id"),
            "assigned_voice": best_match or "磁性的",
            "confidence": best_score / 10 if best_score > 0 else 0.5,
            "alternative_voices": available_voices[:3]
        }
    
    def generate_emotion_voice(self, text: str, base_voice: str, emotion: str) -> Dict:
        """生成带情感的配音参数"""
        voice_config = self.get_voice_profile(base_voice)
        emotion_config = self.emotion_configs.get(emotion, self.emotion_configs["normal"])
        
        # 计算实际音高
        base_pitch = voice_config["pitch_range"][0]
        pitch_shift = emotion_config["pitch_shift"]
        actual_pitch = base_pitch + pitch_shift
        
        # 限制在范围内
        actual_pitch = max(voice_config["pitch_range"][0], 
                          min(voice_config["pitch_range"][1], actual_pitch))
        
        return {
            "text": text,
            "voice": base_voice,
            "emotion": emotion,
            "parameters": {
                "pitch": actual_pitch,
                "speed": emotion_config["speed_mult"],
                "volume": emotion_config["volume"],
                "pitch_shift_hz": pitch_shift,
                "duration_estimate": len(text) * 0.3 * emotion_config["speed_mult"]
            },
            "effects": self._get_effect_for_emotion(emotion),
            "voice_samples": self._generate_samples(text, emotion)
        }
    
    def _get_effect_for_emotion(self, emotion: str) -> List[str]:
        """获取情感对应的音效效果"""
        effects_map = {
            "normal": [],
            "happy": ["slight_reverb", "warm EQ"],
            "sad": ["heavy_reverb", "low_pass_filter"],
            "angry": ["compression", "harsh EQ"],
            "fear": ["high_reverb", "tremolo"],
            "surprised": ["brief_reverb", "slight_distortion"],
            "whisper": ["noise_gate", "isolated"],
            "shout": ["compression", "slight_distortion", "no_reverb"],
            "laugh": ["natural_room_reverb"],
            "cry": ["heavy_reverb", "soft_eq"]
        }
        return effects_map.get(emotion, [])
    
    def _generate_samples(self, text: str, emotion: str) -> List[Dict]:
        """生成示例音频片段"""
        samples = []
        
        # 模拟生成3个不同强度的样本
        for i in range(3):
            intensity = (i + 1) * 33  # 33%, 66%, 100%
            samples.append({
                "sample_id": f"sample_{i+1}",
                "text": text[:min(20, len(text))] + "...",
                "emotion_intensity": intensity,
                "audio_url": f"/audio_samples/{emotion}_{intensity}.mp3",
                "duration": len(text) * 0.3 * (1 + i*0.1)
            })
            
        return samples
    
    def batch_generate_dialogue(self, dialogues: List[Dict]) -> List[Dict]:
        """批量生成对话配音"""
        generated = []
        
        for dialogue in dialogues:
            character = dialogue.get("character", {})
            text = dialogue.get("text", "")
            emotion = dialogue.get("emotion", "normal")
            base_voice = character.get("preferred_voice", "磁性的")
            
            voice_params = self.generate_emotion_voice(text, base_voice, emotion)
            
            generated.append({
                "dialogue_id": dialogue.get("id", len(generated)),
                "character": character.get("name"),
                "text": text,
                "emotion": emotion,
                "voice_params": voice_params,
                "timeline": {
                    "start": dialogue.get("start_time", 0),
                    "end": dialogue.get("start_time", 0) + voice_params["parameters"]["duration_estimate"]
                },
                "priority": dialogue.get("priority", "normal")
            })
            
        return generated
    
    def mix_voice_tracks(self, dialogues: List[Dict]) -> Dict:
        """混合多条配音轨道"""
        tracks = []
        
        for dialogue in dialogues:
            tracks.append({
                "character": dialogue.get("character", {}).get("name", "Unknown"),
                "voice": dialogue.get("voice_params", {}).get("voice", "默认"),
                "emotion": dialogue.get("emotion", "normal"),
                "start": dialogue.get("timeline", {}).get("start", 0),
                "duration": dialogue.get("voice_params", {}).get("parameters", {}).get("duration_estimate", 0),
                "volume": dialogue.get("voice_params", {}).get("parameters", {}).get("volume", 1.0)
            })
            
        # 检测重叠
        overlaps = []
        for i, track1 in enumerate(tracks):
            for j, track2 in enumerate(tracks):
                if i < j:
                    if track1["start"] < track2["start"] + track2["duration"] and \
                       track2["start"] < track1["start"] + track1["duration"]:
                        overlaps.append({
                            "track1": track1["character"],
                            "track2": track2["character"],
                            "overlap_duration": min(track1["start"] + track1["duration"],
                                                   track2["start"] + track2["duration"]) - max(track1["start"], track2["start"])
                        })
                        
        return {
            "tracks": tracks,
            "total_tracks": len(tracks),
            "total_duration": max((t["start"] + t["duration"]) for t in tracks) if tracks else 0,
            "overlaps": overlaps,
            "mix_settings": {
                "auto_ducking": True,
                "fade_duration": 0.5,
                "compression": True
            }
        }

class VoiceCharacterManager:
    """配音角色管理器"""
    
    def __init__(self):
        self.characters = []
        
    def create_voice_character(self, name: str, role_type: str, traits: List[str]) -> Dict:
        """创建配音角色"""
        character = {
            "id": len(self.characters) + 1,
            "name": name,
            "role_type": role_type,
            "traits": traits,
            "preferred_voice": self._recommend_voice(role_type, traits),
            "emotion_defaults": self._get_default_emotions(role_type),
            "lines": [],
            "total_duration": 0
        }
        
        self.characters.append(character)
        return character
    
    def _recommend_voice(self, role_type: str, traits: List[str]) -> str:
        """推荐最适合角色的音色"""
        # 基于角色类型推荐
        type_voice_map = {
            "protagonist_male": "磁性的",
            "protagonist_female": "甜美的",
            "antagonist": "反派腔",
            "comic_relief": "阳光的",
            "elder": "成熟的",
            "child": "正太音",
            "mentor": "大叔音",
            "romantic_interest_female": "御姐音",
            "romantic_interest_male": "阳光的"
        }
        
        if role_type in type_voice_map:
            return type_voice_map[role_type]
            
        # 基于特征推荐
        if "热血" in traits or "活力" in traits:
            return "阳光的"
        if "神秘" in traits or "冷淡" in traits:
            return "神秘感"
        if "温柔" in traits or "亲切" in traits:
            return "甜美的"
            
        return "磁性的"
    
    def _get_default_emotions(self, role_type: str) -> Dict:
        """获取角色的默认情感配置"""
        defaults = {
            "protagonist_male": {"happy": 0.3, "angry": 0.2, "sad": 0.2, "normal": 0.3},
            "protagonist_female": {"happy": 0.35, "sad": 0.25, "angry": 0.15, "normal": 0.25},
            "antagonist": {"angry": 0.3, "normal": 0.3, "fear": 0.2, "surprised": 0.2},
            "comic_relief": {"happy": 0.5, "surprised": 0.3, "normal": 0.2}
        }
        return defaults.get(role_type, {"normal": 1.0})
    
    def add_dialogue_line(self, character_id: int, line: Dict) -> bool:
        """为角色添加台词"""
        for char in self.characters:
            if char["id"] == character_id:
                line_entry = {
                    "line_id": len(char["lines"]) + 1,
                    "text": line.get("text"),
                    "emotion": line.get("emotion", "normal"),
                    "scene": line.get("scene"),
                    "duration_estimate": len(line.get("text", "")) * 0.3
                }
                char["lines"].append(line_entry)
                char["total_duration"] += line_entry["duration_estimate"]
                return True
        return False
    
    def get_character_summary(self) -> List[Dict]:
        """获取角色摘要"""
        return [{
            "id": char["id"],
            "name": char["name"],
            "voice": char["preferred_voice"],
            "line_count": len(char["lines"]),
            "total_duration": char["total_duration"],
            "traits": char["traits"]
        } for char in self.characters]

class VoiceEffectProcessor:
    """音效处理器"""
    
    def __init__(self):
        self.effects = {
            "reverb": self.apply_reverb,
            "echo": self.apply_echo,
            "compression": self.apply_compression,
            "eq": self.apply_eq,
            "noise_reduction": self.apply_noise_reduction,
            "pitch_shift": self.apply_pitch_shift,
            "time_stretch": self.apply_time_stretch
        }
        
    def apply_reverb(self, audio: Dict, amount: float = 0.3) -> Dict:
        """应用混响效果"""
        return {
            "effect": "reverb",
            "parameters": {
                "room_size": 0.5 * amount,
                "damping": 0.5,
                "wet_level": amount,
                "dry_level": 1 - amount
            },
            "description": f"添加混响效果 (强度: {amount:.0%})"
        }
    
    def apply_echo(self, audio: Dict, delay: float = 0.5, feedback: float = 0.3) -> Dict:
        """应用回声效果"""
        return {
            "effect": "echo",
            "parameters": {
                "delay": delay,
                "feedback": feedback,
                "wet_level": 0.4
            },
            "description": f"添加回声 (延迟: {delay}s, 反馈: {feedback:.0%})"
        }
    
    def apply_compression(self, audio: Dict, threshold: float = -20, ratio: float = 4) -> Dict:
        """应用压缩效果"""
        return {
            "effect": "compression",
            "parameters": {
                "threshold": threshold,
                "ratio": ratio,
                "attack": 0.01,
                "release": 0.1
            },
            "description": f"音频压缩 (阈值: {threshold}dB, 比率: {ratio}:1)"
        }
    
    def apply_eq(self, audio: Dict, low: float = 0, mid: float = 0, high: float = 0) -> Dict:
        """应用均衡器"""
        return {
            "effect": "eq",
            "parameters": {
                "low_shelf": {"frequency": 200, "gain": low},
                "mid_peak": {"frequency": 1000, "gain": mid},
                "high_shelf": {"frequency": 4000, "gain": high}
            },
            "description": f"均衡器调整 (低: {low:+dB}, 中: {mid:+dB}, 高: {high:+dB})"
        }
    
    def apply_noise_reduction(self, audio: Dict, strength: float = 0.5) -> Dict:
        """应用降噪"""
        return {
            "effect": "noise_reduction",
            "parameters": {
                "strength": strength,
                "noise_floor": -40
            },
            "description": f"降噪处理 (强度: {strength:.0%})"
        }
    
    def apply_pitch_shift(self, audio: Dict, semitones: int = 0) -> Dict:
        """音高调整"""
        return {
            "effect": "pitch_shift",
            "parameters": {
                "semitones": semitones,
                "formant_preserve": True
            },
            "description": f"音高调整 ({semitones:+d} 半音)"
        }
    
    def apply_time_stretch(self, audio: Dict, rate: float = 1.0) -> Dict:
        """时间拉伸"""
        return {
            "effect": "time_stretch",
            "parameters": {
                "rate": rate,
                "preserve_pitch": True
            },
            "description": f"时间拉伸 (速率: {rate:.2f}x)"
        }
    
    def create_effect_chain(self, effects_list: List[Tuple[str, Dict]]) -> Dict:
        """创建效果链"""
        chain = []
        
        for effect_name, params in effects_list:
            if effect_name in self.effects:
                effect_result = self.effects[effect_name]({}, **params)
                chain.append(effect_result)
                
        return {
            "chain": chain,
            "processing_order": [e["effect"] for e in chain],
            "total_latency": len(chain) * 0.01  # 估算延迟
        }

class TTSService:
    """文字转语音服务"""
    
    def __init__(self):
        self.providers = {
            "OpenAI": {"quality": "high", "languages": ["zh-CN", "en-US"], "cost": "medium"},
            "Azure": {"quality": "high", "languages": ["zh-CN", "en-US", "ja-JP"], "cost": "high"},
            "Google": {"quality": "medium", "languages": ["zh-CN", "en-US"], "cost": "low"},
            "Coqui": {"quality": "medium", "languages": ["zh-CN", "en-US"], "cost": "free"}
        }
        
    def generate_speech(self, text: str, voice_config: Dict, provider: str = "OpenAI") -> Dict:
        """生成语音"""
        if provider not in self.providers:
            provider = "OpenAI"
            
        provider_info = self.providers[provider]
        
        return {
            "audio_id": f"audio_{random.randint(1000, 9999)}",
            "text": text,
            "provider": provider,
            "voice_config": voice_config,
            "audio_url": f"/generated_audio/{provider.lower()}_{random.randint(1000, 9999)}.mp3",
            "duration": len(text) * 0.3 * voice_config.get("parameters", {}).get("speed", 1.0),
            "quality": provider_info["quality"],
            "cost_estimate": len(text) * 0.01 if provider != "Coqui" else 0,
            "status": "ready"
        }
    
    def batch_generate(self, texts: List[Dict], provider: str = "OpenAI") -> List[Dict]:
        """批量生成语音"""
        results = []
        total_cost = 0
        total_duration = 0
        
        for item in texts:
            result = self.generate_speech(
                item.get("text", ""),
                item.get("voice_config", {}),
                provider
            )
            results.append(result)
            total_cost += result["cost_estimate"]
            total_duration += result["duration"]
            
        return {
            "items": results,
            "total_items": len(results),
            "total_duration": total_duration,
            "total_cost": total_cost,
            "provider": provider
        }

def render_voice_system_tab(st, state):
    """渲染配音系统页面"""
    st.header("🎤 多角色配音系统")
    
    # 初始化
    if "voice_system" not in state:
        state.voice_system = MultiCharacterVoiceSystem()
    if "voice_manager" not in state:
        state.voice_manager = VoiceCharacterManager()
    if "voice_effects" not in state:
        state.voice_effects = VoiceEffectProcessor()
    if "tts_service" not in state:
        state.tts_service = TTSService()
    
    # 标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🎭 音色库", "👥 角色配音", "🔊 音效处理", "🎙️ TTS生成"])
    
    with tab1:
        render_voice_library(st, state)
        
    with tab2:
        render_character_voice(st, state)
        
    with tab3:
        render_effects_processor(st, state)
        
    with tab4:
        render_tts_generator(st, state)
    
    return state

def render_voice_library(st, state):
    """渲染音色库"""
    st.subheader("音色库")
    
    # 分类显示
    voice_col1, voice_col2 = st.columns(2)
    
    with voice_col1:
        st.write("**🎤 男声**")
        male_voices = [("磁性的", "男主角/旁白"), ("阳光的", "少年/喜剧"), 
                       ("成熟的", "父亲/导师"), ("反派腔", "反派/阴谋家"), 
                       ("大叔音", "江湖/硬汉"), ("正太音", "儿童/正太")]
        
        for voice_name, use_case in male_voices:
            with st.expander(f"🎵 {voice_name}"):
                voice_info = state.voice_system.get_voice_profile(voice_name)
                st.write(f"**特征:** {', '.join(voice_info['traits'])}")
                st.write(f"**适用:** {use_case}")
                st.write(f"**音高范围:** {voice_info['pitch_range'][0]}-{voice_info['pitch_range'][1]}Hz")
                st.write(f"**语速:** {voice_info['speed']}")
                
    with voice_col2:
        st.write("**🎤 女声**")
        female_voices = [("甜美的", "女主/萝莉"), ("御姐音", "御姐/女王"),
                        ("少女音", "少女/元气"), ("神秘感", "神秘/反派")]
        
        for voice_name, use_case in female_voices:
            with st.expander(f"🎵 {voice_name}"):
                voice_info = state.voice_system.get_voice_profile(voice_name)
                st.write(f"**特征:** {', '.join(voice_info['traits'])}")
                st.write(f"**适用:** {use_case}")
                st.write(f"**音高范围:** {voice_info['pitch_range'][0]}-{voice_info['pitch_range'][1]}Hz")
                st.write(f"**语速:** {voice_info['speed']}")
    
    # 情感配音
    st.write("---")
    st.write("**💫 情感配音**")
    
    emotion_col1, emotion_col2, emotion_col3 = st.columns(3)
    
    emotions = list(state.voice_system.emotion_configs.items())
    for i, (emotion, config) in enumerate(emotions[:6]):
        with [emotion_col1, emotion_col2, emotion_col3][i % 3]:
            st.write(f"**{emotion}:** 音高{config['pitch_shift']:+d}, 语速{config['speed_mult']:.2f}x")
    
    # 预览
    st.write("---")
    st.write("**🎧 音色预览**")
    
    preview_col1, preview_col2 = st.columns(2)
    with preview_col1:
        preview_voice = st.selectbox("选择音色", list(state.voice_system.voice_profiles.keys()), key="preview_voice_select")
    with preview_col2:
        preview_emotion = st.selectbox("选择情感", list(state.voice_system.emotion_configs.keys()), key="preview_emotion_select")
    
    preview_text = st.text_input("预览文本", "今天，我们要讲述一个关于梦想与坚持的故事。", key="preview_text_input")
    
    if st.button("🎵 播放预览", key="preview_play_btn"):
        voice_params = state.voice_system.generate_emotion_voice(
            preview_text, preview_voice, preview_emotion
        )
        
        st.success(f"生成完成！音色: {preview_voice} | 情感: {preview_emotion}")
        st.write(f"**参数:** 音高={voice_params['parameters']['pitch']}Hz, "
                f"语速={voice_params['parameters']['speed']:.2f}x, "
                f"音量={voice_params['parameters']['volume']:.0%}")
        st.write(f"**时长:** 约 {voice_params['parameters']['duration_estimate']:.1f}s")
        st.write(f"**效果:** {', '.join(voice_params['effects'])}")

def render_character_voice(st, state):
    """渲染角色配音管理"""
    st.subheader("角色配音管理")
    
    # 角色管理
    char_col1, char_col2 = st.columns(2)
    
    with char_col1:
        st.write("**📝 添加配音角色**")
        char_name = st.text_input("角色名称", key="char_voice_name")
        char_role = st.selectbox("角色类型", [
            "男主角", "女主角", "反派", "喜剧角色", "长辈", "儿童", "导师", "恋人"
        ], key="char_voice_role")
        
    with char_col2:
        st.write("**🎤 特征标签**")
        trait_options = st.multiselect("选择特征", [
            "热血", "冷酷", "温柔", "活泼", "神秘", "搞笑", "深情", "正义"
        ], default=["热血"], key="char_traits_select")
        
        char_voice = st.selectbox("推荐音色", list(state.voice_system.voice_profiles.keys()), key="char_voice_select")
    
    if st.button("➕ 添加角色", key="add_voice_char_btn"):
        if char_name:
            character = state.voice_manager.create_voice_character(char_name, char_role, trait_options)
            st.success(f"✅ 角色 {character['name']} 已添加！音色: {character['preferred_voice']}")
    
    # 角色列表
    st.write("---")
    st.write("**👥 配音角色列表**")
    
    characters = state.voice_manager.get_character_summary()
    
    if characters:
        for char in characters:
            with st.expander(f"🎭 {char['name']} ({char['voice']})"):
                st.write(f"**类型:** {char['role_type']}")
                st.write(f"**台词数:** {char['line_count']} 句")
                st.write(f"**总时长:** {char['total_duration']:.1f}s")
                st.write(f"**特征:** {', '.join(char['traits'])}")
                
                # 添加台词
                st.write("**➕ 添加台词**")
                line_text = st.text_input("台词内容", key=f"line_text_{char['id']}")
                line_emotion = st.selectbox("情感", list(state.voice_system.emotion_configs.keys()), key=f"line_emotion_{char['id']}")
                
                if st.button("添加", key=f"add_line_btn_{char['id']}"):
                    state.voice_manager.add_dialogue_line(char['id'], {
                        "text": line_text,
                        "emotion": line_emotion,
                        "scene": "默认场景"
                    })
                    st.rerun()
    else:
        st.info("暂无配音角色，请先添加角色")
    
    # 批量生成
    st.write("---")
    st.write("**🎬 批量生成对话**")
    
    if st.button("📋 生成所有对话配音", key="batch_generate_btn"):
        if characters:
            dialogues = []
            for char in characters:
                for line in state.voice_manager.characters[char['id']-1]["lines"]:
                    dialogues.append({
                        "id": len(dialogues),
                        "character": {"id": char['id'], "name": char['name'], "preferred_voice": char['voice']},
                        "text": line.get("text", ""),
                        "emotion": line.get("emotion", "normal"),
                        "start_time": 0
                    })
            
            if dialogues:
                results = state.voice_system.batch_generate_dialogue(dialogues)
                mix_result = state.voice_system.mix_voice_tracks(results)
                
                st.success(f"✅ 生成 {len(results)} 条对话配音！")
                st.write(f"**总时长:** {mix_result['total_duration']:.1f}s")
                st.write(f"**轨道数:** {mix_result['total_tracks']}")
                
                if mix_result['overlaps']:
                    st.warning(f"⚠️ 检测到 {len(mix_result['overlaps'])} 处重叠")
            else:
                st.warning("没有可生成对话的角色台词")

def render_effects_processor(st, state):
    """渲染音效处理器"""
    st.subheader("音效处理")
    
    # 效果选择
    st.write("**🎛️ 添加效果**")
    
    effect_col1, effect_col2 = st.columns(2)
    
    with effect_col1:
        effect_type = st.selectbox("效果类型", [
            "混响 (Reverb)", "回声 (Echo)", "压缩 (Compression)",
            "均衡器 (EQ)", "降噪", "音高调整", "时间拉伸"
        ], key="effect_type_select")
        
    with effect_col2:
        effect_strength = st.slider("效果强度", 0, 100, 50, key="effect_strength_slider")
    
    # 应用预设
    st.write("**✨ 快速预设**")
    preset_col1, preset_col2, preset_col3 = st.columns(3)
    
    with preset_col1:
        if st.button("🎬 电影感", key="movie_preset_btn"):
            effects_chain = [
                ("reverb", {"amount": 0.4}),
                ("eq", {"low": 2, "mid": 0, "high": 1}),
                ("compression", {"threshold": -18, "ratio": 3})
            ]
            result = state.voice_effects.create_effect_chain(effects_chain)
            st.success("电影感预设已应用")
            st.json(result)
            
    with preset_col2:
        if st.button("🎤 录音棚", key="studio_preset_btn"):
            effects_chain = [
                ("noise_reduction", {"strength": 0.7}),
                ("eq", {"low": 0, "mid": 2, "high": 1}),
                ("compression", {"threshold": -15, "ratio": 4})
            ]
            result = state.voice_effects.create_effect_chain(effects_chain)
            st.success("录音棚预设已应用")
            st.json(result)
            
    with preset_col3:
        if st.button("📻 广播", key="radio_preset_btn"):
            effects_chain = [
                ("eq", {"low": -2, "mid": 3, "high": 2}),
                ("compression", {"threshold": -12, "ratio": 5}),
                ("reverb", {"amount": 0.1})
            ]
            result = state.voice_effects.create_effect_chain(effects_chain)
            st.success("广播预设已应用")
            st.json(result)
    
    # 效果预览
    st.write("---")
    st.write("**🎧 效果预览**")
    
    preview_audio = st.selectbox("选择音频", ["demo_dialogue.mp3", "narration_01.mp3", "scene_audio.wav"], key="effect_preview_audio")
    
    if st.button("▶️ 应用并预览", key="apply_effect_btn"):
        effect_mapping = {
            "混响 (Reverb)": ("reverb", {"amount": effect_strength / 100}),
            "回声 (Echo)": ("echo", {"delay": 0.3, "feedback": effect_strength / 200}),
            "压缩 (Compression)": ("compression", {"threshold": -20 + effect_strength/10, "ratio": 2 + effect_strength/50}),
            "均衡器 (EQ)": ("eq", {"low": effect_strength/50, "mid": 0, "high": effect_strength/100}),
            "降噪": ("noise_reduction", {"strength": effect_strength / 100}),
            "音高调整": ("pitch_shift", {"semitones": effect_strength//20 - 2}),
            "时间拉伸": ("time_stretch", {"rate": 0.8 + effect_strength/500})
        }
        
        effect_info = effect_mapping.get(effect_type, ("reverb", {}))
        result = state.voice_effects.create_effect_chain([effect_info])
        
        st.success(f"效果已应用: {effect_type}")
        st.json(result)

def render_tts_generator(st, state):
    """渲染TTS生成器"""
    st.subheader("文字转语音 (TTS)")
    
    # 服务商选择
    provider_col1, provider_col2 = st.columns(2)
    
    with provider_col1:
        tts_provider = st.selectbox("TTS服务商", ["OpenAI", "Azure", "Google", "Coqui"], key="tts_provider_select")
        provider_info = state.tts_service.providers.get(tts_provider, {})
        st.write(f"**质量:** {provider_info.get('quality', 'unknown')} | **成本:** {provider_info.get('cost', 'unknown')}")
        
    with provider_col2:
        output_format = st.selectbox("输出格式", ["MP3", "WAV", "OGG"], key="tts_format_select")
        sample_rate = st.selectbox("采样率", ["16kHz", "22kHz", "44.1kHz"], key="tts_sample_select")
    
    # 文本输入
    st.write("**📝 输入文本**")
    
    tts_text = st.text_area(
        "输入要转换的文本",
        height=150,
        placeholder="请输入需要转换为语音的文本内容...",
        key="tts_text_input"
    )
    
    # 选项
    option_col1, option_col2, option_col3 = st.columns(3)
    
    with option_col1:
        auto_punctuation = st.checkbox("自动标点", True, key="tts_punct_check")
    with option_col2:
        background_music = st.checkbox("添加背景音乐", False, key="tts_bg_music_check")
    with option_col3:
        sound_effects = st.checkbox("添加音效", False, key="tts_sfx_check")
    
    # 生成
    if st.button("🎙️ 生成语音", key="tts_generate_btn"):
        if tts_text:
            voice_config = {
                "parameters": {"speed": 1.0, "pitch": 150, "volume": 1.0}
            }
            
            result = state.tts_service.generate_speech(tts_text, voice_config, tts_provider)
            
            st.success(f"✅ 语音生成成功！")
            st.write(f"**提供商:** {result['provider']}")
            st.write(f"**时长:** {result['duration']:.1f}s")
            st.write(f"**质量:** {result['quality']}")
            st.write(f"**预估成本:** ${result['cost_estimate']:.4f}")
            st.write(f"**状态:** {result['status']}")
            st.audio(result['audio_url'])
    
    # 批量生成
    st.write("---")
    st.write("**📦 批量生成**")
    
    batch_texts = st.text_area(
        "输入多段文本（每行一段）",
        height=120,
        placeholder="第一句台词\n第二句台词\n第三句台词",
        key="batch_text_input"
    )
    
    if st.button("🎙️ 批量生成", key="batch_tts_btn"):
        if batch_texts:
            items = []
            for i, line in enumerate(batch_texts.strip().split('\n')):
                if line.strip():
                    items.append({
                        "text": line.strip(),
                        "voice_config": {
                            "parameters": {"speed": 1.0, "pitch": 150, "volume": 1.0}
                        }
                    })
            
            if items:
                result = state.tts_service.batch_generate(items, tts_provider)
                
                st.success(f"✅ 批量生成完成！共 {result['total_items']} 条")
                st.write(f"**总时长:** {result['total_duration']:.1f}s")
                st.write(f"**总成本:** ${result['total_cost']:.4f}")
                
                # 显示列表
                for item in result['items'][:5]:
                    st.write(f"- [{item['audio_id']}] {item['text'][:30]}... ({item['duration']:.1f}s)")
                
                if result['total_items'] > 5:
                    st.write(f"... 还有 {result['total_items'] - 5} 条")
