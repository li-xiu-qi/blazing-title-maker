# 爆款标题生成助手 - 技术文档

## 项目概述

爆款标题生成助手是一个基于大型语言模型的应用，旨在帮助内容创作者、自媒体运营者和营销人员快速生成具有吸引力和传播力的标题。该工具基于爆款选题的底层逻辑和策划技巧，从多个不同角度为用户提供系统化的标题方案。

## 系统架构

### 项目结构

```
blazing-title-maker/
│
├── main.py                # 主应用程序
├── config.py              # 配置管理模块
├── api_client.py          # API客户端模块
├── utils.py               # 实用工具函数
├── session_manager.py     # 会话状态管理
├── prompt.py              # 提示词加载器
├── prompt.md              # 中文提示词模板
├── prompt_en.md           # 英文提示词模板
├── document.md            # 技术文档
├── article.md             # 项目说明文章
├── requirements.txt       # 依赖清单
├── README.md              # 项目说明文档
├── .env.yaml              # 实际环境配置文件
├── .env.example.yaml      # 示例配置文件
└── .gitignore             # Git忽略配置
```

### 核心模块

1. **主应用程序 (main.py)**
   - 负责Streamlit界面构建和用户交互逻辑
   - 处理用户输入并展示AI生成内容
   - 管理会话状态和上下文

2. **配置管理 (config.py)**
   - 从YAML文件加载配置和API密钥
   - 管理不同服务提供商的模型配置
   - 提供全局应用程序配置常量

3. **API客户端 (api_client.py)**
   - 创建和管理与大模型API的连接
   - 处理客户端切换和模型选择

4. **实用工具 (utils.py)**
   - 提供标题提取功能
   - 实现一键复制功能
   - 处理文本解析和格式化

5. **会话管理 (session_manager.py)**
   - 初始化和管理Streamlit会话状态
   - 处理系统提示词和欢迎消息

6. **提示词加载器 (prompt.py)**
   - 加载和处理提示词模板
   - 提供默认提示词作为备选

## 功能详解

### 1. 多角度标题生成

系统基于以下8个角度生成爆款标题：

1. **好奇心驱动型**：制造信息差，引发读者好奇心
2. **解决问题型**：直接点明能解决的痛点问题
3. **数字清单型**：使用数字增强可信度和具体感
4. **情感共鸣型**：触发读者的情感共鸣和认同感
5. **惊喜反转型**：设置反常识或意料之外的信息
6. **权威背书型**：借助权威人物或机构增加可信度
7. **紧迫感型**：创造时间压力，促使快速点击
8. **争议讨论型**：提出有争议的观点引发讨论

### 2. 多模型支持

系统支持以下大模型服务提供商：

1. **硅基流动**
   - DeepSeek-V3
   - DeepSeek-R1
   - Qwen-14B
   - Qwen-7B

2. **火山引擎**
   - DeepSeek-R1
   - DeepSeek-V3

### 3. 参数自定义

用户可以通过UI自定义以下参数：

- **温度 (Temperature)**：控制生成内容的随机性和创造性，取值范围0.0-2.0
- **最大输出长度 (Max Tokens)**：控制生成文本的最大长度，范围1000-16000
- **选择模型**：从支持的模型列表中选择

### 4. 标题汇总与复制

- 自动提取生成内容中的标题
- 将所有标题汇总展示
- 提供一键复制功能，便于用户使用

## 技术实现

### 提示词工程

系统使用精心设计的提示词模板，基于爆款选题的三大底层逻辑和五大策划技巧。提示词结构包含：

- **角色定位**：内容创作顾问，擅长把握受众心理
- **工作流程**：理解主题、分析受众、多角度构思、提供方案
- **角度框架**：8个不同角度的标题构思指导
- **输出格式**：统一的标题输出格式，便于解析

### API调用流程

1. 接收用户输入
2. 获取当前选择的提供商配置
3. 创建API客户端
4. 处理上下文长度，确保在模型限制范围内
5. 发起流式调用，实现实时显示效果
6. 解析响应，提取标题
7. 保存到会话状态并展示结果

### 标题提取机制

系统使用正则表达式从生成的文本中提取标题：

```python
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
```

### 一键复制功能

系统使用HTML和JavaScript实现无刷新复制功能：

```python
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
```

## 配置说明

### 环境配置

系统使用YAML格式的配置文件存储API密钥和应用设置：

```yaml
# API配置
siliconflow:
  api_key: your_siliconflow_api_key_here
  base_url: https://api.siliconflow.cn/v1

volcano:
  api_key: your_volcano_api_key_here
  base_url: https://ark.cn-beijing.volces.com/api/v3

# 默认提供商设置
default_provider: 火山引擎

# 应用程序配置
app:
  title: 爆款标题生成助手
  description: 基于大模型的多角度爆款标题生成工具，从8个不同角度为您打造爆款标题方案
  author: 筱可
  wechat_platform: DateWhale
  default_max_tokens: 4096
  default_temperature: 0.7
  default_context_length: 16000
```

### 模型参数说明

1. **温度 (Temperature)**
   - **低温度 (0.1-0.5)**: 输出更确定、一致，适合严谨场景
   - **中温度 (0.5-0.8)**: 平衡创造性和一致性，适合标题生成
   - **高温度 (0.8-2.0)**: 更加随机、创造性，但可能出现偏差

2. **最大输出长度 (Max Tokens)**
   - 建议值：3000-5000，保证完整输出多个标题方案
   - 过长会增加生成时间，过短可能导致输出不完整

## 使用指南

### 安装部署

1. **克隆项目**

   ```bash
   git clone https://github.com/li-xiu-qi/blazing-title-maker.git
   cd blazing-title-maker
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **配置API密钥**

   ```bash
   cp .env.example.yaml .env.yaml
   # 编辑 .env.yaml 文件，填入您的API密钥
   ```

4. **启动应用**

   ```bash
   streamlit run main.py
   ```

### 使用方法

1. **输入主题**
   - 在聊天界面输入您想要为哪个主题生成标题
   - 例如："请为Python编程初学者教程生成爆款标题"

2. **调整参数**
   - 在侧边栏选择模型提供商和具体模型
   - 调整温度参数影响标题的创意性
   - 调整最大输出长度确保完整生成

3. **查看结果**
   - 系统会流式展示生成过程
   - 生成完成后，自动提取标题并汇总展示

4. **复制使用**
   - 点击"复制全部标题"按钮一键复制所有标题
   - 可以在您的内容创作中使用这些标题

## 常见问题与解决方案

### API连接问题

**问题**: 调用API时出现连接错误
**解决方案**:

- 检查API密钥是否正确配置
- 验证网络连接是否正常
- 确认服务提供商API是否可用
- 检查账户余额是否充足

### 标题提取失败

**问题**: 系统未能成功提取标题
**解决方案**:

- 检查提示词模板是否指示模型按正确格式输出标题
- 尝试调整温度参数为较低值，使输出更结构化
- 修改utils.py中的正则表达式以适应更多标题格式

### 性能优化

**问题**: 生成过程较慢
**解决方案**:

- 减少最大输出长度
- 选择较小型的模型
- 考虑升级API计划获取更好性能
- 优化上下文管理，减少传入模型的历史消息数量

## 扩展与定制化

### 添加新模型

要添加新的模型或服务提供商，需要在config.py文件中进行以下更新：

```python
PROVIDERS = {
    # 现有提供商...
    
    "新提供商": {
        "name": "新提供商名称",
        "api_key": get_config_value(env_config, 'new_provider.api_key', ""),
        "base_url": get_config_value(env_config, 'new_provider.base_url', ""),
        "models": {
            "模型名称1": "模型ID1",
            "模型名称2": "模型ID2",
        }
    }
}
```

### 修改提示词模板

您可以通过编辑prompt.md文件自定义提示词模板，添加更多标题角度或调整输出格式：

1. 在"标题构思角度"部分添加新角度
2. 调整"输出格式"部分以适应您的需求
3. 修改系统角色和背景以针对特定领域进行优化

### 添加数据持久化功能

目前系统只在会话期间保存生成内容，您可以扩展功能添加数据持久化：

1. 创建数据存储模块，支持文件或数据库存储
2. 在标题生成后保存结果
3. 添加历史记录查询功能
4. 实现标题方案的导入/导出功能

## 贡献指南

我们欢迎社区贡献，提升爆款标题生成助手的功能和质量：

1. Fork项目并创建分支
2. 提交代码改进或新功能
3. 编写测试并确保通过
4. 创建Pull Request详细说明变更内容

## 版本历史

- **v0.1.0** - 初始版本，基本功能实现
- **v0.2.0** - 添加多模型支持
- **v0.3.0** - 实现标题提取和一键复制功能
- **v0.4.0** - 优化UI界面和用户体验
- **v0.5.0** - 添加配置管理和多提供商支持

## 作者信息

- **作者**: 筱可
- **微信公众号**: 筱可AI研习社
- **联系方式**: 关注微信公众号获取支持

## 许可证

本项目采用 MIT 许可证，详情请参见 LICENSE 文件。

