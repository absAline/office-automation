# AutoOffice — 办公自动化工具

说人话，自动帮你处理办公文件。支持 **Excel、邮件、Word文档、文件整理**。

## 🚀 快速使用（推荐）

网页版管理面板，无需装环境，开浏览器就能用：

```bash
cd admin
npm install
npm start
# 打开 http://localhost:4323
```

在网页里直接输入"生成季度销售报表"、"给客户发春节问候邮件"等自然语言指令，AI 会自动执行。

## 💻 命令行模式

适合开发者/Python用户：

```bash
# 激活环境
source .venv/bin/activate
pip install -e .

# Demo模式（无需API Key）
oa run "生成一份季度销售报表，包含三个月的销售数据对比"

# 或指定模块
oa demo excel      # Excel演示
oa list            # 查看所有可用场景
```

## 功能模块

| 模块 | 能力 |
|------|------|
| **Excel** | 生成报表、清洗数据、合并工作表、添加图表 |
| **邮件** | 撰写邮件、模板填充、批量发送、附件支持 |
| **Word** | 模板占位符填充、批量生成合同/通知、合并文档 |
| **文件整理** | 按类型/日期/名称/大小分类、批量重命名、清理空文件 |

## 运行模式

- **Demo**（默认）— 零依赖，关键词匹配，体验完整流程
- **Real** — 配置 API Key，连接 OpenAI / Ollama / 通义千问，获取真实AI生成

## 项目结构

```
├── admin/                     # Web管理面板（Express.js）
│   ├── server.js              #   后端服务器（端口4323）
│   └── public/                #   前端页面
├── src/office_automation/     # Python核心代码
│   ├── cli.py                 #   命令行入口
│   ├── executor.py            #   模块执行器
│   ├── ai/                    #   AI Provider（Mock/OpenAI/Ollama/通义千问）
│   ├── modules/               #   功能模块
│   │   ├── excel/             #   Excel 自动化
│   │   ├── email/             #   邮件自动化
│   │   ├── document/          #   Word 文档自动化
│   │   └── file_organizer/    #   文件整理自动化
│   └── config.py              #   配置管理
├── data/                      # 测试数据和输出文件
└── scripts/                   # 辅助脚本
```
