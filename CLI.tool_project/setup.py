"""
setup.py
--------
Python packaging setup file for `ai-code-reviewer`.

Why we need this file:
1. It tells Python's package manager (`pip`) how to install our tool on any computer.
2. It creates a global terminal command `reviewagent` so users don't have to type `python -m ai_code_reviewer.cli`.
3. It lists external package dependencies so `pip` installs them automatically.
"""

from setuptools import setup, find_packages

setup(
    name="ai-code-reviewer",
    version="0.1.0",
    author="Senior AI Pair Programmer",
    description="An AI-powered CLI code reviewer that analyzes code files for bugs, security risks, and best practices using Gemini API.",
    long_description=open("README.md", "r", encoding="utf-8").read() if open("README.md", "a").closed else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "google-genai>=0.1.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            # This creates the terminal shortcut command 'reviewagent' pointing to main() in cli.py
            "reviewagent = ai_code_reviewer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
