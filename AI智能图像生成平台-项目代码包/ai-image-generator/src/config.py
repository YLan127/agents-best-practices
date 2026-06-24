"""
配置管理模块
负责加载和管理应用的所有配置项
"""
import os
import yaml
from dotenv import load_dotenv
from pathlib import Path


class Config:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self._config = {}
        self._load_config()
        self._load_env_overrides()
    
    def _load_config(self):
        """加载YAML配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        else:
            # 默认配置
            self._config = self._get_default_config()
    
    def _load_env_overrides(self):
        """加载环境变量覆盖配置"""
        load_dotenv()
        
        # 用户信息覆盖
        if os.getenv('STUDENT_ID'):
            self._config.setdefault('USER_INFO', {})['student_id'] = os.getenv('STUDENT_ID')
        if os.getenv('STUDENT_NAME'):
            self._config.setdefault('USER_INFO', {})['student_name'] = os.getenv('STUDENT_NAME')
        
        # 模型配置覆盖
        if os.getenv('MODEL_ID'):
            self._config.setdefault('MODEL', {})['default_model'] = os.getenv('MODEL_ID')
        if os.getenv('DEVICE'):
            self._config.setdefault('MODEL', {})['device'] = os.getenv('DEVICE')
    
    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            'USER_INFO': {
                'student_id': '423830227',
                'student_name': '梁煜岚',
                'show_info': True
            },
            'MODEL': {
                'default_model': 'stabilityai/stable-diffusion-2-1-base',
                'available_models': [
                    'stabilityai/stable-diffusion-2-1-base',
                    'stabilityai/stable-diffusion-xl-base-1.0',
                    'runwayml/stable-diffusion-v1-5'
                ],
                'device': 'auto',
                'safety_checker': True
            },
            'GENERATION': {
                'width': 512,
                'height': 512,
                'num_inference_steps': 30,
                'guidance_scale': 7.5,
                'seed': -1,
                'num_images': 1,
                'negative_prompt': 'blurry, bad quality, distorted, ugly, deformed'
            },
            'APP': {
                'title': 'AI 智能图像生成平台',
                'subtitle': '基于 Stable Diffusion 的创意图像生成工具',
                'theme_color': '#1E88E5',
                'max_dimension': 1024,
                'enable_history': True,
                'max_history': 20
            },
            'OUTPUT': {
                'output_dir': './output',
                'image_format': 'png',
                'image_quality': 95
            }
        }
    
    def get(self, key: str, default=None):
        """
        获取配置项
        
        Args:
            key: 配置键名，支持点分隔（如 'USER_INFO.student_id'）
            default: 默认值
        
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_user_info(self) -> dict:
        """获取用户信息"""
        return self.get('USER_INFO', {})
    
    def get_model_config(self) -> dict:
        """获取模型配置"""
        return self.get('MODEL', {})
    
    def get_generation_config(self) -> dict:
        """获取生成配置"""
        return self.get('GENERATION', {})
    
    def get_app_config(self) -> dict:
        """获取应用配置"""
        return self.get('APP', {})
    
    def get_output_config(self) -> dict:
        """获取输出配置"""
        return self.get('OUTPUT', {})


# 全局配置实例
_config_instance = None


def get_config(config_path: str = "config.yaml") -> Config:
    """
    获取全局配置实例（单例模式）
    
    Args:
        config_path: 配置文件路径
    
    Returns:
        Config实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
