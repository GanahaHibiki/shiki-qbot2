import asyncio
import json
import logging
import signal
import sys
from typing import Any

import websockets
from websockets.exceptions import ConnectionClosed

from config import load_config, Config
from handlers import RepeatHandler, MessageHandler

# 全局配置
config: Config = None
handlers: list[MessageHandler] = []
shutdown_event = asyncio.Event()


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def send_message(ws, action: str, params: dict[str, Any]) -> None:
    """发送 OneBot API 请求"""
    payload = {
        "action": action,
        "params": params,
    }
    await ws.send(json.dumps(payload))
    logging.info(f"发送: action={action}, params={params}")


async def handle_event(event: dict[str, Any], ws) -> None:
    """处理收到的事件"""
    post_type = event.get("post_type")

    # 只处理消息事件
    if post_type == "message":
        msg_type = event.get("message_type")
        user_id = event.get("user_id")
        raw_msg = event.get("raw_message", "")[:100]
        group_id = event.get("group_id", "N/A")

        logging.info(f"收到消息: type={msg_type}, group={group_id}, user={user_id}, msg={raw_msg}")

        # 遍历处理器
        for handler in handlers:
            if await handler.should_handle(event):
                await handler.handle(
                    event,
                    lambda action, params: send_message(ws, action, params),
                )


async def connect_and_run() -> None:
    """连接 WebSocket 并运行"""
    logger = logging.getLogger(__name__)
    reconnect_delay = 5

    while not shutdown_event.is_set():
        try:
            logger.info(f"连接到 {config.bot.ws_url}")
            async with websockets.connect(config.bot.ws_url) as ws:
                logger.info("WebSocket 连接成功")
                reconnect_delay = 5  # 重置重连延迟

                while not shutdown_event.is_set():
                    try:
                        message = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        event = json.loads(message)
                        await handle_event(event, ws)
                    except asyncio.TimeoutError:
                        continue
                    except ConnectionClosed as e:
                        logger.warning(f"WebSocket 连接关闭: code={e.code}, reason={e.reason}")
                        break

        except Exception as e:
            logger.error(f"连接错误: {e}")

        if not shutdown_event.is_set():
            logger.info(f"{reconnect_delay}秒后重连...")
            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, 60)


def handle_shutdown(signum, frame) -> None:
    """处理退出信号"""
    logging.info(f"收到信号 {signum}, 正在退出...")
    shutdown_event.set()


def main() -> None:
    global config, handlers

    # 加载配置
    config = load_config()
    setup_logging(config.log_level)

    logger = logging.getLogger(__name__)
    logger.info("QQ Bot 启动中...")
    logger.info(f"WebSocket URL: {config.bot.ws_url}")
    logger.info(f"复读功能: {'开启' if config.repeat.enabled else '关闭'}, 概率: {config.repeat.probability}%")

    # 初始化处理器
    handlers = [
        RepeatHandler(config),
    ]

    # 注册信号处理
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    # 运行主循环
    try:
        asyncio.run(connect_and_run())
    except KeyboardInterrupt:
        pass

    logger.info("Bot 已退出")


if __name__ == "__main__":
    main()
