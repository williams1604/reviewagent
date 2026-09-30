"""
config.py
---------
Configuration management for ReviewAgent. Handles default settings and supports
optional configuration loading from `.reviewconfig` or `.reviewconfig.json` files.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set, Optional, Dict, Any


DEFAULT_EXCLUDED_DIRS: Set[str] = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "build", "dist", ".idea", ".vscode"
}

DEFAULT_ENABLED_CATEGORIES: List[str] = [
    "bugs", "security", "bad_practices", "performance", "quality"
]

DEFAULT_SUPPORTED_LANGUAGES: List[str] = [
    "Python", "Java", "JavaScript", "TypeScript"
]


@dataclass
class ReviewConfig:
    """
    Configuration model holding review settings and user preferences.
    """
    enabled_categories: List[str] = field(default_factory=lambda: list(DEFAULT_ENABLED_CATEGORIES))
    min_severity: str = "LOW"
    excluded_dirs: Set[str] = field(default_factory=lambda: set(DEFAULT_EXCLUDED_DIRS))
    supported_languages: List[str] = field(default_factory=lambda: list(DEFAULT_SUPPORTED_LANGUAGES))
    default_model: str = "gemini-3.6-flash"

    def to_dict(self) -> Dict[str, Any]:
        """Converts configuration object to dictionary format."""
        return {
            "enabled_categories": self.enabled_categories,
            "min_severity": self.min_severity,
            "excluded_dirs": list(self.excluded_dirs),
            "supported_languages": self.supported_languages,
            "default_model": self.default_model,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReviewConfig":
        """Constructs ReviewConfig instance from a dictionary."""
        config = cls()
        if "enabled_categories" in data and isinstance(data["enabled_categories"], list):
            config.enabled_categories = data["enabled_categories"]
        if "min_severity" in data and isinstance(data["min_severity"], str):
            config.min_severity = data["min_severity"].upper()
        if "excluded_dirs" in data and isinstance(data["excluded_dirs"], list):
            config.excluded_dirs = set(data["excluded_dirs"])
        if "supported_languages" in data and isinstance(data["supported_languages"], list):
            config.supported_languages = data["supported_languages"]
        if "default_model" in data and isinstance(data["default_model"], str):
            config.default_model = data["default_model"]
        return config


def load_config(config_file_path: Optional[Path] = None) -> ReviewConfig:
    """
    Loads configuration settings from disk or returns default configuration.

    Looks for specified `config_file_path`, `.reviewconfig`, or `.reviewconfig.json` in the current working directory.
    If no configuration file is found, returns standard default ReviewConfig.
    """
    candidates = []
    if config_file_path:
        candidates.append(Path(config_file_path))
    else:
        cwd = Path.cwd()
        candidates.append(cwd / ".reviewconfig")
        candidates.append(cwd / ".reviewconfig.json")

    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            try:
                content = candidate.read_text(encoding="utf-8").strip()
                if not content:
                    continue
                data = json.loads(content)
                return ReviewConfig.from_dict(data)
            except Exception:
                # Fallback gracefully to default config if file parsing fails
                pass

    return ReviewConfig()
