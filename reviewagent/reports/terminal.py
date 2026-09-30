"""
terminal.py
-----------
Rich-based terminal reporter for ReviewAgent.
Formats banners, file discovery, findings tables, markdown reviews, and summary boxes.
"""

from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.table import Table

from reviewagent.core.finding import Finding, Severity
from reviewagent.core.aggregator import ReviewSummary

console = Console()


class TerminalReporter:
    """
    Handles stylized terminal output rendering using the Rich library.
    """

    @staticmethod
    def print_banner():
        """Displays modern welcome banner for ReviewAgent."""
        banner_text = Text("🤖 ReviewAgent", style="bold cyan")
        sub_text = Text("Extensible Multi-Language Code Review Platform", style="dim white")

        panel = Panel(
            Text.assemble(banner_text, "\n", sub_text),
            border_style="bold blue",
            expand=False,
            padding=(0, 2)
        )
        console.print(panel)

    @staticmethod
    def print_file_info(filename: str, language_name: str = "Python"):
        """Prints target file header with detected language."""
        console.print(
            f"📄 [bold yellow]Target File:[/bold yellow] [bold white]{filename}[/bold white] "
            f"[dim]({language_name})[/dim]"
        )

    @staticmethod
    def print_error(message: str):
        """Prints formatted red error box."""
        error_panel = Panel(
            f"[bold red]ERROR:[/bold red] {message}",
            title="[bold red]✖ Review Failed[/bold red]",
            border_style="red",
            expand=False
        )
        console.print(error_panel)

    @staticmethod
    def print_warning(message: str):
        """Prints yellow warning message."""
        console.print(f"⚠️ [bold yellow]{message}[/bold yellow]")

    @staticmethod
    def print_success(message: str):
        """Prints green success message."""
        console.print(f"✅ [bold green]{message}[/bold green]")

    @staticmethod
    def render_markdown_review(review_text: str, filename: str):
        """Renders Gemini Markdown response inside a stylized cyan panel."""
        md = Markdown(review_text)
        review_panel = Panel(
            md,
            title=f"[bold green]🔍 Code Review Results for {filename}[/bold green]",
            subtitle="[dim]End of AI Review[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        console.print(review_panel)

    @staticmethod
    def render_findings(findings: List[Finding]):
        """Renders a structured table of findings if present."""
        if not findings:
            return

        table = Table(title="📋 Structured Findings", border_style="dim white")
        table.add_column("Severity", style="bold")
        table.add_column("Category", style="cyan")
        table.add_column("File:Line", style="yellow")
        table.add_column("Message", style="white")

        for f in findings:
            sev_color = "red" if f.severity in (Severity.CRITICAL, Severity.HIGH) else ("yellow" if f.severity == Severity.MEDIUM else "green")
            loc = f"{f.file}:{f.line_number}" if f.line_number else f.file
            table.add_row(f"[{sev_color}]{f.severity.value}[/{sev_color}]", f.category, loc, f.message)

        console.print(table)

    @staticmethod
    def print_summary_box(summary: ReviewSummary):
        """Displays visually distinct summary box panel at the end of a review session."""
        total_issues = summary.total_issues
        is_folder = summary.total_files > 1

        lines = []

        if is_folder:
            lines.append(f"📁 [bold cyan]Files Scanned:[/bold cyan] [bold white]{summary.total_files}[/bold white]")
            lines.append(f"✨ [bold green]Files with Zero Issues:[/bold green] [bold white]{summary.clean_files_count}[/bold white]")
            lines.append(f"⚠️ [bold yellow]Files with Issues:[/bold yellow] [bold white]{summary.files_with_issues}[/bold white]\n")

        if total_issues == 0:
            lines.append("🎉 [bold green]Zero issues found! Your code passed all checks.[/bold green]")
            border_color = "green"
            title_text = "[bold green]🎉 Final Review Summary — All Clear![/bold green]"
        else:
            cat_parts = []
            if summary.total_bugs > 0:
                bug_str = "critical bug" if summary.total_bugs == 1 else "critical bugs"
                cat_parts.append(f"[bold red]{summary.total_bugs} {bug_str}[/bold red]")
            if summary.total_security > 0:
                sec_str = "security issue" if summary.total_security == 1 else "security issues"
                cat_parts.append(f"[bold yellow]{summary.total_security} {sec_str}[/bold yellow]")
            if summary.total_bad_practices > 0:
                prac_str = "bad practice" if summary.total_bad_practices == 1 else "bad practices"
                cat_parts.append(f"[bold cyan]{summary.total_bad_practices} {prac_str}[/bold cyan]")

            issues_str = "issue" if total_issues == 1 else "issues"
            breakdown_summary = ", ".join(cat_parts) if cat_parts else "0 issues"
            lines.append(f"📊 [bold white]{total_issues} {issues_str} found:[/bold white] {breakdown_summary}")

            lines.append("\n[bold underline]Category Breakdown:[/bold underline]")
            lines.append(f"  • 🚨 Bugs & Logic Errors: [bold red]{summary.total_bugs}[/bold red]")
            lines.append(f"  • 🔒 Security Weaknesses: [bold yellow]{summary.total_security}[/bold yellow]")
            lines.append(f"  • ⚠️ Bad Practices:        [bold cyan]{summary.total_bad_practices}[/bold cyan]")

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
