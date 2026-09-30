import sys
import pytest
from reviewagent.cli.main import parse_arguments


def test_cli_parse_default_arguments(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["reviewagent", "sample_test.py"])
    args = parse_arguments()

    assert args.target_path == "sample_test.py"
    assert args.severity == "low"
    assert args.refactor is False
    assert args.model == "gemini-3.6-flash"


def test_cli_parse_custom_flags(monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "reviewagent", "./my_folder",
        "--severity", "high",
        "--refactor",
        "--model", "gemini-1.5-flash",
        "--config", ".customconfig.json"
    ])
    args = parse_arguments()

    assert args.target_path == "./my_folder"
    assert args.severity == "high"
    assert args.refactor is True
    assert args.model == "gemini-1.5-flash"
    assert args.config == ".customconfig.json"
