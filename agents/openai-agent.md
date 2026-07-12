# OpenAI Agent (Real Mode)

## Purpose
Real 模式下使用 OpenAI 兼容接口进行意图分类。支持 OpenAI、DeepSeek、Moonshot、硅基流动 (SiliconFlow) 等所有兼容 OpenAI SDK 的服务。

## File
`src/office_automation/ai/providers/openai_provider.py`

## Implementation

```python
class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, api_url: str, model: str):
        self.model = model
        url = api_url.rstrip("/")
        if "/chat/completions" in url:
            url = url.split("/chat/completions")[0]
        if not url.endswith("/v1"):
            url = url + "/v1"
        self.client = AsyncOpenAI(api_key=api_key, base_url=url)
```

### URL Normalization

支持三种输入格式，自动规整：

| 输入 | 规整后 |
|------|--------|
| `https://api.openai.com/v1` | `https://api.openai.com/v1/` |
| `https://api.openai.com/v1/chat/completions` | `https://api.openai.com/v1/` |
| `https://api.siliconflow.cn` | `https://api.siliconflow.cn/v1/` |

## Configuration

```env
# OpenAI / DeepSeek / Moonshot / SiliconFlow 等
OPENAI_API_KEY=sk-xxxx
OPENAI_API_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### 常用服务配置

| 服务 | API URL | 推荐 Model |
|------|---------|-----------|
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| 硅基流动 | `https://api.siliconflow.cn/v1` | `Qwen/Qwen2.5-7B-Instruct` |
| Moonshot | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |

## How It Works

1. CLI 构造 system prompt（包含可用模块列表 + JSON 格式要求）
2. 将用户输入 + system prompt 发送给 Provider
3. Provider 返回 JSON：`{"module": "...", "action": "...", "params": {...}}`
4. CLI 解析 JSON 后传给 Executor

## Usage

```bash
# 配置 .env
echo 'OPENAI_API_KEY=sk-xxx' >> .env

# 运行（自动检测到 API Key，使用 real 模式）
oa run "给全体员工发送春节放假通知"

# 或显式指定模式
oa run "..." --mode real
```

## Error Handling

- API 调用失败 → 抛出 `AIProviderError`，CLI 展示错误信息
- JSON 解析失败 → CLI 回退到默认模板 `excel.generate_report`
- 流式模式异常 → 正常截断，不阻塞
