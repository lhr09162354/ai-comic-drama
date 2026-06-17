"""项目存档管理 - 保存/加载/列出项目"""

import os
import json
import time
from datetime import datetime
import config

def _projects_dir() -> str:
    d = os.path.join(config.OUTPUT_DIR, "_projects")
    os.makedirs(d, exist_ok=True)
    return d

def save_project(project_name: str, script: dict, character_sheets: dict,
                 pages_data: list, meta: dict = None) -> str:
    """保存项目，返回项目文件路径"""
    safe_name = "".join(c for c in project_name if c.isalnum() or c in "_-") or "untitled"
    proj_dir = os.path.join(_projects_dir(), safe_name)
    os.makedirs(proj_dir, exist_ok=True)
    
    project = {
        "name": project_name,
        "saved_at": datetime.now().isoformat(),
        "script": script,
        "character_sheets": character_sheets,
        "pages_data": pages_data,
        "meta": meta or {},
    }
    
    path = os.path.join(proj_dir, "project.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=2, default=str)
    
    return path

def load_project(project_name: str) -> dict:
    """加载项目"""
    safe_name = "".join(c for c in project_name if c.isalnum() or c in "_-") or "untitled"
    path = os.path.join(_projects_dir(), safe_name, "project.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"项目不存在: {project_name}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_projects() -> list:
    """列出所有已保存项目"""
    projects = []
    proj_dir = _projects_dir()
    if not os.path.exists(proj_dir):
        return projects
    
    for name in os.listdir(proj_dir):
        proj_path = os.path.join(proj_dir, name, "project.json")
        if os.path.exists(proj_path):
            try:
                with open(proj_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                projects.append({
                    "name": data.get("name", name),
                    "saved_at": data.get("saved_at", "未知"),
                    "title": data.get("script", {}).get("title", "未命名"),
                    "pages": len(data.get("script", {}).get("pages", [])),
                })
            except Exception:
                projects.append({"name": name, "saved_at": "读取失败", "title": name, "pages": 0})
    
    # 按保存时间倒序
    projects.sort(key=lambda x: x.get("saved_at", ""), reverse=True)
    return projects

def delete_project(project_name: str) -> bool:
    """删除项目"""
    import shutil
    safe_name = "".join(c for c in project_name if c.isalnum() or c in "_-") or "untitled"
    proj_dir = os.path.join(_projects_dir(), safe_name)
    if os.path.exists(proj_dir):
        shutil.rmtree(proj_dir)
        return True
    return False
