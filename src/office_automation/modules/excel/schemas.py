"""Excel 模块 — Pydantic 参数模型"""
from typing import Any
from pydantic import BaseModel, Field


class GenerateReportParams(BaseModel):
    """生成报表参数"""
    title: str = Field(default="报表", description="报表标题")
    sheet_name: str = Field(default="Sheet1", description="工作表名称")
    headers: list[str] = Field(default_factory=list, description="表头列名列表")
    data: list[list[Any]] = Field(default_factory=list, description="数据行，每行是一个列表")
    include_chart: bool = Field(default=False, description="是否包含图表")
    chart_type: str = Field(default="bar", description="图表类型：bar / line / pie")
    style: str = Field(default="professional", description="表头样式：professional / simple / colorful")


class CleanDataParams(BaseModel):
    """数据清洗参数"""
    source_path: str = Field(default="", description="源 Excel 文件路径")
    sheet_name: str = Field(default="Sheet1", description="要清洗的工作表")
    remove_duplicates: bool = Field(default=True, description="是否去重")
    fill_empty: str = Field(default="", description="空值填充内容，空字符串表示跳过")
    trim_whitespace: bool = Field(default=True, description="是否去除首尾空白")
    drop_empty_rows: bool = Field(default=True, description="是否删除全空行")
    output_filename: str = Field(default="cleaned_data.xlsx", description="输出文件名")


class MergeSheetsParams(BaseModel):
    """合并工作表参数"""
    source_path: str = Field(default="", description="源 Excel 文件路径")
    sheet_names: list[str] = Field(default_factory=list, description="要合并的工作表名称列表，空表示全部")
    include_header: bool = Field(default=True, description="合并后是否保留表头")
    add_source_column: bool = Field(default=False, description="是否添加来源列标识")
    output_filename: str = Field(default="merged_sheets.xlsx", description="输出文件名")
