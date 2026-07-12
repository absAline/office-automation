# Scenario 03: 文档模板填充
> **实现状态**: ✅ 已实现 — `document/` 模块，支持模板加载、文本替换

## 场景描述
用 AI 从数据源（CSV/Excel）读取数据，自动填充 Word 文档模板，批量生成文档。

## 痛点
- 入职通知、合同、证明信等批量文档重复劳动
- 从 Excel 复制数据到 Word 容易出错
- 模板更新后所有文档要重新调整

## AI 参与方式
AI 分析模板结构和数据源 → 智能字段映射 → 批量填充 → 生成文档

## 演示示例
```bash
oa run "用 data/sample/employees.csv 的数据填充入职通知模板"
```

## 核心命令
```bash
# Demo 模式
oa run "用员工数据批量生成入职通知"
oa run --module document --action fill_template "填充模板"
```

## 交付物
- `data/output/入职通知_张三.docx` 等批量文档
- 支持: Word (.docx) 模板填充

## 依赖
```bash
pip install python-docx
```
