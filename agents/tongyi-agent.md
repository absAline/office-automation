# 通义千问 Agent (DashScope)

## Purpose
Real 模式下使用阿里云 DashScope 通义千问模型进行意图分类。

## Prerequisites

```bash
# 申请 API Key
# https://dashscope.aliyun.com
```

## File
`src/office_automation/ai/providers/tongyi_provider.py`

## Implementation

```python
class TongyiProvider(AIProvider):
    API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    async def chat(self, messages: list[dict], **kwargs) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.API_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "input": {"messages": messages},
                    "parameters": {
                        "result_format": "message",
                        "temperature": kwargs.get("temperature", 0.7),
                    },
                },
            )
            data = resp.json()
            return data["output"]["choices"][0]["message"]["content"]
```

## Configuration

```env
DASHSCOPE_API_KEY=sk-xxxx
TONGYI_MODEL=qwen2.5-7b-instruct
```

## Usage

```bash
# 配置 API Key
echo 'DASHSCOPE_API_KEY=sk-xxx' >> .env

# 运行
oa run "给销售团队发送季度报表" --mode real
```

## Available Models

| 模型 | 说明 |
|------|------|
| `qwen2.5-7b-instruct` | 推荐，性价比高 |
| `qwen2.5-14b-instruct` | 效果更好，成本更高 |
| `qwen2.5-72b-instruct` | 最强效果 |

## API Details

- 端点: `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
- 认证: Bearer Token（`Authorization: Bearer sk-xxx`）
- 流式: 支持 SSE 逐行输出 (`incremental_output: true`)
- 限频: 免费用户 100 次/天，付费用户按量计费
