"""
detector.py
-----------
Language detection foundation for identifying programming languages based on file extensions.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Union, Dict


@dataclass(frozen=True)
class LanguageInfo:
    """
    Structured representation of language detection results.
    """
    name: str
    extension: str
    is_supported: bool
    description: str = ""


EXTENSION_MAP: Dict[str, tuple[str, bool, str]] = {
    ".py": ("Python", True, "Python Source File"),
    ".java": ("Java", True, "Java Source File"),
    ".js": ("JavaScript", True, "JavaScript Source File"),
    ".jsx": ("JavaScript", True, "JavaScript React File"),
    ".ts": ("TypeScript", True, "TypeScript Source File"),
    ".tsx": ("TypeScript/React", True, "TypeScript React File"),
}


class LanguageDetector:
    """
    Detects the programming language of a given file based on file path or extension.
    """

    @staticmethod
    def detect(file_path_or_ext: Union[str, Path]) -> LanguageInfo:
        """
        Detects language based on file extension or filename.

        Examples:
            LanguageDetector.detect("sample.py") -> LanguageInfo(name="Python", extension=".py", is_supported=True, ...)
            LanguageDetector.detect("App.tsx") -> LanguageInfo(name="TypeScript/React", extension=".tsx", is_supported=True, ...)
            LanguageDetector.detect("style.css") -> LanguageInfo(name="Unknown", extension=".css", is_supported=False, ...)
        """
        path = Path(file_path_or_ext)
        ext = path.suffix.lower()

        if ext in EXTENSION_MAP:
            name, supported, desc = EXTENSION_MAP[ext]
            return LanguageInfo(
                name=name,
                extension=ext,
                is_supported=supported,
                description=desc
            )

        return LanguageInfo(
            name="Unknown",
            extension=ext if ext else "none",
            is_supported=False,
            description="Unsupported or unknown file type"
        )
