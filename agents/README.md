# AutoOffice Agent System

AutoOffice 使用 **AI Agent** 架构：用户输入自然语言 → Agent 分类意图 → 模块执行器调用工具函数 → 返回结果。

## Architecture

```
User Input ("生成一份销售报表")
        │
        ▼
┌─────────────────────────────────┐
│         Intent Classifier        │  ← AI Agent (Mock / OpenAI / Ollama / 通义千问)
│  输出: {"module":"excel",        │
│         "action":"generate_report",
│         "params":{...}}          │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│         Module Executor          │  ← executor.py
│  1. 查注册表 → 找到模块          │
│  2. 加载 schema → 校验参数       │
│  3. 调用 handler → 执行工具函数   │
│  4. 返回结果                     │
└──────────────┬──────────────────┘
               │
               ▼
        excel/tools.py
        generate_report()
        → 生成 report_xxx.xlsx
```

## Available Agents

| Agent | Type | Mode | API Key Required |
|-------|------|------|------------------|
| [Mock](mock-agent.md) | Keyword matching | `demo` | No |
| [OpenAI](openai-agent.md) | OpenAI SDK compatible | `real` | Yes (OPENAI_API_KEY) |
| [Ollama](ollama-agent.md) | Local LLM (ollama) | `real` | No |
| [通义千问](tongyi-agent.md) | DashScope API | `real` | Yes (DASHSCOPE_API_KEY) |

## Flow

1. **CLI** (`oa run "..."`) 接收用户输入
2. **AI Provider** 分析意图，返回结构化 JSON
3. **Executor** 解析 JSON → 通过注册表定位模块 → 校验参数 → 调用工具函数
4. **工具函数** 执行真实操作（创建 Excel / 发送邮件 / 填充文档 / 整理文件）
5. **结果** 返回给用户（输出文件路径、成功/失败信息）

## Configuration

See [.env.example](../.env.example) for all environment variables.
