import streamlit as st
import yaml

# 固定个人信息
NAME = "梁煜岚"
SID = "423830227"

st.set_page_config(page_title="Agent调优平台", layout="wide")
st.header("大模型智能Agent参数调优可视化系统")
st.subheader(f"开发学生：{NAME} | 学号：{SID}")
st.divider()

# 侧边栏：可调AI参数
with st.sidebar:
    st.title("智能体超参数控制面板")
    temp = st.slider("模型温度Temperature", 0.0, 1.0, 0.7)
    max_token = st.slider("输出最大Token", 128, 4096, 1024)
    agent_mode = st.selectbox("Agent工作模式", ["单任务Agent", "多Agent协作", "工具调用Agent"])
    prompt_opt = st.radio("提示词优化方案", ["基础Prompt", "Few-shot", "CoT思维链"])

# 主页面：配置预览、迁移加载
tab1, tab2 = st.tabs(["参数配置预览", "迁移加载历史配置"])
with tab1:
    st.json({
        "temperature": temp,
        "max_tokens": max_token,
        "agent_workflow": agent_mode,
        "prompt_strategy": prompt_opt
    })
with tab2:
    st.file_uploader("上传yaml配置文件，一键迁移复用Agent工作流")