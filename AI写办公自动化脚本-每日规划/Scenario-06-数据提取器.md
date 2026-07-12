# Scenario 06: 数据提取器
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
从网页 HTML 或文本文件中提取结构化数据，导出为 CSV 或 JSON。

## 痛点
- 手动从网页复制数据到表格效率低
- 需要定期监控竞品价格
- 从大量文档中提取特定字段

## AI 参与方式
AI 理解要提取的字段 → 分析页面结构 → 定位数据位置 → 提取并格式化导出

## 演示示例
```bash
oa run "从 data/sample/products.html 提取商品名称、价格和评分"
```

## 核心命令
```bash
# Demo 模式（从 sample HTML 提取）
oa run "提取 data/sample/products.html 中的商品信息"
oa run "把产品列表中的价格和销量数据导出为 CSV"

# Real 模式（真实爬取）
oa run --mode real "抓取 https://example.com/products 的商品信息"
```

## 交付物
- `data/output/extracted_data.csv` — 结构化数据
- `data/output/extracted_data.json` — JSON 格式

## 支持格式
- HTML 表格提取
- 列表页数据提取
- 纯文本字段提取
