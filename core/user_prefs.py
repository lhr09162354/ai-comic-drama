"""用户偏好持久化 - 记住设置"""

import os
import json
import config

PREFS_FILE = os.path.join(config.OUTPUT_DIR, "_prefs.json")

def load_prefs() -> dict:
    """加载用户偏好"""
    defaults = {
        "lang": "zh",
        "style": "manga",
        "layout_template": "auto",
        "cover_template": "classic",
        "gen_char_sheets": True,
        "parallel_gen": True,
        "max_workers": 3,
        "auto_bubble": True,
        "watermark_text": "",
        "watermark_position": "bottom_right",
        "page_width": 1200,
        "page_height": 1600,
        "print_dpi": 300,
        "print_crop_marks": True,
        "print_bleed_mm": 3,
    }
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            defaults.update(saved)
        except Exception:
            pass
    return defaults

def save_prefs(prefs: dict):
    """保存用户偏好"""
    os.makedirs(os.path.dirname(PREFS_FILE), exist_ok=True)
    # 只保存有意义的字段
    saveable = {
        "lang", "style", "layout_template", "cover_template",
        "gen_char_sheets", "parallel_gen", "max_workers", "auto_bubble",
        "watermark_text", "watermark_position",
        "page_width", "page_height",
        "print_dpi", "print_crop_marks", "print_bleed_mm",
    }
    filtered = {k: v for k, v in prefs.items() if k in saveable}
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

def update_from_prefs(session_state):
    """从偏好文件更新session state"""
    prefs = load_prefs()
    mapping = {
        "lang": "lang", "style": "style", "layout_template": "layout_template",
        "cover_template": "cover_template", "gen_char_sheets": "gen_char_sheets",
        "parallel_gen": "parallel_gen", "max_workers": "max_workers",
        "auto_bubble": "auto_bubble", "watermark_text": "watermark_text",
        "watermark_position": "watermark_position",
        "page_width": None, "page_height": None,  # 这些更新到config
        "print_dpi": "print_dpi", "print_crop_marks": "print_crop_marks",
        "print_bleed_mm": "print_bleed_mm",
    }
    for prefs_key, state_key in mapping.items():
        if state_key and prefs_key in prefs:
            if state_key not in session_state or session_state[state_key] == DEF.get(state_key):
                session_state[state_key] = prefs[prefs_key]
    
    # 更新config
    if "page_width" in prefs: config.PAGE_WIDTH = prefs["page_width"]
    if "page_height" in prefs: config.PAGE_HEIGHT = prefs["page_height"]
    
    return prefs

DEF = dict(lang="zh", style="manga", layout_template="auto", cover_template="classic",
           gen_char_sheets=True, parallel_gen=True, max_workers=3, auto_bubble=True,
           watermark_text="", watermark_position="bottom_right",
           print_dpi=300, print_crop_marks=True, print_bleed_mm=3)
