# Scenario 08: 发票处理器
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
从 PDF/文本发票中提取关键信息（发票号、日期、金额、供应商），批量生成费用报表。

## 痛点
- 月底报销手动录入发票信息
- 发票数据不一致难以核对
- 多张发票汇总到一张报表费时

## AI 参与方式
AI 解析发票文本 → 提取结构化字段 → 校验金额一致性 → 生成费用报表

## 演示示例
```bash
oa run "处理 data/sample/invoices 目录下的发票文件"
```

## 核心命令
```bash
# Demo 模式
oa run "处理这批发票数据，生成费用报销报表"
oa run --module invoice --action process "提取所有发票的金额和供应商"
```

## 交付物
- `data/output/expense_report.xlsx` — 费用报表
- `data/output/invoice_validated.json` — 校验结果

## 支持格式
- 文本发票 (.txt)
- PDF 发票（需要 pdfplumber）
