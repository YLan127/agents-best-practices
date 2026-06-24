"""
图像生成核心模块
封装Stable Diffusion图像生成逻辑
"""
import os
import random
import torch
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image

from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionXLPipeline,
    DPMSolverMultistepScheduler,
    EulerDiscreteScheduler
)

from .config import get_config


class ImageGenerator:
    """AI图像生成器"""
    
    def __init__(self, model_id: Optional[str] = None, device: Optional[str] = None):
        """
        初始化图像生成器
        
        Args:
            model_id: 模型ID，为None时使用配置中的默认模型
            device: 设备类型（cpu/cuda/auto），为None时使用配置
        """
        self.config = get_config()
        self.model_id = model_id or self.config.get('MODEL.default_model')
        self.device = self._resolve_device(device or self.config.get('MODEL.device', 'auto'))
        self.pipeline = None
        self._output_dir = Path(self.config.get('OUTPUT.output_dir', './output'))
        self._output_dir.mkdir(parents=True, exist_ok=True)
    
    def _resolve_device(self, device: str) -> str:
        """
        解析设备类型
        
        Args:
            device: 设备配置
        
        Returns:
            实际设备类型
        """
        if device == 'auto':
            return 'cuda' if torch.cuda.is_available() else 'cpu'
        return device
    
    def load_model(self):
        """加载模型到内存"""
        if self.pipeline is not None:
            return
        
        print(f"正在加载模型: {self.model_id}")
        print(f"使用设备: {self.device}")
        
        # 根据模型类型选择pipeline
        if 'xl' in self.model_id.lower():
            # SDXL模型
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == 'cuda' else None
            )
        else:
            # 标准SD模型
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                use_safetensors=True
            )
        
        # 设置调度器
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipeline.scheduler.config
        )
        
        # 移动到设备
        self.pipeline = self.pipeline.to(self.device)
        
        # 启用内存优化（如果是CUDA）
        if self.device == 'cuda':
            self.pipeline.enable_attention_slicing()
            self.pipeline.enable_vae_slicing()
        
        print("模型加载完成")
    
    def unload_model(self):
        """卸载模型释放内存"""
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
            if self.device == 'cuda':
                torch.cuda.empty_cache()
            print("模型已卸载")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        num_inference_steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        seed: Optional[int] = None,
        num_images: Optional[int] = None
    ) -> Tuple[List[Image.Image], dict]:
        """
        生成图像
        
        Args:
            prompt: 正向提示词
            negative_prompt: 负面提示词
            width: 图像宽度
            height: 图像高度
            num_inference_steps: 推理步数
            guidance_scale: CFG比例
            seed: 随机种子
            num_images: 生成数量
        
        Returns:
            (生成的图像列表, 生成参数信息)
        """
        # 确保模型已加载
        self.load_model()
        
        # 使用默认参数
        gen_config = self.config.get_generation_config()
        width = width or gen_config.get('width', 512)
        height = height or gen_config.get('height', 512)
        num_inference_steps = num_inference_steps or gen_config.get('num_inference_steps', 30)
        guidance_scale = guidance_scale or gen_config.get('guidance_scale', 7.5)
        seed = seed if seed is not None else gen_config.get('seed', -1)
        num_images = num_images or gen_config.get('num_images', 1)
        negative_prompt = negative_prompt or gen_config.get('negative_prompt', '')
        
        # 处理随机种子
        if seed == -1:
            seed = random.randint(0, 2**32 - 1)
        
        # 设置生成器
        generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # 生成图像
        print(f"正在生成图像...")
        print(f"提示词: {prompt}")
        print(f"种子: {seed}")
        
        result = self.pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            num_images_per_prompt=num_images,
            generator=generator
        )
        
        images = result.images
        
        # 生成参数信息
        info = {
            'model': self.model_id,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'width': width,
            'height': height,
            'num_inference_steps': num_inference_steps,
            'guidance_scale': guidance_scale,
            'seed': seed,
            'num_images': num_images,
            'device': self.device
        }
        
        return images, info
    
    def save_images(self, images: List[Image.Image], info: dict) -> List[str]:
        """
        保存生成的图像
        
        Args:
            images: 图像列表
            info: 生成信息
        
        Returns:
            保存的文件路径列表
        """
        saved_paths = []
        img_format = self.config.get('OUTPUT.image_format', 'png')
        img_quality = self.config.get('OUTPUT.image_quality', 95)
        
        for i, img in enumerate(images):
            # 生成文件名
            seed = info.get('seed', 0)
            filename = f"generated_{seed}_{i+1}.{img_format}"
            filepath = self._output_dir / filename
            
            # 保存图像
            save_kwargs = {}
            if img_format.lower() in ['jpg', 'jpeg']:
                save_kwargs['quality'] = img_quality
                img = img.convert('RGB')
            
            img.save(filepath, **save_kwargs)
            saved_paths.append(str(filepath))
            print(f"图像已保存: {filepath}")
        
        return saved_paths


# 生成器单例
_generator_instance = None


def get_image_generator(model_id: Optional[str] = None) -> ImageGenerator:
    """
    获取图像生成器实例（单例模式）
    
    Args:
        model_id: 模型ID
    
    Returns:
        ImageGenerator实例
    """
    global _generator_instance
    if _generator_instance is None or (model_id and _generator_instance.model_id != model_id):
        _generator_instance = ImageGenerator(model_id=model_id)
    return _generator_instance
