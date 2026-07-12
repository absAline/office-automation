"""Module: excel — Excel 表格自动化"""
from office_automation.modules.registry import register, ModuleInfo

register(ModuleInfo(
    name="excel",
    title="Excel 表格处理",
    description="自动生成报表、清洗数据、合并工作表、添加图表，支持多种专业格式样式",
    module_path="office_automation.modules.excel",
))

HANDLERS = {
    "generate_report": {"handler": "generate_report", "schema": "GenerateReportParams"},
    "clean_data": {"handler": "clean_data", "schema": "CleanDataParams"},
    "merge_sheets": {"handler": "merge_sheets", "schema": "MergeSheetsParams"},
    "analyze": {"handler": "analyze", "schema": "GenerateReportParams"},
}


def get_handler(action: str):
    import importlib
    info = HANDLERS.get(action)
    if not info:
        raise ValueError(f"未知操作: {action}")
    mod = importlib.import_module("office_automation.modules.excel.tools")
    handler = getattr(mod, info["handler"])
    schema_cls = info.get("schema")
    return handler, schema_cls
