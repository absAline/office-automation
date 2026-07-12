"""模块注册与发现"""

from typing import Any
from office_automation.exceptions import ModuleNotFoundError


class ModuleInfo:
    """模块元信息"""

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        module_path: str,
        enabled: bool = True,
    ):
        self.name = name
        self.title = title
        self.description = description
        self.module_path = module_path
        self.enabled = enabled


# 全局模块注册表
_MODULES: dict[str, ModuleInfo] = {}


def register(module_info: ModuleInfo):
    """注册模块"""
    _MODULES[module_info.name] = module_info


def get_module(name: str) -> ModuleInfo:
    """获取模块信息"""
    if name not in _MODULES:
        raise ModuleNotFoundError(f"未找到模块: {name}，可用模块: {list(_MODULES.keys())}")
    return _MODULES[name]


def list_modules() -> list[ModuleInfo]:
    """列出所有已注册模块"""
    return list(_MODULES.values())


def is_registered(name: str) -> bool:
    """检查模块是否已注册"""
    return name in _MODULES


# ============ 导入模块以触发注册 ============

def init():
    """初始化所有模块（导入触发注册）"""
    import importlib

    modules_to_load = [
        "office_automation.modules.excel",
        "office_automation.modules.email",
        "office_automation.modules.document",
        "office_automation.modules.file_organizer",
    ]

    for mod_path in modules_to_load:
        try:
            importlib.import_module(mod_path)
        except ImportError as e:
            print(f"  [警告] 加载模块 {mod_path} 失败: {e}")
