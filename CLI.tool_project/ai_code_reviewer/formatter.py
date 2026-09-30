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
