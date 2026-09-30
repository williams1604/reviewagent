import json
from pathlib import Path
from reviewagent.config import ReviewConfig, load_config


def test_default_config():
    config = ReviewConfig()
    assert config.min_severity == "LOW"
    assert config.default_model == "gemini-3.6-flash"
    assert ".git" in config.excluded_dirs
    assert "Python" in config.supported_languages


def test_config_to_dict_and_from_dict():
    config = ReviewConfig(
        min_severity="HIGH",
        default_model="gemini-1.5-flash",
        excluded_dirs={".git", "custom_build"}
    )

    data = config.to_dict()
    assert data["min_severity"] == "HIGH"
    assert data["default_model"] == "gemini-1.5-flash"
    assert "custom_build" in data["excluded_dirs"]

    reloaded = ReviewConfig.from_dict(data)
    assert reloaded.min_severity == "HIGH"
    assert "custom_build" in reloaded.excluded_dirs


def test_load_config_from_file(tmp_path):
    cfg_file = tmp_path / ".reviewconfig.json"
    cfg_file.write_text(json.dumps({
        "min_severity": "MEDIUM",
        "default_model": "gemini-3.6-flash",
        "excluded_dirs": ["custom_dir"]
    }), encoding="utf-8")

    loaded = load_config(cfg_file)
    assert loaded.min_severity == "MEDIUM"
    assert "custom_dir" in loaded.excluded_dirs
