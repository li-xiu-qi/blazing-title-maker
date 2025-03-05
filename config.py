#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：筱可
"""
配置文件 - 管理不同AI服务提供商的设置
仅使用YAML文件进行配置
"""

import os
import yaml
from datetime import datetime

# 加载YAML格式的环境变量
def load_yaml_env(file_path=".env.yaml"):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        return {}
    except Exception as e:
        print(f"加载YAML配置文件失败: {e}")
        return {}

# 加载环境配置
env_config = load_yaml_env()

# 获取配置值的辅助函数
def get_config_value(config, yaml_path, default=None):
    """
    从YAML配置中获取值

    参数:
    - config: YAML配置字典
    - yaml_path: YAML中的路径，如 'siliconflow.api_key'
    - default: 默认值
    """
    # 从YAML获取
    keys = yaml_path.split('.')
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value

# 服务提供商配置
PROVIDERS = {
    "硅基流动": {
        "name": "硅基流动",
        "api_key": get_config_value(env_config, 'siliconflow.api_key', ""),
        "base_url": get_config_value(env_config, 'siliconflow.base_url', "https://api.siliconflow.cn/v1"),
        "models": {
            "DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
            "DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
            "Qwen-14B": "Qwen/Qwen2.5-14B-Instruct",
            "Qwen-7B": "Qwen/Qwen2.5-7B-Instruct",
        }
    },
    "火山引擎": {
        "name": "火山引擎",
        "api_key": get_config_value(env_config, 'volcano.api_key', ""),
        "base_url": get_config_value(env_config, 'volcano.base_url', "https://ark.cn-beijing.volces.com/api/v3"),
        "models": {
            "DeepSeek-R1": "deepseek-r1-250120",
            "DeepSeek-V3": "deepseek-v3-241226",
        }
    }
}

# 从配置获取默认提供商
DEFAULT_PROVIDER = get_config_value(env_config, 'default_provider', "火山引擎")

# 检查默认提供商是否有效
if DEFAULT_PROVIDER not in PROVIDERS:
    print(f"警告: 配置中的默认提供商 '{DEFAULT_PROVIDER}' 无效，使用火山引擎作为默认值")
    DEFAULT_PROVIDER = "火山引擎"

# 全局常量定义
APP_CONFIG = {
    "AUTHOR": get_config_value(env_config, 'app.author', "筱可"),
    "CURRENT_DATE": datetime.now().strftime("%Y-%m-%d"),
    "WECHAT_PLATFORM": get_config_value(env_config, 'app.wechat_platform', "筱可AI研习社"),
    "APP_TITLE": get_config_value(env_config, 'app.title', "爆款标题生成助手"),
    "APP_DESCRIPTION": get_config_value(env_config, 'app.description', "基于大模型的多角度爆款标题生成工具，从8个不同角度为您打造爆款标题方案"),
    "DEFAULT_MAX_TOKENS": int(get_config_value(env_config, 'app.default_max_tokens', 4096)),
    "DEFAULT_TEMPERATURE": float(get_config_value(env_config, 'app.default_temperature', 0.7)),
    "DEFAULT_CONTEXT_LENGTH": int(get_config_value(env_config, 'app.default_context_length', 16000)),
}

def get_provider_config(provider_name=None):
    """获取指定服务提供商的配置"""
    if provider_name is None:
        provider_name = DEFAULT_PROVIDER

    if provider_name not in PROVIDERS:
        raise ValueError(f"未知的服务提供商: {provider_name}")

    return PROVIDERS[provider_name]

# 获取当前提供商的模型列表
def get_current_models(provider_name=None):
    provider_config = get_provider_config(provider_name)
    return provider_config.get("models", {})

# 验证配置的完整性
def validate_config():
    """验证配置是否完整有效"""
    warnings = []

    # 检查每个提供商是否都有API密钥
    for provider, config in PROVIDERS.items():
        if not config["api_key"]:
            warnings.append(f"警告: {provider} 未配置API密钥")

    if warnings:
        print("\n".join(warnings))
        return False
    return True

# 启动时验证配置
validate_config()
