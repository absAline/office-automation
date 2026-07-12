"""邮件模块 — Pydantic 参数模型"""
from pydantic import BaseModel, Field


class ComposeParams(BaseModel):
    """撰写并发送邮件参数"""
    to: str = Field(default="", description="收件人邮箱地址")
    subject: str = Field(default="", description="邮件主题")
    body: str = Field(default="", description="邮件正文（支持纯文本或简单 HTML）")
    cc: str = Field(default="", description="抄送，多个用英文逗号分隔")
    bcc: str = Field(default="", description="密送，多个用英文逗号分隔")
    attachments: list[str] = Field(default_factory=list, description="附件文件路径列表")
    template_path: str = Field(default="", description="HTML 模板文件路径")
    template_vars: dict = Field(default_factory=dict, description="模板变量替换 {key: value}")
    save_draft: bool = Field(default=True, description="是否保存草稿（demo 模式强制保存）")


class BatchSendParams(BaseModel):
    """批量发送邮件参数"""
    recipients: list[dict] = Field(
        default_factory=list,
        description="收件人列表，每项含 email/name/vars 字段",
    )
    subject_template: str = Field(default="", description="主题模板，支持 {name} 等变量")
    body_template: str = Field(default="", description="正文模板，支持格式化变量")
    attachments: list[str] = Field(default_factory=list, description="公共附件路径列表")
    delay_seconds: float = Field(default=1.0, description="每封邮件之间的发送间隔（秒）")
