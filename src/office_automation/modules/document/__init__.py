"""Module: document — Word 文档自动化"""
from office_automation.modules.registry import register, ModuleInfo

register(ModuleInfo(
    name="document",
    title="Word 文档处理",
    description="自动填充 Word 模板、批量生成文档、合并文档，支持 CSV 数据源",
    module_path="office_automation.modules.document",
))

HANDLERS = {
    "fill_template": {"handler": "fill_template", "schema": "FillTemplateParams"},
    "batch_generate": {"handler": "batch_generate", "schema": "BatchGenerateParams"},
    "merge_documents": {"handler": "merge_documents", "schema": "FillTemplateParams"},
}


def get_handler(action: str):
    import importlib
    info = HANDLERS.get(action)
    if not info:
        raise ValueError(f"未知操作: {action}")
    mod = importlib.import_module("office_automation.modules.document.tools")
    handler = getattr(mod, info["handler"])
    schema_cls = info.get("schema")
    return handler, schema_cls
