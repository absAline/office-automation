"""自定义异常"""


class OfficeAutomationError(Exception):
    """所有自定义异常的基类"""


class AIProviderError(OfficeAutomationError):
    """AI 提供商相关错误"""


class ModuleNotFoundError(OfficeAutomationError):
    """未找到对应的自动化模块"""


class ValidationError(OfficeAutomationError):
    """参数校验失败"""


class ConfigError(OfficeAutomationError):
    """配置错误"""


class ExecutionError(OfficeAutomationError):
    """脚本执行错误"""
