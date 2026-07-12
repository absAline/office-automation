"""文件整理模块 — 核心工具函数

使用 pathlib + shutil 实现文件分类、重命名、清理
所有写操作均支持 dry_run 预览模式
"""
import re
import shutil
import fnmatch
from pathlib import Path
from datetime import datetime, timedelta
from office_automation.shared.utils import output_path, save_json, timestamp


# --------------- 默认分类规则 ---------------

DEFAULT_CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".json", ".xml"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    "视频": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "代码": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs", ".sh", ".bat"],
    "Excel": [".xls", ".xlsx", ".xlsm"],
}

TEMP_PATTERNS = ["*.tmp", "*.bak", "*~", "*.temp", "*.swp", "*.cache"]


def _is_excluded(file_path: Path, exclude_patterns: list[str]) -> bool:
    """检查文件是否在排除列表中"""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_path.name, pattern):
            return True
    return False


def _categorize_by_scheme(files: list[Path], scheme: str, categories: dict) -> dict[str, list[Path]]:
    """按指定方案对文件分组"""
    cats = categories if categories else DEFAULT_CATEGORIES
    grouped: dict[str, list[Path]] = {cat: [] for cat in cats}
    grouped["其他"] = []

    for f in files:
        ext = f.suffix.lower()
        matched = False

        if scheme == "by_type":
            for cat, exts in cats.items():
                if ext in [e.lower() for e in exts]:
                    grouped[cat].append(f)
                    matched = True
                    break
            if not matched:
                grouped["其他"].append(f)

        elif scheme == "by_date":
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            key = mtime.strftime("%Y-%m")
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(f)

        elif scheme == "by_size":
            size = f.stat().st_size
            if size == 0:
                key = "空文件"
            elif size < 1024 * 100:  # <100KB
                key = "小文件(<100KB)"
            elif size < 1024 * 1024:  # <1MB
                key = "中文件(100KB-1MB)"
            elif size < 1024 * 1024 * 10:  # <10MB
                key = "大文件(1MB-10MB)"
            else:
                key = "超大文件(>10MB)"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(f)

        elif scheme == "by_name":
            name = f.stem.lower()
            grouped_by_initial = {}
            for f2 in files:
                initial = f2.stem[0].upper() if f2.stem and f2.stem[0].isalpha() else "#"
                if initial not in grouped_by_initial:
                    grouped_by_initial[initial] = []
                grouped_by_initial[initial].append(f2)
            return grouped_by_initial

    # 移除空分类
    return {k: v for k, v in grouped.items() if v}


# --------------- 公开工具函数 ---------------

def classify_by_type(target_dir: str, categories: dict = None, dry_run: bool = True) -> dict:
    """按文件类型分类"""
    return organize(target_dir=target_dir, scheme="by_type", categories=categories or {}, dry_run=dry_run)


def classify_by_keyword(target_dir: str, keyword: str, dry_run: bool = True) -> dict:
    """按文件名关键词查找文件"""
    try:
        p = Path(target_dir)
        if not p.exists() or not p.is_dir():
            return {"success": False, "error": f"目录不存在: {target_dir}"}

        matched = []
        for f in p.rglob("*"):
            if f.is_file() and keyword.lower() in f.name.lower():
                matched.append(str(f))

        return {
            "success": True,
            "message": f"找到 {len(matched)} 个包含 '{keyword}' 的文件",
            "files": matched,
            "dry_run": dry_run,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def batch_rename(
    target_dir: str = "",
    pattern: str = r"(.*)",
    replacement: str = r"\1",
    dry_run: bool = True,
    include_extensions: list = None,
) -> dict:
    """批量重命名文件（正则替换）"""
    try:
        p = Path(target_dir)
        if not p.exists() or not p.is_dir():
            return {"success": False, "error": f"目录不存在: {target_dir}"}

        include_exts = [ext.lower() for ext in (include_extensions or [])]
        renamed_plan = []
        errors = []

        for f in sorted(p.iterdir()):
            if not f.is_file():
                continue
            if include_exts and f.suffix.lower() not in include_exts:
                continue

            try:
                new_name = re.sub(pattern, replacement, f.name)
            except re.error as e:
                errors.append(f"正则错误 ({f.name}): {e}")
                continue

            if new_name == f.name:
                continue

            new_path = f.parent / new_name
            if new_path.exists():
                errors.append(f"目标文件已存在: {new_name}")
                continue

            renamed_plan.append({"from": str(f), "to": str(new_path)})

            if not dry_run:
                f.rename(new_path)

        result = {
            "success": True,
            "message": f"重命名计划: {len(renamed_plan)} 个文件" + (" (预览模式)" if dry_run else " (已执行)"),
            "renamed": renamed_plan,
            "dry_run": dry_run,
        }
        if errors:
            result["errors"] = errors
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


def cleanup_empty(
    target_dir: str = "",
    remove_empty_dirs: bool = True,
    remove_empty_files: bool = True,
    remove_temp_files: bool = True,
    dry_run: bool = True,
    older_than_days: int = 0,
) -> dict:
    """清理空文件和临时文件"""
    try:
        p = Path(target_dir)
        if not p.exists() or not p.is_dir():
            return {"success": False, "error": f"目录不存在: {target_dir}"}

        cutoff_time = datetime.now() - timedelta(days=older_than_days) if older_than_days > 0 else None
        to_delete = []
        stats = {"empty_files": 0, "temp_files": 0, "empty_dirs": 0}

        # 收集要删除的文件
        for f in p.rglob("*"):
            if not f.is_file():
                continue

            if cutoff_time:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime > cutoff_time:
                    continue

            should_delete = False
            reason = ""

            if remove_empty_files and f.stat().st_size == 0:
                should_delete = True
                reason = "空文件(0字节)"
                stats["empty_files"] += 1

            if remove_temp_files and not should_delete:
                for pat in TEMP_PATTERNS:
                    if fnmatch.fnmatch(f.name, pat):
                        should_delete = True
                        reason = f"临时文件({f.name})"
                        stats["temp_files"] += 1
                        break

            if should_delete:
                to_delete.append({"path": str(f), "reason": reason})
                if not dry_run:
                    f.unlink()

        # 清理空目录（从深到浅）
        if remove_empty_dirs and not dry_run:
            for d in sorted(p.rglob("*"), key=lambda x: len(x.parts), reverse=True):
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
                    stats["empty_dirs"] += 1
        elif remove_empty_dirs:
            # dry_run 模式统计空目录
            for d in sorted(p.rglob("*"), key=lambda x: len(x.parts), reverse=True):
                if d.is_dir() and not any(d.iterdir()):
                    to_delete.append({"path": str(d), "reason": "空目录"})
                    stats["empty_dirs"] += 1

        return {
            "success": True,
            "message": f"清理计划: {len(to_delete)} 项" + (" (预览模式)" if dry_run else " (已执行)"),
            "to_delete": to_delete,
            "stats": stats,
            "dry_run": dry_run,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_stats(target_dir: str) -> dict:
    """获取目录文件统计信息"""
    try:
        p = Path(target_dir)
        if not p.exists() or not p.is_dir():
            return {"success": False, "error": f"目录不存在: {target_dir}"}

        total_size = 0
        file_count = 0
        dir_count = 0
        ext_counts = {}
        size_distribution = {"<100KB": 0, "100KB-1MB": 0, "1MB-10MB": 0, ">10MB": 0, "空文件": 0}

        for f in p.rglob("*"):
            if f.is_file():
                file_count += 1
                size = f.stat().st_size
                total_size += size
                ext = f.suffix.lower() or "(无后缀)"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1

                if size == 0:
                    size_distribution["空文件"] += 1
                elif size < 1024 * 100:
                    size_distribution["<100KB"] += 1
                elif size < 1024 * 1024:
                    size_distribution["100KB-1MB"] += 1
                elif size < 1024 * 1024 * 10:
                    size_distribution["1MB-10MB"] += 1
                else:
                    size_distribution[">10MB"] += 1
            elif f.is_dir():
                dir_count += 1

        def format_size(b):
            for unit in ["B", "KB", "MB", "GB"]:
                if b < 1024.0:
                    return f"{b:.1f} {unit}"
                b /= 1024.0
            return f"{b:.1f} TB"

        return {
            "success": True,
            "message": f"目录统计完成",
            "stats": {
                "directory": str(p),
                "file_count": file_count,
                "dir_count": dir_count,
                "total_size": format_size(total_size),
                "total_size_bytes": total_size,
                "extension_distribution": dict(sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)),
                "size_distribution": size_distribution,
            },
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def organize(
    target_dir: str = "",
    scheme: str = "by_type",
    categories: dict = None,
    dry_run: bool = True,
    exclude_patterns: list = None,
) -> dict:
    """按指定方案整理/分类文件"""
    try:
        p = Path(target_dir)
        if not p.exists() or not p.is_dir():
            return {"success": False, "error": f"目录不存在: {target_dir}"}

        exclude_patterns = exclude_patterns or []

        # 收集文件（仅当前层级，不递归）
        files = []
        for f in p.iterdir():
            if f.is_file() and not _is_excluded(f, exclude_patterns):
                files.append(f)

        # 分组
        grouped = _categorize_by_scheme(files, scheme, categories or {})

        # 执行或预览
        operations = []
        for category, cat_files in grouped.items():
            cat_dir = p / category
            for f in cat_files:
                dest = cat_dir / f.name
                operations.append({"from": str(f), "to": str(dest)})
                if not dry_run:
                    cat_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(f), str(dest))

        # 保存整理计划到输出
        plan_path = save_json(
            {"target": str(p), "scheme": scheme, "dry_run": dry_run, "operations": operations},
            output_path(f"organize_plan_{timestamp()}.json"),
        )

        return {
            "success": True,
            "message": f"整理计划: {len(operations)} 个文件 → {len(grouped)} 个分类"
            + (" (预览模式)" if dry_run else " (已执行)"),
            "files": [str(plan_path)],
            "grouped": {k: [str(f) for f in v] for k, v in grouped.items()},
            "operations_count": len(operations),
            "dry_run": dry_run,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def rename_batch(
    target_dir: str = "",
    pattern: str = r"(.*)",
    replacement: str = r"\1",
    dry_run: bool = True,
    include_extensions: list = None,
) -> dict:
    """批量重命名（handler 入口，与 batch_rename 一致）"""
    return batch_rename(
        target_dir=target_dir,
        pattern=pattern,
        replacement=replacement,
        dry_run=dry_run,
        include_extensions=include_extensions,
    )


def cleanup(
    target_dir: str = "",
    remove_empty_dirs: bool = True,
    remove_empty_files: bool = True,
    remove_temp_files: bool = True,
    dry_run: bool = True,
    older_than_days: int = 0,
) -> dict:
    """清理文件（handler 入口）"""
    return cleanup_empty(
        target_dir=target_dir,
        remove_empty_dirs=remove_empty_dirs,
        remove_empty_files=remove_empty_files,
        remove_temp_files=remove_temp_files,
        dry_run=dry_run,
        older_than_days=older_than_days,
    )


def analyze(
    target_dir: str = "",
    scheme: str = "by_type",
    categories: dict = None,
    dry_run: bool = True,
    exclude_patterns: list = None,
) -> dict:
    """分析目录文件结构 = get_stats + organize preview"""
    stats = get_stats(target_dir)
    org = organize(
        target_dir=target_dir,
        scheme=scheme,
        categories=categories or {},
        dry_run=True,  # analyze 总是预览
        exclude_patterns=exclude_patterns,
    )
    return {
        "success": stats["success"] and org["success"],
        "message": "目录分析完成",
        "stats": stats.get("stats", {}),
        "grouped": org.get("grouped", {}),
    }
