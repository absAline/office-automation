"""AI Provider 抽象基类"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class AIProvider(ABC):
    """AI 提供商抽象接口"""

    @abstractmethod
    async def chat(self, messages: list[dict], **kwargs) -> str:
        """非流式对话，返回完整响应文本"""
        ...

    @abstractmethod
    async def stream(self, messages: list[dict], **kwargs) -> AsyncIterator[str]:
        """流式对话，逐 token 产出"""
        ...
        yield  # pragma: no cover
