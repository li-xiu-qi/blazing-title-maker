# 🔥 爆款标题生成助手

基于大模型的多角度爆款标题生成工具，从多个不同角度为您打造具有吸引力且易于传播的爆款标题方案。

![爆款标题生成助手](https://img.shields.io/badge/爆款标题-生成助手-orange)

## 📝 项目简介

"爆款标题生成助手"是一个基于大型语言模型的工具，旨在帮助内容创作者、自媒体运营者和营销人员快速生成具有爆款潜力的标题。该工具基于爆款选题的底层逻辑和策划技巧，从多个不同角度为用户提供系统化的标题方案，有效提升内容的点击率和传播效果。

## ✨ 核心功能

- 📊 **多角度标题生成**：从8个不同角度生成标题方案，包括情感共鸣型、问题解决型、好奇心驱动型等
- 🔄 **多模型支持**：支持多种大语言模型，包括DeepSeek、Qwen等
- ⚙️ **参数自定义**：提供温度、最大输出长度等参数调整，满足不同创作需求
- 💬 **交互式体验**：通过Streamlit实现直观的用户界面，支持实时对话和反馈
- 📋 **标题汇总与复制**：自动提取并汇总生成的标题，支持一键复制功能

## 🛠️ 安装指南

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

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

  复制示例配置文件并填入您的API密钥:

  ```bash
  cp .env.example.yaml .env.yaml
  # 编辑 .env.yaml 文件，填入您的API密钥
  ```

## 🚀 使用方法

1. **启动应用**

  ```bash
  streamlit run main.py
  ```

2. **使用界面**

- 在输入框中输入您想要为其生成标题的内容主题或关键词
- 助手会从多个角度为您生成爆款标题方案
- 使用侧边栏调整模型和生成参数
- 通过"标题汇总"部分一键复制所有生成的标题

## ⚙️ 配置说明

在`.env.yaml`文件中配置以下参数:

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
```

## 📁 项目结构

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

## 🧠 提示词设计

该项目采用精心设计的提示词模板，基于爆款选题的三大底层逻辑：

- 覆盖人群
- 痛点程度
- 社交原力

以及策划爆款选题的5大技巧：

- 戳中普遍痛点
- 引发群体共鸣
- 制造身份认同
- 借用热点赋能
- 多维提供新知

## 👨‍💻 作者

筱可 - 微信公众号：「筱可AI研习社」

## 📄 许可证

[MIT](LICENSE)

---

*探索AI的无限可能*
