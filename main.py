#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：筱可
"""
爆款标题生成助手 - 主应用程序
"""

import time
import streamlit as st
from config import APP_CONFIG, PROVIDERS, DEFAULT_PROVIDER, get_provider_config, get_current_models

# 从APP_CONFIG提取常量
APP_TITLE = APP_CONFIG["APP_TITLE"]
APP_DESCRIPTION = APP_CONFIG["APP_DESCRIPTION"]
DEFAULT_MAX_TOKENS = APP_CONFIG["DEFAULT_MAX_TOKENS"]
DEFAULT_TEMPERATURE = APP_CONFIG["DEFAULT_TEMPERATURE"]
DEFAULT_CONTEXT_LENGTH = APP_CONFIG["DEFAULT_CONTEXT_LENGTH"]

from api_client import get_current_client_and_models
from utils import extract_titles, add_copy_button_for_titles
from session_manager import init_session


# 处理聊天
def handle_chat(prompt, model, temperature, max_tokens):
    """处理用户输入并获取AI回复"""
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 截断上下文以满足上下文长度要求
    messages_for_api = st.session_state.messages.copy()

    # 计算上下文总长度
    total_length = sum(len(msg["content"]) for msg in messages_for_api)

    # 如果上下文长度超过限制，移除旧的对话消息
    max_context_length = DEFAULT_CONTEXT_LENGTH
    if total_length > max_context_length:
        # 保留系统提示词和最近的对话
        system_message = None
        if messages_for_api and messages_for_api[0]["role"] == "system":
            system_message = messages_for_api.pop(0)

        # 移除中间的消息直到总长度低于限制
        while total_length > max_context_length and len(messages_for_api) > 2:
            # 从第二条消息开始移除 (保留最近的一对对话)
            removed_msg = messages_for_api.pop(1)
            total_length -= len(removed_msg["content"])

        # 重新添加系统提示词
        if system_message:
            messages_for_api.insert(0, system_message)

    # 生成助手回复
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        collected_messages = []

        try:
            # 调用API并流式显示回复
            client, model_list = get_current_client_and_models()

            # 获取选择的模型ID
            provider_name, model_name = model
            selected_model = get_provider_config(provider_name)["models"].get(
                model_name
            )

            if not selected_model:
                response_placeholder.error(f"错误: 无效的模型选择 {model}")
                return

            response = client.chat.completions.create(
                model=selected_model,
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
                    time.sleep(0.01)

            # 最终响应处理
            final_response = "".join(collected_messages)
            response_placeholder.markdown(final_response)

            # 保存到会话状态
            st.session_state.messages.append(
                {"role": "assistant", "content": final_response}
            )

            # 处理首次请求，提取标题
            if (
                len(st.session_state.titles) == 0
                and "生成" in prompt
                and "标题" in prompt
            ):
                titles = extract_titles(final_response)
                st.session_state.titles = titles

                # 显示标题汇总和复制按钮
                if titles:
                    with st.expander("📋 标题汇总", expanded=True):
                        st.subheader("生成的爆款标题")
                        add_copy_button_for_titles(titles)

        except Exception as e:
            # 错误处理逻辑
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


# 主应用程序
def main():
    """主函数，设置Streamlit界面"""
    # 设置页面配置
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🔥",
        layout="wide",
    )

    # 添加自定义CSS美化界面
    st.markdown(
        """
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
    
    /* 边栏样式 */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* 按钮样式 */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # 初始化会话状态
    init_session()

    # 显示标题和描述
    st.title(f"🔥 {APP_TITLE}")

    # 更紧凑的应用信息展示
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; 
                margin-bottom: 15px; max-width: 600px; margin-left: auto; margin-right: auto;">
            <p style="margin: 0; font-size: 0.8em;"><strong>作者</strong>: {}</p>
            <p style="margin: 0; font-size: 0.8em;"><strong></strong>{}</p>
            <p style="margin: 0; font-size: 0.8em;"><em>{}</em></p>
        </div>
    """.format(
        APP_CONFIG['AUTHOR'],
        APP_CONFIG['WECHAT_PLATFORM'],
        APP_CONFIG['APP_DESCRIPTION']
    ), unsafe_allow_html=True)
    
    # 创建侧边栏
    with st.sidebar:
        st.header("⚙️ 参数设置")

        # 提供商选择
        provider_options = list(PROVIDERS.keys())
        selected_provider = st.selectbox(
            "选择服务提供商",
            provider_options,
            index=(
                provider_options.index(st.session_state.selected_provider)
                if st.session_state.selected_provider in provider_options
                else 0
            ),
        )

        # 更新会话状态中的提供商
        if selected_provider != st.session_state.selected_provider:
            st.session_state.selected_provider = selected_provider

        # 获取当前提供商的模型列表
        MODEL_LIST = get_current_models(selected_provider)

        # 模型选择
        selected_model_name = st.selectbox("选择模型", list(MODEL_LIST.keys()), index=1)

        # 组合为模型标识符
        selected_model = (selected_provider, selected_model_name)

        # 温度参数
        temperature = st.slider(
            "温度参数",
            min_value=0.0,
            max_value=2.0,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
            help="较高的值会使输出更随机，较低的值会使其更加集中和确定",
        )

        # 最大输出长度
        max_tokens = st.slider(
            "最大输出长度",
            min_value=1000,
            max_value=16000,
            value=DEFAULT_MAX_TOKENS,
            step=100,
            help="控制生成文本的最大长度",
        )

        # 添加新建对话按钮
        if st.button("🔄 新建对话", type="primary"):
            # 清空对话历史和标题缓存
            st.session_state.messages = []
            st.session_state.titles = []
            # init_session()
            st.rerun()

  
    

    # 显示对话历史
    for message in st.session_state.messages:
        if message["role"] != "system":  # 不显示系统提示词
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 创建聊天输入框
    user_input = st.chat_input("请告诉我您想为什么主题或内容生成标题？")
    if user_input:
        handle_chat(user_input, selected_model, temperature, max_tokens)




if __name__ == "__main__":
    main()
