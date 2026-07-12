# Scenario 13: 自动化流水线
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
将多个自动化步骤链式组合成一个流水线，数据从前一步传递到后一步。

## 痛点
- 日常工作包含多个连续步骤（提取→处理→产出→发送）
- 每个步骤单独执行效率低
- 需要可重复执行的自动化流程

## AI 参与方式
AI 理解多步流程需求 → 分解为原子步骤 → 串联执行 → 数据传递

## 演示示例
```bash
oa run "创建一个流水线：提取产品数据，生成分析报表，通过邮件发送给团队"
```

## 核心命令
```bash
# Demo 模式
oa run --module pipeline --action create "创建日报流水线：提取数据→生成报表→发送邮件"
oa run "创建一个每周自动执行的流水线：爬取竞品价格→生成对比表→邮件群发"

# 查看流水线
oa run --module pipeline --action list "列出所有流水线"
```

## 流水线示例
```
步骤1: data_extraction.extract → 提取产品数据 → 输出 CSV
步骤2: excel.generate_report → 生成对比报表 → 输出 XLSX
步骤3: email.compose_and_send → 附件发送 → 输出发送确认
```

## 交付物
- `data/pipelines/{name}.json` — 流水线配置
- 流水线执行日志
