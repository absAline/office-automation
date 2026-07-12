"""模块执行器 —— AI 指令分发、参数校验、动态调用模块工具函数"""

import importlib
import traceback
from pathlib import Path
from typing import Any

from office_automation.exceptions import (
    ModuleNotFoundError,
    ValidationError,
    ExecutionError,
)
from office_automation.modules.registry import get_module, is_registered
from office_automation.config import get_config
from office_automation.shared.utils import timestamp


# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------

def _resolve_handler(module_path: str, handler_path: str):
    """
    将字符串路径 "tools.generate_report" 解析为实际可调用对象。

    约定：handler_path 中最后一个 . 之后的部分为函数名，
         之前的部分（可为空或多级）为相对于 module_path 的子模块路径。

    示例
    ----
    _resolve_handler("office_automation.modules.excel", "tools.generate_report")
      → import office_automation.modules.excel.tools; return tools.generate_report
    _resolve_handler("...excel", "tools.charts.create_pie")
      → import ...excel.tools.charts; return charts.create_pie
    """
    if "." not in handler_path:
        handler_path = f"tools.{handler_path}"

    parts = handler_path.split(".")
    fn_name = parts[-1]
    sub_path = ".".join(parts[:-1])
    full_submodule = f"{module_path}.{sub_path}"

    try:
        submod = importlib.import_module(full_submodule)
    except ImportError as e:
        raise ExecutionError(f"无法加载子模块 {full_submodule}: {e}") from e

    handler_fn = getattr(submod, fn_name, None)
    if handler_fn is None:
        raise ExecutionError(
            f"子模块 {full_submodule} 中未找到函数 '{fn_name}'"
        )
    if not callable(handler_fn):
        raise ExecutionError(
            f"{full_submodule}.{fn_name} 不是可调用的函数"
        )

    return handler_fn


def _resolve_schema(module_path: str, schema_name: str) -> type:
    """
    将 schema 字符串名解析为实际的 Pydantic 模型类。

    例如 module_path="office_automation.modules.excel", schema_name="GenerateReportParams"
    → import office_automation.modules.excel.schemas → getattr(schemas, "GenerateReportParams")
    """
    try:
        schema_mod = importlib.import_module(f"{module_path}.schemas")
    except ImportError as e:
        raise ExecutionError(
            f"无法导入 schema 定义模块 ({module_path}.schemas): {e}"
        ) from e

    cls = getattr(schema_mod, schema_name, None)
    if cls is None:
        raise ExecutionError(
            f"Schema 类 '{schema_name}' 未在 {module_path}.schemas 中定义"
        )
    if not isinstance(cls, type):
        raise ExecutionError(f"'{schema_name}' 不是有效的类")

    return cls


def _validate_params(schema: type, params: dict) -> Any:
    """用 Pydantic schema 校验参数字典，返回模型实例。"""
    try:
        return schema(**params)
    except Exception as e:
        # 提取 Pydantic ValidationError 中的友好信息
        detail = str(e)
        raise ValidationError(f"参数校验失败 [{schema.__name__}]: {detail}") from e


def _call_handler(handler_fn, validated_params, output_base: str) -> dict:
    """
    调用 handler，将 Pydantic 模型解包为关键字参数；
    尝试传入 _output_base 辅助参数，若 handler 不接受则降级。
    """
    if validated_params is None:
        try:
            result = handler_fn(_output_base=output_base)
        except TypeError:
            result = handler_fn()
        return result

    params_dict = validated_params.model_dump()
    try:
        result = handler_fn(**params_dict, _output_base=output_base)
    except TypeError:
        result = handler_fn(**params_dict)
    return result


# ---------------------------------------------------------------------------
# 对外接口
# ---------------------------------------------------------------------------

def execute_module(module_name: str, action: str, params: dict) -> dict:
    """
    执行指定模块的指定动作。

    完整流程：
    1.  通过注册表查找模块
    2.  动态 import 模块包
    3.  从模块 __init__.py 中读取 HANDLERS 字典
    4.  用 Pydantic schema 校验参数
    5.  按 handler 字符串路径解析并加载实际函数
    6.  生成模块专属输出目录
    7.  调用 handler，收集结果

    参数
    ----
    module_name : str   – 已在注册表中的模块名，如 "excel"
    action : str        – HANDLERS 中注册的动作名，如 "generate_report"
    params : dict       – 对应 schema 所需字段的原始字典

    返回
    ----
    dict:
        成功 → {"success": True,  "output": "...", "files": [...], "module": ..., "action": ...}
        失败 → {"success": False, "error": "失败原因"}
    """
    # ---------- 1. 模块存在性检查 ----------
    if not is_registered(module_name):
        return {
            "success": False,
            "error": f"未注册的模块: '{module_name}'",
        }

    try:
        module_info = get_module(module_name)
    except ModuleNotFoundError as e:
        return {"success": False, "error": str(e)}

    # ---------- 2. 动态加载模块 ----------
    try:
        mod = importlib.import_module(module_info.module_path)
    except ImportError as e:
        return {
            "success": False,
            "error": f"加载模块 '{module_name}' 失败: {e}",
        }

    # ---------- 3. 获取 HANDLERS 注册表 ----------
    handlers: dict = getattr(mod, "HANDLERS", None)
    if handlers is None:
        return {
            "success": False,
            "error": f"模块 '{module_name}' 未定义 HANDLERS 注册表，"
                     f"请在 __init__.py 中添加 HANDLERS = {{...}}",
        }

    if action not in handlers:
        available = list(handlers.keys())
        return {
            "success": False,
            "error": f"模块 '{module_name}' 不支持动作 '{action}'，"
                     f"可用动作: {available}",
        }

    handler_info: dict = handlers[action]

    # ---------- 4. 参数校验 ----------
    schema_name = handler_info.get("schema")
    validated_params = None

    if schema_name is not None:
        try:
            schema = _resolve_schema(module_info.module_path, schema_name)
        except ExecutionError as e:
            return {"success": False, "error": str(e)}

        try:
            validated_params = _validate_params(schema, params)
        except ValidationError as e:
            return {
                "success": False,
                "error": str(e),
                "params": params,
                "schema": schema_name,
            }

    # ---------- 5. 解析 handler 函数 ----------
    handler_path = handler_info.get("handler")
    if not handler_path:
        return {
            "success": False,
            "error": f"动作 '{action}' 未定义 handler 路径",
        }

    try:
        handler_fn = _resolve_handler(module_info.module_path, handler_path)
    except ExecutionError as e:
        return {"success": False, "error": str(e)}

    # ---------- 6. 生成输出路径 ----------
    output_dir = Path(get_config().output_dir) / module_name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_base = str(output_dir / f"{action}_{timestamp()}")

    # ---------- 7. 执行 ----------
    try:
        result = _call_handler(handler_fn, validated_params, output_base)
    except Exception as e:
        return {
            "success": False,
            "error": f"执行失败: {e}",
            "traceback": traceback.format_exc(),
        }

    # ---------- 8. 构建返回 ----------
    if isinstance(result, dict):
        output_msg = result.get("message") or result.get("output") or "执行成功"
        files = result.get("files", [])
        # 其余字段放入 data
        extra = {
            k: v
            for k, v in result.items()
            if k not in ("message", "output", "files")
        }
    else:
        output_msg = str(result) if result is not None else "执行成功"
        files = []
        extra = {}

    response: dict[str, Any] = {
        "success": True,
        "output": output_msg,
        "files": files,
        "module": module_name,
        "action": action,
    }
    if extra:
        response["data"] = extra

    return response
