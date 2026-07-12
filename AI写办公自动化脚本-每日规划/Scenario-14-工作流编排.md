# Scenario 14: 工作流编排
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
最终章：编排多步骤自动化工作流，支持定时执行和状态监控。

## 痛点
- 复杂的业务流程涉及多个工具和系统
- 需要定时执行但不能写 crontab
- 工作流执行状态需要可视化跟踪

## AI 参与方式
AI 理解完整业务流程 → 分解工作流步骤 → 配置执行计划 → 监控执行状态

## 演示示例
```bash
oa run "编排一个工作流：每周一早上自动从数据库提取销售数据，生成报表，通过邮件发送给管理层"
```

## 核心命令
```bash
# Demo 模式
oa run --module workflow --action orchestrate "每天下班前备份数据并发送状态报告"
oa run "每周五生成项目周报，邮件发送给所有项目成员"

# 查看工作流状态
oa run --module workflow --action status "查看所有工作流状态"

# 执行工作流
oa run --module workflow --action execute "立即执行周报工作流"
```

## 工作流示例
```
名称: 每周销售报告
触发: 每周一 09:00
步骤:
  1. 连接数据库 → 执行 SQL
  2. 数据导出为 CSV
  3. 生成 Excel 图表报表
  4. 邮件发送给管理层
  5. 记录执行日志
```

## 交付物
- `data/workflows/configs/` — 工作流配置
- `data/workflows/logs/` — 执行日志
- `data/workflows/reports/` — 执行报告
