import pytest
from pathlib import Path
from reviewagent.core.scanner import ProjectScanner


def test_scan_single_file(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text("print('hello world')", encoding="utf-8")

    scanner = ProjectScanner()
    results = scanner.scan(f)

    assert len(results) == 1
    assert results[0].path.resolve() == f.resolve()
    assert results[0].language.name == "Python"


def test_scan_directory(tmp_path):
    sub1 = tmp_path / "sub1"
    sub1.mkdir()
    (sub1 / "main.py").write_text("def foo(): pass", encoding="utf-8")
    (sub1 / "app.js").write_text("console.log('hi')", encoding="utf-8")

    scanner = ProjectScanner()
    results = scanner.scan(tmp_path)

    assert len(results) == 2
    names = [r.path.name for r in results]
    assert "main.py" in names
    assert "app.js" in names


def test_scan_ignored_directories(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "ignored.py").write_text("pass", encoding="utf-8")

    node_dir = tmp_path / "node_modules"
    node_dir.mkdir()
    (node_dir / "package.js").write_text("pass", encoding="utf-8")

    valid_dir = tmp_path / "src"
    valid_dir.mkdir()
    (valid_dir / "valid.py").write_text("print('valid')", encoding="utf-8")

    scanner = ProjectScanner()
    results = scanner.scan(tmp_path)

    assert len(results) == 1
    assert results[0].path.name == "valid.py"


def test_scan_nonexistent_path():
    scanner = ProjectScanner()
    with pytest.raises(FileNotFoundError):
        scanner.scan("non_existent_folder_xyz_123")
