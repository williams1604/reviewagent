"""
cli.py
------
The Command Line Interface (CLI) entry point for AI Code Reviewer.

Why we need this module:
This file is the orchestra conductor of our application:
1. `parse_arguments()`: Uses Python's built-in `argparse` module to read CLI flags (`target_path`, `--severity`, `--refactor`, `--model`).
2. `main()`: Resolves target files, initializes `CodeReviewer`, runs API queries with a live timer spinner, and handles exceptions cleanly.
"""

import sys
import time
import argparse
import concurrent.futures
from pathlib import Path
from ai_code_reviewer.utils import discover_source_files, read_source_file
from ai_code_reviewer.reviewer import CodeReviewer, parse_review_summary
from ai_code_reviewer import formatter
from ai_code_reviewer import __version__


def parse_arguments():
    """
    Parses command-line arguments using Python's standard `argparse` library.

    Example CLI command inputs:
        reviewagent sample_test.py
        reviewagent ./my_project --severity high
        reviewagent sample_test.py --refactor --model gemini-1.5-flash
    """
    parser = argparse.ArgumentParser(
        prog="reviewagent",
        description="🤖 AI Code Review Agent — Instant Senior Developer Code Reviews in your terminal.",
        epilog="Powered by Google Gemini API"
    )

    # Required Argument: Target file path or folder path
    parser.add_argument(
        "target_path",
        type=str,
        help="Path to a source code file or a folder to review (e.g., myfile.py or ./my_project)"
    )

    # Optional Flag: Severity filtering level
    parser.add_argument(
        "-s", "--severity",
        type=str,
        choices=["low", "medium", "high"],
        default="low",
        help="Filter severity level: low (all issues), medium (bugs/security/bad practices), high (critical bugs/security only)"
    )

    # Optional Flag: Enable full rewritten refactored code snippets
    parser.add_argument(
        "--refactor", "--fix",
        action="store_true",
        default=False,
        help="Include full refactored/rewritten code snippet in review (off by default for fast performance)"
    )

    # Optional Flag: Select specific Gemini API model
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3.6-flash",
        help="Gemini model to use for analysis (default: gemini-3.6-flash)"
    )

    # Optional Flag: Show version number
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"AI Code Reviewer v{__version__}"
    )

    return parser.parse_args()


def main():
    """
    Main entry point function executed when `reviewagent` command is run.
    """
    session_start_time = time.perf_counter()

    # Ensure Windows PowerShell / Command Prompt supports UTF-8 icons & emojis
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    # Display welcome banner
    formatter.print_banner()

    # Parse input arguments
    args = parse_arguments()

    # Step 1: Discover source code files & measure discovery duration
    t_disc_start = time.perf_counter()
    try:
        files_to_review = discover_source_files(args.target_path)
    except Exception as e:
        formatter.print_error(str(e))
        sys.exit(1)

    discovery_duration = time.perf_counter() - t_disc_start
    total_files = len(files_to_review)
    
    # Display active CLI parameters
    formatter.console.print(
        f"🎚️ [bold yellow]Severity Level:[/bold yellow] [bold white]{args.severity.upper()}[/bold white] | "
        f"💡 [bold yellow]Refactor Code:[/bold yellow] [bold white]{'ON' if args.refactor else 'OFF (Fast Mode)'}[/bold white]"
    )

    if total_files > 1:
        formatter.console.print(
            f"📁 [bold cyan]Folder Review Mode:[/bold cyan] Found [bold white]{total_files}[/bold white] file(s) in {discovery_duration:.3f}s.\n"
        )
    else:
        formatter.console.print()

    # Step 2: Initialize Gemini Code Reviewer client
    try:
        reviewer = CodeReviewer(model_name=args.model)
    except RuntimeError as e:
        formatter.print_error(str(e))
        sys.exit(1)

    total_bugs = 0
    total_security = 0
    total_bad_practices = 0
    clean_files_count = 0

    # Step 3: Review each discovered file sequentially
    for idx, file_path in enumerate(files_to_review, start=1):
        rel_name = file_path.name
        
        if total_files > 1:
            formatter.console.print(f"─────────────────────────────────────────────────────────────")
            formatter.console.print(f"📄 [bold yellow]File [{idx}/{total_files}]:[/bold yellow] [bold white]{rel_name}[/bold white]")
        else:
            formatter.print_file_info(rel_name)

        # Measure file read time
        t_read_start = time.perf_counter()
        try:
            content, filename = read_source_file(file_path)
        except Exception as e:
            formatter.print_warning(f"Skipping '{rel_name}': {str(e)}")
            continue
        read_duration = time.perf_counter() - t_read_start

        # Execute API query in a background thread while displaying live elapsed timer spinner
        try:
            start_t = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    reviewer.review_code,
                    content,
                    filename,
                    severity=args.severity,
                    refactor=args.refactor,
                )

                with formatter.console.status(
                    f"[bold cyan]🤖 Requesting Gemini API ({args.model})... 0.0s[/bold cyan]",
                    spinner="dots"
                ) as status:
                    while not future.done():
                        time.sleep(0.1)
                        elapsed = time.perf_counter() - start_t
                        status.update(f"[bold cyan]🤖 Requesting Gemini API ({args.model})... {elapsed:.1f}s[/bold cyan]")

                review_markdown, api_duration = future.result(timeout=120)

            # Warning if API call exceeded 60s threshold
            if api_duration > 60.0:
                formatter.print_warning(f"Gemini API call took {api_duration:.1f}s (exceeded 60s threshold).")

            # Parse issue counts and strip summary tag
            cleaned_markdown, issue_counts = parse_review_summary(review_markdown)
            total_bugs += issue_counts["bugs"]
            total_security += issue_counts["security"]
            total_bad_practices += issue_counts["bad_practices"]
            if issue_counts["total"] == 0:
                clean_files_count += 1

            # Render markdown review results
            t_render_start = time.perf_counter()
            formatter.render_markdown_review(cleaned_markdown, filename)
            render_duration = time.perf_counter() - t_render_start

            # Print exact performance metrics
            formatter.console.print(
                f"⏱️ [dim]Performance Log ({rel_name}): File Read: {read_duration*1000:.1f}ms | "
                f"Gemini API: {api_duration:.2f}s | Terminal Render: {render_duration*1000:.1f}ms[/dim]"
            )

        except concurrent.futures.TimeoutError:
            formatter.print_error(f"Failed to review '{rel_name}': Gemini API request timed out (>120s).")
        except Exception as e:
            formatter.print_error(f"Failed to review '{rel_name}': {str(e)}")

    # Print summary box panel
    formatter.print_summary_box(
        total_files=total_files,
        clean_files_count=clean_files_count,
        total_bugs=total_bugs,
        total_security=total_security,
        total_bad_practices=total_bad_practices
    )

    total_session_time = time.perf_counter() - session_start_time
    formatter.console.print(f"\n⌛ [dim white]Total Session Elapsed Time: {total_session_time:.2f}s[/dim white]")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        formatter.print_warning("\nCode review cancelled by user.")
        sys.exit(0)
