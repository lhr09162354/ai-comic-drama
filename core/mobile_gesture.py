"""
AI Comic Drama Generator v15 - 移动端手势交互模块
支持触摸手势、滑动导航、缩放等移动端优化
"""

import streamlit as st
import json
from typing import Callable, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

class GestureType(Enum):
    """手势类型枚举"""
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"
    PINCH_IN = "pinch_in"
    PINCH_OUT = "pinch_out"
    LONG_PRESS = "long_press"
    DOUBLE_TAP = "double_tap"
    SINGLE_TAP = "single_tap"
    DRAG = "drag"

@dataclass
class GestureEvent:
    """手势事件数据"""
    gesture_type: GestureType
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    distance: float
    duration: float
    scale: float = 1.0
    timestamp: float = 0

class GestureConfig:
    """手势配置"""
    
    DEFAULTS = {
        "swipe_threshold": 50,      # 滑动阈值（像素）
        "swipe_velocity_threshold": 0.3,  # 滑动速度阈值
        "long_press_duration": 0.5,  # 长按持续时间（秒）
        "double_tap_interval": 0.3,   # 双击间隔（秒）
        "pinch_scale_min": 0.5,      # 最小缩放
        "pinch_scale_max": 3.0,      # 最大缩放
        "drag_threshold": 10,        # 拖拽阈值
    }
    
    @classmethod
    def get_config(cls, custom: Dict = None) -> Dict:
        """获取配置"""
        config = cls.DEFAULTS.copy()
        if custom:
            config.update(custom)
        return config

class TouchNavigation:
    """触摸导航控制器"""
    
    def __init__(self, config: Dict = None):
        self.config = GestureConfig.get_config(config)
        self.current_panel = 0
        self.total_panels = 0
        self.current_chapter = 0
        self.total_chapters = 0
        self._callbacks = {}
    
    def set_content_info(
        self,
        current_panel: int,
        total_panels: int,
        current_chapter: int = 0,
        total_chapters: int = 1
    ):
        """设置内容信息"""
        self.current_panel = current_panel
        self.total_panels = total_panels
        self.current_chapter = current_chapter
        self.total_chapters = total_chapters
    
    def register_callback(self, gesture: GestureType, callback: Callable):
        """注册手势回调"""
        self._callbacks[gesture] = callback
    
    def handle_gesture(self, event: GestureEvent) -> Optional[str]:
        """
        处理手势事件
        
        Args:
            event: 手势事件
        
        Returns:
            动作描述
        """
        action = None
        
        # 根据手势类型处理
        if event.gesture_type == GestureType.SWIPE_LEFT:
            if self.current_panel < self.total_panels - 1:
                self.current_panel += 1
                action = "next_panel"
        
        elif event.gesture_type == GestureType.SWIPE_RIGHT:
            if self.current_panel > 0:
                self.current_panel -= 1
                action = "prev_panel"
        
        elif event.gesture_type == GestureType.SWIPE_UP:
            if self.current_chapter < self.total_chapters - 1:
                self.current_chapter += 1
                self.current_panel = 0
                action = "next_chapter"
        
        elif event.gesture_type == GestureType.SWIPE_DOWN:
            if self.current_chapter > 0:
                self.current_chapter -= 1
                self.current_panel = 0
                action = "prev_chapter"
        
        elif event.gesture_type == GestureType.DOUBLE_TAP:
            action = "toggle_fullscreen"
        
        elif event.gesture_type == GestureType.LONG_PRESS:
            action = "show_context_menu"
        
        elif event.gesture_type == GestureType.PINCH_IN:
            action = "zoom_out"
        
        elif event.gesture_type == GestureType.PINCH_OUT:
            action = "zoom_in"
        
        # 执行回调
        if action and action in self._callbacks:
            self._callbacks[action]()
        
        return action
    
    def get_state(self) -> Dict:
        """获取导航状态"""
        return {
            "panel": self.current_panel,
            "total_panels": self.total_panels,
            "chapter": self.current_chapter,
            "total_chapters": self.total_chapters,
        }

class GestureDetector:
    """手势检测器（JavaScript桥接）"""
    
    # JavaScript手势检测代码
    GESTURE_JS = """
    <script>
    class GestureDetector {
        constructor(options = {}) {
            this.swipeThreshold = options.swipeThreshold || 50;
            this.longPressDuration = options.longPressDuration || 500;
            this.doubleTapInterval = options.doubleTapInterval || 300;
            this.pinchScaleMin = options.pinchScaleMin || 0.5;
            this.pinchScaleMax = options.pinchScaleMax || 3;
            
            this.touchStartX = 0;
            this.touchStartY = 0;
            this.touchStartTime = 0;
            this.lastTapTime = 0;
            this.lastTapX = 0;
            this.lastTapY = 0;
            this.longPressTimer = null;
            this.initialDistance = 0;
            this.initialScale = 1;
            
            this.element = null;
            this.callbacks = {};
        }
        
        attach(element) {
            this.element = element;
            
            element.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
            element.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
            element.addEventListener('touchend', (e) => this.onTouchEnd(e), { passive: false });
            element.addEventListener('touchcancel', (e) => this.onTouchCancel(e));
            
            // 禁用默认触摸行为
            element.style.touchAction = 'none';
            element.style.webkitTouchCallout = 'none';
            element.style.webkitUserSelect = 'none';
            element.style.userSelect = 'none';
        }
        
        detach() {
            if (!this.element) return;
            
            this.element.removeEventListener('touchstart', this.onTouchStart);
            this.element.removeEventListener('touchmove', this.onTouchMove);
            this.element.removeEventListener('touchend', this.onTouchEnd);
            this.element.removeEventListener('touchcancel', this.onTouchCancel);
        }
        
        on(event, callback) {
            this.callbacks[event] = callback;
        }
        
        emit(event, data) {
            if (this.callbacks[event]) {
                this.callbacks[event](data);
            }
        }
        
        onTouchStart(e) {
            e.preventDefault();
            
            if (e.touches.length === 1) {
                const touch = e.touches[0];
                this.touchStartX = touch.clientX;
                this.touchStartY = touch.clientY;
                this.touchStartTime = Date.now();
                
                // 长按检测
                this.longPressTimer = setTimeout(() => {
                    this.emit('gesture', { type: 'long_press', x: touch.clientX, y: touch.clientY });
                }, this.longPressDuration);
            }
            
            if (e.touches.length === 2) {
                this.initialDistance = this.getDistance(e.touches[0], e.touches[1]);
                this.initialScale = 1;
                clearTimeout(this.longPressTimer);
            }
        }
        
        onTouchMove(e) {
            e.preventDefault();
            
            if (e.touches.length === 2) {
                const currentDistance = this.getDistance(e.touches[0], e.touches[1]);
                const scale = currentDistance / this.initialDistance;
                
                this.emit('gesture', {
                    type: scale > 1 ? 'pinch_out' : 'pinch_in',
                    scale: Math.min(Math.max(scale, this.pinchScaleMin), this.pinchScaleMax)
                });
            }
        }
        
        onTouchEnd(e) {
            clearTimeout(this.longPressTimer);
            
            if (e.changedTouches.length === 1) {
                const touch = e.changedTouches[0];
                const deltaX = touch.clientX - this.touchStartX;
                const deltaY = touch.clientY - this.touchStartY;
                const duration = Date.now() - this.touchStartTime;
                
                // 双击检测
                const timeSinceLastTap = Date.now() - this.lastTapTime;
                const distSinceLastTap = Math.sqrt(
                    Math.pow(touch.clientX - this.lastTapX, 2) +
                    Math.pow(touch.clientY - this.lastTapY, 2)
                );
                
                if (timeSinceLastTap < this.doubleTapInterval && distSinceLastTap < 30) {
                    this.emit('gesture', { type: 'double_tap', x: touch.clientX, y: touch.clientY });
                    this.lastTapTime = 0;
                    return;
                }
                
                this.lastTapTime = Date.now();
                this.lastTapX = touch.clientX;
                this.lastTapY = touch.clientY;
                
                // 滑动检测
                const absDeltaX = Math.abs(deltaX);
                const absDeltaY = Math.abs(deltaY);
                
                if (Math.max(absDeltaX, absDeltaY) > this.swipeThreshold) {
                    if (absDeltaX > absDeltaY) {
                        this.emit('gesture', {
                            type: deltaX > 0 ? 'swipe_right' : 'swipe_left',
                            deltaX, deltaY, duration
                        });
                    } else {
                        this.emit('gesture', {
                            type: deltaY > 0 ? 'swipe_down' : 'swipe_up',
                            deltaX, deltaY, duration
                        });
                    }
                } else if (duration < 200 && absDeltaX < 10 && absDeltaY < 10) {
                    this.emit('gesture', { type: 'tap', x: touch.clientX, y: touch.clientY });
                }
            }
        }
        
        onTouchCancel(e) {
            clearTimeout(this.longPressTimer);
        }
        
        getDistance(touch1, touch2) {
            const dx = touch1.clientX - touch2.clientX;
            const dy = touch1.clientY - touch2.clientY;
            return Math.sqrt(dx * dx + dy * dy);
        }
    }
    
    // 初始化手势检测器
    window.gestureDetector = new GestureDetector({
        swipeThreshold: 50,
        longPressDuration: 500,
        doubleTapInterval: 300
    });
    </script>
    """
    
    @staticmethod
    def get_js() -> str:
        """获取JavaScript代码"""
        return GestureDetector.GESTURE_JS

class MobileLayout:
    """移动端布局优化"""
    
    @staticmethod
    def get_thumb_zone_buttons() -> str:
        """获取拇指区按钮布局的HTML"""
        return """
        <style>
        /* 拇指区按钮布局 */
        .thumb-zone {
            position: fixed;
            bottom: 20px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 1000;
            pointer-events: none;
        }
        
        .thumb-zone-btn {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: rgba(74, 144, 217, 0.9);
            color: white;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            pointer-events: auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s, background 0.2s;
        }
        
        .thumb-zone-btn:active {
            transform: scale(0.95);
            background: rgba(74, 144, 217, 1);
        }
        
        .thumb-zone-btn.prev { margin-right: auto; }
        .thumb-zone-btn.next { margin-left: auto; }
        </style>
        
        <div class="thumb-zone" id="thumbZone" style="display: none;">
            <button class="thumb-zone-btn prev" onclick="window.gesturePrev()">◀</button>
            <button class="thumb-zone-btn next" onclick="window.gestureNext()">▶</button>
        </div>
        """
    
    @staticmethod
    def get_gesture_hint() -> str:
        """获取手势提示"""
        return """
        <style>
        .gesture-hint {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 20px 30px;
            border-radius: 12px;
            font-size: 18px;
            z-index: 2000;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        }
        
        .gesture-hint.show {
            opacity: 1;
        }
        </style>
        
        <div class="gesture-hint" id="gestureHint"></div>
        
        <script>
        function showGestureHint(text) {
            const hint = document.getElementById('gestureHint');
            hint.textContent = text;
            hint.classList.add('show');
            setTimeout(() => hint.classList.remove('show'), 1000);
        }
        
        window.showGestureHint = showGestureHint;
        </script>
        """
    
    @staticmethod
    def detect_mobile() -> str:
        """检测移动端并注入优化代码"""
        return """
        <script>
        function isMobile() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        }
        
        function isTouchDevice() {
            return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        }
        
        // 移动端优化
        if (isMobile() || isTouchDevice()) {
            document.body.classList.add('mobile-optimized');
            
            // 显示拇指区按钮
            setTimeout(() => {
                const thumbZone = document.getElementById('thumbZone');
                if (thumbZone) thumbZone.style.display = 'flex';
            }, 1000);
        }
        </script>
        """

class SwipeReader:
    """滑动阅读器"""
    
    def __init__(self, panels: List[str]):
        self.panels = panels
        self.current_index = 0
        self.history = []
    
    def next(self) -> Optional[str]:
        """下一格"""
        if self.current_index < len(self.panels) - 1:
            self.history.append(self.current_index)
            self.current_index += 1
            return self.panels[self.current_index]
        return None
    
    def prev(self) -> Optional[str]:
        """上一格"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.panels[self.current_index]
        return None
    
    def go_to(self, index: int) -> Optional[str]:
        """跳转到指定格子"""
        if 0 <= index < len(self.panels):
            self.history.append(self.current_index)
            self.current_index = index
            return self.panels[self.current_index]
        return None
    
    def get_current(self) -> Optional[str]:
        """获取当前格子"""
        return self.panels[self.current_index] if 0 <= self.current_index < len(self.panels) else None
    
    def can_next(self) -> bool:
        """能否下一格"""
        return self.current_index < len(self.panels) - 1
    
    def can_prev(self) -> bool:
        """能否上一格"""
        return self.current_index > 0
    
    def get_progress(self) -> Dict:
        """获取阅读进度"""
        return {
            "current": self.current_index + 1,
            "total": len(self.panels),
            "percentage": (self.current_index + 1) / len(self.panels) * 100 if self.panels else 0
        }

class GestureShortcutManager:
    """手势快捷键管理器"""
    
    DEFAULT_SHORTCUTS = {
        "swipe_left": "下一页",
        "swipe_right": "上一页",
        "swipe_up": "下一章",
        "swipe_down": "上一章",
        "double_tap": "全屏",
        "long_press": "菜单",
        "pinch_in": "缩小",
        "pinch_out": "放大",
    }
    
    def __init__(self):
        self.shortcuts = self.DEFAULT_SHORTCUTS.copy()
        self.enabled = True
    
    def customize_shortcut(self, gesture: str, action: str):
        """自定义快捷键"""
        self.shortcuts[gesture] = action
    
    def get_shortcuts(self) -> Dict:
        """获取快捷键配置"""
        return self.shortcuts.copy()
    
    def render_shortcuts_help(self) -> str:
        """渲染快捷键帮助"""
        items = [f"**{g}** → {a}" for g, a in self.shortcuts.items()]
        return "### 手势快捷键\n\n" + "\n".join(items)

def render_mobile_gesture_ui():
    """渲染移动端手势设置UI"""
    st.subheader("📱 移动端手势设置")
    
    # 手势开关
    enable_gestures = st.checkbox("启用手势操作", value=True)
    
    if enable_gestures:
        # 手势设置
        with st.expander("⚙️ 手势配置"):
            col1, col2 = st.columns(2)
            
            with col1:
                swipe_threshold = st.slider(
                    "滑动阈值", 30, 100, 50,
                    help="触发滑动所需的最小距离（像素）"
                )
                long_press = st.slider(
                    "长按时间", 0.3, 1.0, 0.5, step=0.1,
                    help="长按持续多久触发"
                )
            
            with col2:
                double_tap = st.slider(
                    "双击间隔", 0.2, 0.5, 0.3, step=0.05,
                    help="两次点击的最大间隔"
                )
                zoom_range = st.slider(
                    "缩放范围", 1, 4, (0.5, 3.0),
                    help="双指缩放的范围"
                )
        
        # 手势动作映射
        with st.expander("🎮 手势动作映射"):
            st.info("自定义各手势对应的操作")
            
            gestures = {
                "swipe_left": "左滑",
                "swipe_right": "右滑",
                "swipe_up": "上滑",
                "swipe_down": "下滑",
                "double_tap": "双击",
                "long_press": "长按",
            }
            
            actions = {
                "next_panel": "下一格",
                "prev_panel": "上一格",
                "next_chapter": "下一章",
                "prev_chapter": "上一章",
                "toggle_fullscreen": "全屏/退出全屏",
                "show_context_menu": "显示菜单",
                "zoom_in": "放大",
                "zoom_out": "缩小",
            }
            
            mappings = {}
            for gesture, gesture_name in gestures.items():
                mappings[gesture] = st.selectbox(
                    gesture_name,
                    options=list(actions.keys()),
                    format_func=lambda x: actions[x],
                    index=list(actions.keys()).index(
                        GestureShortcutManager.DEFAULT_SHORTCUTS.get(gesture, "next_panel")
                        .replace("下一页", "next_panel")
                        .replace("上一页", "prev_panel")
                        .replace("下一章", "next_chapter")
                        .replace("上一章", "prev_chapter")
                        .replace("全屏", "toggle_fullscreen")
                        .replace("菜单", "show_context_menu")
                    ) if gesture in GestureShortcutManager.DEFAULT_SHORTCUTS else 0
                )
        
        # 拇指区按钮
        show_thumb_buttons = st.checkbox("显示拇指区快捷按钮", value=True)
        
        # 手势提示
        show_gesture_hints = st.checkbox("显示手势操作提示", value=True)
    
    # 阅读模式
    st.divider()
    st.subheader("📖 阅读模式")
    
    read_mode = st.radio(
        "阅读方式",
        options=["滑动阅读", "点击翻页", "自动播放"],
        horizontal=True
    )
    
    if read_mode == "滑动阅读":
        st.success("✓ 左右滑动切换面板，上下滑动切换章节")
    elif read_mode == "点击翻页":
        st.success("✓ 点击屏幕两侧翻页")
    else:
        auto_play_interval = st.slider("自动播放间隔", 2, 10, 4, help="秒")
        st.success(f"✓ 每 {auto_play_interval} 秒自动播放下一格")
    
    return {
        "enabled": enable_gestures,
        "swipe_threshold": swipe_threshold if 'swipe_threshold' in dir() else 50,
        "long_press": long_press if 'long_press' in dir() else 0.5,
        "double_tap": double_tap if 'double_tap' in dir() else 0.3,
        "zoom_range": zoom_range if 'zoom_range' in dir() else (0.5, 3.0),
        "show_thumb_buttons": show_thumb_buttons if 'show_thumb_buttons' in dir() else True,
        "show_gesture_hints": show_gesture_hints if 'show_gesture_hints' in dir() else True,
        "read_mode": read_mode,
    }
