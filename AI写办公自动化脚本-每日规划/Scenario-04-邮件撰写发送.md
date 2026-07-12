# Scenario 04: 邮件撰写发送
> **实现状态**: ✅ 已实现 — `email/` 模块，支持SMTP发送/草稿保存/Demo模式

## 场景描述
AI 根据自然语言描述撰写邮件正文，自动添加附件，批量发送。

## 痛点
- 写邮件花时间，尤其英文邮件
- 群发个性化邮件（每个收件人不同称呼、内容）
- 需要附件的批量发送操作繁琐

## AI 参与方式
AI 理解发送意图 → 生成邮件正文（含称呼、正文、结尾）→ 确定收件人和附件 → Demo 模式存草稿 / Real 模式真实发送

## 演示示例
```bash
oa run "给王经理发邮件提醒明天下午2点开会，附件带上会议议程"
```

## 核心命令
```bash
# Demo 模式（存草稿到 data/output/）
oa run "给项目团队发一封周报邮件，汇报本周进展"
oa run "写一封英文邮件给客户，确认下周会议时间"

# 配置邮箱后 Real 模式
oa run --mode real "给张三发邮件，主题：季度考核通知"
```

## 配置 SMTP（Real 模式）
```python
# 在 Python 中配置
from scripts.email.tools import configure_smtp
configure_smtp("your@qq.com", "smtp_authorization_code")
```

## 交付物（Demo 模式）
- `data/output/email_draft_xxx.json` — 邮件草稿
- 预览邮件内容

## 注意
- Demo 模式不会真实发送邮件
- Real 模式需要配置 SMTP
