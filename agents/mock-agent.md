# Mock Agent (Demo Mode)

## Purpose
Demo 模式下的 AI Provider。无需任何 API Key，通过关键词匹配模拟意图分类，用于展示全流程。

## File
`src/office_automation/ai/providers/mock_provider.py`

## How It Works

1. 用户输入自然语言指令
2. `_classify_intent()` 遍历 `INTENT_KEYWORDS` 列表
3. 按关键词命中率返回预设的模板 JSON
4. 模板参数已对齐各模块的 Pydantic schema

## Intent Keywords

| 关键词 | 命中模板 | 输出模块.动作 |
|--------|---------|-------------|
| 报表, 季度, 月报, 图表, excel表格, 生成, 表格, 销售 | `excel_generate_report` | `excel.generate_report` |
| 清洗数据, 脏数据, 去重, 数据清洗 | `excel_clean_data` | `excel.clean_data` |
| 发邮件, 发送邮件, 群发, 批量发送, 抄送, 邮件, 提醒, 发给 | `email_compose` | `email.compose_and_send` |
| 批量群发, 多收件人 | `email_batch_send` | `email.batch_send` |
| 模板填充, 入职通知, word模板, 批量生成文档, 合并文档, word, docx, 文档, 入职, 通知 | `document_fill_template` | `document.fill_template` |
| 批量文档, 批量生成 | `document_batch_generate` | `document.batch_generate` |
| 文件整理, 分类归档, 按类型, 按日期, 整理, 分类, 归档, 文件, 目录, 排序 | `file_organize` | `file_organizer.organize` |
| 重命名, 改名, 批量重命名 | `file_rename` | `file_organizer.rename_batch` |
| 清理文件, 清理目录, 清空, 临时文件 | `file_cleanup` | `file_organizer.cleanup` |

## Template Architecture

每个模板包含 `module`, `action`, `params` 三个字段，其中 `params` 的字段名和类型与对应模块的 Pydantic schema 完全一致。

模板示例（精简）：
```python
MOCK_TEMPLATES = {
    "excel_generate_report": {
        "module": "excel",
        "action": "generate_report",
        "params": {
            "title": "季度销售报表",
            "headers": ["月份", "销售额", "成本", "利润", "利润率"],
            "data": [["1月", 120000, 78000, 42000, "35%"], ...],
            "include_chart": True,
            "chart_type": "bar",
        },
    },
    # ... 8 个模板覆盖 4 个模块
}
```

## Priority Rules

1. **长尾/具体关键词优先**（如"模板填充" > "文档"）
2. **同一关键词出现在多个模板中时，列表靠前的胜出**
3. **全无命中时回退**到 `excel_generate_report`

## Usage

```bash
oa run "生成一份销售报表" --mode demo
# → excel.generate_report → 输出 .xlsx 文件
```
