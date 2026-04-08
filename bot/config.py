import os
from pathlib import Path
from dataclasses import dataclass, field

import yaml


@dataclass
class RepeatConfig:
    enabled: bool = True
    probability: int = 5  # 0-100


@dataclass
class AIReplyConfig:
    enabled: bool = False
    probability: int = 10  # 0-100
    api_key: str = ""
    model: str = "deepseek-ai/DeepSeek-V3"
    system_prompt: str = "你是一个活泼可爱的群聊助手，喜欢用简洁幽默的方式回复消息。请用1-2句话自然地回应用户，不要过于正式。"
    http_proxy: str = ""  # HTTP 代理
    https_proxy: str = ""  # HTTPS 代理


@dataclass
class BotConfig:
    ws_url: str = "ws://napcat:3001"
    token: str = ""


@dataclass
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    repeat: RepeatConfig = field(default_factory=RepeatConfig)
    ai_reply: AIReplyConfig = field(default_factory=AIReplyConfig)
    log_level: str = "INFO"


def load_config(config_path: str = "config.yaml") -> Config:
    """加载配置，优先级: 环境变量 > config.yaml > 默认值"""
    config = Config()

    # 从 yaml 文件加载
    path = Path(config_path)
    if path.is_file():
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if "bot" in data:
            config.bot = BotConfig(
                ws_url=data["bot"].get("ws_url", config.bot.ws_url),
                token=data["bot"].get("token", config.bot.token),
            )

        if "repeat" in data:
            config.repeat = RepeatConfig(
                enabled=data["repeat"].get("enabled", config.repeat.enabled),
                probability=data["repeat"].get("probability", config.repeat.probability),
            )

        if "ai_reply" in data:
            config.ai_reply = AIReplyConfig(
                enabled=data["ai_reply"].get("enabled", config.ai_reply.enabled),
                probability=data["ai_reply"].get("probability", config.ai_reply.probability),
                api_key=data["ai_reply"].get("api_key", config.ai_reply.api_key),
                model=data["ai_reply"].get("model", config.ai_reply.model),
                system_prompt=data["ai_reply"].get("system_prompt", config.ai_reply.system_prompt),
                http_proxy=data["ai_reply"].get("http_proxy", config.ai_reply.http_proxy),
                https_proxy=data["ai_reply"].get("https_proxy", config.ai_reply.https_proxy),
            )

        config.log_level = data.get("log_level", config.log_level)

    # 环境变量覆盖
    if ws_url := os.getenv("WS_URL"):
        config.bot.ws_url = ws_url

    if token := os.getenv("WS_TOKEN"):
        config.bot.token = token

    if prob := os.getenv("REPEAT_PROBABILITY"):
        config.repeat.probability = int(prob)

    if ai_api_key := os.getenv("AI_API_KEY"):
        config.ai_reply.api_key = ai_api_key

    if ai_model := os.getenv("AI_MODEL"):
        config.ai_reply.model = ai_model

    if ai_system_prompt := os.getenv("AI_SYSTEM_PROMPT"):
        config.ai_reply.system_prompt = ai_system_prompt

    if ai_prob := os.getenv("AI_REPLY_PROBABILITY"):
        config.ai_reply.probability = int(ai_prob)

    # 代理配置（支持标准环境变量）
    if http_proxy := os.getenv("HTTP_PROXY") or os.getenv("http_proxy"):
        config.ai_reply.http_proxy = http_proxy

    if https_proxy := os.getenv("HTTPS_PROXY") or os.getenv("https_proxy"):
        config.ai_reply.https_proxy = https_proxy

    if log_level := os.getenv("LOG_LEVEL"):
        config.log_level = log_level

    return config
