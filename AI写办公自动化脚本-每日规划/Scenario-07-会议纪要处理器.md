# Scenario 07: 会议纪要处理器
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
AI 自动解析会议纪要文本，提取待办事项、关键决策、时间节点。

## 痛点
- 会议纪要写完了还要手动整理待办项
- 容易遗漏会议中提到的关键决定
- 待办事项没有截止日期跟踪

## AI 参与方式
AI 解析会议纪要文本 → 识别 "待办"/"TODO"/"- [ ]" 等标记 → 提取决策 → 结构化输出

## 演示示例
```bash
oa run "处理 data/sample/meeting_notes.txt，提取待办事项和决定"
```

## 核心命令
```bash
# Demo 模式
oa run "处理今天的项目会议纪要，生成待办清单"
oa run --module meeting_notes --action process "提取会议中的关键决定"

# 输出为 Markdown
oa run "把会议纪要整理成 Markdown 格式输出"
```

## 交付物
- `data/output/action_items.md` — 待办清单
- `data/output/meeting_summary.md` — 会议摘要
- `data/output/meeting_decisions.json` — 关键决定

## 解析规则
- 关键词匹配: "TODO:", "待办:", "决定:", "- [ ]"
- 自动提取: 负责人、截止日期、任务描述
