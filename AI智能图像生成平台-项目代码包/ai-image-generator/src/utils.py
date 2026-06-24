"""
工具函数模块
提供通用的工具函数
"""
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image


def get_project_root() -> Path:
    """
    获取项目根目录
    
    Returns:
        项目根目录路径
    """
    return Path(__file__).parent.parent


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，不存在则创建
    
    Args:
        path: 目录路径
    
    Returns:
        目录Path对象
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def save_json(data: dict, filepath: str):
    """
    保存JSON文件
    
    Args:
        data: 数据字典
        filepath: 文件路径
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath: str) -> Optional[dict]:
    """
    加载JSON文件
    
    Args:
        filepath: 文件路径
    
    Returns:
        数据字典，文件不存在时返回None
    """
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_image_info(image_path: str) -> dict:
    """
    获取图像信息
    
    Args:
        image_path: 图像路径
    
    Returns:
        图像信息字典
    """
    img = Image.open(image_path)
    return {
        'path': image_path,
        'size': img.size,
        'mode': img.mode,
        'format': img.format
    }


def generate_timestamp() -> str:
    """
    生成时间戳字符串
    
    Returns:
        时间戳字符串
    """
    return time.strftime('%Y%m%d_%H%M%S')


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 字节数
    
    Returns:
        格式化后的大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, history_file: str = "./output/history.json", max_items: int = 20):
        """
        初始化历史记录管理器
        
        Args:
            history_file: 历史记录文件路径
            max_items: 最大记录数
        """
        self.history_file = Path(history_file)
        self.max_items = max_items
        self._ensure_history_file()
    
    def _ensure_history_file(self):
        """确保历史记录文件存在"""
        if not self.history_file.parent.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_file.exists():
            save_json([], str(self.history_file))
    
    def add_record(self, record: dict):
        """
        添加历史记录
        
        Args:
            record: 记录字典
        """
        history = self.get_history()
        
        # 添加时间戳
        record['timestamp'] = generate_timestamp()
        record['time_str'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # 插入到开头
        history.insert(0, record)
        
        # 限制数量
        if len(history) > self.max_items:
            history = history[:self.max_items]
        
        save_json(history, str(self.history_file))
    
    def get_history(self) -> List[Dict]:
        """
        获取历史记录列表
        
        Returns:
            历史记录列表
        """
        data = load_json(str(self.history_file))
        return data if data else []
    
    def clear_history(self):
        """清空历史记录"""
        save_json([], str(self.history_file))
