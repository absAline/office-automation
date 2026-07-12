# Scenario 01: Excel 报表生成器
> **实现状态**: ✅ 已实现 — `excel/` 模块，支持 create_workbook, add_chart, 样式设置

## 场景描述
用自然语言描述报表需求 → AI 自动生成格式化 Excel 报表，支持图表和数据清洗。

## 痛点
- 月底做报表手动复制粘贴费时费力
- 不会写 Excel 公式，数据汇总靠手工加总
- 报表格式不统一，每次都要调样式

## AI 参与方式
输入自然语言 → MockProvider/真实 AI 解析意图 → 输出结构化 JSON 参数 → 工具函数执行 → 生成 .xlsx 文件

## 演示示例
```bash
oa run "生成季度销售报表，包含收入、成本、利润和图表"
```

## 核心命令
```bash
# Demo 模式（无需 API Key）
oa run "生成季度销售报表"
oa run "帮我生成一份上半年各月销售趋势的报表，加上折线图"

# 指定模块
oa run --module excel --action generate_report "生成报表"

# 真实 AI 模式（需配置 .env）
oa run --mode real "用这份销售数据生成一份分析报表"
```

## 交付物
- `data/output/sales_report.xlsx` — 格式化 Excel 报表
- 支持样式: professional / simple / colorful
- 支持图表: bar / line / pie

## 脚本说明
- `excel/tools.py`: create_workbook(), add_sheet(), format_header(), add_data_rows(), add_chart(), save()
- `excel/schemas.py`: GenerateReportParams, CleanDataParams, MergeSheetsParams
