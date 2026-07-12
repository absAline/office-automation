# Scenario 11: Excel 公式生成器
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
AI 根据自然语言描述生成 Excel 公式，批量应用到现有表格。

## 痛点
- Excel 公式语法记不住
- 复杂的嵌套公式（IF/VLOOKUP/SUMIFS）难写
- 批量给已有报表添加公式列

## AI 参与方式
AI 理解计算需求 → 生成正确的 Excel 公式 → 写入指定单元格

## 演示示例
```bash
oa run "给销售报表加一列利润率公式（利润/销售额）"
```

## 核心命令
```bash
# Demo 模式
oa run "给报表加上利润率列，公式为利润除以销售额"
oa run "在最后一列加一个合计公式"
oa run --module formula --action create_formulas "添加上月环比增长率"

# 支持的公式类型
# =SUM(), =AVERAGE(), =IF(), =VLOOKUP(), =XLOOKUP()
# =SUMIFS(), =COUNTIF(), 自定义运算等
```

## 交付物
- 更新后的 Excel 文件（含公式）
- `data/output/formula_report.json` — 公式清单
