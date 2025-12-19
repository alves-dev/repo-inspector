from abc import ABC, abstractmethod

from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig


class VerificationInterface(ABC):
    KEY: str
    RULE_DESCRIPTION: str
    SEVERITY: Severity

    @classmethod
    @abstractmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        """Deve retornar um RepoVerificationResult indicando a regra e se foi ou não aprovado"""
        pass
