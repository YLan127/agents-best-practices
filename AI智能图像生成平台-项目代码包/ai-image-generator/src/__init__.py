"""
AI图像生成平台 - 核心模块
"""
from .config import get_config, Config
from .image_generator import ImageGenerator, get_image_generator
from .utils import HistoryManager, get_project_root, ensure_dir

__all__ = [
    'get_config',
    'Config',
    'ImageGenerator',
    'get_image_generator',
    'HistoryManager',
    'get_project_root',
    'ensure_dir'
]

__version__ = '1.0.0'
