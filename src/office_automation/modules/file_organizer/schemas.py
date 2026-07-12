"""文件整理模块 — Pydantic 参数模型"""
from pydantic import BaseModel, Field


class OrganizeParams(BaseModel):
    """文件整理/分类参数"""
    target_dir: str = Field(default="", description="要整理的目标目录")
    scheme: str = Field(default="by_type", description="分类方案：by_type / by_name / by_date / by_size")
    categories: dict = Field(default_factory=dict, description="自定义分类规则，如 {'图片': ['.jpg', '.png', '.gif']}")
    dry_run: bool = Field(default=True, description="预览模式，不实际移动文件")
    exclude_patterns: list[str] = Field(default_factory=list, description="排除的文件模式，如 ['*.tmp', '.DS_Store']")


class RenameParams(BaseModel):
    """批量重命名参数"""
    target_dir: str = Field(default="", description="要重命名的目标目录")
    pattern: str = Field(default=r"old_(.*)\.txt", description="匹配的正则表达式模式")
    replacement: str = Field(default=r"new_\1.txt", description="替换模板（支持正则分组 \\1, \\2...）")
    dry_run: bool = Field(default=True, description="预览模式")
    include_extensions: list[str] = Field(default_factory=list, description="限定处理的文件扩展名，空=所有")


class CleanupParams(BaseModel):
    """文件清理参数"""
    target_dir: str = Field(default="", description="要清理的目标目录")
    remove_empty_dirs: bool = Field(default=True, description="是否删除空目录")
    remove_empty_files: bool = Field(default=True, description="是否删除空文件（0字节）")
    remove_temp_files: bool = Field(default=True, description="是否删除临时文件（.tmp .bak ~ 结尾）")
    dry_run: bool = Field(default=True, description="预览模式")
    older_than_days: int = Field(default=0, description="只删除 N 天前的文件，0=不限")
