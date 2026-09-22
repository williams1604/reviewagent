# 🤖 reviewagent

**AI-powered code review, right in your terminal.**

`reviewagent` scans your Python files and folders using Google's Gemini API and instantly reports bugs, security vulnerabilities, and bad practices — like having a senior developer review your code before you push it.

```
╭────────────────────────────────╮
│  🤖 AI Code Reviewer Agent     │
│  Powered by Google Gemini API  │
╰────────────────────────────────╯
🎚️ Severity Level: HIGH

📄 Target File: sample_test.py
╭──────────────────── 🔍 Code Review Results ────────────────────╮
│  🚨 Critical Bugs & Logic Errors                                │
│   • Unhandled ZeroDivisionError in calc()                       │
│  🔒 Security Weaknesses                                         │
│   • Hardcoded credentials found in source code                 │
╰──────────────────────────────────────────────────────────────╯
```

---

## ✨ Features

- **Instant AI code review** — powered by Gemini, right in your terminal
- **Single file or whole folder** — review one file or recursively scan an entire project
- **Severity filtering** — focus on what matters with `--severity low / medium / high`
- **Fast Mode by default** — concise, quick reviews; add `--refactor` when you want a full rewritten version of your code
- **Clean, styled output** — powered by [`rich`](https://github.com/Textualize/rich) for readable, color-coded terminal reports
- **Zero config to get started** — works out of the box with just an API key

---

## 📦 Installation

```bash
git clone https://github.com/williams1604/reviewagent.git
cd reviewagent
pip install -e .
```

This installs the `reviewagent` command globally in your environment.

---

## 🔑 Setup

`reviewagent` uses the Gemini API to power its reviews. You'll need a free API key:

1. Go to [Google AI Studio](https://aistudio.google.com/) and sign in
2. Click **"Get API key"** and copy the generated key
3. Set it as an environment variable:

```bash
# macOS / Linux
export GEMINI_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```

> Your key is never stored or transmitted anywhere except directly to Google's API. It is never read, logged, or included in this project.

---

## 🚀 Usage

**Review a single file:**
```bash
reviewagent myfile.py
```

**Review an entire folder:**
```bash
reviewagent ./my_project
```

**Filter by severity:**
```bash
reviewagent myfile.py --severity high     # critical bugs & security only
reviewagent myfile.py --severity medium   # + bad practices
reviewagent myfile.py --severity low      # full detailed review (default)
```

**Get a full rewritten version of your code:**
```bash
reviewagent myfile.py --refactor
```

---

## 🗺️ Roadmap

- [ ] Configurable rules via a `.reviewconfig` file
- [ ] End-of-scan summary report for multi-file reviews
- [ ] Support for additional languages beyond Python
- [ ] CI/CD integration (GitHub Actions)

Have an idea? Open an issue — contributions and suggestions are welcome!

---

## 🤝 Contributing

Contributions are welcome and appreciated!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Open a pull request

Look for issues labeled `good first issue` if you're new to the project.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋 Author

Built by [williams1604](https://github.com/williams1604) — feedback, issues, and stars are always appreciated! ⭐
