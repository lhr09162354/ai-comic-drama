# -*- coding: utf-8 -*-
"""
高级特效库 - 粒子特效、光效、转场特效、滤镜
v27 新增功能
"""
import streamlit as st
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class AdvancedEffectsLibrary:
    """高级特效库"""
    
    def __init__(self):
        # 粒子特效
        self.particle_effects = {
            "fire": {
                "name": "火焰粒子",
                "description": "逼真的火焰燃烧效果",
                "parameters": {
                    "particle_count": 500,
                    "particle_size": (2, 8),
                    "colors": ["#FF4500", "#FF6347", "#FFD700"],
                    "lifetime": 2.0,
                    "velocity": (0, -5),
                    "spread": 0.3
                },
                "use_cases": ["战斗", "魔法", "爆炸", "篝火"]
            },
            "sparkle": {
                "name": "闪光粒子",
                "description": "星星点点的闪光效果",
                "parameters": {
                    "particle_count": 200,
                    "particle_size": (1, 4),
                    "colors": ["#FFFFFF", "#FFE4B5", "#FFD700"],
                    "lifetime": 1.5,
                    "velocity": (0, -2),
                    "twinkle": True
                },
                "use_cases": ["魔法", "希望", "变身", "成功"]
            },
            "smoke": {
                "name": "烟雾粒子",
                "description": "飘散的烟雾效果",
                "parameters": {
                    "particle_count": 300,
                    "particle_size": (5, 15),
                    "colors": ["#808080", "#A9A9A9", "#696969"],
                    "lifetime": 4.0,
                    "velocity": (0, -1),
                    "turbulence": 0.5
                },
                "use_cases": ["爆炸后", "神秘", "悲伤", "消失"]
            },
            "rain": {
                "name": "雨滴粒子",
                "description": "逼真的雨滴效果",
                "parameters": {
                    "particle_count": 1000,
                    "particle_size": (1, 3),
                    "colors": ["#4169E1", "#6495ED"],
                    "lifetime": 5.0,
                    "velocity": (0, 15),
                    "angle": 15
                },
                "use_cases": ["雨天场景", "悲伤", "孤独", "浪漫"]
            },
            "snow": {
                "name": "雪花粒子",
                "description": "飘落的雪花效果",
                "parameters": {
                    "particle_count": 500,
                    "particle_size": (2, 6),
                    "colors": ["#FFFFFF", "#FFFAFA", "#F0F8FF"],
                    "lifetime": 6.0,
                    "velocity": (0, 2),
                    "sway": True
                },
                "use_cases": ["冬天", "浪漫", "温馨", "孤独"]
            },
            "leaves": {
                "name": "落叶粒子",
                "description": "飘落的树叶效果",
                "parameters": {
                    "particle_count": 100,
                    "particle_size": (5, 12),
                    "colors": ["#8B4513", "#D2691E", "#CD853F", "#228B22"],
                    "lifetime": 5.0,
                    "velocity": (0, 1),
                    "rotation": True
                },
                "use_cases": ["秋天", "离别", "时光流逝"]
            },
            "energy": {
                "name": "能量粒子",
                "description": "聚集的能量效果",
                "parameters": {
                    "particle_count": 400,
                    "particle_size": (2, 6),
                    "colors": ["#00FFFF", "#00BFFF", "#1E90FF"],
                    "lifetime": 2.5,
                    "velocity": (-2, 2),
                    "glow": True
                },
                "use_cases": ["技能", "觉醒", "超能力", "传送"]
            },
            "dust": {
                "name": "尘埃粒子",
                "description": "飘浮的尘埃效果",
                "parameters": {
                    "particle_count": 150,
                    "particle_size": (1, 3),
                    "colors": ["#D2B48C", "#C4A77D", "#A0522D"],
                    "lifetime": 3.0,
                    "velocity": (0, 0.5),
                    "random_drift": True
                },
                "use_cases": ["废墟", "古老", "废墟探险", "沙漠"]
            },
            "confetti": {
                "name": "彩带礼花",
                "description": "庆祝的彩带效果",
                "parameters": {
                    "particle_count": 300,
                    "particle_size": (3, 8),
                    "colors": ["#FF69B4", "#FFD700", "#00CED1", "#FF6347", "#9370DB"],
                    "lifetime": 4.0,
                    "velocity": (0, -3),
                    "rotation": True
                },
                "use_cases": ["庆祝", "成功", "胜利", "节日"]
            },
            "magic": {
                "name": "魔法粒子",
                "description": "神秘的魔法效果",
                "parameters": {
                    "particle_count": 350,
                    "particle_size": (2, 5),
                    "colors": ["#9400D3", "#8A2BE2", "#DA70D6", "#9370DB"],
                    "lifetime": 3.0,
                    "velocity": (0, -1),
                    "spiral": True
                },
                "use_cases": ["魔法", "变身", "结界", "传送门"]
            }
        }
        
        # 光效
        self.light_effects = {
            "sun_rays": {"name": "阳光射线", "intensity": 0.8, "use": ["希望", "温暖", "英雄"]},
            "lens_flare": {"name": "镜头光晕", "intensity": 0.6, "use": ["逆光", "梦幻", "浪漫"]},
            "neon_glow": {"name": "霓虹光效", "intensity": 0.9, "use": ["赛博朋克", "夜晚", "都市"]},
            "golden_hour": {"name": "黄金时刻", "intensity": 0.7, "use": ["温馨", "浪漫", "回忆"]},
            "dramatic_shadow": {"name": "戏剧光影", "intensity": 0.85, "use": ["紧张", "悬疑", "戏剧"]},
            "rim_light": {"name": "轮廓光", "intensity": 0.75, "use": ["突出", "帅气", "超能力"]},
            "volumetric": {"name": "体积光", "intensity": 0.65, "use": ["神圣", "神秘", "仪式"]},
            "flickering": {"name": "闪烁光效", "intensity": 0.5, "use": ["紧张", "恐怖", "故障"]},
            "candlelight": {"name": "烛光", "intensity": 0.4, "use": ["温馨", "浪漫", "古老"]},
            "laser": {"name": "激光光效", "intensity": 1.0, "use": ["科幻", "战斗", "科技"]}
        }
        
        # 转场特效
        self.transitions = {
            "fade": {"name": "淡入淡出", "duration": 1.0, "type": "smooth"},
            "dissolve": {"name": "叠化", "duration": 0.8, "type": "blend"},
            "whip_pan": {"name": "甩切", "duration": 0.3, "type": "motion"},
            "zoom_blur": {"name": "缩放模糊", "duration": 0.5, "type": "blur"},
            "spin": {"name": "旋转", "duration": 0.6, "type": "rotation"},
            "page_turn": {"name": "翻页", "duration": 0.8, "type": "transform"},
            "glitch": {"name": "故障", "duration": 0.4, "type": "digital"},
            "circle_wipe": {"name": "圆形擦除", "duration": 0.7, "type": "wipe"},
            "light_streak": {"name": "光带", "duration": 0.5, "type": "light"},
            "match_cut": {"name": "匹配剪切", "duration": 0.2, "type": "cut"},
            "iris": {"name": "虹膜", "duration": 0.8, "type": "classic"},
            "film_burn": {"name": "胶片烧灼", "duration": 0.6, "type": "vintage"}
        }
        
        # 滤镜
        self.filters = {
            "cinematic": {
                "name": "电影感",
                "adjustments": {"contrast": 1.2, "saturation": 0.9, "warmth": -5},
                "vignette": 0.3
            },
            "noir": {
                "name": "黑白电影",
                "adjustments": {"saturation": 0, "contrast": 1.4, "grain": 0.2},
                "vignette": 0.4
            },
            "vintage": {
                "name": "复古",
                "adjustments": {"sepia": 0.3, "contrast": 0.9, "warmth": 10},
                "vignette": 0.2
            },
            "cyberpunk": {
                "name": "赛博朋克",
                "adjustments": {"saturation": 1.3, "cyan_tint": 0.3, "contrast": 1.3},
                "vignette": 0.1
            },
            "warm": {
                "name": "暖色调",
                "adjustments": {"warmth": 15, "saturation": 1.1, "brightness": 0.05},
                "vignette": 0
            },
            "cool": {
                "name": "冷色调",
                "adjustments": {"warmth": -15, "saturation": 1.0, "contrast": 1.1},
                "vignette": 0
            },
            "dramatic": {
                "name": "戏剧化",
                "adjustments": {"contrast": 1.5, "saturation": 1.1, "shadows": -20},
                "vignette": 0.35
            },
            "dreamy": {
                "name": "梦幻",
                "adjustments": {"brightness": 0.1, "blur": 0.05, "saturation": 0.9},
                "vignette": 0.15
            },
            "high_contrast": {
                "name": "高对比",
                "adjustments": {"contrast": 1.8, "brightness": 0, "shadows": -30},
                "vignette": 0.2
            },
            "muted": {
                "name": "低饱和",
                "adjustments": {"saturation": 0.5, "contrast": 0.95, "warmth": 0},
                "vignette": 0
            }
        }
        
    def get_particle_effect(self, effect_name: str) -> Dict:
        """获取粒子特效配置"""
        return self.particle_effects.get(effect_name, self.particle_effects["sparkle"])
    
    def generate_particle_config(self, base_effect: str, customizations: Dict) -> Dict:
        """生成自定义粒子配置"""
        base = self.get_particle_effect(base_effect)
        
        config = {
            "effect_name": base["name"],
            "parameters": {**base["parameters"], **customizations},
            "render_settings": {
                "blend_mode": customizations.get("blend_mode", "additive"),
                "quality": customizations.get("quality", "high"),
                "fps": customizations.get("fps", 30)
            }
        }
        
        return config
    
    def combine_effects(self, effects: List[Dict]) -> Dict:
        """组合多个特效"""
        combined = {
            "layers": [],
            "total_particle_count": 0,
            "estimated_render_time": 0
        }
        
        for effect in effects:
            layer = {
                "type": effect.get("type", "particle"),
                "name": effect.get("name", "Effect"),
                "opacity": effect.get("opacity", 1.0),
                "blend_mode": effect.get("blend_mode", "normal")
            }
            combined["layers"].append(layer)
            combined["total_particle_count"] += effect.get("particle_count", 0)
            combined["estimated_render_time"] += effect.get("duration", 1.0)
            
        return combined

class TransitionEffects:
    """转场特效库"""
    
    def __init__(self):
        self.transition_presets = {
            "action_sequence": ["whip_pan", "zoom_blur", "hard_cut", "speed_ramp"],
            "emotional_beat": ["dissolve", "fade", "iris", "slow_dissolve"],
            "comedic_timing": ["bounce", "spin", "flash", "speed_ramp"],
            "dramatic_reveal": ["fade_to_black", "circle_wipe", "iris", "film_burn"],
            "smooth_flow": ["dissolve", "cross_dissolve", "match_cut", "slide"]
        }
        
    def select_transition(self, scene1_type: str, scene2_type: str) -> str:
        """根据场景类型选择转场"""
        if scene1_type == scene2_type:
            return "hard_cut"
            
        transitions = {
            ("dialogue", "action"): "whip_pan",
            ("action", "dialogue"): "dissolve",
            ("emotional", "action"): "fade",
            ("action", "emotional"): "iris",
            ("comedic", "dramatic"): "glitch",
            ("dramatic", "comedic"): "bounce"
        }
        
        return transitions.get((scene1_type, scene2_type), "dissolve")
    
    def generate_transition_animation(self, transition_type: str, duration: float = 1.0) -> Dict:
        """生成转场动画配置"""
        animations = {
            "fade": {
                "keyframes": [
                    {"time": 0, "opacity_scene1": 1.0, "opacity_scene2": 0},
                    {"time": 0.5, "opacity_scene1": 0.5, "opacity_scene2": 0.5},
                    {"time": 1.0, "opacity_scene1": 0, "opacity_scene2": 1.0}
                ],
                "easing": "ease-in-out"
            },
            "whip_pan": {
                "keyframes": [
                    {"time": 0, "x_offset": 0, "blur": 0},
                    {"time": 0.5, "x_offset": "100%", "blur": 10},
                    {"time": 1.0, "x_offset": "200%", "blur": 0}
                ],
                "easing": "ease-out"
            },
            "dissolve": {
                "keyframes": [
                    {"time": 0, "opacity_scene1": 1.0, "opacity_scene2": 0, "noise": 0},
                    {"time": 0.5, "opacity_scene1": 0.5, "opacity_scene2": 0.5, "noise": 0.3},
                    {"time": 1.0, "opacity_scene1": 0, "opacity_scene2": 1.0, "noise": 0}
                ],
                "easing": "linear"
            },
            "zoom_blur": {
                "keyframes": [
                    {"time": 0, "scale": 1.0, "blur_radius": 0},
                    {"time": 0.5, "scale": 1.5, "blur_radius": 20},
                    {"time": 1.0, "scale": 1.0, "blur_radius": 0}
                ],
                "easing": "ease-in-out"
            }
        }
        
        return {
            "type": transition_type,
            "duration": duration,
            "animation": animations.get(transition_type, animations["fade"]),
            "audio_cue": self._get_audio_cue(transition_type)
        }
    
    def _get_audio_cue(self, transition_type: str) -> Dict:
        """获取转场音效提示"""
        cues = {
            "fade": {"sound": "soft_swipe", "volume": 0.3},
            "whip_pan": {"sound": "whoosh", "volume": 0.6},
            "dissolve": {"sound": "ambient_drone", "volume": 0.2},
            "glitch": {"sound": "digital_glitch", "volume": 0.5},
            "hard_cut": {"sound": "sharp_cut", "volume": 0.4}
        }
        return cues.get(transition_type, {"sound": "none", "volume": 0})

class ColorGrading:
    """色彩校正"""
    
    def __init__(self):
        self.color_schemes = {
            "teal_orange": {
                "name": "青橙色",
                "shadows": [0, 0.2, 0.4],  # R, G, B
                "midtones": [0.5, 0.5, 0.5],
                "highlights": [1.0, 0.6, 0.3],
                "lut": "teal_orange.png"
            },
            "orange_teal": {
                "name": "橙青色",
                "shadows": [0.3, 0.5, 0.6],
                "midtones": [0.5, 0.5, 0.5],
                "highlights": [1.0, 0.7, 0.4],
                "lut": "orange_teal.png"
            },
            "desaturated_blue": {
                "name": "冷灰蓝",
                "shadows": [0.1, 0.15, 0.25],
                "midtones": [0.4, 0.45, 0.5],
                "highlights": [0.8, 0.85, 0.95],
                "lut": "desaturated_blue.png"
            },
            "warm_wood": {
                "name": "暖木色",
                "shadows": [0.2, 0.15, 0.1],
                "midtones": [0.6, 0.5, 0.4],
                "highlights": [1.0, 0.9, 0.7],
                "lut": "warm_wood.png"
            },
            "cinematic_mood": {
                "name": "电影氛围",
                "shadows": [0.05, 0.08, 0.12],
                "midtones": [0.4, 0.42, 0.45],
                "highlights": [0.9, 0.85, 0.8],
                "lut": "cinematic_mood.png"
            }
        }
        
    def apply_color_grade(self, scheme_name: str, intensity: float = 1.0) -> Dict:
        """应用色彩分级"""
        scheme = self.color_schemes.get(scheme_name, self.color_schemes["cinematic_mood"])
        
        # 根据强度调整
        def adjust(color, intensity):
            base = 0.5  # 中性灰
            return base + (color - base) * intensity
        
        return {
            "scheme": scheme_name,
            "intensity": intensity,
            "shadows": [adjust(c, intensity) for c in scheme["shadows"]],
            "midtones": [adjust(c, intensity) for c in scheme["midtones"]],
            "highlights": [adjust(c, intensity) for c in scheme["highlights"]],
            "lut_file": scheme["lut"],
            "color_wheels": {
                "shadow_tint": scheme["shadows"],
                "midtone_tint": scheme["midtones"],
                "highlight_tint": scheme["highlights"]
            }
        }
    
    def create_custom_scheme(self, name: str, shadow_color: str, highlight_color: str) -> Dict:
        """创建自定义配色方案"""
        # 简单转换 hex 到 RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
        
        shadow = hex_to_rgb(shadow_color)
        highlight = hex_to_rgb(highlight_color)
        
        return {
            "name": name,
            "shadows": list(shadow),
            "midtones": [(s+h)/2 for s, h in zip(shadow, highlight)],
            "highlights": list(highlight),
            "lut": f"custom_{name.replace(' ', '_')}.png"
        }

class EffectPresetBuilder:
    """特效预设构建器"""
    
    def __init__(self):
        self.effect_library = AdvancedEffectsLibrary()
        self.transitions = TransitionEffects()
        self.color_grading = ColorGrading()
        
        # 场景预设
        self.scene_presets = {
            "hero_transformation": {
                "name": "英雄变身",
                "effects": ["energy", "light_rays"],
                "color": "dramatic",
                "transition": "zoom_blur",
                "sound_effect": "power_up"
            },
            "romantic_moment": {
                "name": "浪漫时刻",
                "effects": ["sparkle", "bokeh"],
                "color": "warm",
                "transition": "dissolve",
                "sound_effect": "soft_music"
            },
            "action_climax": {
                "name": "动作高潮",
                "effects": ["fire", "smoke", "speed_lines"],
                "color": "high_contrast",
                "transition": "whip_pan",
                "sound_effect": "explosion"
            },
            "mystery_reveal": {
                "name": "悬疑揭示",
                "effects": ["dust", "fog"],
                "color": "noir",
                "transition": "iris",
                "sound_effect": "suspense"
            },
            "comedic_punchline": {
                "name": "喜剧高潮",
                "effects": ["confetti", "bounce"],
                "color": "bright",
                "transition": "bounce",
                "sound_effect": "laugh_track"
            },
            "emotional_resolution": {
                "name": "情感化解",
                "effects": ["soft_light", "warm_particles"],
                "color": "warm",
                "transition": "fade",
                "sound_effect": "gentle_music"
            },
            "supernatural_event": {
                "name": "超自然事件",
                "effects": ["magic", "energy"],
                "color": "purple_mood",
                "transition": "glitch",
                "sound_effect": "magic_spell"
            },
            "peaceful_ending": {
                "name": "和平结局",
                "effects": ["soft_glow", "bokeh"],
                "color": "golden_hour",
                "transition": "dissolve",
                "sound_effect": "peaceful_ambient"
            }
        }
        
    def build_scene_preset(self, preset_name: str) -> Dict:
        """构建场景预设"""
        preset = self.scene_presets.get(preset_name, self.scene_presets["romantic_moment"])
        
        built = {
            "preset_name": preset_name,
            "effects": [],
            "color_grading": None,
            "transition": None,
            "sound_effect": preset.get("sound_effect")
        }
        
        # 构建特效
        for effect_name in preset.get("effects", []):
            effect = self.effect_library.get_particle_effect(effect_name)
            built["effects"].append(effect)
            
        # 色彩分级
        if preset.get("color"):
            built["color_grading"] = self.color_grading.apply_color_grade(preset["color"])
            
        # 转场
        if preset.get("transition"):
            built["transition"] = self.transitions.generate_transition_animation(preset["transition"])
            
        return built
    
    def create_mixed_preset(self, effects: List[str], color_scheme: str, transition: str) -> Dict:
        """创建混合预设"""
        return {
            "effects": [self.effect_library.get_particle_effect(e) for e in effects],
            "color_grading": self.color_grading.apply_color_grade(color_scheme),
            "transition": self.transitions.generate_transition_animation(transition),
            "custom": True
        }

def render_effects_library_tab(st, state):
    """渲染特效库页面"""
    st.header("✨ 高级特效库")
    
    # 初始化
    if "effects_library" not in state:
        state.effects_library = AdvancedEffectsLibrary()
    if "preset_builder" not in state:
        state.preset_builder = EffectPresetBuilder()
    
    # 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎆 粒子特效", "💡 光效", "🔄 转场", "🎨 滤镜", "📦 预设"])
    
    with tab1:
        render_particle_effects(st, state)
        
    with tab2:
        render_light_effects(st, state)
        
    with tab3:
        render_transitions(st, state)
        
    with tab4:
        render_filters(st, state)
        
    with tab5:
        render_effect_presets(st, state)
    
    return state

def render_particle_effects(st, state):
    """渲染粒子特效"""
    st.subheader("粒子特效库")
    
    # 特效分类
    effect_category = st.selectbox("特效分类", [
        "全部", "自然", "魔法", "战斗", "氛围", "特殊"
    ], key="particle_category")
    
    # 显示特效
    effects = state.effects_library.particle_effects
    
    cols = st.columns(3)
    for i, (effect_key, effect) in enumerate(effects.items()):
        with cols[i % 3]:
            with st.expander(f"🎆 {effect['name']}"):
                st.write(f"**描述:** {effect['description']}")
                st.write(f"**粒子数:** {effect['parameters']['particle_count']}")
                st.write(f"**适用:** {', '.join(effect['use_cases'])}")
                
                # 预览按钮
                if st.button(f"预览", key=f"preview_{effect_key}"):
                    st.info(f"🎆 正在渲染 {effect['name']} 特效...")
                    st.image(f"https://via.placeholder.com/300x150/{effect['parameters']['colors'][0][1:]}/000000?text={effect['name']}")
                
                # 使用按钮
                if st.button(f"应用到场景", key=f"use_{effect_key}"):
                    st.success(f"✅ {effect['name']} 已添加到场景")
    
    # 自定义粒子效果
    st.write("---")
    st.subheader("🎛️ 自定义粒子效果")
    
    custom_col1, custom_col2 = st.columns(2)
    
    with custom_col1:
        base_effect = st.selectbox("基础效果", list(effects.keys()), key="custom_base_effect")
        particle_count = st.slider("粒子数量", 50, 2000, 500, key="custom_particle_count")
        
    with custom_col2:
        particle_size_min, particle_size_max = st.slider(
            "粒子大小范围", 1, 20, (2, 8), key="custom_particle_size"
        )
        particle_lifetime = st.slider("粒子寿命", 0.5, 10.0, 3.0, key="custom_lifetime")
    
    # 颜色选择
    st.write("**🎨 粒子颜色**")
    color_options = st.multiselect(
        "选择颜色",
        ["红色", "橙色", "黄色", "绿色", "蓝色", "紫色", "白色", "粉色"],
        default=["蓝色", "白色"],
        key="custom_colors"
    )
    
    color_map = {
        "红色": "#FF4500", "橙色": "#FF6347", "黄色": "#FFD700",
        "绿色": "#32CD32", "蓝色": "#00BFFF", "紫色": "#9400D3",
        "白色": "#FFFFFF", "粉色": "#FF69B4"
    }
    selected_colors = [color_map[c] for c in color_options]
    
    if st.button("✨ 生成自定义粒子", key="generate_custom_particle"):
        custom_config = state.effects_library.generate_particle_config(base_effect, {
            "particle_count": particle_count,
            "particle_size": (particle_size_min, particle_size_max),
            "colors": selected_colors,
            "lifetime": particle_lifetime
        })
        
        st.success("✅ 自定义粒子效果已生成！")
        st.json(custom_config)

def render_light_effects(st, state):
    """渲染光效"""
    st.subheader("光效库")
    
    lights = state.effects_library.light_effects
    
    for i, (light_key, light) in enumerate(lights.items()):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.write(f"**{light['name']}**")
        with col2:
            st.write(f"强度: {light['intensity']:.0%} | 适用: {', '.join(light['use'][:2])}")
        with col3:
            if st.button("应用", key=f"apply_light_{light_key}"):
                st.success(f"✅ {light['name']} 已应用")
    
    # 光效组合
    st.write("---")
    st.subheader("💫 光效组合")
    
    combo_col1, combo_col2 = st.columns(2)
    
    with combo_col1:
        primary_light = st.selectbox("主光效", list(lights.keys()), key="primary_light")
        primary_intensity = st.slider("主光强度", 0, 100, 70, key="primary_intensity")
        
    with combo_col2:
        secondary_light = st.selectbox("辅助光效", ["无"] + list(lights.keys()), key="secondary_light")
        secondary_intensity = st.slider("辅助光强度", 0, 100, 30, key="secondary_intensity")
    
    if st.button("🔆 组合光效", key="combine_lights"):
        result = {
            "layers": [
                {"type": primary_light, "intensity": primary_intensity/100},
            ],
            "total_intensity": (primary_intensity + (secondary_intensity if secondary_light != "无" else 0)) / 100
        }
        
        if secondary_light != "无":
            result["layers"].append({"type": secondary_light, "intensity": secondary_intensity/100})
            
        st.success("光效组合已生成！")
        st.json(result)

def render_transitions(st, state):
    """渲染转场特效"""
    st.subheader("转场特效库")
    
    transitions = state.effects_library.transitions
    
    # 分类展示
    for i, (trans_key, trans) in enumerate(transitions.items()):
        with st.expander(f"🔄 {trans['name']} ({trans['type']})"):
            st.write(f"**时长:** {trans['duration']}s")
            st.write(f"**类型:** {trans['type']}")
            
            # 动画预览
            if st.button(f"▶️ 预览转场", key=f"preview_trans_{trans_key}"):
                animation = state.preset_builder.transitions.generate_transition_animation(trans_key, trans['duration'])
                st.json(animation)
            
            if st.button(f"应用到剪辑", key=f"use_trans_{trans_key}"):
                st.success(f"✅ {trans['name']} 已设置")

def render_filters(st, state):
    """渲染滤镜"""
    st.subheader("滤镜库")
    
    filters = state.effects_library.filters
    
    filter_col1, filter_col2 = st.columns(2)
    
    for i, (filter_key, filter_data) in enumerate(filters.items()):
        with filter_col1 if i % 2 == 0 else filter_col2:
            with st.expander(f"🎨 {filter_data['name']}"):
                st.write(f"**对比度:** {filter_data['adjustments'].get('contrast', 1.0):.1f}")
                st.write(f"**饱和度:** {filter_data['adjustments'].get('saturation', 1.0):.1f}")
                st.write(f"**暗角:** {filter_data['vignette']:.0%}")
                
                # 强度调节
                intensity = st.slider("滤镜强度", 0, 100, 80, key=f"intensity_{filter_key}")
                
                if st.button(f"应用滤镜", key=f"apply_filter_{filter_key}"):
                    st.success(f"✅ {filter_data['name']} 已应用 (强度: {intensity}%)")
    
    # 色彩分级
    st.write("---")
    st.subheader("🎬 色彩分级")
    
    color_grading = state.preset_builder.color_grading
    
    scheme_col1, scheme_col2 = st.columns(2)
    with scheme_col1:
        color_scheme = st.selectbox("选择配色", list(color_grading.color_schemes.keys()), key="color_scheme_select")
    with scheme_col2:
        grade_intensity = st.slider("分级强度", 0, 100, 70, key="grade_intensity")
    
    if st.button("🎨 应用色彩分级", key="apply_grade_btn"):
        grade_result = color_grading.apply_color_grade(color_scheme, grade_intensity/100)
        st.success(f"✅ 色彩分级 {color_scheme} 已应用")
        st.json(grade_result)

def render_effect_presets(st, state):
    """渲染特效预设"""
    st.subheader("场景特效预设")
    
    presets = state.preset_builder.scene_presets
    
    # 预设选择
    preset_options = list(presets.keys())
    selected_preset = st.selectbox("选择预设", preset_options, key="preset_select")
    
    # 显示预设详情
    preset_detail = presets[selected_preset]
    
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.write(f"**预设名称:** {preset_detail['name']}")
        st.write(f"**特效:** {', '.join(preset_detail['effects'])}")
        st.write(f"**色调:** {preset_detail['color']}")
        
    with detail_col2:
        st.write(f"**转场:** {preset_detail['transition']}")
        st.write(f"**音效:** {preset_detail['sound_effect']}")
    
    # 构建并应用
    if st.button("🚀 应用预设", key="apply_preset_btn"):
        built_preset = state.preset_builder.build_scene_preset(selected_preset)
        st.success(f"✅ 预设 {preset_detail['name']} 已应用！")
        
        with st.expander("预设详情"):
            st.json(built_preset)
    
    # 组合预设
    st.write("---")
    st.write("**🛠️ 组合自定义预设**")
    
    combo_col1, combo_col2, combo_col3 = st.columns(3)
    
    with combo_col1:
        combo_effects = st.multiselect(
            "选择特效",
            list(state.effects_library.particle_effects.keys()),
            default=["energy", "light_rays"],
            key="combo_effects"
        )
    with combo_col2:
        combo_color = st.selectbox("色彩方案", list(state.preset_builder.color_grading.color_schemes.keys()), key="combo_color")
    with combo_col3:
        combo_transition = st.selectbox("转场", list(state.effects_library.transitions.keys()), key="combo_transition")
    
    if st.button("✨ 创建自定义预设", key="create_custom_preset"):
        custom = state.preset_builder.create_mixed_preset(combo_effects, combo_color, combo_transition)
        st.success("✅ 自定义预设已创建！")
        
        with st.expander("预设详情"):
            st.json(custom)
    
    # 预设预览
    st.write("---")
    st.subheader("🎬 实时预览")
    
    if st.button("▶️ 预览所有预设", key="preview_all_presets"):
        st.info("正在生成预设预览...")
        
        preview_cols = st.columns(4)
        for i, (preset_key, preset_data) in enumerate(presets.items()):
            with preview_cols[i % 4]:
                st.write(f"**{preset_data['name']}**")
                st.caption(f"特效: {len(preset_data['effects'])} | {preset_data['transition']}")
                st.progress(len(preset_data['effects']) / 5, text=preset_data['color'])


# v35: 兼容别名
def render_effects_library_page():
    """兼容 page 命名约定"""
    import streamlit as st_local
    render_effects_library_tab(st_local, st_local.session_state)
