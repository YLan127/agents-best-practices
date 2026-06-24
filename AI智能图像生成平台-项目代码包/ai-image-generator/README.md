# 🎨 AI 智能图像生成平台

> 基于 Streamlit + Hugging Face Diffusers 的 AI 图像生成 Web 应用

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 项目简介

本项目是一个基于 Stable Diffusion 的 AI 智能图像生成平台，提供友好的 Web 界面，让用户可以通过文字描述快速生成高质量的 AI 图像。项目采用模块化设计，参数全部可配置，易于迁移和部署。

**开发者信息：**
- 👤 姓名：**梁煜岚**
- 🎓 学号：**423830227**

## ✨ 功能特性

- 🎨 **文本生成图像**：通过文字描述生成高质量 AI 图像
- ⚙️ **参数可配置**：支持调整模型、尺寸、步数、CFG 等多种参数
- 📐 **多尺寸支持**：支持 256x256 到 1024x1024 多种图像尺寸
- 🎯 **多模型支持**：兼容 Stable Diffusion v1.5、v2.1、SDXL 等多种模型
- 📜 **历史记录**：自动保存生成历史，方便回顾和复用
- 🚫 **负面提示词**：支持负面提示词，精确控制图像内容
- 🔄 **可复现生成**：通过种子值实现完全可复现的图像生成
- 🎨 **精美界面**：现代化 UI 设计，响应式布局
- 📥 **一键下载**：生成的图像可直接下载保存

## 🛠️ 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 前端框架 | **Streamlit** | 快速构建数据应用的 Python 框架 |
| AI 模型 | **Hugging Face Diffusers** | 最先进的扩散模型库 |
| 深度学习 | **PyTorch** | 深度学习框架 |
| 图像处理 | **Pillow** | Python 图像处理库 |
| 配置管理 | **PyYAML + python-dotenv** | 灵活的配置管理方案 |
| 模型格式 | **Safetensors** | 安全的模型存储格式 |

## 📁 项目结构

```
ai-image-generator/
├── app.py                 # 主应用入口（Streamlit Web 界面）
├── config.yaml            # 主配置文件（YAML格式）
├── .env.example           # 环境变量示例
├── requirements.txt       # Python 依赖包列表
├── README.md              # 项目说明文档
├── LICENSE                # 许可证文件
├── src/                   # 核心源码目录
│   ├── __init__.py        # 包初始化文件
│   ├── config.py          # 配置管理模块
│   ├── image_generator.py # 图像生成核心逻辑
│   └── utils.py           # 工具函数模块
├── assets/                # 静态资源目录
└── output/                # 输出目录（运行时自动创建）
    └── history.json       # 生成历史记录
```

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 推荐使用 GPU（CUDA 支持）以获得更好的性能
- 至少 8GB 内存（GPU 模式建议 12GB+ 显存）

### 1. 克隆项目

```bash
git clone https://github.com/YLan127/agents-best-practices.git
cd agents-best-practices
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Hugging Face API Token（可选，用于访问受限模型）
HF_TOKEN=your_huggingface_token_here

# 用户信息（可覆盖 config.yaml 中的配置）
STUDENT_ID=423830227
STUDENT_NAME=梁煜岚

# 模型配置
MODEL_ID=stabilityai/stable-diffusion-2-1-base
DEVICE=auto

# 应用端口
STREAMLIT_PORT=8501
```

### 4. 运行应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 启动。

### 5. 开始使用

1. 在浏览器中打开应用
2. 在左侧边栏调整生成参数（可选）
3. 在主区域输入图像描述提示词
4. 点击「生成图像」按钮
5. 等待生成完成，查看并下载结果

## ⚙️ 配置说明

### config.yaml 配置文件

项目使用 `config.yaml` 作为主要配置文件，包含以下配置项：

#### 用户信息配置 (USER_INFO)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| student_id | string | "423830227" | 学号 |
| student_name | string | "梁煜岚" | 姓名 |
| show_info | boolean | true | 是否在前端显示学号姓名 |

#### 模型配置 (MODEL)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| default_model | string | "stabilityai/stable-diffusion-2-1-base" | 默认使用的模型 |
| available_models | list | [...] | 可用模型列表 |
| device | string | "auto" | 运行设备（auto/cpu/cuda） |
| safety_checker | boolean | true | 是否启用安全检查 |

#### 图像生成参数 (GENERATION)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| width | int | 512 | 默认图像宽度（像素） |
| height | int | 512 | 默认图像高度（像素） |
| num_inference_steps | int | 30 | 默认推理步数 |
| guidance_scale | float | 7.5 | 默认 CFG Scale |
| seed | int | -1 | 默认随机种子（-1 表示随机） |
| num_images | int | 1 | 每次生成图片数量 |
| negative_prompt | string | "blurry, bad quality..." | 默认负面提示词 |

#### 应用配置 (APP)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | string | "AI 智能图像生成平台" | 页面标题 |
| subtitle | string | "基于 Stable Diffusion..." | 页面副标题 |
| theme_color | string | "#1E88E5" | 主题颜色 |
| max_dimension | int | 1024 | 最大图像尺寸限制 |
| enable_history | boolean | true | 是否启用历史记录 |
| max_history | int | 20 | 历史记录最大数量 |

#### 输出配置 (OUTPUT)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| output_dir | string | "./output" | 输出目录 |
| image_format | string | "png" | 图像格式（png/jpg） |
| image_quality | int | 95 | JPG 图像质量（0-100） |

### 环境变量优先级

环境变量会覆盖 `config.yaml` 中的对应配置，优先级如下：

1. 环境变量（`.env` 文件或系统环境变量）
2. `config.yaml` 配置文件
3. 代码中的默认值

## 🎯 使用指南

### 提示词技巧

#### 正向提示词结构

一个好的提示词通常包含以下元素：

```
[主体描述] + [风格/艺术形式] + [细节描述] + [质量描述]
```

示例：
```
一只可爱的猫咪坐在樱花树下，阳光透过花瓣洒落，动漫风格，高清画质，8k分辨率，杰作
```

#### 负面提示词使用

负面提示词用于描述你不希望出现在图像中的内容：

```
模糊, 低质量, 变形, 丑陋, 畸形, 水印, 文字
```

### 参数调优指南

#### 推理步数 (num_inference_steps)

- **10-20 步**：快速生成，适合预览，质量较低
- **20-40 步**：平衡速度和质量，推荐日常使用
- **40-100 步**：高质量生成，速度较慢，细节更丰富

#### CFG Scale (guidance_scale)

- **1-5**：创意性强，可能偏离提示词
- **5-10**：平衡创意和贴合度，推荐默认值 7.5
- **10-20**：高度贴合提示词，可能导致图像过饱和或不自然

#### 图像尺寸

- **256x256**：快速预览，细节较少
- **512x512**：标准尺寸，平衡质量和速度
- **768x768 / 1024x1024**：高分辨率，细节丰富，生成较慢

### 模型选择

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| Stable Diffusion v1.5 | 成熟稳定，资源占用低 | 日常使用，快速生成 |
| Stable Diffusion v2.1 | 质量更高，人像更好 | 高质量生成 |
| Stable Diffusion XL | 最新技术，细节最丰富 | 专业级高质量生成 |

## 🔧 开发指南

### 添加新模型

在 `config.yaml` 的 `MODEL.available_models` 列表中添加新的模型 ID：

```yaml
MODEL:
  available_models:
    - "stabilityai/stable-diffusion-2-1-base"
    - "your-new-model-id"
```

### 自定义主题

修改 `config.yaml` 中的 `APP.theme_color` 来更改主题颜色：

```yaml
APP:
  theme_color: "#FF5722"  # 橙色主题
```

### 扩展功能

项目采用模块化设计，可以轻松扩展新功能：

1. 在 `src/` 目录下创建新的模块文件
2. 在 `app.py` 中导入并使用新模块
3. 在 `config.yaml` 中添加相应的配置项

## 🐳 Docker 部署（可选）

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

构建并运行：

```bash
docker build -t ai-image-generator .
docker run -p 8501:8501 ai-image-generator
```

## 📊 性能优化建议

1. **使用 GPU**：CUDA GPU 可以大幅提升生成速度
2. **启用半精度**：FP16 模式可以减少显存占用并提升速度
3. **注意力切片**：已默认启用，降低显存峰值
4. **VAE 切片**：已默认启用，处理大图像时更高效
5. **模型缓存**：首次加载后模型会缓存到本地，后续加载更快

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Hugging Face Diffusers](https://github.com/huggingface/diffusers) - 提供强大的扩散模型库
- [Streamlit](https://streamlit.io/) - 提供优秀的 Web 应用框架
- [Stability AI](https://stability.ai/) - 提供 Stable Diffusion 模型
- 所有开源社区的贡献者们

## 📞 联系方式

- 👤 开发者：梁煜岚
- 🎓 学号：423830227
- 📧 项目地址：[GitHub Repository](https://github.com/YLan127/agents-best-practices)

---

⭐ 如果这个项目对你有帮助，欢迎给个 Star 支持一下！
