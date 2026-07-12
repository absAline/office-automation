"""生成演示用测试数据"""

import csv
import json
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
OUTPUT_DIR = DATA_DIR / "output"
TEMPLATE_DIR = DATA_DIR / "templates"


def ensure_dirs():
    for d in [SAMPLE_DIR, OUTPUT_DIR, TEMPLATE_DIR]:
        d.mkdir(parents=True, exist_ok=True)


# ============ 1. Excel 测试数据 ============

def create_sales_data():
    """创建销售数据 Excel（模拟脏数据）"""
    try:
        import openpyxl
    except ImportError:
        print("  [跳过] openpyxl 未安装")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "销售数据"
    ws.append(["月份", "销售额", "成本", "利润", "备注"])
    data = [
        ["1月", 120000, 78000, 42000, ""],
        ["2月", 158000, 95000, 63000, ""],
        ["3月", 185000, 110000, 75000, ""],
        ["4月", "N/A", 100000, None, "数据异常"],
        ["5月", 220000, 130000, 90000, ""],
        ["6月", 250000, 150000, 100000, ""],
        ["7月",  -5000, 80000, None, "异常值"],
        ["8月", 280000, 160000, 120000, ""],
        ["9月", 310000, 190000, 120000, ""],
        ["10月", 290000, 170000, 120000, ""],
        ["11月", 350000, 200000, 150000, ""],
        ["12月", 400000, 240000, 160000, ""],
    ]
    for row in data:
        ws.append(row)
    wb.save(SAMPLE_DIR / "sales_data_messy.xlsx")
    print(f"  ✅ 创建: {SAMPLE_DIR / 'sales_data_messy.xlsx'}")


# ============ 2. 员工数据 CSV ============

def create_employees_csv():
    path = SAMPLE_DIR / "employees.csv"
    rows = [
        ["姓名", "部门", "岗位", "入职日期", "邮箱"],
        ["张三", "技术部", "高级工程师", "2024-03-15", "zhangsan@company.com"],
        ["李四", "市场部", "市场经理", "2024-06-01", "lisi@company.com"],
        ["王五", "技术部", "架构师", "2023-09-10", "wangwu@company.com"],
        ["赵六", "人事部", "HRBP", "2024-01-20", "zhaoliu@company.com"],
        ["钱七", "财务部", "财务分析师", "2024-04-08", "qianqi@company.com"],
        ["孙八", "技术部", "前端开发", "2024-07-22", "sunba@company.com"],
        ["周九", "市场部", "品牌专员", "2024-02-14", "zhoujiu@company.com"],
        ["吴十", "产品部", "产品经理", "2023-11-05", "wushi@company.com"],
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"  ✅ 创建: {path}")


# ============ 3. 产品页面 HTML (爬虫演示) ============

def create_products_html():
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>电子产品商城</title></head><body>
<h1>热销商品</h1>
<table id="product-list">
<tr><th>商品名称</th><th>价格</th><th>评分</th><th>销量</th></tr>
<tr><td>iPhone 15 Pro Max</td><td>¥9,999</td><td>4.8</td><td>12,345</td></tr>
<tr><td>MacBook Air M3</td><td>¥8,999</td><td>4.9</td><td>8,921</td></tr>
<tr><td>AirPods Pro 2</td><td>¥1,899</td><td>4.7</td><td>23,456</td></tr>
<tr><td>iPad Air M2</td><td>¥4,799</td><td>4.6</td><td>6,789</td></tr>
<tr><td>Apple Watch Ultra 2</td><td>¥5,999</td><td>4.5</td><td>3,456</td></tr>
</table>
<div class="article">
<h2>Apple 发布新款 MacBook Pro</h2>
<p>搭载 M4 芯片，性能提升 50%</p>
<span class="date">2026-05-15</span>
</div>
<div class="article">
<h2>iOS 18 新功能预览</h2>
<p>AI 驱动的新一代操作系统</p>
<span class="date">2026-05-10</span>
</div>
</body></html>"""
    (SAMPLE_DIR / "products.html").write_text(html, encoding="utf-8")
    print(f"  ✅ 创建: {SAMPLE_DIR / 'products.html'}")


# ============ 4. 会议纪要 ============

def create_meeting_notes():
    notes = """# 项目评审会议纪要

日期：2026-05-20 14:00-15:30
地点：3楼会议室
参会人：张总、王经理、李工、赵产品

## 会议议程
1. Q2 项目进展回顾
2. 技术方案评审
3. 资源调配讨论

## 讨论内容

张总：Q2 整体进展符合预期，但研发部项目排期偏紧，需要评估是否需要延期。

王经理：市场部需要在下周前拿到 Demo 版本用于客户演示，这个时间点很关键。

李工：技术方案已经完成评审，有几个风险点需要关注：
  - 数据库迁移可能影响现有服务
  - 第三方 API 依赖需要确认 SLA
  预计需要额外 2 名开发人员支持。

赵产品：用户需求文档已经更新到 v2.3，新增了数据导出功能，需要评估开发量。

## 决定
- TODO: 李工周五前输出技术风险评估报告
- TODO: 王经理协调客户 Demo 时间
- TODO: 赵产品下周三前完成 PRD 终版
- TODO: 张总评估是否需要从其他项目组调配资源
- 决定：如果周五评估风险可控，按原计划 6/15 上线
- 决定：数据导出功能放到 v2.1 版本

## 待办事项
- [ ] 李工：输出技术风险评估报告（截止：周五）
- [ ] 王经理：确认客户 Demo 时间（截止：周三）
- [ ] 赵产品：完成 PRD 终版（截止：下周三）
- [ ] 张总：资源调配评估（截止：周五）
"""
    (SAMPLE_DIR / "meeting_notes.txt").write_text(notes, encoding="utf-8")
    print(f"  ✅ 创建: {SAMPLE_DIR / 'meeting_notes.txt'}")


# ============ 5. 混合文件目录 ============

def create_mixed_files():
    dir_path = SAMPLE_DIR / "mixed_files"
    dir_path.mkdir(parents=True, exist_ok=True)

    files = [
        ("report_2026.pdf", "文档"),
        ("photo_vacation.jpg", "图片"),
        ("data_analysis.xlsx", "表格"),
        ("meeting_notes.docx", "文档"),
        ("profile_pic.png", "图片"),
        ("budget_2026.xlsx", "表格"),
        ("project_summary.pdf", "文档"),
        ("screenshot_01.png", "图片"),
        ("backup_data.zip", "压缩包"),
        ("README.txt", "文档"),
        ("config.ini", "其他"),
        ("temp_cache.tmp", "其他"),
        ("presentation.pptx", "演示"),
        ("invoice_template.xlsx", "表格"),
        ("team_photo.jpg", "图片"),
    ]

    for fname, _ in files:
        (dir_path / fname).touch()

    print(f"  ✅ 创建 {len(files)} 个测试文件: {dir_path}")


# ============ 6. 发票 PDF 文本模拟 ============

def create_sample_invoice():
    dir_path = SAMPLE_DIR / "invoices"
    dir_path.mkdir(parents=True, exist_ok=True)

    invoices = [
        {"发票号": "INV-2026-001", "日期": "2026-05-01", "供应商": "阿里云", "金额": 12500.00, "税率": "6%", "合计": 13250.00},
        {"发票号": "INV-2026-002", "日期": "2026-05-05", "供应商": "腾讯云", "金额": 8900.00, "税率": "6%", "合计": 9434.00},
        {"发票号": "INV-2026-003", "日期": "2026-05-10", "供应商": "京东企业购", "金额": 3500.00, "税率": "13%", "合计": 3955.00},
        {"发票号": "INV-2026-004", "日期": "2026-05-15", "供应商": "顺丰速运", "金额": 1200.00, "税率": "6%", "合计": 1272.00},
        {"发票号": "INV-2026-005", "日期": "2026-05-20", "供应商": "用友软件", "金额": 28000.00, "税率": "6%", "合计": 29680.00},
    ]

    for inv in invoices:
        text = f"""
发票号码：{inv['发票号']}
开票日期：{inv['日期']}
销售方：{inv['供应商']}
金额：{inv['金额']}
税率：{inv['税率']}
价税合计：{inv['合计']}
        """.strip()
        (dir_path / f"{inv['发票号']}.txt").write_text(text, encoding="utf-8")

    print(f"  ✅ 创建 {len(invoices)} 个发票文件: {dir_path}")


# ============ 7. 英文报告 (翻译演示) ============

def create_english_report():
    content = """# Quarterly Technology Review Report

## Executive Summary
The Q2 2026 technology review indicates significant progress across all major initiatives. 
Cloud migration has reached 78% completion, ahead of the projected 70% target. 
The AI-assisted development pilot showed a 35% increase in developer productivity.

## Key Metrics
- Cloud Migration: 78% complete (target: 70%)
- Developer Productivity: +35% (AI-assisted)
- System Uptime: 99.97%
- Security Incidents: 0 (critical), 3 (low)
- New Features Delivered: 47

## Challenges
1. Database latency increased 15% after the latest schema migration
2. Third-party API dependency creates bottleneck in CI/CD pipeline
3. Team capacity remains the primary constraint for accelerated delivery

## Recommendations
1. Invest in database query optimization with AI-powered index recommendations
2. Evaluate alternative CI/CD tools with better third-party integration
3. Hire 2 additional backend engineers for the next quarter

## Next Steps
- Complete cloud migration by Q3 2026
- Launch internal AI code review tool by August
- Reduce CI/CD pipeline time by 40%
"""
    (SAMPLE_DIR / "report_en.md").write_text(content, encoding="utf-8")
    print(f"  ✅ 创建: {SAMPLE_DIR / 'report_en.md'}")


# ============ 8. 文档模板 ============

def create_templates():
    # Word 模板 (作为 .txt 模拟，实际用 python-docx 读取)
    template_content = """姓名：{name}
部门：{department}
岗位：{position}
入职日期：{start_date}

入职通知

{name} 先生/女士：

欢迎您加入 {department} 部门，担任 {position} 一职。
您的入职日期为 {start_date}。

请于入职当天携带以下材料到人力资源部办理手续：
1. 身份证原件及复印件
2. 学历学位证书原件
3. 近期一寸照片两张
4. 银行卡信息

祝您工作愉快！

人力资源部
"""
    (TEMPLATE_DIR / "入职通知模板.txt").write_text(template_content, encoding="utf-8")
    print(f"  ✅ 创建: {TEMPLATE_DIR / '入职通知模板.txt'}")


# ============ Main ============

def main():
    print("=" * 50)
    print("  生成演示数据")
    print("=" * 50)
    ensure_dirs()

    print("\n📊 Excel 数据:")
    create_sales_data()

    print("\n📋 员工数据:")
    create_employees_csv()

    print("\n🌐 产品页面:")
    create_products_html()

    print("\n📝 会议纪要:")
    create_meeting_notes()

    print("\n📁 混合测试文件:")
    create_mixed_files()

    print("\n🧾 发票数据:")
    create_sample_invoice()

    print("\n📚 英文报告:")
    create_english_report()

    print("\n📄 文档模板:")
    create_templates()

    print("\n" + "=" * 50)
    print("  ✅ 所有演示数据生成完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
