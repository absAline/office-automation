# Scenario 10: 文本摘要与翻译
> **实现状态**: ❌ 规划中 — 对应代码模块尚未实现

## 场景描述
AI 自动总结长文档生成摘要，支持中英文互译，提取关键信息。

## 痛点
- 英文技术文档读起来费劲
- 长篇报告需要快速了解核心内容
- 需要提取文档关键词做标签

## AI 参与方式
AI 读取源文件 → 理解内容 → 生成摘要 / 翻译 → 输出到目标文件

## 演示示例
```bash
oa run "总结 data/sample/report_en.md 并翻译成中文"
```

## 核心命令
```bash
# Demo 模式
oa run "总结这份报告，输出三点核心内容"
oa run "把这份英文文档翻译成中文"

# 提取关键词
oa run --module text_processor --action extract_keywords "提取这份报告的关键词"
```

## 交付物
- `data/output/summary_zh.md` — 中文摘要
- `data/output/translated.md` — 翻译结果
- `data/output/keywords.json` — 关键词列表
