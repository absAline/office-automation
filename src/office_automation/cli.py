"""Typer CLI 入口 — oa 命令"""

import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

from office_automation import __version__
from office_automation.config import get_config
from office_automation.modules.registry import list_modules, init as init_modules

app = typer.Typer(
    name="oa",
    help="AutoOffice — 自然语言驱动的办公自动化工具集",
    add_completion=False,
)
console = Console()


@app.command()
def list(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="显示详细信息"),
):
    """列出所有可用的自动化场景"""
    init_modules()
    modules = list_modules()

    if verbose:
        for m in modules:
            console.print(f"\n[bold cyan]{m.name}[/bold cyan] — {m.title}")
            console.print(f"  {m.description}")
    else:
        table = Table(title=f"可用场景 ({len(modules)} 个)")
        table.add_column("编号", style="dim")
        table.add_column("模块名", style="cyan")
        table.add_column("场景", style="green")
        table.add_column("说明")

        for i, m in enumerate(modules, 1):
            table.add_row(str(i), m.name, m.title, m.description)
        console.print(table)


@app.command()
def run(
    description: str = typer.Argument(..., help="自然语言描述你要执行的自动化任务"),
    module: Optional[str] = typer.Option(None, "--module", "-m", help="指定模块名，跳过 AI 意图分类"),
    action: Optional[str] = typer.Option(None, "--action", "-a", help="指定动作名"),
    mode: Optional[str] = typer.Option(None, "--mode", help="运行模式: demo | real"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """用自然语言执行自动化任务"""
    init_modules()

    console.print("[yellow]▶ 演示模式[/yellow]")

    if module:
        # 直接指定模块
        from office_automation.executor import execute_module
        result = execute_module(module, action, {"description": description})
    else:
        # AI 分类意图
        from office_automation.ai import create_provider
        provider = create_provider(mode=mode)

        system_prompt = """你是一个办公自动化助手。分析用户的自然语言需求，输出 JSON 格式：
{
    "module": "模块名",
    "action": "动作名",
    "params": { ... }
}
可用模块: excel, email, document, file_organizer
        
只输出 JSON，不要额外文字。"""

        with console.status("[bold green]AI 正在分析你的需求..."):
            response = asyncio.run(provider.chat([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": description},
            ]))

        try:
            intent = json.loads(response)
        except json.JSONDecodeError:
            console.print("[red]AI 返回格式异常，使用默认模块[/red]")
            intent = {"module": "excel", "action": "generate_report", "params": {"title": description}}

        module_name = intent.get("module", "excel")
        action_name = intent.get("action", "generate_report")
        params = intent.get("params", {})

        console.print(f"[green]→ 识别为: {module_name}.{action_name}[/green]")

        if output:
            params["output"] = output

        from office_automation.executor import execute_module
        result = execute_module(module_name, action_name, params)

    # 显示结果
    if result.get("success"):
        msg = result.get("output") or result.get("message") or ""
        console.print(f"\n[bold green]✅ {msg}[/bold green]")
        if result.get("files"):
            console.print("\n[bold]生成文件:[/bold]")
            for f in result["files"]:
                console.print(f"  📄 {f}")
    else:
        console.print(f"\n[bold red]❌ 执行失败: {result.get('error', '未知错误')}[/bold red]")


@app.command()
def demo(
    module_name: str = typer.Argument(None, help="指定模块演示，留空则运行所有模块"),
):
    """运行 Demo 模式（无需 API Key）"""
    init_modules()

    if module_name:
        modules = [m for m in list_modules() if m.name == module_name]
    else:
        modules = list_modules()

    if not modules:
        console.print("[red]未找到模块[/red]")
        raise typer.Exit(1)

    from office_automation.ai import create_provider
    from office_automation.executor import execute_module

    provider = create_provider(mode="demo")

    for mod in modules:
        console.print(f"\n[bold cyan]▶ {mod.title}[/bold cyan]")
        console.print(f"  {mod.description}")

        test_prompt = f"执行 {mod.title} 的自动化任务"
        response = asyncio.run(provider.chat([
            {"role": "system", "content": "输出 JSON: {\"module\": \"...\", \"action\": \"...\", \"params\": {...}}"},
            {"role": "user", "content": test_prompt},
        ]))

        try:
            intent = json.loads(response)
        except json.JSONDecodeError:
            console.print(f"  [yellow]⚠ 跳过 (AI 返回格式异常)[/yellow]")
            continue

        with console.status(f"  [green]执行中..."):
            result = execute_module(
                intent.get("module", mod.name),
                intent.get("action", "info"),
                intent.get("params", {}),
            )

        if result.get("success"):
            msg = result.get("output") or result.get("message") or "成功"
            console.print(f"  [green]✅ {msg}[/green]")
        else:
            console.print(f"  [red]❌ {result.get('error', '失败')}[/red]")


@app.command()
def configure():
    """查看当前配置"""
    console.print("[cyan]演示模式 — 配置已固化，无需额外设置[/cyan]")


@app.command()
def version():
    """显示版本信息"""
    console.print(f"[cyan]AutoOffice[/cyan] v{__version__}")
    console.print("自然语言驱动的办公自动化工具集")


if __name__ == "__main__":
    app()
