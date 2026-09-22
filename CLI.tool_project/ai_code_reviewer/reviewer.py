"""
reviewer.py
-----------
Interacts with Google's Gemini API to analyze source code files.

Why we need this module:
This module connects to the Gemini API and manages performance controls:
1. Token limits (`max_output_tokens=2000`) so responses stay fast and compact.
2. Optional refactor generation (`--refactor` flag).
3. Call duration tracking & 60-second timeout warnings.
4. Graceful 429 Rate Limit error messages with model fallback advice.
"""

import os
import time
from typing import Optional, Tuple


class CodeReviewer:
    """
    A class that manages communication with the Gemini API for reviewing code.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
        """Initializes the CodeReviewer."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model_name = model_name

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is missing!\n"
                "Please set your key before running the review tool.\n"
                "Example (PowerShell): $env:GEMINI_API_KEY='your_api_key_here'"
            )

        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        except ImportError:
            raise RuntimeError("The 'google-genai' package is missing. Run: pip install google-genai")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini API client: {str(e)}")

    def build_prompt(self, code_content: str, filename: str, severity: str = "low", refactor: bool = False) -> str:
        """
        Constructs a concise, fast-responding prompt for Gemini.
        """
        sev = severity.lower()

        if sev == "high":
            severity_instruction = (
                "Focus ONLY on critical issues:\n"
                "1. 🚨 Bugs & Logic Errors: Fatal flaws, runtime crash risks, unhandled exceptions.\n"
                "2. 🔒 Security Weaknesses: Exposed credentials or unsafe inputs to fix.\n"
                "Omit minor style choices, naming, or formatting."
            )
        elif sev == "medium":
            severity_instruction = (
                "Report functional bugs, security weaknesses, and bad practices.\n"
                "Omit minor cosmetic style preferences or non-essential refactoring."
            )
        else:
            severity_instruction = (
                "Provide a complete review covering:\n"
                "1. 🚨 Bugs & Logic Errors\n"
                "2. 🔒 Security Weaknesses\n"
                "3. ⚠️ Bad Practices & Readability"
            )

        if refactor:
            refactor_instruction = "4. 💡 Refactored Code: Provide a full rewritten code snippet fixing the issues."
        else:
            refactor_instruction = "IMPORTANT: Do NOT write full refactored source code files or large code blocks. Summarize suggestions briefly in bullet points."

        prompt = f"""
You are a helpful senior software engineer performing a code review of `{filename}`.

REVIEW INSTRUCTIONS:
{severity_instruction}
{refactor_instruction}

Keep your response concise, well-structured, and fast to read.

---
SOURCE CODE ({filename}):
```
{code_content}
```
"""
        return prompt

    def review_code(
        self, code_content: str, filename: str, severity: str = "low", refactor: bool = False
    ) -> Tuple[str, float]:
        """
        Sends code to Gemini API with max_output_tokens limit and returns (markdown, duration).
        """
        prompt = self.build_prompt(code_content, filename, severity=severity, refactor=refactor)

        start_time = time.perf_counter()

        # Configuration dictionary to cap output tokens (prevents huge slow generation)
        config_dict = {"max_output_tokens": 2000}

        try:
            if hasattr(self.client, "interactions"):
                try:
                    interaction = self.client.interactions.create(
                        model=self.model_name,
                        input=prompt,
                        config=config_dict,
                    )
                except TypeError:
                    interaction = self.client.interactions.create(
                        model=self.model_name,
                        input=prompt,
                    )
                output_text = getattr(interaction, "output_text", getattr(interaction, "text", str(interaction)))
            else:
                try:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=config_dict,
                    )
                except TypeError:
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                    )
                output_text = response.text

            api_duration = time.perf_counter() - start_time

            if not output_text:
                return "Received an empty response from Gemini API.", api_duration

            lowered = output_text.lower()
            refusal_triggers = ["cannot fulfill", "cannot perform", "against our policies", "unable to assist with security audits"]
            if any(trigger in lowered for trigger in refusal_triggers):
                return (
                    "⚠️ **Gemini declined to review this file under the requested severity level.**\n\n"
                    "Tip: Try running with `--severity low` or `--severity medium` for a broader developer review format.",
                    api_duration
                )

            return output_text, api_duration

        except Exception as e:
            api_duration = time.perf_counter() - start_time
            err_str = str(e)
            lowered_err = err_str.lower()

            # Handle Rate Limit (429) Error cleanly
            if "429" in lowered_err or "rate limit" in lowered_err or "too_many_requests" in lowered_err:
                return (
                    f"⚠️ **Gemini API Rate Limit Reached (429)**\n\n"
                    f"Your API key hit the free tier quota limit for model `{self.model_name}`.\n\n"
                    f"💡 **Solutions:**\n"
                    f"- Try using a different model: `reviewagent {filename} --model gemini-1.5-flash`\n"
                    f"- Or wait ~60 seconds for your rate limit window to reset.",
                    api_duration
                )

            refusal_triggers = ["cannot fulfill", "cannot perform", "against our policies", "declined", "blocked"]
            if any(trigger in lowered_err for trigger in refusal_triggers):
                return (
                    "⚠️ **Gemini declined to review this file under the requested severity level.**\n\n"
                    "Tip: Try running with `--severity low` or `--severity medium` for a broader developer review format.",
                    api_duration
                )
            raise RuntimeError(f"Gemini API Error: {err_str}")
