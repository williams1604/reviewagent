# ReviewAgent Modular Architecture

ReviewAgent is designed as a modular, extensible code-review platform. Phase 1 establishes the foundational abstractions and core systems.

## Component Overview

```
reviewagent/
│
├── reviewagent/
│   ├── cli/
│   │   └── main.py           # CLI entry point, argument parsing, execution loop
│   │
│   ├── core/
│   │   ├── scanner.py        # Single-file and folder recursive project scanner
│   │   ├── finding.py        # Structured Finding model and Severity levels
│   │   └── aggregator.py     # Aggregates findings and summary metrics
│   │
│   ├── agents/
│   │   └── base.py           # BaseAgent interface and GeminiReviewAgent implementation
│   │
│   ├── languages/
│   │   └── detector.py       # LanguageDetector identifying file types & languages
│   │
│   ├── reports/
│   │   └── terminal.py       # Rich-based terminal reporting engine
│   │
│   └── config.py             # Configuration model & .reviewconfig.json loader
│
├── tests/                    # Pytest test suite
├── examples/                 # Sample configuration files
├── docs/                     # Architecture documentation
└── README.md
```

## Key Abstractions

### 1. BaseAgent (`reviewagent/agents/base.py`)
Defines the `BaseAgent` abstract base class. All future specialized agents (e.g. `SecurityAgent`, `BugAgent`, `CodeQualityAgent`, `PerformanceAgent`) will extend `BaseAgent` and implement `analyze()`.

### 2. LanguageDetector (`reviewagent/languages/detector.py`)
Identifies source code language based on file extension and returns a `LanguageInfo` object containing language name, extension, support status, and description.

### 3. ProjectScanner (`reviewagent/core/scanner.py`)
Discovers source files recursively, ignoring virtual environments (`.venv`, `venv`), VCS metadata (`.git`), dependency directories (`node_modules`), and build artifacts (`build`, `dist`, `__pycache__`).

### 4. Finding & Severity (`reviewagent/core/finding.py`)
Defines the structured `Finding` model (`severity`, `category`, `message`, `file`, `line_number`, `explanation`, `recommendation`, `suggested_fix`) and `Severity` enum (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`).

### 5. ReviewConfig (`reviewagent/config.py`)
Loads settings from `.reviewconfig` or `.reviewconfig.json` in the working directory or falls back to sensible defaults.
