"""Result schema for grading system."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TestResult:
    """Individual test result."""

    name: str
    passed: bool
    error: Optional[str] = None


@dataclass
class GradingResult:
    """Complete grading result for an exercise."""

    score: int
    total_tests: int
    passed_tests: int
    test_results: List[TestResult]
    status: str
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "score": self.score,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "test_results": [{"name": tr.name, "passed": tr.passed, "error": tr.error} for tr in self.test_results],
            "status": self.status,
            "error": self.error,
        }
