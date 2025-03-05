import os
import streamlit as st

def load_prompt_template(file_path="prompt.md"):
    """加载提示词模板"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            st.error(f"提示词模板文件 {file_path} 不存在!")
            return """你是一个专业的爆款标题生成助手，擅长为各类内容创作者生成吸引人的标题。
请根据我提供的内容，从多个角度生成10个吸引人的标题，标题需要有吸引力、好奇心和价值点。
每个标题请使用《》包裹，并给出简短的创作思路说明。"""
    except Exception as e:
        st.error(f"加载提示词模板失败: {e}")
        return """你是一个专业的爆款标题生成助手，擅长为各类内容创作者生成吸引人的标题，请根据我提供的内容，从多个角度生成10个吸引人的标题，标题需要有吸引力、好奇心和价值点，每个标题请使用《》包裹，并给出简短的创作思路说明。"""
