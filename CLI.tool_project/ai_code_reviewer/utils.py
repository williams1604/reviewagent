"""
utils.py
--------
Helper functions for discovering, validating, and reading source code files safely.

Why we need this module:
When a user passes a file or folder path to our CLI tool, several things can happen:
1. The path might be a single file (e.g., `myfile.py`).
2. The path might be a folder containing multiple Python files (e.g., `./src`).
3. The path might not exist, or the file might be empty / non-text binary data.

This module encapsulates all path discovery and file safety checks cleanly so the CLI
never crashes unexpectedly.
"""

from pathlib import Path
from typing import Tuple, List

# Folders we automatically ignore when scanning a project folder so we don't waste AI API calls
DEFAULT_IGNORE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", "build", "dist", ".idea", ".vscode"
}


def discover_source_files(target_path_str: str, file_extension: str = ".py") -> List[Path]:
    """
    Scans a target path and returns a list of source code files to review.

    How it works:
    - Uses Python's standard `pathlib.Path` to handle Windows/Mac/Linux path formats seamlessly.
    - If `target_path_str` points to a single file, it returns a list with just that file.
    - If `target_path_str` points to a folder, it uses `rglob()` to recursively search for `.py` files,
      filtering out hidden/virtualenv directories automatically.

    Parameters:
        target_path_str (str): The file or folder path passed by the user.
        file_extension (str): The extension to match when scanning folders (default: '.py').

    Returns:
        List[Path]: A sorted list of `pathlib.Path` objects for all target files.

    Raises:
        FileNotFoundError: If the input path does not exist on disk.
        ValueError: If no matching `.py` files are found inside a target folder.
    """
    # Convert string path to a Path object and get its absolute full path
    path = Path(target_path_str).resolve()

    # Step 1: Verify path exists on disk
    if not path.exists():
        raise FileNotFoundError(f"Path not found: '{target_path_str}'. Please check the path and try again.")

    # Step 2: Handle Single File case
    if path.is_file():
        return [path]

    # Step 3: Handle Folder directory case — recursive scan
    if path.is_dir():
        found_files: List[Path] = []

        # rglob(f"*{file_extension}") recursively finds all matching files in subfolders
        for p in path.rglob(f"*{file_extension}"):
            # Skip any file that lives inside an ignored directory (like venv or .git)
            parts = set(p.parts)
            if not parts.intersection(DEFAULT_IGNORE_DIRS):
                found_files.append(p)

        # Sort files alphabetically for clean, predictable CLI output
        found_files.sort()

        if not found_files:
            raise ValueError(
                f"No '{file_extension}' source files found inside folder '{path.name}'. "
                f"Ignored directories: {', '.join(sorted(DEFAULT_IGNORE_DIRS))}"
            )

        return found_files

    raise FileNotFoundError(f"Invalid path type: '{target_path_str}'")


def read_source_file(file_path: Path) -> Tuple[str, str]:
    """
    Safely reads the text content of a single target file.

    How it works:
    - Reads text using UTF-8 encoding (the standard encoding for code).
    - Checks for permission issues, binary non-text files, or empty files.

    Parameters:
        file_path (Path): Path object pointing to the file.

    Returns:
        Tuple[str, str]: (text_content, simple_filename)

    Raises:
        FileNotFoundError: If file is missing.
        ValueError: If file is empty or cannot be read as text.
        PermissionError: If file permissions prevent reading.
    """
    path = Path(file_path).resolve()

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: '{path.name}'")

    try:
        # Read full file contents as string with UTF-8 encoding
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"Could not read '{path.name}' as UTF-8 text. Make sure it is a valid source code file.")
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to read file '{path.name}'.")

    # Ensure file isn't completely empty or just whitespace
    if not content.strip():
        raise ValueError(f"The file '{path.name}' is empty. Nothing to review!")

    return content, path.name
