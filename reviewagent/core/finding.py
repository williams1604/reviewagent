"""
finding.py
----------
Structured finding models and severity levels for code review results.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


class Severity(str, Enum):
    """
    Standard severity levels supported by ReviewAgent.
    """
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

    @classmethod
    def from_str(cls, val: str) -> "Severity":
        """Converts string representation safely to a Severity enum member."""
        normalized = val.strip().upper()
        for member in cls:
            if member.value == normalized:
                return member
        return cls.LOW


@dataclass
class Finding:
    """
    Structured code review finding model representing a single detected issue.
    """
    severity: Severity
    category: str
    message: str
    file: str
    line_number: Optional[int] = None
    explanation: str = ""
    recommendation: str = ""
    suggested_fix: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts Finding object into dictionary representation."""
        return {
            "severity": self.severity.value,
            "category": self.category,
            "message": self.message,
            "file": self.file,
            "line_number": self.line_number,
            "explanation": self.explanation,
            "recommendation": self.recommendation,
            "suggested_fix": self.suggested_fix,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Finding":
        """Constructs a Finding instance from a dictionary."""
        severity_val = data.get("severity", "LOW")
        severity = Severity.from_str(severity_val) if isinstance(severity_val, str) else severity_val

        return cls(
            severity=severity,
            category=data.get("category", "quality"),
            message=data.get("message", ""),
            file=data.get("file", ""),
            line_number=data.get("line_number"),
            explanation=data.get("explanation", ""),
            recommendation=data.get("recommendation", ""),
            suggested_fix=data.get("suggested_fix"),
        )
