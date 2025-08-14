"""Result schema for grading system."""

from dataclasses import dataclass
from typing import Any


@dataclass
class TestResult:
    """Individual test result."""

    name: str
    passed: bool
    error: str | None = None


@dataclass
class GradingResult:
    """Complete grading result for an exercise."""

    score: int
    total_tests: int
    passed_tests: int
    test_results: list[TestResult]
    status: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "score": self.score,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "test_results": [
                {"name": tr.name, "passed": tr.passed, "error": tr.error}
                for tr in self.test_results
            ],
            "status": self.status,
            "error": self.error,
        }
