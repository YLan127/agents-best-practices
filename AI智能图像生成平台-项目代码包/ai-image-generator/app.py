"""
AI 智能图像生成平台 - 主应用
基于 Streamlit + Stable Diffusion 的 Web 应用
作者：梁煜岚
学号：423830227
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import streamlit as st
from PIL import Image
import io

from src.config import get_config
from src.utils import HistoryManager


def init_session_state():
    """初始化会话状态"""
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'generation_info' not in st.session_state:
        st.session_state.generation_info = None
    if 'is_generating' not in st.session_state:
        st.session_state.is_generating = False


def apply_custom_style(config):
    """应用自定义样式"""
    theme_color = config.get('APP.theme_color', '#1E88E5')
    
    st.markdown(f"""
    <style>
    .main-header {{
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, {theme_color} 0%, #1565C0 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }}
    .main-header h1 {{
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }}
    .main-header p {{
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }}
    .user-info-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }}
    .user-info-card .student-id {{
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 2px;
    }}
    .user-info-card .student-name {{
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 5px;
    }}
    .user-info-card .label {{
        font-size: 0.85rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .section-title {{
        font-size: 1.3rem;
        font-weight: bold;
        color: {theme_color};
        border-left: 4px solid {theme_color};
        padding-left: 12px;
        margin: 20px 0 15px 0;
    }}
    .info-box {{
        background-color: #f0f7ff;
        border-left: 4px solid {theme_color};
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }}
    .success-box {{
        background-color: #f0fff4;
        border-left: 4px solid #10b981;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {theme_color} 0%, #1565C0 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4);
    }}
    .image-container {{
        text-align: center;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 10px 0;
    }}
    .param-card {{
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }}
    .param-card h4 {{
        margin: 0 0 10px 0;
        color: {theme_color};
    }}
    .footer {{
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #eee;
        margin-top: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_header(config):
    """渲染页面头部"""
    title = config.get('APP.title', 'AI 智能图像生成平台')
    subtitle = config.get('APP.subtitle', '基于 Stable Diffusion 的创意图像生成工具')
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🎨 {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_user_info(config):
    """渲染用户信息卡片"""
    user_info = config.get_user_info()
    
    if not user_info.get('show_info', True):
        return
    
    student_id = user_info.get('student_id', '423830227')
    student_name = user_info.get('student_name', '梁煜岚')
    
    st.markdown(f"""
    <div class="user-info-card">
        <div class="label">学号 / Student ID</div>
        <div class="student-id">{student_id}</div>
        <div class="label" style="margin-top: 10px;">姓名 / Name</div>
        <div class="student-name">{student_name}</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(config):
    """渲染侧边栏参数配置"""
    with st.sidebar:
        st.markdown("## ⚙️ 参数配置")
        
        # 模型选择
        st.markdown("### 🤖 模型设置")
        available_models = config.get('MODEL.available_models', [
            'stabilityai/stable-diffusion-2-1-base'
        ])
        default_model = config.get('MODEL.default_model', available_models[0])
        
        selected_model = st.selectbox(
            "选择模型",
            options=available_models,
            index=available_models.index(default_model) if default_model in available_models else 0,
            help="选择要使用的Stable Diffusion模型"
        )
        
        device = st.selectbox(
            "运行设备",
            options=['auto', 'cpu', 'cuda'],
            index=0,
            help="选择运行设备，auto会自动检测"
        )
        
        st.divider()
        
        # 图像参数
        st.markdown("### 📐 图像参数")
        gen_config = config.get_generation_config()
        
        width = st.slider(
            "图像宽度",
            min_value=256,
            max_value=config.get('APP.max_dimension', 1024),
            value=gen_config.get('width', 512),
            step=64,
            help="生成图像的宽度（像素）"
        )
        
        height = st.slider(
            "图像高度",
            min_value=256,
            max_value=config.get('APP.max_dimension', 1024),
            value=gen_config.get('height', 512),
            step=64,
            help="生成图像的高度（像素）"
        )
        
        num_images = st.slider(
            "生成数量",
            min_value=1,
            max_value=4,
            value=gen_config.get('num_images', 1),
            help="每次生成的图像数量"
        )
        
        st.divider()
        
        # 生成参数
        st.markdown("### ⚡ 生成参数")
        
        num_inference_steps = st.slider(
            "推理步数",
            min_value=10,
            max_value=100,
            value=gen_config.get('num_inference_steps', 30),
            step=5,
            help="推理步数越多，图像质量越好，但生成速度越慢"
        )
        
        guidance_scale = st.slider(
            "CFG Scale",
            min_value=1.0,
            max_value=20.0,
            value=float(gen_config.get('guidance_scale', 7.5)),
            step=0.5,
            help="控制图像与提示词的贴合程度，值越高越贴合但可能降低质量"
        )
        
        seed = st.number_input(
            "随机种子",
            min_value=-1,
            max_value=2**32 - 1,
            value=gen_config.get('seed', -1),
            help="设置随机种子，-1表示随机。相同种子+相同参数可复现相同图像"
        )
        
        st.divider()
        
        # 负面提示词
        st.markdown("### 🚫 负面提示词")
        negative_prompt = st.text_area(
            "负面提示词",
            value=gen_config.get('negative_prompt', ''),
            height=100,
            help="描述你不希望出现在图像中的内容"
        )
        
        st.divider()
        
        # 高级设置
        with st.expander("🔧 高级设置"):
            safety_checker = st.checkbox(
                "启用安全检查",
                value=config.get('MODEL.safety_checker', True),
                help="启用NSFW内容检测"
            )
            
            enable_history = st.checkbox(
                "启用历史记录",
                value=config.get('APP.enable_history', True),
                help="保存生成历史记录"
            )
        
        # 返回参数
        return {
            'model': selected_model,
            'device': device,
            'width': width,
            'height': height,
            'num_images': num_images,
            'num_inference_steps': num_inference_steps,
            'guidance_scale': guidance_scale,
            'seed': seed,
            'negative_prompt': negative_prompt,
            'safety_checker': safety_checker,
            'enable_history': enable_history
        }


def render_main_content(params, config):
    """渲染主内容区域"""
    
    # 提示词输入
    st.markdown('<div class="section-title">💡 输入提示词</div>', unsafe_allow_html=True)
    
    prompt = st.text_area(
        "描述你想要生成的图像",
        placeholder="例如：一只可爱的猫咪坐在樱花树下，阳光透过花瓣洒落，动漫风格，高清画质",
        height=120,
        label_visibility="collapsed"
    )
    
    # 快速提示词模板
    with st.expander("✨ 快速提示词模板"):
        col1, col2, col3 = st.columns(3)
        
        templates = {
            "动漫角色": "anime style, beautiful character, detailed eyes, vibrant colors, masterpiece",
            "风景照片": "photorealistic landscape, mountains, sunset, golden hour, 8k, highly detailed",
            "赛博朋克": "cyberpunk city, neon lights, rain, futuristic, cinematic lighting, 4k",
            "油画风格": "oil painting style, classic art, textured brushstrokes, warm colors, museum quality",
            "科幻场景": "sci-fi scene, spaceship, stars, nebula, epic, cinematic, ultra detailed",
            "梦幻森林": "magical forest, fairy lights, mystical atmosphere, ethereal, dreamy"
        }
        
        for i, (name, template) in enumerate(templates.items()):
            if i % 3 == 0:
                col = col1
            elif i % 3 == 1:
                col = col2
            else:
                col = col3
            
            if col.button(name, key=f"template_{name}"):
                prompt = template
                st.rerun()
    
    # 生成按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button(
            "🎨 生成图像",
            use_container_width=True,
            disabled=not prompt.strip()
        )
    
    # 生成图像
    if generate_button and prompt.strip():
        generate_images(prompt, params, config)
    
    # 显示生成结果
    if st.session_state.generated_images:
        st.markdown('<div class="section-title">🖼️ 生成结果</div>', unsafe_allow_html=True)
        display_generated_images()
    
    # 显示历史记录
    if params.get('enable_history', True):
        render_history(config)


def generate_images(prompt, params, config):
    """生成图像"""
    st.session_state.is_generating = True
    
    try:
        # 显示进度
        with st.spinner('🎨 正在生成图像，请稍候...'):
            # 这里使用模拟生成，实际部署时会调用真实的Diffusers
            # 为了演示目的，我们创建一个占位图像
            from PIL import Image, ImageDraw, ImageFont
            
            images = []
            for i in range(params['num_images']):
                # 创建演示图像
                img = Image.new('RGB', (params['width'], params['height']), color='#f0f7ff')
                draw = ImageDraw.Draw(img)
                
                # 绘制装饰边框
                draw.rectangle([10, 10, params['width']-10, params['height']-10], 
                             outline='#1E88E5', width=3)
                
                # 添加文字
                try:
                    # 尝试加载字体
                    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
                    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
                except:
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                
                # 标题
                title = "AI 图像生成演示"
                draw.text((params['width']//2, 60), title, fill='#1E88E5', 
                         font=font_large, anchor='mm')
                
                # 提示词预览
                prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
                draw.text((params['width']//2, 110), f"提示词: {prompt_preview}", 
                         fill='#333', font=font_medium, anchor='mm')
                
                # 参数信息
                info_lines = [
                    f"模型: {params['model'].split('/')[-1]}",
                    f"尺寸: {params['width']}x{params['height']}",
                    f"步数: {params['num_inference_steps']}",
                    f"CFG: {params['guidance_scale']}",
                    f"种子: {params['seed'] if params['seed'] != -1 else '随机'}"
                ]
                
                y_start = 160
                for i, line in enumerate(info_lines):
                    draw.text((params['width']//2, y_start + i * 30), line, 
                             fill='#666', font=font_small, anchor='mm')
                
                # 底部用户信息
                user_info = config.get_user_info()
                footer_text = f"学号: {user_info.get('student_id', '')} | 姓名: {user_info.get('student_name', '')}"
                draw.text((params['width']//2, params['height'] - 40), footer_text, 
                         fill='#999', font=font_small, anchor='mm')
                
                images.append(img)
            
            # 保存到会话状态
            st.session_state.generated_images = images
            st.session_state.generation_info = {
                'prompt': prompt,
                'model': params['model'],
                'width': params['width'],
                'height': params['height'],
                'num_inference_steps': params['num_inference_steps'],
                'guidance_scale': params['guidance_scale'],
                'seed': params['seed'],
                'negative_prompt': params['negative_prompt'],
                'device': params['device']
            }
            
            # 添加到历史记录
            if params.get('enable_history', True):
                history_manager = HistoryManager(
                    max_items=config.get('APP.max_history', 20)
                )
                history_manager.add_record({
                    'prompt': prompt,
                    'params': st.session_state.generation_info
                })
        
        st.success('✅ 图像生成完成！')
        
    except Exception as e:
        st.error(f'❌ 生成失败: {str(e)}')
    finally:
        st.session_state.is_generating = False


def display_generated_images():
    """显示生成的图像"""
    images = st.session_state.generated_images
    info = st.session_state.generation_info
    
    # 显示图像网格
    num_images = len(images)
    if num_images == 1:
        st.image(images[0], caption=f"生成图像 1", use_container_width=True)
    elif num_images == 2:
        cols = st.columns(2)
        for i, img in enumerate(images):
            cols[i].image(img, caption=f"生成图像 {i+1}", use_container_width=True)
    else:
        cols = st.columns(2)
        for i, img in enumerate(images):
            cols[i % 2].image(img, caption=f"生成图像 {i+1}", use_container_width=True)
    
    # 显示生成参数
    if info:
        with st.expander("📋 生成参数详情"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**基础信息**")
                st.write(f"- 模型: `{info['model']}`")
                st.write(f"- 尺寸: {info['width']} x {info['height']}")
                st.write(f"- 推理步数: {info['num_inference_steps']}")
                st.write(f"- CFG Scale: {info['guidance_scale']}")
            
            with col2:
                st.markdown("**其他参数**")
                st.write(f"- 种子: {info['seed'] if info['seed'] != -1 else '随机'}")
                st.write(f"- 设备: {info['device']}")
                st.write(f"- 负面提示词: {info['negative_prompt'][:50]}...")
            
            st.markdown("**提示词:**")
            st.info(info['prompt'])
    
    # 下载按钮
    st.markdown("### 📥 下载图像")
    for i, img in enumerate(images):
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        st.download_button(
            label=f"下载图像 {i+1}",
            data=buf,
            file_name=f"generated_image_{i+1}.png",
            mime="image/png",
            key=f"download_{i}"
        )


def render_history(config):
    """渲染历史记录"""
    st.markdown('<div class="section-title">📜 生成历史</div>', unsafe_allow_html=True)
    
    history_manager = HistoryManager(
        max_items=config.get('APP.max_history', 20)
    )
    history = history_manager.get_history()
    
    if not history:
        st.info("暂无历史记录，开始生成你的第一张图像吧！")
        return
    
    # 显示最近的历史记录
    for i, record in enumerate(history[:5]):
        with st.expander(f"🕐 {record.get('time_str', '')} - {record.get('prompt', '')[:50]}..."):
            st.write(f"**提示词:** {record.get('prompt', '')}")
            params = record.get('params', {})
            if params:
                st.write(f"**模型:** {params.get('model', '')}")
                st.write(f"**尺寸:** {params.get('width', '')} x {params.get('height', '')}")
                st.write(f"**步数:** {params.get('num_inference_steps', '')}")
    
    if len(history) > 5:
        st.caption(f"共 {len(history)} 条历史记录，仅显示最近 5 条")


def render_footer(config):
    """渲染页脚"""
    user_info = config.get_user_info()
    
    st.markdown(f"""
    <div class="footer">
        <p>🎨 AI 智能图像生成平台 v1.0.0</p>
        <p>开发者: <strong>{user_info.get('student_name', '梁煜岚')}</strong> | 学号: <strong>{user_info.get('student_id', '423830227')}</strong></p>
        <p style="font-size: 0.8rem; color: #999;">基于 Streamlit + Hugging Face Diffusers 构建</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """主函数"""
    # 加载配置
    config = get_config()
    
    # 初始化会话状态
    init_session_state()
    
    # 页面配置
    st.set_page_config(
        page_title=config.get('APP.title', 'AI 智能图像生成平台'),
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 应用自定义样式
    apply_custom_style(config)
    
    # 渲染头部
    render_header(config)
    
    # 创建两栏布局
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # 左侧显示用户信息
        render_user_info(config)
        
        # 快速信息
        st.markdown('<div class="section-title">ℹ️ 项目信息</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <strong>项目名称:</strong> AI 智能图像生成平台<br>
        <strong>技术栈:</strong> Streamlit + Diffusers<br>
        <strong>版本:</strong> v1.0.0
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 渲染侧边栏参数
        params = render_sidebar(config)
        
        # 渲染主内容
        render_main_content(params, config)
    
    # 渲染页脚
    render_footer(config)


if __name__ == "__main__":
    main()
