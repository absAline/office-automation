# Scenario 05: 智能文件整理
> **实现状态**: ✅ 已实现 — `file_organizer/` 模块，支持按类型/关键词分类、批量重命名

## 场景描述
AI 智能分类指定目录下的文件，支持按类型、按关键词、按日期整理。

## 痛点
- 桌面/下载文件夹乱七八糟，找文件困难
- 手动分类大量文件费时
- 需要定期清理临时文件

## AI 参与方式
AI 理解整理规则 → 扫描目标目录 → 根据规则分类文件 → 执行移动/重命名/删除

## 演示示例
```bash
oa run "把 data/sample/mixed_files 按文件类型分类整理"
```

## 核心命令
```bash
# Demo 模式
oa run "把 Downloads 目录的文件按类型整理到子文件夹"
oa run "把项目文档按日期归档到 2026 年文件夹"

# 模拟运行（不实际移动）
oa run --module file_organizer --action organize "先模拟运行看看结果"

# 自定义分类
oa run "把图片和视频分开，文档按项目名分类"
```

## 交付物
- 文件被分类到对应子目录
- `data/output/organize_report.txt` — 整理报告

## 安全机制
- 支持 dry_run（模拟运行）模式预览结果
- 实际执行前确认
