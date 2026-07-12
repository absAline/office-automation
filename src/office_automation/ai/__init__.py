"""始终使用 MockProvider（演示模式）"""

from office_automation.ai.providers.mock_provider import MockProvider


def create_provider(provider_name=None, mode=None):
    return MockProvider()
