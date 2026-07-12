# Executor Agent (Module Execution Pipeline)

## Purpose
接收 AI Agent 的意图分类结果，执行实际的办公自动化操作。是连接"AI 理解"和"真实操作"的桥梁。

## Files
- `executor.py` — 模块执行器
- `modules/registry.py` — 模块注册与发现

## Execution Flow

```
AI Agent JSON
  {module:"excel", action:"generate_report", params:{...}}
        │
        ▼
1. Module Lookup ─── registry.get_module("excel")
        │
        ▼
2. Schema Validation ─── resolve Pydantic schema → params validate
        │
        ▼
3. Handler Resolution ─── "tools.generate_report" → actual function
        │
        ▼
4. Execution ─── call handler(**params)
        │
        ▼
5. Result ─── {success, output, files, data}
```

## Module Structure

每个模块位于 `modules/<name>/`，包含 3 个文件：

```
modules/excel/
├── __init__.py    # 注册 + HANDLERS 字典 + get_handler()
├── schemas.py     # Pydantic 参数模型
└── tools.py       # 实际工具函数
```

### `__init__.py`

```python
register(ModuleInfo(name="excel", title="Excel表格处理", ...))

HANDLERS = {
    "generate_report": {"handler": "tools.generate_report", "schema": "GenerateReportParams"},
    "clean_data":      {"handler": "tools.clean_data",      "schema": "CleanDataParams"},
}
```

### `schemas.py`

Pydantic BaseModel，定义每个 action 的入参：

```python
class GenerateReportParams(BaseModel):
    title: str = Field(default="报表")
    headers: list[str] = Field(default_factory=list)
    data: list[list[Any]] = Field(default_factory=list)
    include_chart: bool = Field(default=False)
    chart_type: str = Field(default="bar")
```

### `tools.py`

纯函数，接收 Pydantic 模型解包后的关键字参数，返回统一 dict：

```python
def generate_report(title, headers, data, ...) -> dict:
    try:
        # 真实操作...
        return {"success": True, "message": "...", "files": [...]}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Registry

全局注册表在 `modules/registry.py`：

- `register(info)` — 注册模块
- `get_module(name)` — 查找模块
- `list_modules()` — 列出所有模块
- `init()` — 导入所有模块（触发自动注册）

## Current Modules

| Module | Actions | Real Dependencies |
|--------|---------|-----------------|
| `excel` | generate_report, clean_data, merge_sheets, analyze | openpyxl |
| `email` | compose_and_send, batch_send, create_template | smtplib, jinja2 |
| `document` | fill_template, batch_generate, merge_documents | python-docx |
| `file_organizer` | organize, rename_batch, cleanup, analyze | shutil, os |

## Schema Resolution

Executor 自动将 schema 字符串名（如 `"GenerateReportParams"`）解析为实际 Pydantic 类：

```python
# executor.py
def _resolve_schema(module_path: str, schema_name: str) -> type:
    schema_mod = importlib.import_module(f"{module_path}.schemas")
    return getattr(schema_mod, schema_name)
```

## Handler Auto-Prefix

如果 handler 路径不含 `.`（如 `"generate_report"`），自动补为 `"tools.generate_report"`。
