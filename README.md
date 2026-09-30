# 🤖 ReviewAgent

> **AI-powered code review, right in your terminal.**

`reviewagent` scans your source code files and folders using Google's Gemini API and instantly reports bugs, security vulnerabilities, and bad practices — like having a senior developer review your code before you push it.

---

## ✨ CURRENT FEATURES (Phase 1)

* 📄 **Single-File & Folder Scanning**: Review individual source code files or recursively scan entire project directories.
* 🌐 **Language Detection Foundation**: Automatically identifies **Python** (`.py`), **Java** (`.java`), **JavaScript** (`.js`, `.jsx`), and **TypeScript** (`.ts`, `.tsx`).
* 🎚️ **Severity Filtering**: Filter review depth using `--severity` (`low`, `medium`, `high`, `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`).
* 💡 **Fast Mode & Optional Refactoring**: Concise bulleted summary suggestions by default, or full refactored code snippets with `--refactor`.
* ⚙️ **Config File Support**: Customize settings via `.reviewconfig` or `.reviewconfig.json` in your project root.
* 📊 **Summary Box**: Colorized Rich panel showing total issues found, category breakdowns (bugs, security, bad practices), and folder zero-issue stats.
* 🧱 **Modular Platform Architecture**: Reusable base review agent abstractions (`BaseAgent`), structured finding model (`Finding`, `Severity`), and clean component separation (`scanner`, `detector`, `aggregator`, `reporter`).

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/williams1604/reviewagent.git
cd reviewagent

# Install in editable mode
pip install -e .
```

This installs the `reviewagent` CLI command globally in your environment.

---

## 🔑 Setup

`reviewagent` uses the Gemini API to power its reviews. You will need a Gemini API key:

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/)
2. Set it as an environment variable in your shell:

**PowerShell (Windows):**
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

**Bash / Zsh (Linux / macOS):**
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

> Your key is never stored or transmitted anywhere except directly to Google's API.

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
  "enabled_categories": ["bugs", "security", "bad_practices", "performance", "quality"],
  "excluded_dirs": [".git", ".venv", "venv", "__pycache__", "node_modules", "build", "dist", ".idea", ".vscode"],
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

## 🗺️ FUTURE ROADMAP (Phase 2+)

- 🛡️ **Specialized Review Agents**: `SecurityAgent`, `BugAgent`, `CodeQualityAgent`, `PerformanceAgent`
- 🤖 **Multi-Agent Orchestration**: Parallel evaluation using specialized prompt agents
- 📝 **HTML & JSON Report Generation**: Export review reports to `.html` or `.json` files
- 🐙 **GitHub Actions & PR Integration**: Automated PR review bot posting inline PR comments
- 📦 **PyPI Distribution**: Official package distribution on PyPI

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋 Author

Built by [williams1604](https://github.com/williams1604) — feedback, issues, and stars are always appreciated! ⭐
