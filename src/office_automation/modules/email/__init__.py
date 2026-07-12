"""Module: email — 邮件自动化"""
from office_automation.modules.registry import register, ModuleInfo

register(ModuleInfo(
    name="email",
    title="邮件发送",
    description="自动撰写邮件、批量发送、模板填充，支持附件和草稿保存",
    module_path="office_automation.modules.email",
))

HANDLERS = {
    "compose_and_send": {"handler": "compose_and_send", "schema": "ComposeParams"},
    "batch_send": {"handler": "batch_send", "schema": "BatchSendParams"},
    "create_template": {"handler": "create_template", "schema": "ComposeParams"},
}


def get_handler(action: str):
    import importlib
    info = HANDLERS.get(action)
    if not info:
        raise ValueError(f"未知操作: {action}")
    mod = importlib.import_module("office_automation.modules.email.tools")
    handler = getattr(mod, info["handler"])
    schema_cls = info.get("schema")
    return handler, schema_cls
