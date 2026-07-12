"""全局配置 — 纯 Demo 模式"""

from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

_config = SimpleNamespace(
    mode="demo",
    data_dir=str(PROJECT_ROOT / "data"),
    output_dir=str(PROJECT_ROOT / "data" / "output"),
    template_dir=str(PROJECT_ROOT / "data" / "templates"),
    sample_dir=str(PROJECT_ROOT / "data" / "sample"),
)


def get_config():
    return _config