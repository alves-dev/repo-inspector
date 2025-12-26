from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Set
from typing import Optional


@dataclass
class InspectorConfig:
    github_topics: List[str]
    ignored_rules_by_repo: Dict[str, Set[str]]
    max_days_without_update: int
    repo_yml: dict

class Severity(str, Enum):
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class RepoVerificationResult:
    key: str
    rule_description: str
    passed: bool
    failure_reason: Optional[str] = None
    severity: Severity = Severity.WARNING

    @staticmethod
    def passed(
            key: str,
            rule_description: str,
            severity: Severity
    ) -> "RepoVerificationResult":
        return RepoVerificationResult(
            key=key,
            rule_description=rule_description,
            passed=True,
            severity=severity
        )

    @staticmethod
    def failure(
            key: str,
            rule_description: str,
            severity: Severity,
            failure_reason: str
    ) -> "RepoVerificationResult":
        return RepoVerificationResult(
            key=key,
            rule_description=rule_description,
            passed=False,
            severity=severity,
            failure_reason=failure_reason
        )
