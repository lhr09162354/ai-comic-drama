"""图像生成模块 v2 - 支持并行生成、自动重试、负面提示"""

import os
import io
import time
import requests
from openai import OpenAI
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import config

def generate_panel_image(prompt: str, panel_index: int, negative_prompt: str = "",
                         output_dir: str = "output/panels", max_retries: int = 3) -> str:
    """生成单格分镜画面，支持自动重试"""
    os.makedirs(output_dir, exist_ok=True)
    
    last_error = None
    for attempt in range(max_retries):
        try:
            backend = config.IMAGE_BACKEND
            if backend == "dalle":
                image_path = _generate_dalle(prompt, panel_index, output_dir)
            elif backend == "siliconflow":
                image_path = _generate_siliconflow(prompt, panel_index, output_dir, negative_prompt)
            elif backend == "stability":
                image_path = _generate_stability(prompt, panel_index, output_dir, negative_prompt)
            else:
                raise ValueError(f"不支持的图像后端: {backend}")
            return image_path
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)  # 指数退避: 2s, 4s, 8s
                time.sleep(wait)
    
    raise RuntimeError(f"画面生成失败（已重试{max_retries}次）: {last_error}")

def generate_panels_parallel(tasks: list, max_workers: int = 3) -> dict:
    """
    并行生成多格画面
    
    tasks: [{"prompt": str, "panel_index": int, "negative_prompt": str, "output_dir": str}]
    返回: {panel_index: image_path}
    """
    results = {}
    
    # DALL-E 并发有限制，降低并行数
    if config.IMAGE_BACKEND == "dalle":
        max_workers = min(max_workers, 2)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {}
        for task in tasks:
            future = executor.submit(
                generate_panel_image,
                prompt=task["prompt"],
                panel_index=task["panel_index"],
                negative_prompt=task.get("negative_prompt", ""),
                output_dir=task.get("output_dir", "output/panels"),
            )
            future_map[future] = task["panel_index"]
        
        for future in as_completed(future_map):
            panel_idx = future_map[future]
            try:
                path = future.result()
                results[panel_idx] = path
            except Exception as e:
                results[panel_idx] = None
                print(f"Panel {panel_idx} 生成失败: {e}")
    
    return results

def _generate_dalle(prompt: str, panel_index: int, output_dir: str) -> str:
    """DALL-E 生成"""
    api_key = config.DALLE_API_KEY or config.LLM_API_KEY
    client = OpenAI(api_key=api_key, base_url=config.LLM_BASE_URL)
    
    response = client.images.generate(
        model=config.DALLE_MODEL,
        prompt=prompt,
        size=config.DALLE_SIZE,
        quality=config.DALLE_QUALITY,
        n=1,
    )
    
    image_url = response.data[0].url
    img_data = requests.get(image_url, timeout=60).content
    image = Image.open(io.BytesIO(img_data))
    
    path = os.path.join(output_dir, f"panel_{panel_index:03d}.png")
    image.save(path, "PNG")
    return path

def _generate_siliconflow(prompt: str, panel_index: int, output_dir: str,
                          negative_prompt: str = "") -> str:
    """SiliconFlow 生成"""
    api_key = config.SILICONFLOW_API_KEY
    if not api_key:
        raise ValueError("请设置 SILICONFLOW_API_KEY")
    
    payload = {
        "model": config.SILICONFLOW_MODEL,
        "prompt": prompt,
        "image_size": "1024x1024",
        "num_inference_steps": 25,
    }
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    
    response = requests.post(
        "https://api.siliconflow.cn/v1/images/generations",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"SiliconFlow API 错误: {response.text}")
    
    data = response.json()
    image_url = data["images"][0]["url"]
    img_data = requests.get(image_url, timeout=60).content
    image = Image.open(io.BytesIO(img_data))
    
    path = os.path.join(output_dir, f"panel_{panel_index:03d}.png")
    image.save(path, "PNG")
    return path

def _generate_stability(prompt: str, panel_index: int, output_dir: str,
                        negative_prompt: str = "") -> str:
    """Stability AI 生成"""
    import base64
    api_key = config.STABILITY_API_KEY
    if not api_key:
        raise ValueError("请设置 STABILITY_API_KEY")
    
    text_prompts = [{"text": prompt, "weight": 1}]
    if negative_prompt:
        text_prompts.append({"text": negative_prompt, "weight": -1})
    
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        },
        json={
            "text_prompts": text_prompts,
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
        timeout=120,
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"Stability API 错误: {response.text}")
    
    data = response.json()
    img_bytes = base64.b64decode(data["artifacts"][0]["base64"])
    image = Image.open(io.BytesIO(img_bytes))
    
    path = os.path.join(output_dir, f"panel_{panel_index:03d}.png")
    image.save(path, "PNG")
    return path
