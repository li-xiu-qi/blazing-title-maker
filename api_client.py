from openai import OpenAI
import streamlit as st
from config import get_provider_config, DEFAULT_PROVIDER

def get_current_client_and_models():
    """获取当前API客户端和模型列表"""
    provider_config = get_provider_config(
        st.session_state.get("selected_provider", DEFAULT_PROVIDER)
    )
    api_key = provider_config["api_key"]
    base_url = provider_config["base_url"]

    # 创建OpenAI客户端
    client = OpenAI(api_key=api_key, base_url=base_url)

    return client, provider_config["models"]
