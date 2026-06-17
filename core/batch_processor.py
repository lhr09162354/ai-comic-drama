"""
批量处理系统
支持多集批量生成、断点续传、队列管理
"""
import json
import time
import threading
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid

class BatchStatus(Enum):
    """批处理状态"""
    PENDING = "pending"           # 等待中
    RUNNING = "running"          # 运行中
    PAUSED = "paused"            # 已暂停
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"            # 失败
    CANCELLED = "cancelled"      # 已取消

class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

@dataclass
class BatchTask:
    """批处理任务"""
    id: str
    name: str
    task_type: str  # 'generate_episode', 'generate_character', etc.
    params: Dict
    priority: TaskPriority = TaskPriority.NORMAL
    status: BatchStatus = BatchStatus.PENDING
    progress: float = 0.0  # 0.0 - 1.0
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

@dataclass
class BatchJob:
    """批量作业"""
    id: str
    name: str
    description: str = ""
    tasks: List[BatchTask] = field(default_factory=list)
    status: BatchStatus = BatchStatus.PENDING
    progress: float = 0.0
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    settings: Dict = field(default_factory=dict)
    checkpoints: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.total_tasks and self.tasks:
            self.total_tasks = len(self.tasks)

class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total: int, callback: Optional[Callable] = None):
        self.total = total
        self.completed = 0
        self.failed = 0
        self.current_task = ""
        self.start_time = time.time()
        self.callback = callback
        self._lock = threading.Lock()
    
    def update(
        self,
        increment: float = 0.0,
        task_name: str = "",
        status: str = ""
    ) -> Dict:
        """更新进度"""
        with self._lock:
            if increment > 0:
                self.completed += increment
            
            if task_name:
                self.current_task = task_name
            
            progress = self.total > 0 and self.completed / self.total or 0
            elapsed = time.time() - self.start_time
            eta = elapsed / progress - elapsed if progress > 0 else 0
            
            info = {
                'progress': min(1.0, progress),
                'progress_percent': f"{min(100, progress * 100):.1f}%",
                'completed': self.completed,
                'total': self.total,
                'failed': self.failed,
                'current_task': self.current_task,
                'elapsed_seconds': elapsed,
                'eta_seconds': max(0, eta),
                'eta_formatted': self._format_eta(eta),
                'status': status
            }
            
            if self.callback:
                self.callback(info)
            
            return info
    
    def _format_eta(self, seconds: float) -> str:
        """格式化剩余时间"""
        if seconds < 60:
            return f"{int(seconds)}秒"
        elif seconds < 3600:
            return f"{int(seconds / 60)}分钟"
        else:
            hours = int(seconds / 3600)
            mins = int((seconds % 3600) / 60)
            return f"{hours}小时{mins}分钟"
    
    def fail(self):
        """标记失败"""
        with self._lock:
            self.failed += 1
            self.completed += 1

class CheckpointManager:
    """断点管理器"""
    
    def __init__(self, storage_path: str = "checkpoints"):
        self.storage_path = storage_path
        self.checkpoints = {}
    
    def save_checkpoint(
        self,
        job_id: str,
        task_id: str,
        state: Dict
    ) -> str:
        """保存断点"""
        checkpoint_id = f"{job_id}_{task_id}_{int(time.time())}"
        
        checkpoint = {
            'id': checkpoint_id,
            'job_id': job_id,
            'task_id': task_id,
            'state': state,
            'timestamp': datetime.now().isoformat()
        }
        
        self.checkpoints[checkpoint_id] = checkpoint
        return checkpoint_id
    
    def load_checkpoint(
        self,
        job_id: str,
        task_id: Optional[str] = None
    ) -> Optional[Dict]:
        """加载断点"""
        if task_id:
            # 加载特定任务的断点
            for cp in self.checkpoints.values():
                if cp['job_id'] == job_id and cp['task_id'] == task_id:
                    return cp
        else:
            # 加载最新断点
            for cp in sorted(
                self.checkpoints.values(),
                key=lambda x: x['timestamp'],
                reverse=True
            ):
                if cp['job_id'] == job_id:
                    return cp
        return None
    
    def get_job_checkpoints(self, job_id: str) -> List[Dict]:
        """获取作业的所有断点"""
        return [
            cp for cp in self.checkpoints.values()
            if cp['job_id'] == job_id
        ]
    
    def clear_checkpoints(self, job_id: str):
        """清除作业的断点"""
        to_remove = [
            cid for cid, cp in self.checkpoints.items()
            if cp['job_id'] == job_id
        ]
        for cid in to_remove:
            del self.checkpoints[cid]

class TaskQueue:
    """任务队列"""
    
    def __init__(self, max_concurrent: int = 2):
        self.queue: List[BatchTask] = []
        self.running: List[BatchTask] = []
        self.completed: List[BatchTask] = []
        self.failed: List[BatchTask] = []
        self.max_concurrent = max_concurrent
        self._lock = threading.Lock()
    
    def add(self, task: BatchTask) -> str:
        """添加任务"""
        with self._lock:
            self.queue.append(task)
            self._sort_queue()
        return task.id
    
    def add_batch(self, tasks: List[BatchTask]) -> List[str]:
        """批量添加任务"""
        return [self.add(task) for task in tasks]
    
    def get_next(self) -> Optional[BatchTask]:
        """获取下一个任务"""
        with self._lock:
            if len(self.running) >= self.max_concurrent:
                return None
            
            if not self.queue:
                return None
            
            # 获取最高优先级任务
            task = self.queue.pop(0)
            task.status = BatchStatus.RUNNING
            task.started_at = datetime.now().isoformat()
            self.running.append(task)
            return task
    
    def complete(self, task_id: str, result: Optional[Dict] = None):
        """标记任务完成"""
        with self._lock:
            task = self._find_task(task_id, self.running)
            if task:
                task.status = BatchStatus.COMPLETED
                task.result = result
                task.completed_at = datetime.now().isoformat()
                task.progress = 1.0
                self.running.remove(task)
                self.completed.append(task)
    
    def fail(self, task_id: str, error: str):
        """标记任务失败"""
        with self._lock:
            task = self._find_task(task_id, self.running)
            if task:
                task.retry_count += 1
                if task.retry_count < task.max_retries:
                    # 重试
                    task.status = BatchStatus.PENDING
                    self.running.remove(task)
                    self.queue.insert(0, task)
                else:
                    # 彻底失败
                    task.status = BatchStatus.FAILED
                    task.error = error
                    task.completed_at = datetime.now().isoformat()
                    self.running.remove(task)
                    self.failed.append(task)
    
    def pause(self, task_id: str):
        """暂停任务"""
        with self._lock:
            task = self._find_task(task_id, self.running)
            if task:
                task.status = BatchStatus.PAUSED
                self.running.remove(task)
                self.queue.insert(0, task)
    
    def cancel(self, task_id: str):
        """取消任务"""
        with self._lock:
            task = self._find_task(task_id, self.queue + self.running)
            if task:
                task.status = BatchStatus.CANCELLED
                task.completed_at = datetime.now().isoformat()
                if task in self.queue:
                    self.queue.remove(task)
                if task in self.running:
                    self.running.remove(task)
    
    def get_status(self) -> Dict:
        """获取队列状态"""
        with self._lock:
            return {
                'pending': len(self.queue),
                'running': len(self.running),
                'completed': len(self.completed),
                'failed': len(self.failed),
                'total': len(self.queue) + len(self.running) + 
                         len(self.completed) + len(self.failed)
            }
    
    def _sort_queue(self):
        """按优先级排序队列"""
        self.queue.sort(key=lambda t: t.priority.value, reverse=True)
    
    def _find_task(self, task_id: str, task_list: List[BatchTask]) -> Optional[BatchTask]:
        """查找任务"""
        for task in task_list:
            if task.id == task_id:
                return task
        return None

class BatchProcessor:
    """批量处理器 - 主控制器"""
    
    def __init__(self, max_concurrent: int = 2):
        self.queue = TaskQueue(max_concurrent)
        self.checkpoint_manager = CheckpointManager()
        self.current_job: Optional[BatchJob] = None
        self.worker_thread: Optional[threading.Thread] = None
        self.running = False
        self.paused = False
        self.progress_callback: Optional[Callable] = None
    
    def create_job(
        self,
        name: str,
        description: str = "",
        settings: Optional[Dict] = None
    ) -> str:
        """创建批量作业"""
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        
        job = BatchJob(
            id=job_id,
            name=name,
            description=description,
            settings=settings or {}
        )
        
        self.current_job = job
        return job_id
    
    def add_tasks(
        self,
        job_id: str,
        tasks: List[Dict]
    ) -> int:
        """向作业添加任务"""
        if not self.current_job or self.current_job.id != job_id:
            return 0
        
        batch_tasks = []
        for task_data in tasks:
            task = BatchTask(
                id=f"task_{uuid.uuid4().hex[:8]}",
                name=task_data.get('name', '未命名任务'),
                task_type=task_data.get('type', 'default'),
                params=task_data.get('params', {}),
                priority=TaskPriority(task_data.get('priority', 2))
            )
            batch_tasks.append(task)
            self.queue.add(task)
        
        self.current_job.tasks.extend(batch_tasks)
        self.current_job.total_tasks = len(self.current_job.tasks)
        
        return len(batch_tasks)
    
    def start(self, callback: Optional[Callable] = None) -> bool:
        """开始处理"""
        if not self.current_job or not self.current_job.tasks:
            return False
        
        self.progress_callback = callback
        self.current_job.status = BatchStatus.RUNNING
        self.current_job.started_at = datetime.now().isoformat()
        self.running = True
        self.paused = False
        
        # 启动工作线程
        self.worker_thread = threading.Thread(target=self._process_loop)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
        return True
    
    def pause(self):
        """暂停处理"""
        self.paused = True
        if self.current_job:
            self.current_job.status = BatchStatus.PAUSED
    
    def resume(self):
        """恢复处理"""
        self.paused = False
        if self.current_job:
            self.current_job.status = BatchStatus.RUNNING
    
    def cancel(self):
        """取消处理"""
        self.running = False
        if self.current_job:
            self.current_job.status = BatchStatus.CANCELLED
            for task in self.current_job.tasks:
                if task.status == BatchStatus.PENDING:
                    task.status = BatchStatus.CANCELLED
    
    def _process_loop(self):
        """处理循环"""
        while self.running and any(
            t.status == BatchStatus.PENDING 
            for t in self.current_job.tasks
        ):
            if self.paused:
                time.sleep(0.5)
                continue
            
            task = self.queue.get_next()
            if not task:
                time.sleep(0.5)
                continue
            
            try:
                # 保存断点
                self.checkpoint_manager.save_checkpoint(
                    self.current_job.id,
                    task.id,
                    {'progress': 0, 'status': 'running'}
                )
                
                # 模拟任务执行
                result = self._execute_task(task)
                
                # 完成
                self.queue.complete(task.id, result)
                self.current_job.completed_tasks += 1
                
                # 更新进度
                self._update_progress(task)
                
            except Exception as e:
                self.queue.fail(task.id, str(e))
                self.current_job.failed_tasks += 1
                self._update_progress(task)
        
        # 处理完成
        if self.running:
            self.current_job.status = BatchStatus.COMPLETED
            self.current_job.completed_at = datetime.now().isoformat()
        
        self.running = False
    
    def _execute_task(self, task: BatchTask) -> Dict:
        """执行单个任务"""
        # 模拟执行
        for i in range(10):
            if not self.running or self.paused:
                break
            
            time.sleep(0.1)  # 模拟处理
            task.progress = (i + 1) / 10
            
            # 保存进度断点
            self.checkpoint_manager.save_checkpoint(
                self.current_job.id,
                task.id,
                {'progress': task.progress, 'status': 'running'}
            )
        
        return {
            'task_id': task.id,
            'status': 'success',
            'output': {}
        }
    
    def _update_progress(self, task: BatchTask):
        """更新作业进度"""
        if not self.current_job:
            return
        
        total = self.current_job.total_tasks
        completed = self.current_job.completed_tasks
        failed = self.current_job.failed_tasks
        
        self.current_job.progress = (completed + failed) / total if total > 0 else 0
        
        if self.progress_callback:
            self.progress_callback({
                'job_id': self.current_job.id,
                'job_name': self.current_job.name,
                'progress': self.current_job.progress,
                'completed_tasks': completed,
                'failed_tasks': failed,
                'total_tasks': total,
                'status': self.current_job.status.value
            })
    
    def get_job_status(self) -> Optional[Dict]:
        """获取作业状态"""
        if not self.current_job:
            return None
        
        return {
            'id': self.current_job.id,
            'name': self.current_job.name,
            'status': self.current_job.status.value,
            'progress': self.current_job.progress,
            'completed_tasks': self.current_job.completed_tasks,
            'failed_tasks': self.current_job.failed_tasks,
            'total_tasks': self.current_job.total_tasks,
            'created_at': self.current_job.created_at,
            'started_at': self.current_job.started_at,
            'completed_at': self.current_job.completed_at
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        for task in self.current_job.tasks if self.current_job else []:
            if task.id == task_id:
                return {
                    'id': task.id,
                    'name': task.name,
                    'type': task.task_type,
                    'status': task.status.value,
                    'progress': task.progress,
                    'retry_count': task.retry_count,
                    'error': task.error
                }
        return None
    
    def retry_failed(self) -> int:
        """重试失败的任务"""
        if not self.current_job:
            return 0
        
        count = 0
        for task in self.current_job.tasks:
            if task.status == BatchStatus.FAILED:
                task.status = BatchStatus.PENDING
                task.retry_count = 0
                self.queue.add(task)
                count += 1
        
        return count
    
    def export_results(self) -> Dict:
        """导出结果"""
        if not self.current_job:
            return {}
        
        return {
            'job': self.get_job_status(),
            'tasks': [
                {
                    'id': t.id,
                    'name': t.name,
                    'status': t.status.value,
                    'result': t.result
                }
                for t in self.current_job.tasks
            ],
            'checkpoints': self.checkpoint_manager.get_job_checkpoints(
                self.current_job.id
            )
        }

class EpisodeBatchGenerator:
    """多集批量生成器"""
    
    def __init__(self, processor: BatchProcessor):
        self.processor = processor
    
    def create_episode_batch(
        self,
        project_id: str,
        story_outline: str,
        num_episodes: int,
        episode_template: Dict
    ) -> str:
        """创建多集批量生成任务"""
        job_id = self.processor.create_job(
            name=f"批量生成{num_episodes}集",
            description=f"故事：{story_outline[:50]}...",
            settings={
                'project_id': project_id,
                'story_outline': story_outline,
                'num_episodes': num_episodes
            }
        )
        
        # 创建每集任务
        tasks = []
        for i in range(num_episodes):
            task = {
                'name': f"生成第{i+1}集",
                'type': 'generate_episode',
                'params': {
                    'episode_number': i + 1,
                    'outline': story_outline,
                    'template': episode_template,
                    'previous_episode_summary': "" if i == 0 else f"第{i}集内容摘要"
                },
                'priority': TaskPriority.HIGH if i == 0 else TaskPriority.NORMAL
            }
            tasks.append(task)
        
        self.processor.add_tasks(job_id, tasks)
        return job_id
    
    def create_character_batch(
        self,
        project_id: str,
        character_list: List[Dict]
    ) -> str:
        """创建角色批量生成任务"""
        job_id = self.processor.create_job(
            name=f"批量生成{len(character_list)}个角色",
            description="角色设定批量生成"
        )
        
        tasks = [
            {
                'name': f"生成角色：{char.get('name', '未知')}",
                'type': 'generate_character',
                'params': {
                    'character_data': char
                }
            }
            for char in character_list
        ]
        
        self.processor.add_tasks(job_id, tasks)
        return job_id
