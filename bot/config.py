import os
from pathlib import Path
from dataclasses import dataclass, field

import yaml


@dataclass
class RepeatConfig:
    enabled: bool = True
    probability: int = 5  # 0-100


@dataclass
class BotConfig:
    ws_url: str = "ws://napcat:3001"


@dataclass
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    repeat: RepeatConfig = field(default_factory=RepeatConfig)
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
                ws_url=data["bot"].get("ws_url", config.bot.ws_url)
            )

        if "repeat" in data:
            config.repeat = RepeatConfig(
                enabled=data["repeat"].get("enabled", config.repeat.enabled),
                probability=data["repeat"].get("probability", config.repeat.probability),
            )

        config.log_level = data.get("log_level", config.log_level)

    # 环境变量覆盖
    if ws_url := os.getenv("WS_URL"):
        config.bot.ws_url = ws_url

    if prob := os.getenv("REPEAT_PROBABILITY"):
        config.repeat.probability = int(prob)

    if log_level := os.getenv("LOG_LEVEL"):
        config.log_level = log_level

    return config
