"""
aggregator.py
-------------
Aggregates findings and summary metrics across scanned files.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from reviewagent.core.finding import Finding, Severity


@dataclass
class ReviewSummary:
    """
    Summary metrics and statistics for a review run.
    """
    total_files: int = 0
    clean_files_count: int = 0
    total_bugs: int = 0
    total_security: int = 0
    total_bad_practices: int = 0
    findings: List[Finding] = field(default_factory=list)

    @property
    def total_issues(self) -> int:
        """Returns total number of issues found across all files."""
        return self.total_bugs + self.total_security + self.total_bad_practices

    @property
    def files_with_issues(self) -> int:
        """Returns number of files that contained issues."""
        return self.total_files - self.clean_files_count

    def add_file_results(self, issue_counts: Dict[str, int], file_findings: List[Finding] = None):
        """
        Updates summary counts based on file review results.
        """
        bugs = issue_counts.get("bugs", 0)
        security = issue_counts.get("security", 0)
        bad_practices = issue_counts.get("bad_practices", 0)
        total = issue_counts.get("total", bugs + security + bad_practices)

        self.total_bugs += bugs
        self.total_security += security
        self.total_bad_practices += bad_practices

        if total == 0:
            self.clean_files_count += 1

        if file_findings:
            self.findings.extend(file_findings)
