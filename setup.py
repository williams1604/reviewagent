"""
setup.py
--------
Python packaging setup file for `reviewagent`.
Registers the global `reviewagent` terminal command and specifies package dependencies.
"""

from setuptools import setup, find_packages

setup(
    name="reviewagent",
    version="0.2.0",
    author="Senior AI Pair Programmer",
    description="An extensible multi-language AI code review platform powered by Gemini API.",
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
            "reviewagent = reviewagent.cli.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
