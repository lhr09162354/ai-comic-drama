# -*- coding: utf-8 -*-
"""
AI漫剧自动生成器 v18 - 高级视频生成模块
支持可灵、Runway、Minimax、Pika等多个视频生成API
"""

import os
import json
import time
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse
import hashlib

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

class VideoProvider(Enum):
    """视频生成提供商"""
    KLING = "kling"
    RUNWAY = "runway"
    MINIMAX = "minimax"
    PIKA = "pika"
    FAL = "fal"
    LOCAL = "local"  # 本地FFmpeg生成

class VideoQuality(Enum):
    """视频质量等级"""
    DRAFT = "draft"        # 草稿级
    STANDARD = "standard"  # 标准
    HIGH = "high"          # 高清
    ULTRA = "ultra"        # 超清

class VideoAspectRatio(Enum):
    """视频宽高比"""
    PORTRAIT_9_16 = "9:16"      # 竖屏（抖音/快手）
    SQUARE_1_1 = "1:1"          # 方形
    LANDSCAPE_16_9 = "16:9"     # 横屏（YouTube）
    LANDSCAPE_4_3 = "4:3"       # 4:3横屏
    CINEMATIC_21_9 = "21:9"     # 电影宽屏

@dataclass
class VideoGenerationRequest:
    """视频生成请求"""
    prompt: str
    image: Optional[str] = None  # 图片路径或URL
    provider: VideoProvider = VideoProvider.KLING
    duration: int = 5
    quality: VideoQuality = VideoQuality.HIGH
    aspect_ratio: VideoAspectRatio = VideoAspectRatio.PORTRAIT_9_16
    seed: Optional[int] = None
    guidance_scale: float = 7.5
    negative_prompt: str = ""
    style: str = "anime"  # anime, realistic, cinematic, comic
    callback_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoGenerationResult:
    """视频生成结果"""
    success: bool
    video_url: Optional[str] = None
    local_path: Optional[str] = None
    provider: VideoProvider = VideoProvider.LOCAL
    duration: float = 0
    resolution: Tuple[int, int] = (1920, 1080)
    file_size_mb: float = 0
    generation_time: float = 0
    task_id: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseVideoGenerator:
    """视频生成器基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.api_key = config.get("api_key", "")
        self.endpoint = config.get("endpoint", "")

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Generator", "")

    def is_available(self) -> bool:
        """检查API是否可用"""
        return self.enabled and bool(self.api_key)

    async def generate(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """生成视频"""
        raise NotImplementedError

    async def get_status(self, task_id: str) -> str:
        """获取任务状态"""
        raise NotImplementedError

    async def download(self, video_url: str, save_path: Path) -> bool:
        """下载视频"""
        raise NotImplementedError

class KlingGenerator(BaseVideoGenerator):
    """可灵视频生成器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.default_duration = config.get("default_duration", 5)
        self.max_duration = config.get("max_duration", 60)
        self.default_quality = config.get("default_quality", "720p")

    async def generate(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """使用可灵API生成视频"""
        if not self.is_available():
            return VideoGenerationResult(
                success=False,
                error="可灵API未配置或未启用",
                provider=VideoProvider.KLING
            )

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "kling-v1",
                "prompt": request.prompt,
                "duration": min(request.duration, self.max_duration),
                "aspect_ratio": request.aspect_ratio.value,
                "quality": self.default_quality,
                "guidance_scale": request.guidance_scale
            }

            if request.image:
                payload["image"] = request.image
            if request.negative_prompt:
                payload["negative_prompt"] = request.negative_prompt
            if request.seed:
                payload["seed"] = request.seed

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.endpoint}/videos/generations",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                task_id = data.get("id")
                return VideoGenerationResult(
                    success=True,
                    task_id=task_id,
                    status="processing",
                    provider=VideoProvider.KLING,
                    metadata={"request": payload}
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"可灵API调用失败: {str(e)}",
                provider=VideoProvider.KLING
            )

    async def get_status(self, task_id: str) -> str:
        """获取可灵任务状态"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    f"{self.endpoint}/videos/generations/{task_id}",
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                return data.get("status", "unknown")
        except Exception:
            return "error"

class RunwayGenerator(BaseVideoGenerator):
    """Runway视频生成器"""

    async def generate(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """使用Runway API生成视频"""
        if not self.is_available():
            return VideoGenerationResult(
                success=False,
                error="Runway API未配置或未启用",
                provider=VideoProvider.RUNWAY
            )

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "gen3a_turbo",
                "prompt": request.prompt,
                "duration": request.duration,
                "aspect_ratio": request.aspect_ratio.value.replace(":", "x")
            }

            if request.image:
                payload["image"] = request.image

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.endpoint}/video_generation",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                return VideoGenerationResult(
                    success=True,
                    task_id=data.get("id"),
                    status="processing",
                    provider=VideoProvider.RUNWAY
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"Runway API调用失败: {str(e)}",
                provider=VideoProvider.RUNWAY
            )

class MinimaxGenerator(BaseVideoGenerator):
    """MiniMax视频生成器"""

    async def generate(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """使用MiniMax API生成视频"""
        if not self.is_available():
            return VideoGenerationResult(
                success=False,
                error="MiniMax API未配置或未启用",
                provider=VideoProvider.MINIMAX
            )

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "video-01",
                "prompt": request.prompt,
                "duration": request.duration,
                "aspect_ratio": request.aspect_ratio.value,
                "quality": self.config.get("default_quality", "1080p")
            }

            if request.image:
                payload["image_url"] = request.image

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.endpoint}/t2v",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                return VideoGenerationResult(
                    success=True,
                    task_id=data.get("task_id"),
                    status="processing",
                    provider=VideoProvider.MINIMAX
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"MiniMax API调用失败: {str(e)}",
                provider=VideoProvider.MINIMAX
            )

class PikaGenerator(BaseVideoGenerator):
    """Pika视频生成器"""

    async def generate(self, request: VideoGenerationRequest) -> VideoGenerationResult:
        """使用Pika API生成视频"""
        if not self.is_available():
            return VideoGenerationResult(
                success=False,
                error="Pika API未配置或未启用",
                provider=VideoProvider.PIKA
            )

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": request.prompt,
                "duration": request.duration,
                "aspect_ratio": request.aspect_ratio.value,
                "fps": 24,
                "model": "pika-v1"
            }

            if request.image:
                payload["image_url"] = request.image

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.endpoint}/generate",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                return VideoGenerationResult(
                    success=True,
                    task_id=data.get("id"),
                    status="processing",
                    provider=VideoProvider.PIKA
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"Pika API调用失败: {str(e)}",
                provider=VideoProvider.PIKA
            )

class LocalVideoGenerator:
    """本地视频生成器（使用FFmpeg）"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get("output_dir", "output/videos"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def is_available(self) -> bool:
        """检查FFmpeg是否可用"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    async def generate_from_images(
        self,
        images: List[str],
        duration_per_image: float = 2.0,
        transitions: List[str] = None,
        output_name: str = None
    ) -> VideoGenerationResult:
        """从图片序列生成视频"""
        if not self.is_available():
            return VideoGenerationResult(
                success=False,
                error="FFmpeg未安装",
                provider=VideoProvider.LOCAL
            )

        try:
            output_name = output_name or f"video_{int(time.time())}.mp4"
            output_path = self.output_dir / output_name

            # 创建临时文件列表
            list_file = self.output_dir / "filelist.txt"
            with open(list_file, "w") as f:
                for img in images:
                    f.write(f"file '{img}'\n")
                    f.write(f"duration {duration_per_image}\n")

            # 添加最后一个图片
            with open(list_file, "a") as f:
                f.write(f"file '{images[-1]}'\n")

            # 生成命令
            cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(list_file),
                "-vf", f"fps={self.config.get('default_fps', 30)},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                "-c:v", "libx264", "-preset", "medium",
                "-crf", "23", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k",
                str(output_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # 清理临时文件
                list_file.unlink()

                # 获取视频信息
                duration = self._get_duration(output_path)

                return VideoGenerationResult(
                    success=True,
                    local_path=str(output_path),
                    provider=VideoProvider.LOCAL,
                    duration=duration,
                    resolution=(1080, 1920),
                    file_size_mb=output_path.stat().st_size / (1024 * 1024),
                    status="completed"
                )
            else:
                return VideoGenerationResult(
                    success=False,
                    error=f"FFmpeg生成失败: {result.stderr}",
                    provider=VideoProvider.LOCAL
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"本地视频生成失败: {str(e)}",
                provider=VideoProvider.LOCAL
            )

    async def generate_with_audio(
        self,
        video_path: str,
        audio_path: str,
        output_name: str = None,
        fade_duration: float = 1.0
    ) -> VideoGenerationResult:
        """为视频添加音频"""
        try:
            output_name = output_name or f"video_with_audio_{int(time.time())}.mp4"
            output_path = self.output_dir / output_name

            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                "-af", f"afade=t=in:st=0:d={fade_duration},afade=t=out:st=-{fade_duration}:d={fade_duration}",
                str(output_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return VideoGenerationResult(
                    success=True,
                    local_path=str(output_path),
                    provider=VideoProvider.LOCAL,
                    status="completed"
                )
            else:
                return VideoGenerationResult(
                    success=False,
                    error=f"音频合成失败: {result.stderr}",
                    provider=VideoProvider.LOCAL
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"音频合成失败: {str(e)}",
                provider=VideoProvider.LOCAL
            )

    def _get_duration(self, video_path: Path) -> float:
        """获取视频时长"""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip()) if result.returncode == 0 else 0
        except Exception:
            return 0

class VideoGeneratorManager:
    """视频生成管理器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers: Dict[VideoProvider, BaseVideoGenerator] = {}
        self.local_generator = LocalVideoGenerator(config.get("local", {}))
        self._init_providers()

    def _init_providers(self):
        """初始化所有提供商"""
        video_config = self.config.get("video_api", {})

        # 可灵
        if "kling" in video_config:
            self.providers[VideoProvider.KLING] = KlingGenerator(video_config["kling"])

        # Runway
        if "runway" in video_config:
            self.providers[VideoProvider.RUNWAY] = RunwayGenerator(video_config["runway"])

        # MiniMax
        if "minimax" in video_config:
            self.providers[VideoProvider.MINIMAX] = MinimaxGenerator(video_config["minimax"])

        # Pika
        if "pika" in video_config:
            self.providers[VideoProvider.PIKA] = PikaGenerator(video_config["pika"])

    def get_available_providers(self) -> List[VideoProvider]:
        """获取可用的提供商"""
        available = []
        for provider, generator in self.providers.items():
            if generator.is_available():
                available.append(provider)
        if self.local_generator.is_available():
            available.append(VideoProvider.LOCAL)
        return available

    async def generate(
        self,
        request: VideoGenerationRequest,
        wait_for_completion: bool = True,
        poll_interval: int = 5,
        max_wait: int = 300
    ) -> VideoGenerationResult:
        """生成视频"""
        # 选择提供商
        provider = request.provider
        if provider not in self.providers:
            # 尝试使用本地生成器
            if self.local_generator.is_available() and provider == VideoProvider.LOCAL:
                return await self._generate_local_from_request(request)
            return VideoGenerationResult(
                success=False,
                error=f"提供商 {provider.value} 不可用"
            )

        generator = self.providers[provider]

        # 发起生成请求
        result = await generator.generate(request)

        if not result.success or not wait_for_completion:
            return result

        # 等待完成
        start_time = time.time()
        while time.time() - start_time < max_wait:
            status = await generator.get_status(result.task_id)
            result.status = status

            if status == "completed":
                result.status = "completed"
                return result
            elif status in ["failed", "error"]:
                result.success = False
                result.error = f"生成失败: {status}"
                return result

            await asyncio.sleep(poll_interval)

        result.error = "生成超时"
        return result

    async def _generate_local_from_request(
        self,
        request: VideoGenerationRequest
    ) -> VideoGenerationResult:
        """使用本地生成器生成视频"""
        # 如果有图片，使用本地生成器
        if request.image:
            return await self.local_generator.generate_from_images(
                images=[request.image],
                duration_per_image=request.duration
            )
        else:
            return VideoGenerationResult(
                success=False,
                error="本地生成需要提供图片",
                provider=VideoProvider.LOCAL
            )

    def get_provider_info(self, provider: VideoProvider) -> Dict[str, Any]:
        """获取提供商信息"""
        info = {
            "name": provider.value,
            "available": False,
            "features": {}
        }

        if provider == VideoProvider.LOCAL:
            info["available"] = self.local_generator.is_available()
            info["features"] = {
                "max_duration": "无限制",
                "quality_options": ["取决于硬件"],
                "requires_image": True
            }
        elif provider in self.providers:
            gen = self.providers[provider]
            info["available"] = gen.is_available()
            info["features"] = {
                "max_duration": gen.max_duration if hasattr(gen, "max_duration") else "未知",
                "quality_options": gen.config.get("quality_options", []),
                "requires_image": False
            }

        return info

class VideoComposer:
    """视频合成器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get("output_dir", "output/videos"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def compose_with_transitions(
        self,
        video_clips: List[str],
        transitions: List[str] = None,
        transition_duration: float = 0.5,
        output_name: str = None
    ) -> VideoGenerationResult:
        """使用转场效果合成视频"""
        if not video_clips:
            return VideoGenerationResult(
                success=False,
                error="没有视频片段"
            )

        try:
            output_name = output_name or f"composed_{int(time.time())}.mp4"
            output_path = self.output_dir / output_name

            # 使用FFmpeg滤镜链合成
            filter_complex = self._build_transition_filter(
                len(video_clips),
                transitions or ["fade"] * (len(video_clips) - 1),
                transition_duration
            )

            inputs = []
            for clip in video_clips:
                inputs.extend(["-i", clip])

            cmd = [
                "ffmpeg", "-y"
            ] + inputs + [
                "-filter_complex", filter_complex,
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac",
                str(output_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return VideoGenerationResult(
                    success=True,
                    local_path=str(output_path),
                    provider=VideoProvider.LOCAL,
                    status="completed"
                )
            else:
                return VideoGenerationResult(
                    success=False,
                    error=f"视频合成失败: {result.stderr}",
                    provider=VideoProvider.LOCAL
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"视频合成失败: {str(e)}",
                provider=VideoProvider.LOCAL
            )

    def _build_transition_filter(
        self,
        num_clips: int,
        transitions: List[str],
        duration: float
    ) -> str:
        """构建转场滤镜"""
        if num_clips == 1:
            return f"[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2[v]"

        filters = []
        for i in range(num_clips):
            filters.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30,setsar=1[v{i}]")

        # 添加转场
        for i, transition in enumerate(transitions):
            if transition == "fade":
                filters.append(
                    f"[v{i}][v{i+1}]xfade=transition=fade:duration={duration}:offset={i*5}[v{i}_fade];"
                )
            elif transition == "dissolve":
                filters.append(
                    f"[v{i}][v{i+1}]xfade=transition=dissolve:duration={duration}:offset={i*5}[v{i}_fade];"
                )
            elif transition == "wipe_left":
                filters.append(
                    f"[v{i}][v{i+1}]xfade=transition=hl wipe:duration={duration}:offset={i*5}[v{i}_fade];"
                )
            elif transition == "wipe_right":
                filters.append(
                    f"[v{i}][v{i+1}]xfade=transition=hr wipe:duration={duration}:offset={i*5}[v{i}_fade];"
                )
            elif transition == "zoom_in":
                filters.append(
                    f"[v{i}][v{i+1}]xfade=transition=zoom:duration={duration}:offset={i*5}[v{i}_fade];"
                )

        # 最后一帧
        filters.append(f"[v{num_clips-1}_fade]null[vout]")

        return "".join(filters[:-1]) + "[vout]"

    async def add_subtitles(
        self,
        video_path: str,
        subtitles: List[Dict[str, str]],
        output_name: str = None
    ) -> VideoGenerationResult:
        """添加字幕到视频"""
        try:
            output_name = output_name or f"subtitled_{int(time.time())}.mp4"
            output_path = self.output_dir / output_name

            # 生成字幕文件
            srt_path = self.output_dir / f"temp_{int(time.time())}.srt"
            self._write_srt(subtitles, srt_path)

            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", f"subtitles='{srt_path}':force_style='FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=2,Bold=1'",
                "-c:a", "copy",
                str(output_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            # 清理临时字幕文件
            srt_path.unlink(missing_ok=True)

            if result.returncode == 0:
                return VideoGenerationResult(
                    success=True,
                    local_path=str(output_path),
                    provider=VideoProvider.LOCAL,
                    status="completed"
                )
            else:
                return VideoGenerationResult(
                    success=False,
                    error=f"字幕添加失败: {result.stderr}",
                    provider=VideoProvider.LOCAL
                )

        except Exception as e:
            return VideoGenerationResult(
                success=False,
                error=f"字幕添加失败: {str(e)}",
                provider=VideoProvider.LOCAL
            )

    def _write_srt(self, subtitles: List[Dict[str, str]], output_path: Path):
        """写入SRT字幕文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            for i, sub in enumerate(subtitles, 1):
                start = self._format_srt_time(sub.get("start", 0))
                end = self._format_srt_time(sub.get("end", 0))
                text = sub.get("text", "")

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

    def _format_srt_time(self, seconds: float) -> str:
        """格式化SRT时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

# 导出
__all__ = [
    "VideoProvider",
    "VideoQuality",
    "VideoAspectRatio",
    "VideoGenerationRequest",
    "VideoGenerationResult",
    "VideoGeneratorManager",
    "VideoComposer",
    "BaseVideoGenerator",
    "KlingGenerator",
    "RunwayGenerator",
    "MinimaxGenerator",
    "PikaGenerator",
    "LocalVideoGenerator"
]
