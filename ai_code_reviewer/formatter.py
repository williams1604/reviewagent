"""
formatter.py
------------
Handles colored terminal output and visual layout using the `rich` library.

Why we need this module:
`rich` is a popular Python library for terminal formatting. Instead of printing raw text,
this module uses `rich`:
1. `Panel`: Displays border boxes around titles and code reviews.
2. `Markdown`: Parses markdown syntax (bold text, code blocks, headers) and renders them cleanly.
3. `Console`: Manages stdout printing across Windows, Mac, and Linux consoles.
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

# Initialize the Rich Console — this object controls all output rendering
console = Console()


def print_banner():
    """
    Displays a modern welcome banner at the start of the CLI application.
    """
    banner_text = Text("🤖 AI Code Reviewer Agent", style="bold cyan")
    sub_text = Text("Powered by Google Gemini API", style="dim white")
    
    panel = Panel(
        Text.assemble(banner_text, "\n", sub_text),
        border_style="bold blue",
        expand=False,
        padding=(0, 2)
    )
    console.print(panel)


def print_file_info(filename: str):
    """
    Prints a highlight header showing which file is currently being reviewed.
    """
    console.print(f"📄 [bold yellow]Target File:[/bold yellow] [bold white]{filename}[/bold white]")


def print_error(message: str):
    """
    Prints a formatted error box in red when something goes wrong.
    """
    error_panel = Panel(
        f"[bold red]ERROR:[/bold red] {message}",
        title="[bold red]✖ Review Failed[/bold red]",
        border_style="red",
        expand=False
    )
    console.print(error_panel)


def print_success(message: str):
    """
    Prints a success message in green.
    """
    console.print(f"✅ [bold green]{message}[/bold green]")


def print_warning(message: str):
    """
    Prints a warning message in yellow.
    """
    console.print(f"⚠️ [bold yellow]{message}[/bold yellow]")


def render_markdown_review(review_text: str, filename: str):
    """
    Parses Gemini's Markdown response and renders it inside a stylized cyan Rich panel.
    """
    md = Markdown(review_text)
    review_panel = Panel(
        md,
        title=f"[bold green]🔍 Code Review Results for {filename}[/bold green]",
        subtitle="[dim]End of AI Review[/dim]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(review_panel)


def print_summary_box(
    total_files: int,
    clean_files_count: int,
    total_bugs: int,
    total_security: int,
    total_bad_practices: int
):
    """
    Displays a visually distinct summary panel at the end of a review session.
    """
    total_issues = total_bugs + total_security + total_bad_practices
    is_folder = total_files > 1

    lines = []

    if is_folder:
        lines.append(f"📁 [bold cyan]Files Scanned:[/bold cyan] [bold white]{total_files}[/bold white]")
        lines.append(f"✨ [bold green]Files with Zero Issues:[/bold green] [bold white]{clean_files_count}[/bold white]")
        issues_files = total_files - clean_files_count
        lines.append(f"⚠️ [bold yellow]Files with Issues:[/bold yellow] [bold white]{issues_files}[/bold white]\n")

    if total_issues == 0:
        lines.append("🎉 [bold green]Zero issues found! Your code passed all checks.[/bold green]")
        border_color = "green"
        title_text = "[bold green]🎉 Review Summary — All Clear![/bold green]"
    else:
        cat_parts = []
        if total_bugs > 0:
            bug_str = "critical bug" if total_bugs == 1 else "critical bugs"
            cat_parts.append(f"[bold red]{total_bugs} {bug_str}[/bold red]")
        if total_security > 0:
            sec_str = "security issue" if total_security == 1 else "security issues"
            cat_parts.append(f"[bold yellow]{total_security} {sec_str}[/bold yellow]")
        if total_bad_practices > 0:
            prac_str = "bad practice" if total_bad_practices == 1 else "bad practices"
            cat_parts.append(f"[bold cyan]{total_bad_practices} {prac_str}[/bold cyan]")

        issues_str = "issue" if total_issues == 1 else "issues"
        breakdown_summary = ", ".join(cat_parts) if cat_parts else "0 issues"
        lines.append(f"📊 [bold white]{total_issues} {issues_str} found:[/bold white] {breakdown_summary}")

        lines.append("\n[bold underline]Category Breakdown:[/bold underline]")
        lines.append(f"  • 🚨 Bugs & Logic Errors: [bold red]{total_bugs}[/bold red]")
        lines.append(f"  • 🔒 Security Weaknesses: [bold yellow]{total_security}[/bold yellow]")
        lines.append(f"  • ⚠️ Bad Practices:        [bold cyan]{total_bad_practices}[/bold cyan]")

        border_color = "magenta"
        title_text = "[bold magenta]📊 Final Review Summary[/bold magenta]"

    summary_panel = Panel(
        "\n".join(lines),
        title=title_text,
        border_style=border_color,
        padding=(1, 2),
        expand=False
    )
    console.print(summary_panel)

