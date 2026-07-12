"""通用工具函数"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    """确保目录存在"""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_json(data: Any, path: str | Path) -> Path:
    """保存 JSON 文件"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def load_json(path: str | Path) -> Any:
    """加载 JSON 文件"""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def timestamp() -> str:
    """返回当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def output_path(filename: str) -> Path:
    """生成输出目录下的文件路径"""
    from office_automation.config import get_config
    out_dir = Path(get_config().output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename
