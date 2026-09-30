"""
base.py
-------
Base interface and abstractions for ReviewAgent review agents.
Provides the foundation for specialized code review agents (e.g. GeminiReviewAgent,
and future SecurityAgent, BugAgent, CodeQualityAgent, PerformanceAgent).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from reviewagent.core.finding import Finding


@dataclass
class AgentResult:
    """
    Structured result returned by a review agent analysis.
    """
    agent_name: str
    findings: List[Finding] = field(default_factory=list)
    raw_markdown: str = ""
    duration_seconds: float = 0.0
    issue_counts: dict = field(default_factory=lambda: {"bugs": 0, "security": 0, "bad_practices": 0, "total": 0})


class BaseAgent(ABC):
    """
    Abstract base class for all code review agents in ReviewAgent.
    """

    def __init__(self, name: str, description: str, supported_languages: List[str]):
        self.name = name
        self.description = description
        self.supported_languages = supported_languages

    @abstractmethod
    def analyze(
        self,
        code_content: str,
        filename: str,
        severity: str = "LOW",
        refactor: bool = False
    ) -> AgentResult:
        """
        Analyzes source code content and returns structured AgentResult containing findings.
        """
        pass

    def supports_language(self, language_name: str) -> bool:
        """
        Checks if the agent supports reviewing the specified programming language.
        """
        if "*" in self.supported_languages:
            return True
        return language_name in self.supported_languages


class GeminiReviewAgent(BaseAgent):
    """
    ReviewAgent implementation powered by Google Gemini API.
    Adapts existing CodeReviewer API client into the BaseAgent modular foundation.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
        super().__init__(
            name="GeminiAIReviewer",
            description="General code review agent powered by Google Gemini API",
            supported_languages=["Python", "Java", "JavaScript", "TypeScript"]
        )
        from ai_code_reviewer.reviewer import CodeReviewer, parse_review_summary
        self.reviewer = CodeReviewer(api_key=api_key, model_name=model_name)
        self.parse_summary = parse_review_summary

    def analyze(
        self,
        code_content: str,
        filename: str,
        severity: str = "LOW",
        refactor: bool = False
    ) -> AgentResult:
        """
        Executes Gemini API review and returns structured AgentResult.
        """
        review_markdown, duration = self.reviewer.review_code(
            code_content=code_content,
            filename=filename,
            severity=severity,
            refactor=refactor
        )

        cleaned_markdown, issue_counts = self.parse_summary(review_markdown)

        return AgentResult(
            agent_name=self.name,
            findings=[],  # Future specialized agents populate structured Finding models here
            raw_markdown=cleaned_markdown,
            duration_seconds=duration,
            issue_counts=issue_counts
        )
