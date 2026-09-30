from pathlib import Path
from reviewagent.languages.detector import LanguageDetector, LanguageInfo


def test_detect_python():
    info = LanguageDetector.detect("script.py")
    assert info.name == "Python"
    assert info.extension == ".py"
    assert info.is_supported is True


def test_detect_java():
    info = LanguageDetector.detect("Main.java")
    assert info.name == "Java"
    assert info.extension == ".java"
    assert info.is_supported is True


def test_detect_javascript():
    info = LanguageDetector.detect("app.js")
    assert info.name == "JavaScript"
    assert info.extension == ".js"
    assert info.is_supported is True


def test_detect_typescript():
    info = LanguageDetector.detect("index.ts")
    assert info.name == "TypeScript"
    assert info.extension == ".ts"
    assert info.is_supported is True

    info_tsx = LanguageDetector.detect("Component.tsx")
    assert info_tsx.name == "TypeScript/React"
    assert info_tsx.extension == ".tsx"
    assert info_tsx.is_supported is True


def test_detect_unknown():
    info = LanguageDetector.detect("document.pdf")
    assert info.name == "Unknown"
    assert info.is_supported is False
