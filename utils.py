import re
import streamlit as st

def extract_titles(text):
    """从生成的文本中提取所有标题"""
    titles = re.findall(r"\*\*标题\*\*：《(.*?)》", text)
    if not titles:
        # 尝试其他可能的格式
        titles = re.findall(r"标题[：:]\s*《(.*?)》", text)
    if not titles:
        # 尝试仅匹配《》中的内容
        titles = re.findall(r"《(.*?)》", text)

    return titles

def add_copy_button_for_titles(titles):
    """为标题添加复制按钮，使用JavaScript实现无刷新复制"""
    if not titles:
        return

    all_titles = "\n".join([f"{i+1}. 《{title}》" for i, title in enumerate(titles)])

    # 显示标题列表
    st.code(all_titles, language="text")

    # 创建JavaScript复制按钮
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
