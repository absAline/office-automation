"""通用校验器"""

import re
from pathlib import Path
from typing import Any


def validate_file_exists(path: str | Path) -> Path:
    """校验文件存在"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {p}")
    return p


def validate_email(email: str) -> str:
    """校验邮箱格式"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError(f"无效的邮箱地址: {email}")
    return email


def validate_output_path(path: str | Path) -> Path:
    """校验输出路径可写"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
