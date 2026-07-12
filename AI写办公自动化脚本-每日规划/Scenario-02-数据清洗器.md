# Scenario 02: 数据清洗器
> **实现状态**: ⚠️ 部分实现 — `excel/` 模块有基础工具函数，完整清洗流水线待补充

## 场景描述
AI 自动识别脏数据（空值、异常值、格式不一致），生成清洗规则并执行。

## 痛点
- 从多个系统导出的数据格式不统一
- 数据中有空值、异常值需要手动处理
- 日期格式、数字格式乱七八糟

## AI 参与方式
AI 分析数据特征 → 识别脏数据类型 → 推荐清洗规则 → 用户确认 → 执行清洗

## 演示示例
```bash
oa run "清理 data/sample/sales_data_messy.xlsx 中的异常值"
```

## 核心命令
```bash
# Demo 模式
oa run "清洗这份销售数据，把空值和异常值去掉"
oa run "把销售额列中的负数和文本值标记出来"

# 指定模块
oa run --module excel --action clean_data "清洗数据"
```

## 交付物
- `data/output/cleaned_data.xlsx` — 清洗后的数据
- `data/output/cleaning_report.json` — 清洗报告（记录修改内容）
