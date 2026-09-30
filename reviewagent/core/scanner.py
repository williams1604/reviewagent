"""
scanner.py
----------
Reusable project and source file scanner for ReviewAgent.
Handles single files, folder recursion, ignored directories, and language detection.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Set, Union, Optional
from reviewagent.languages.detector import LanguageDetector, LanguageInfo
from reviewagent.config import DEFAULT_EXCLUDED_DIRS


@dataclass
class ScannedFile:
    """
    Representation of a scanned file with its path and detected language.
    """
    path: Path
    relative_path: str
    language: LanguageInfo


class ProjectScanner:
    """
    Scans single files or project directories recursively for source code files,
    excluding specified dependency or generated directories.
    """

    def __init__(self, excluded_dirs: Optional[Set[str]] = None):
        """
        Initializes the ProjectScanner with optional custom excluded directories.
        """
        self.excluded_dirs = excluded_dirs if excluded_dirs is not None else DEFAULT_EXCLUDED_DIRS

    def scan(self, target_path_str: Union[str, Path], file_extension: Optional[str] = None) -> List[ScannedFile]:
        """
        Scans target path and returns list of ScannedFile objects.

        Parameters:
            target_path_str: Path to a file or folder.
            file_extension: Optional extension filter (e.g. '.py'). If None, scans all supported language files.

        Returns:
            List[ScannedFile]: Sorted list of discovered source files.

        Raises:
            FileNotFoundError: If the target path does not exist.
            ValueError: If target path is valid but contains no matching source files.
        """
        path = Path(target_path_str).resolve()

        if not path.exists():
            raise FileNotFoundError(f"Path not found: '{target_path_str}'. Please check the path and try again.")

        # Single file scan
        if path.is_file():
            lang_info = LanguageDetector.detect(path)
            return [ScannedFile(path=path, relative_path=path.name, language=lang_info)]

        # Folder directory scan
        if path.is_dir():
            scanned_files: List[ScannedFile] = []

            # Determine match pattern
            pattern = f"*{file_extension}" if file_extension else "*"

            for p in path.rglob(pattern):
                if p.is_file():
                    # Check if file resides in any excluded directory
                    parts = set(p.parts)
                    if parts.intersection(self.excluded_dirs):
                        continue

                    lang_info = LanguageDetector.detect(p)
                    # If specific extension was asked OR language is supported/known
                    if file_extension or lang_info.is_supported:
                        rel_path = str(p.relative_to(path))
                        scanned_files.append(ScannedFile(
                            path=p,
                            relative_path=rel_path,
                            language=lang_info
                        ))

            # Sort alphabetically by path for consistent ordering
            scanned_files.sort(key=lambda sf: sf.path)

            if not scanned_files:
                raise ValueError(
                    f"No supported source files found inside folder '{path.name}'. "
                    f"Ignored directories: {', '.join(sorted(self.excluded_dirs))}"
                )

            return scanned_files

        raise FileNotFoundError(f"Invalid path type: '{target_path_str}'")


def read_file_content(file_path: Path) -> tuple[str, str]:
    """
    Safely reads text content from a file using UTF-8 encoding.
    """
    path = Path(file_path).resolve()

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: '{path.name}'")

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"Could not read '{path.name}' as UTF-8 text.")
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to read file '{path.name}'.")

    if not content.strip():
        raise ValueError(f"The file '{path.name}' is empty. Nothing to review!")

    return content, path.name
