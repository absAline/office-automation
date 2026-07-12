# Ollama Agent (Local)

## Purpose
Real 模式下使用本地部署的 Ollama 模型进行意图分类。无需 API Key，完全本地运行。

## Prerequisites

```bash
# 安装 Ollama
brew install ollama

# 启动服务
ollama serve

# 拉取模型（推荐）
ollama pull qwen2.5:7b

# 验证
curl http://localhost:11434/api/tags
```

## File
`src/office_automation/ai/providers/ollama_provider.py`

## Implementation

使用 Ollama `/api/chat` 接口（支持原生 messages 格式），不依赖第三方 SDK：

```python
class OllamaProvider(AIProvider):
    async def chat(self, messages: list[dict], **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,  # 原生消息格式
                    "stream": False,
                    "options": {"temperature": 0.7},
                },
            )
            data = resp.json()
            return data.get("message", {}).get("content", "")
```

### 与旧版 `/api/generate` 的区别

| | `/api/generate` (旧) | `/api/chat` (当前) |
|---|---|---|
| 输入格式 | 单 prompt 字符串 | 标准 messages 列表 |
| 需手动拼 prompt | 是 (`_build_prompt()`) | 否 |
| 多轮对话 | 手动拼接历史 | 自动支持 |
| System prompt | 拼入 prompt 开头 | 原生 role=system |

## Configuration

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

## Usage

```bash
# 确保 Ollama 已启动
ollama serve

# AutoOffice 会自动检测并使用（无 OPENAI_API_KEY 时）
oa run "按日期整理下载文件夹" --mode real

# 或显式指定
oa run "..." --mode real
```

## Known Models

| 模型 | RAM 要求 | 推荐场景 |
|------|---------|---------|
| `qwen2.5:7b` | 8GB | 意图分类，中文效果好 |
| `qwen2.5:3b` | 4GB | 轻量分类 |
| `llama3.2:3b` | 4GB | 英文场景 |
| `deepseek-r1:7b` | 8GB | 推理能力更强 |

## Limitations

- 首次加载模型需等待（~10-30s 取决于模型大小）
- JSON 输出格式不稳定 → CLI 有解析失败回退逻辑
- 流式模式下每个 token 为单独一行 JSON
