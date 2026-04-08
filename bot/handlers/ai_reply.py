import random
import logging
from typing import Any
import httpx

from .base import MessageHandler

logger = logging.getLogger(__name__)


class AIReplyHandler(MessageHandler):
    """AI回复处理器 - 使用免费AI模型随机回复消息"""

    def __init__(self, config):
        super().__init__(config)

        # 配置代理
        proxies = {}
        if self.config.ai_reply.http_proxy:
            proxies["http://"] = self.config.ai_reply.http_proxy
            logger.info(f"配置 HTTP 代理: {self.config.ai_reply.http_proxy}")

        if self.config.ai_reply.https_proxy:
            proxies["https://"] = self.config.ai_reply.https_proxy
            logger.info(f"配置 HTTPS 代理: {self.config.ai_reply.https_proxy}")

        # 创建 HTTP 客户端（带或不带代理）
        self.client = httpx.AsyncClient(
            timeout=30.0,
            proxies=proxies if proxies else None
        )

    async def should_handle(self, event: dict[str, Any]) -> bool:
        """判断是否处理: 群消息 + 随机概率命中 + 功能开启"""
        if not self.config.ai_reply.enabled:
            return False

        if event.get("post_type") != "message":
            return False

        if event.get("message_type") != "group":
            return False

        # 随机概率判断
        roll = random.randint(0, 99)
        hit = roll < self.config.ai_reply.probability
        if hit:
            logger.debug(f"AI回复命中: roll={roll}, prob={self.config.ai_reply.probability}")
        return hit

    async def _call_ai_api(self, user_message: str) -> str:
        """调用免费AI API获取回复

        使用 SiliconFlow 的免费API (deepseek-chat)
        其他备选：GLM-4-Flash (智谱), Qwen-Turbo (通义千问)
        """
        try:
            # 使用 SiliconFlow 的免费 DeepSeek API
            api_url = "https://api.siliconflow.cn/v1/chat/completions"
            api_key = self.config.ai_reply.api_key or "sk-placeholder"  # 需要用户配置

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # 构建消息
            messages = [
                {"role": "system", "content": self.config.ai_reply.system_prompt},
                {"role": "user", "content": user_message}
            ]

            payload = {
                "model": self.config.ai_reply.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }

            logger.debug(f"调用AI API: model={self.config.ai_reply.model}")

            response = await self.client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            reply = data["choices"][0]["message"]["content"].strip()

            logger.info(f"AI回复生成成功: {reply[:50]}...")
            return reply

        except httpx.HTTPStatusError as e:
            logger.error(f"AI API HTTP错误: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"AI API调用失败: {e}")
            return None

    async def handle(self, event: dict[str, Any], send_func) -> None:
        """使用AI生成回复并发送"""
        group_id = event.get("group_id")
        raw_message = event.get("raw_message", "")

        logger.info(f"AI回复触发: group={group_id}, message={raw_message[:50]}")

        # 调用AI获取回复
        ai_response = await self._call_ai_api(raw_message)

        if not ai_response:
            logger.warning("AI回复失败，跳过")
            return

        # 发送AI回复
        await send_func(
            action="send_group_msg",
            params={
                "group_id": group_id,
                "message": ai_response,
            },
        )

        logger.info(f"AI回复已发送: group={group_id}")

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()
