"""Module: file_organizer — 文件整理自动化"""
from office_automation.modules.registry import register, ModuleInfo

register(ModuleInfo(
    name="file_organizer",
    title="文件整理",
    description="按类型/名称/日期分类文件、批量重命名、清理空文件和临时文件，支持预览模式",
    module_path="office_automation.modules.file_organizer",
))

HANDLERS = {
    "organize": {"handler": "organize", "schema": "OrganizeParams"},
    "rename_batch": {"handler": "rename_batch", "schema": "RenameParams"},
    "cleanup": {"handler": "cleanup", "schema": "CleanupParams"},
    "analyze": {"handler": "analyze", "schema": "OrganizeParams"},
}


def get_handler(action: str):
    import importlib
    info = HANDLERS.get(action)
    if not info:
        raise ValueError(f"未知操作: {action}")
    mod = importlib.import_module("office_automation.modules.file_organizer.tools")
    handler = getattr(mod, info["handler"])
    schema_cls = info.get("schema")
    return handler, schema_cls
