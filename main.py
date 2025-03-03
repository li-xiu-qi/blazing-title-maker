#!/usr/bin/env python  
# -*- coding: utf-8 -*-
# author：筱可
# 2025/3/2
"""
爆款标题生成助手 - 简化版

主要功能：
1. 生成多角度的爆款标题方案
2. 自定义模型参数（温度、最大输出长度）
3. 选择不同大模型进行生成

使用方法：
1. 安装依赖：pip install streamlit openai pyyaml
2. 设置配置：在.env.yaml中配置API_KEY和BASE_URL
3. 运行：streamlit run main.py
"""

import os
import streamlit as st
from openai import OpenAI
from datetime import datetime
import re
import yaml
import time
from config import get_provider_config, APP_CONFIG, DEFAULT_PROVIDER, PROVIDERS

# 全局常量定义
AUTHOR = APP_CONFIG["AUTHOR"]
CURRENT_DATE = APP_CONFIG["CURRENT_DATE"]
WECHAT_PLATFORM = APP_CONFIG["WECHAT_PLATFORM"]
APP_TITLE = APP_CONFIG["APP_TITLE"]
APP_DESCRIPTION = APP_CONFIG["APP_DESCRIPTION"]
DEFAULT_MAX_TOKENS = APP_CONFIG["DEFAULT_MAX_TOKENS"]

# 初始化 session_state
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "titles" not in st.session_state:
        st.session_state.titles = []
    if "content_topic" not in st.session_state:
        st.session_state.content_topic = ""
    if "context_length" not in st.session_state:
        st.session_state.context_length = APP_CONFIG["DEFAULT_CONTEXT_LENGTH"]
    if "first_load" not in st.session_state:
        st.session_state.first_load = True
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = DEFAULT_PROVIDER
    if "api_client" not in st.session_state:
        st.session_state.api_client = None

# 初始化会话状态
init_session()

def create_api_client(provider_name):
    """创建并返回API客户端"""
    provider_config = get_provider_config(provider_name)
    api_key = provider_config["api_key"]
    base_url = provider_config["base_url"]
    
    if not api_key:
        st.error(f"错误: {provider_name} 的API密钥未配置")
        return None
    
    return OpenAI(api_key=api_key, base_url=base_url)

# 获取当前选择的提供商并创建API客户端
def get_current_client_and_models():
    provider_name = st.session_state.selected_provider
    if st.session_state.api_client is None:
        st.session_state.api_client = create_api_client(provider_name)
    
    provider_config = get_provider_config(provider_name)
    return st.session_state.api_client, provider_config["models"]

def create_system_prompt():
    """创建系统提示词，采用结构化模板"""
    with open("prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    return system_prompt

def extract_titles(text):
    """从生成的文本中提取所有标题"""
    titles = re.findall(r'\*\*标题\*\*：《(.*?)》', text)
    if not titles:
        # 尝试其他可能的格式
        titles = re.findall(r'标题[：:]\s*《(.*?)》', text)
    
    return titles

def add_copy_button_for_titles(titles):
    """为标题添加复制按钮，使用JavaScript实现无刷新复制"""
    if not titles:
        return
        
    all_titles = "\n".join([f"{i+1}. 《{title}》" for i, title in enumerate(titles)])
    
    # 显示标题列表
    st.code(all_titles, language="text")
    
    # 创建一个使用 JavaScript 的复制按钮
    # 这将避免页面刷新
    copy_button_html = f"""
    <script>
    function copyToClipboard() {{
        const text = `{all_titles}`;
        navigator.clipboard.writeText(text)
            .then(() => {{
                document.getElementById('copy-status').textContent = '✅ 复制成功！';
                setTimeout(() => {{
                    document.getElementById('copy-status').textContent = '';
                }}, 2000);
            }}).catch(err => {{
                document.getElementById('copy-status').textContent = '❌ 复制失败';
                console.error('复制失败:', err);
            }});
    }}
    </script>
    <button onclick="copyToClipboard()" style="background-color: #4CAF50; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">
        📋 复制全部标题
    </button>
    <span id="copy-status" style="margin-left: 10px;"></span>
    """
    
    st.components.v1.html(copy_button_html, height=50)

def handle_chat(prompt, model, temperature, max_tokens):
    """处理用户输入并获取AI回复"""
    
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 获取消息历史，确保在上下文限制范围内
    messages_for_api = st.session_state.messages.copy()
    
    # 截断上下文以满足上下文长度要求
    total_length = sum(len(m["content"]) for m in messages_for_api)
    while len(messages_for_api) > 2 and total_length > st.session_state.context_length:
        # 保留system消息，从最早的用户/助手消息开始删除
        if messages_for_api[1]["role"] != "system":
            messages_for_api.pop(1)
        else:
            messages_for_api.pop(2)
        total_length = sum(len(m["content"]) for m in messages_for_api)
    
    # 生成助手回复
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        collected_messages = []
        
        try:
            # 调用API并流式显示回复
            client, model_list = get_current_client_and_models()
            response = client.chat.completions.create(
                model=model_list[model],
                messages=messages_for_api,
                stream=True,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            # 流式显示响应
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    token = chunk.choices[0].delta.content
                    collected_messages.append(token)
                    response_placeholder.markdown("".join(collected_messages) + "▌")
                    time.sleep(0.01)  # 轻微延迟，使UI更新更平滑
            
            # 最终响应
            final_response = "".join(collected_messages)
            response_placeholder.markdown(final_response)
            
            # 保存到会话状态
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            
            # 处理首次请求，提取标题
            if len(st.session_state.titles) == 0 and "生成" in prompt and "标题" in prompt:
                titles = extract_titles(final_response)
                st.session_state.titles = titles
                
                # 显示标题汇总和复制按钮
                if titles:
                    with st.expander("📋 标题汇总", expanded=True):
                        st.subheader("生成的爆款标题")
                        add_copy_button_for_titles(titles)
        
        except Exception as e:
            error_msg = f"""
            <error>
                [错误分析]
                API请求失败，可能原因：
                1. 上下文过长（当前约：{total_length}字符）
                2. API连接问题
                
                [修正建议]
                请尝试以下操作：
                - 重新组织问题表述
                - 点击"新建对话"以重试
                - 检查API连接设置
                
                技术错误: {str(e)}
            </error>
            """
            response_placeholder.error(error_msg)

def main():
    """主函数，设置Streamlit界面"""
    # 设置页面配置
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🔥",
        layout="wide",
    )
    
    # 添加自定义CSS美化界面
    st.markdown("""
    <style>
    /* 页面标题样式 */
    h1 {
        color: #FF4500;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    
    /* 聊天消息样式 */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 12px !important;
    }
    
    /* 用户消息样式 */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #e6f7ff !重要;
        border-left: 4px solid #1890ff !重要;
    }
    
    /* 助手消息样式 */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #f0f5ea !重要;
        border-left: 4px solid #52c41a !重要;
    }
    
    /* 输入框样式 */
    .stChatInput {
        border-radius: 20px !重要;
        padding: 10px !重要;
        border: 2px solid #ddd !重要;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !重要;
    }
    
    /* 按钮样式美化 */
    .stButton>button {
        border-radius: 10px !重要;
        font-weight: bold !重要;
        transition: all 0.3s ease !重要;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !重要;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !重要;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 显示标题和描述
    st.title(f"🔥 {APP_TITLE}")
    st.markdown(APP_DESCRIPTION)
    
    # 添加作者信息
    st.markdown(
        f"""
        <div style='
            text-align: center;
            padding: 15px;
            background: linear-gradient(45deg, #FFD700, #FFA07A);
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
        '>
            <h4 style='color: #2F4F4F; margin: 0;'>🐰 作者：{AUTHOR}</h4>
            <p style='color: #800080; margin: 10px 0 0;'>
                🌸 公众号：「<strong style='color: #FF4500;'>{WECHAT_PLATFORM}</strong>」
                <br>
                <span style='font-size:14px; color: #4682B4;'>✨ 探索AI的无限可能 ✨</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 首次加载时显示气球
    if st.session_state.first_load:
        st.balloons()
        st.session_state.first_load = False
    
    # 创建侧边栏
    with st.sidebar:
        st.header("⚙️ 参数设置")
        
        # 模型选择
        selected_model = st.selectbox(
            "选择模型",
            list(MODEL_LIST.keys()),
            index=0
        )
        
        # 温度参数
        temperature = st.slider(
            "温度参数",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="较高的值会使输出更随机，较低的值会使其更加集中和确定"
        )
        
        # 最大输出长度
        max_tokens = st.slider(
            "最大输出长度",
            min_value=1000,
            max_value=16000,
            value=DEFAULT_MAX_TOKENS,
            step=100,
            help="控制生成文本的最大长度"
        )
        
        # 上下文长度
        st.session_state.context_length = st.slider(
            "上下文长度",
            min_value=4000,
            max_value=32000,
            value=16000,
            step=1000,
            help="控制保留的对话上下文长度"
        )
        
        # 添加水平分隔线
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 新建对话按钮
        if st.button("🔄 新建对话", use_container_width=True):
            st.session_state.messages = []
            st.session_state.titles = []
            st.session_state.content_topic = ""
            st.rerun()
    
    # 初始化系统消息（如果是新对话）
    if not st.session_state.messages:
        system_prompt = create_system_prompt()
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        # 添加欢迎消息
        welcome_msg = """
        👋 欢迎使用爆款标题生成助手！

        请告诉我您想要为什么内容生成爆款标题？您可以输入内容主题、关键词或描述，我会从8个不同角度为您生成吸引人的标题方案。

        例如：
        - "如何提高工作效率"
        - "健康饮食的好处"
        - "我想为一篇关于数字营销的文章生成标题"
        """
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # 显示聊天记录
    for message in st.session_state.messages:
        if message["role"] != "system":  # 不显示系统消息
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # 聊天输入框
    if prompt := st.chat_input("输入您的内容主题或调整需求..."):
        if not prompt.strip():
            st.warning("请输入内容后再提交")
        else:
            # 处理用户输入
            handle_chat(prompt, selected_model, temperature, max_tokens)
    
    # 标题汇总区（如果已有标题且不在聊天流中显示）
    if st.session_state.titles and len(st.session_state.messages) <= 3:
        st.subheader("📋 标题汇总")
        add_copy_button_for_titles(st.session_state.titles)
    
    # 添加页脚，移到最底部位置
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: #888;">
            © 2025 爆款标题生成助手 | 由{AUTHOR}开发 | {CURRENT_DATE}
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
