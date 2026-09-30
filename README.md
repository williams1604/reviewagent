# 🤖 ReviewAgent

> An extensible, multi-language AI code review platform built with Python and powered by Google Gemini API.

ReviewAgent provides senior-developer level code reviews right in your terminal. It scans individual source files or entire project directories recursively, identifies programming languages, filters reviews by severity level, and presents colorized markdown reports with summary metrics.

---

## 🎯 CURRENT FEATURES (Phase 1)

* 📄 **Single-File & Folder Scanning**: Review individual source code files or recursively scan entire directories.
* 🌐 **Language Detection**: Automatically detects **Python** (`.py`), **Java** (`.java`), **JavaScript** (`.js`, `.jsx`), and **TypeScript** (`.ts`, `.tsx`).
* 🎚️ **Severity Filtering**: Filter review depth using `--severity` (`low`, `medium`, `high`, `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`).
* 💡 **Fast Mode & Optional Refactoring**: Bulleted summary suggestions by default, or full refactored code snippets with `--refactor`.
* ⚙️ **Config File Support**: Customize settings via `.reviewconfig` or `.reviewconfig.json` in your project folder.
* 📊 **Summary Box**: Colorized Rich panel showing total issues found, category breakdowns (bugs, security, bad practices), and folder zero-issue stats.
* 🧱 **Modular Architecture**: Base review agent abstractions (`BaseAgent`), structured finding model (`Finding`, `Severity`), and clean component separation (`scanner`, `detector`, `aggregator`, `reporter`).

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/williams1604/reviewagent.git
cd reviewagent

# Install in editable mode
pip install -e .
```

### 🔑 API Key Setup

ReviewAgent requires a Google Gemini API key. Set your key in your terminal environment:

**PowerShell (Windows):**
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

**Bash / Zsh (Linux / macOS):**
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

---

## 💡 Usage & Example Commands

### 1. Review a Single File
```bash
reviewagent sample_test.py
```

### 2. Review an Entire Directory
```bash
reviewagent ./sample_project
```

### 3. Filter by Severity Level
```bash
reviewagent sample_test.py --severity high
```

### 4. Enable Full Code Refactoring Mode
```bash
reviewagent sample_test.py --refactor
```

### 5. Use Custom Model or Config File
```bash
reviewagent ./my_project --model gemini-3.6-flash --config .reviewconfig.json
```

---

## ⚙️ Configuration (`.reviewconfig.json`)

You can create an optional `.reviewconfig.json` file in your project root:

```json
{
  "min_severity": "LOW",
  "default_model": "gemini-3.6-flash",
  "enabled_categories": ["bugs", "security", "bad_practices"],
  "excluded_dirs": [".git", ".venv", "venv", "__pycache__", "node_modules", "build", "dist"],
  "supported_languages": ["Python", "Java", "JavaScript", "TypeScript"]
}
```

---

## 🏗️ Project Architecture

```
reviewagent/
│
├── reviewagent/
│   ├── cli/
│   │   └── main.py           # CLI entry point & argument handler
│   ├── core/
│   │   ├── scanner.py        # Recursive project scanner & file reader
│   │   ├── finding.py        # Structured Finding model & Severity levels
│   │   └── aggregator.py     # Metrics accumulator & ReviewSummary
│   ├── agents/
│   │   └── base.py           # BaseAgent interface & GeminiReviewAgent adapter
│   ├── languages/
│   │   └── detector.py       # LanguageDetector foundation
│   ├── reports/
│   │   └── terminal.py       # Rich terminal output reporter
│   └── config.py             # Configuration loader & defaults
│
├── tests/                    # Pytest unit tests
├── examples/                 # Sample configuration files
├── docs/                     # Architecture documentation
├── setup.py                  # Package setup script
└── pyproject.toml            # Build metadata & dependency declaration
```

---

## 🧪 Running Tests

Run the full unit test suite using `pytest`:

```bash
pytest -v
```

---

## ⚠️ Current Limitations

- AST-level deep static analysis for non-Python languages is not yet included (files are reviewed via Gemini API prompt instructions).
- Parallel multi-threading across multiple files executes sequentially to stay within API rate limit quotas.

---

## 🗺️ FUTURE ROADMAP (Phase 2+)

* 🛡️ **Specialized Review Agents**: `SecurityAgent`, `BugAgent`, `CodeQualityAgent`, `PerformanceAgent`.
* 🤖 **Multi-Agent Orchestration**: Parallel evaluation using specialized prompt agents.
* 📝 **HTML & JSON Report Generation**: Export review reports to `.html` or `.json` files.
* 🐙 **GitHub Actions & PR Integration**: Automated PR review bot posting inline PR comments.
* 🛠️ **Language AST Analysis**: Deep static analysis parsers for Java, JavaScript, and TypeScript.
* 📦 **PyPI Distribution**: Official package distribution on PyPI.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
