"""
main.py
-------
CLI entry point for ReviewAgent.
Parses command-line arguments, loads configuration, orchestrates scanning, language detection,
review agent execution, and rich terminal reporting.
"""

import sys
import time
import argparse
import concurrent.futures
from pathlib import Path

from reviewagent import __version__
from reviewagent.config import load_config
from reviewagent.core.scanner import ProjectScanner, read_file_content
from reviewagent.core.aggregator import ReviewSummary
from reviewagent.agents.base import GeminiReviewAgent
from reviewagent.reports.terminal import TerminalReporter, console


def parse_arguments():
    """
    Parses command-line arguments for ReviewAgent CLI.
    """
    parser = argparse.ArgumentParser(
        prog="reviewagent",
        description="🤖 ReviewAgent — Extensible Multi-Language Code Review Platform.",
        epilog="Powered by Google Gemini API"
    )

    parser.add_argument(
        "target_path",
        type=str,
        help="Path to a source code file or folder to review (e.g., myfile.py or ./my_project)"
    )

    parser.add_argument(
        "-s", "--severity",
        type=str,
        choices=["low", "medium", "high", "LOW", "MEDIUM", "HIGH", "CRITICAL", "INFO"],
        default="low",
        help="Filter severity level: low (all issues), medium (bugs/security/bad practices), high (critical bugs/security only)"
    )

    parser.add_argument(
        "--refactor", "--fix",
        action="store_true",
        default=False,
        help="Include full refactored/rewritten code snippet in review (off by default for fast performance)"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3.6-flash",
        help="Gemini model to use for analysis (default: gemini-3.6-flash)"
    )

    parser.add_argument(
        "-c", "--config",
        type=str,
        default=None,
        help="Path to custom configuration file (e.g. .reviewconfig.json)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"ReviewAgent v{__version__}"
    )

    return parser.parse_args()


def main():
    """
    Main entry point function executed when `reviewagent` command is run.
    """
    session_start_time = time.perf_counter()

    # Reconfigure encoding for Windows compatibility
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    # Display welcome banner
    TerminalReporter.print_banner()

    # Parse CLI arguments
    args = parse_arguments()

    # Load configuration settings
    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)

    # Step 1: Discover source files
    t_disc_start = time.perf_counter()
    scanner = ProjectScanner(excluded_dirs=config.excluded_dirs)
    try:
        scanned_files = scanner.scan(args.target_path)
    except Exception as e:
        TerminalReporter.print_error(str(e))
        sys.exit(1)

    total_files = len(scanned_files)
    discovery_duration = time.perf_counter() - t_disc_start

    # Print CLI active parameters
    console.print(
        f"🎚️ [bold yellow]Severity Level:[/bold yellow] [bold white]{args.severity.upper()}[/bold white] | "
        f"💡 [bold yellow]Refactor Mode:[/bold yellow] [bold white]{'ON' if args.refactor else 'OFF (Fast Mode)'}[/bold white]"
    )

    if total_files > 1:
        console.print(
            f"📁 [bold cyan]Folder Review Mode:[/bold cyan] Found [bold white]{total_files}[/bold white] file(s) in {discovery_duration:.3f}s.\n"
        )
    else:
        console.print()

    # Step 2: Initialize Gemini Review Agent
    try:
        agent = GeminiReviewAgent(model_name=args.model)
    except RuntimeError as e:
        TerminalReporter.print_error(str(e))
        sys.exit(1)

    summary = ReviewSummary(total_files=total_files)

    # Step 3: Execute review for each scanned file
    for idx, sf in enumerate(scanned_files, start=1):
        rel_name = sf.relative_path
        lang_name = sf.language.name

        if total_files > 1:
            console.print("─────────────────────────────────────────────────────────────")
            console.print(f"📄 [bold yellow]File [{idx}/{total_files}]:[/bold yellow] [bold white]{rel_name}[/bold white] [dim]({lang_name})[/dim]")
        else:
            TerminalReporter.print_file_info(rel_name, lang_name)

        # Read file content
        t_read_start = time.perf_counter()
        try:
            content, filename = read_file_content(sf.path)
        except Exception as e:
            TerminalReporter.print_warning(f"Skipping '{rel_name}': {str(e)}")
            continue
        read_duration = time.perf_counter() - t_read_start

        # Execute agent analysis in background thread with live spinner
        try:
            start_t = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    agent.analyze,
                    content,
                    filename,
                    severity=args.severity,
                    refactor=args.refactor,
                )

                with console.status(
                    f"[bold cyan]🤖 Requesting Gemini API ({args.model})... 0.0s[/bold cyan]",
                    spinner="dots"
                ) as status:
                    while not future.done():
                        time.sleep(0.1)
                        elapsed = time.perf_counter() - start_t
                        status.update(f"[bold cyan]🤖 Requesting Gemini API ({args.model})... {elapsed:.1f}s[/bold cyan]")

                agent_result = future.result(timeout=120)

            # Warning if API call exceeded 60s
            if agent_result.duration_seconds > 60.0:
                TerminalReporter.print_warning(f"Gemini API call took {agent_result.duration_seconds:.1f}s (exceeded 60s threshold).")

            # Update summary metrics
            summary.add_file_results(agent_result.issue_counts, agent_result.findings)

            # Render markdown review & findings
            t_render_start = time.perf_counter()
            TerminalReporter.render_markdown_review(agent_result.raw_markdown, filename)
            TerminalReporter.render_findings(agent_result.findings)
            render_duration = time.perf_counter() - t_render_start

            # Print performance metrics
            console.print(
                f"⏱️ [dim]Performance Log ({rel_name}): File Read: {read_duration*1000:.1f}ms | "
                f"Gemini API: {agent_result.duration_seconds:.2f}s | Terminal Render: {render_duration*1000:.1f}ms[/dim]"
            )

        except concurrent.futures.TimeoutError:
            TerminalReporter.print_error(f"Failed to review '{rel_name}': Gemini API request timed out (>120s).")
        except Exception as e:
            TerminalReporter.print_error(f"Failed to review '{rel_name}': {str(e)}")

    # Print summary box panel
    TerminalReporter.print_summary_box(summary)

    total_session_time = time.perf_counter() - session_start_time
    console.print(f"\n⌛ [dim white]Total Session Elapsed Time: {total_session_time:.2f}s[/dim white]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        TerminalReporter.print_warning("\nCode review cancelled by user.")
        sys.exit(0)
