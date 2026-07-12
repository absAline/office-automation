"""邮件模块 — 核心工具函数

在 demo 模式下：邮件内容保存为草稿文件到 data/output/，不实际发送。
真实发送需配置 SMTP 环境变量并设置 OA_MODE=real。
"""
import os
import json
from pathlib import Path
from office_automation.shared.utils import output_path, timestamp


def _get_smtp_config() -> dict:
    """获取 SMTP 配置"""
    return {
        "host": os.getenv("SMTP_HOST", "smtp.qq.com"),
        "port": int(os.getenv("SMTP_PORT", "465")),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "from_addr": os.getenv("SMTP_FROM", ""),
    }


def _is_demo_mode() -> bool:
    """检查是否为 demo 模式"""
    from office_automation.config import get_config
    return get_config().mode == "demo"


def _format_template(text: str, variables: dict) -> str:
    """用变量填充模板文本"""
    if not variables:
        return text
    result = text
    for key, val in variables.items():
        result = result.replace(f"{{{key}}}", str(val))
    return result


def _save_draft(to: str, subject: str, body: str, cc: str = "", attachments: list = None) -> dict:
    """保存邮件草稿为文本文件"""
    filename = f"email_draft_{timestamp()}.txt"
    draft_path = output_path(filename)
    content_parts = [
        f"To: {to}",
        f"Subject: {subject}",
    ]
    if cc:
        content_parts.append(f"CC: {cc}")
    content_parts.append("")
    content_parts.append(body)
    if attachments:
        content_parts.append("")
        content_parts.append("--- Attachments ---")
        for att in attachments:
            content_parts.append(f"  {att}")

    draft_path.write_text("\n".join(content_parts), encoding="utf-8")
    return {"success": True, "message": f"草稿已保存", "files": [str(draft_path)]}


def _send_real(to: str, subject: str, body: str, cc: str = "", bcc: str = "", attachments: list = None) -> dict:
    """通过 SMTP 真实发送邮件"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    config = _get_smtp_config()
    if not config["user"] or not config["password"]:
        return {"success": False, "error": "SMTP 未配置，请设置 SMTP_USER / SMTP_PASSWORD 环境变量"}

    msg = MIMEMultipart()
    msg["From"] = config["from_addr"] or config["user"]
    msg["To"] = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc

    is_html = "<html" in body.lower() or "<body" in body.lower()
    msg.attach(MIMEText(body, "html" if is_html else "plain", "utf-8"))

    # 附件
    attachments = attachments or []
    for att_path in attachments:
        p = Path(att_path)
        if not p.exists():
            continue
        with open(p, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{p.name}"')
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(config["host"], config["port"], timeout=30)
        server.login(config["user"], config["password"])
        all_rcpts = [to] + [a.strip() for a in cc.split(",") if a.strip()] + [a.strip() for a in bcc.split(",") if a.strip()]
        server.sendmail(config["from_addr"] or config["user"], all_rcpts, msg.as_string())
        server.quit()
        return {"success": True, "message": f"邮件已发送至 {to}"}
    except Exception as e:
        return {"success": False, "error": f"发送失败: {str(e)}"}


def compose_email(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = "",
    attachments: list = None,
    template_path: str = "",
    template_vars: dict = None,
    save_draft: bool = True,
) -> dict:
    """撰写邮件并选择发送或保存草稿"""
    try:
        # 模板填充
        if template_path and Path(template_path).exists():
            body = Path(template_path).read_text(encoding="utf-8")
        if template_vars:
            body = _format_template(body, template_vars)
            subject = _format_template(subject, template_vars)

        if _is_demo_mode() or save_draft:
            return _save_draft(to, subject, body, cc, attachments)
        else:
            return _send_real(to, subject, body, cc, bcc, attachments)
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_attachment(filepath: str) -> dict:
    """验证附件文件是否存在"""
    try:
        p = Path(filepath)
        if not p.exists():
            return {"success": False, "error": f"附件文件不存在: {filepath}"}
        return {"success": True, "message": f"附件已就绪: {p.name}", "files": [str(p)]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_draft(to: str, subject: str, body: str, cc: str = "", attachments: list = None) -> dict:
    """单独保存邮件草稿"""
    try:
        return _save_draft(to, subject, body, cc, attachments)
    except Exception as e:
        return {"success": False, "error": str(e)}


def batch_send(
    recipients: list = None,
    subject_template: str = "",
    body_template: str = "",
    attachments: list = None,
    delay_seconds: float = 1.0,
) -> dict:
    """批量发送邮件（demo 模式保存草稿）"""
    try:
        recipients = recipients or []
        if not recipients:
            return {"success": False, "error": "收件人列表为空"}

        results = []
        files_created = []

        for r in recipients:
            name = r.get("name", r.get("email", ""))
            email = r.get("email", "")
            vars_ = r.get("vars", {})
            vars_["name"] = name
            vars_["email"] = email

            subject = _format_template(subject_template, vars_)
            body = _format_template(body_template, vars_)

            if _is_demo_mode():
                filename = f"batch_email_{name}_{timestamp()}.txt"
                draft_path = output_path(filename)
                content = f"To: {email}\nSubject: {subject}\n\n{body}"
                draft_path.write_text(content, encoding="utf-8")
                files_created.append(str(draft_path))
                results.append({"email": email, "status": "draft_saved"})
            else:
                res = _send_real(email, subject, body, attachments=attachments)
                results.append({"email": email, "status": "sent" if res["success"] else "failed", "error": res.get("error")})
                import time
                time.sleep(delay_seconds)

        return {
            "success": True,
            "message": f"批量处理完成: {len(recipients)} 封",
            "files": files_created if files_created else [],
            "results": results,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_template(
    to: str = "",
    subject: str = "",
    body: str = "",
    template_path: str = "",
    template_vars: dict = None,
    cc: str = "",
    bcc: str = "",
    attachments: list = None,
    save_draft: bool = True,
) -> dict:
    """从模板创建邮件并保存为草稿"""
    try:
        if not template_path and not body:
            return {"success": False, "error": "请提供模板路径或邮件正文"}

        return compose_email(
            to=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
            template_path=template_path,
            template_vars=template_vars,
            save_draft=True,  # 模板邮件强制保存草稿
        )
    except Exception as e:
        return {"success": False, "error": str(e)}


def compose_and_send(
    to: str = "",
    subject: str = "",
    body: str = "",
    cc: str = "",
    bcc: str = "",
    attachments: list = None,
    template_path: str = "",
    template_vars: dict = None,
    save_draft: bool = True,
) -> dict:
    """撰写并发送邮件（handler 入口，与 compose_email 一致）"""
    return compose_email(
        to=to,
        subject=subject,
        body=body,
        cc=cc,
        bcc=bcc,
        attachments=attachments,
        template_path=template_path,
        template_vars=template_vars,
        save_draft=save_draft,
    )
