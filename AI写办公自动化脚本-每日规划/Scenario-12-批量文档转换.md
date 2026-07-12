# Scenario 12: 批量文档转换
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
批量在不同文档格式间转换：CSV→Excel、TXT→Word、Docx→Txt。

## 痛点
- 收到 CSV 文件但需要 Excel 格式发给领导
- 多个 TXT 笔记需要合并成 Word 文档
- 格式转换工具质量参差不齐

## AI 参与方式
AI 理解转换需求 → 选择合适的转换工具 → 批量执行 → 检查结果

## 演示示例
```bash
oa run "把 data/sample/employees.csv 转换为 xlsx 格式"
```

## 核心命令
```bash
# Demo 模式
oa run --module converter --action batch_convert "把 data/sample/ 下的 csv 转为 xlsx"
oa run "把所有 txt 文件合并成一个 Word 文档"

# 支持的转换
# CSV → XLSX
# TXT → DOCX
# DOCX → TXT
```

## 交付物
- `data/output/converted_{filename}.xlsx` — 转换后的文件
- 批量转换报告
