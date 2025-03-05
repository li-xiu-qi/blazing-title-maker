import streamlit as st
from config import DEFAULT_PROVIDER
from prompt import load_prompt_template

def init_session():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "titles" not in st.session_state:
        st.session_state.titles = []

    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = DEFAULT_PROVIDER

    # 设置系统提示词
    if len(st.session_state.messages) == 0:
        system_prompt = load_prompt_template()
        if system_prompt:
            st.session_state.messages.append(
                {"role": "system", "content": system_prompt}
            )
            # 添加欢迎消息
            welcome_message = "您好！我是爆款标题生成助手，可以从多个角度为您的内容生成具有吸引力的标题。请告诉我您想为什么主题或内容生成标题？"
            st.session_state.messages.append(
                {"role": "assistant", "content": welcome_message}
            )
