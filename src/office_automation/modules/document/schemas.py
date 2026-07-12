"""文档模块 — Pydantic 参数模型"""
from pydantic import BaseModel, Field


class FillTemplateParams(BaseModel):
    """填充 Word 模板参数"""
    template: str = Field(default="", description="Word 模板文件路径（.docx）")
    data_source: str = Field(default="", description="数据源路径：JSON 文件或 CSV 文件")
    output_pattern: str = Field(default="filled_{index}.docx", description="输出文件名模式，{index} 为序号")
    fields: dict = Field(default_factory=dict, description="要填充的字段及值 {placeholder: value}")


class BatchGenerateParams(BaseModel):
    """批量生成文档参数"""
    template: str = Field(default="", description="Word 模板文件路径")
    data_source: str = Field(default="", description="CSV 或 JSON 数据源文件路径")
    output_pattern: str = Field(default="doc_{row}.docx", description="输出文件名模式")
    output_dir: str = Field(default="", description="输出目录，空则默认 data/output/")
