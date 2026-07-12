"""Mock Provider — Demo 模式，无需任何 API Key"""

import json
import asyncio
from pathlib import Path
from typing import AsyncIterator, Optional
from office_automation.ai.base import AIProvider

# 场景对应的 Mock 响应模板（与实际 schema 字段一致）
MOCK_TEMPLATES: dict[str, dict] = {
    "excel_generate_report": {
        "module": "excel",
        "action": "generate_report",
        "params": {
            "title": "季度销售报表",
            "sheet_name": "销售数据",
            "headers": ["月份", "销售额", "成本", "利润", "利润率"],
            "data": [
                ["1月", 120000, 78000, 42000, "35%"],
                ["2月", 158000, 95000, 63000, "40%"],
                ["3月", 185000, 110000, 75000, "41%"],
            ],
            "include_chart": True,
            "chart_type": "bar",
            "style": "professional",
        },
    },
    "excel_clean_data": {
        "module": "excel",
        "action": "clean_data",
        "params": {
            "source_path": "",
            "sheet_name": "Sheet1",
            "remove_duplicates": True,
            "fill_empty": "N/A",
            "trim_whitespace": True,
            "drop_empty_rows": True,
            "output_filename": "cleaned_data.xlsx",
        },
    },
    "email_compose": {
        "module": "email",
        "action": "compose_and_send",
        "params": {
            "to": "wangjingli@company.com",
            "subject": "明天项目会议提醒",
            "body": "王经理您好，\n\n提醒您明天下午 2:00 在 3 楼会议室召开项目评审会，请提前准备 Q2 项目进展报告。\n\n此致\n敬礼",
            "cc": "",
            "bcc": "",
            "attachments": [],
            "template_path": "",
            "template_vars": {},
            "save_draft": True,
        },
    },
    "email_batch_send": {
        "module": "email",
        "action": "batch_send",
        "params": {
            "recipients": [
                {"email": "alice@company.com", "name": "Alice"},
                {"email": "bob@company.com", "name": "Bob"},
            ],
            "subject_template": "月度报表通知 - {name}",
            "body_template": "Hi {name}，请查收附件中的月度报表。",
            "attachments": [],
            "delay_seconds": 0.5,
        },
    },
    "document_fill_template": {
        "module": "document",
        "action": "fill_template",
        "params": {
            "template": "",
            "data_source": "",
            "output_pattern": "filled_{index}.docx",
            "fields": {
                "姓名": "张三",
                "部门": "技术部",
                "入职日期": "2026-06-01",
                "岗位": "高级工程师",
            },
        },
    },
    "document_batch_generate": {
        "module": "document",
        "action": "batch_generate",
        "params": {
            "template": "",
            "data_source": "",
            "output_pattern": "doc_{row}.docx",
            "output_dir": "",
        },
    },
    "file_organize": {
        "module": "file_organizer",
        "action": "organize",
        "params": {
            "target_dir": "data/sample",
            "scheme": "by_type",
            "categories": {
                "文档": [".pdf", ".docx", ".txt"],
                "表格": [".xlsx", ".csv"],
                "图片": [".jpg", ".png"],
                "压缩包": [".zip"],
            },
            "dry_run": True,
            "exclude_patterns": [".DS_Store", "*.tmp"],
        },
    },
    "file_rename": {
        "module": "file_organizer",
        "action": "rename_batch",
        "params": {
            "target_dir": "data/sample",
            "pattern": r"(.*)\.(.+)",
            "replacement": r"backup_\1.\2",
            "dry_run": True,
            "include_extensions": [],
        },
    },
    "file_cleanup": {
        "module": "file_organizer",
        "action": "cleanup",
        "params": {
            "target_dir": "data/sample",
            "remove_empty_dirs": True,
            "remove_empty_files": True,
            "remove_temp_files": True,
            "dry_run": True,
            "older_than_days": 0,
        },
    },
}

# 意图分类关键词（只保留 4 个存活模块）
INTENT_KEYWORDS: list[tuple[list[str], str]] = [
    # document first (more specific before general)
    (["模板填充", "入职通知", "word模板", "批量生成文档", "合并文档"], "document_fill_template"),
    (["批量文档", "批量生成"], "document_batch_generate"),
    # file operations
    (["文件整理", "分类归档", "按类型", "按日期"], "file_organize"),
    (["重命名", "改名", "批量重命名"], "file_rename"),
    (["清理文件", "清理目录", "清空", "临时文件"], "file_cleanup"),
    # excel
    (["报表", "销售报表", "季度", "月报", "年报", "图表", "excel表格"], "excel_generate_report"),
    (["清洗数据", "脏数据", "去重", "数据清洗"], "excel_clean_data"),
    # email
    (["发邮件", "发送邮件", "群发", "批量发送", "抄送"], "email_compose"),
    (["批量群发", "多收件人"], "email_batch_send"),
    # fallback generic
    (["生成", "表格", "excel", "报表", "制作"], "excel_generate_report"),
    (["文档", "word", "docx", "模板", "填充", "入职", "通知"], "document_fill_template"),
    (["邮件", "发送", "提醒", "发给", "收件人"], "email_compose"),
    (["整理", "分类", "归档", "文件", "目录", "排序"], "file_organize"),
]


class MockProvider(AIProvider):
    """Mock Provider — 根据意图关键词返回对应模板"""

    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates = MOCK_TEMPLATES

    async def chat(self, messages: list[dict], **kwargs) -> str:
        """根据用户输入匹配意图，返回对应模板 JSON"""
        user_msg = self._get_last_user_message(messages)
        template_key = self._classify_intent(user_msg)
        template = self.templates.get(template_key, self.templates["excel_generate_report"])
        return json.dumps(template, ensure_ascii=False)

    async def stream(self, messages: list[dict], **kwargs) -> AsyncIterator[str]:
        """模拟流式输出"""
        response = await self.chat(messages, **kwargs)
        for chunk in _chunk_string(response, 20):
            await asyncio.sleep(0.05)
            yield chunk

    def _get_last_user_message(self, messages: list[dict]) -> str:
        """提取最后一条用户消息"""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                return msg.get("content", "")
        return ""

    def _classify_intent(self, text: str) -> str:
        """通过关键词匹配分类意图"""
        text_lower = text.lower()
        for keywords, intent_key in INTENT_KEYWORDS:
            if any(kw in text_lower for kw in keywords):
                return intent_key
        return "excel_generate_report"


def _chunk_string(text: str, size: int) -> list[str]:
    """将字符串分块"""
    return [text[i:i + size] for i in range(0, len(text), size)]
