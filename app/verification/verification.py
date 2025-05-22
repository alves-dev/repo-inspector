from abc import ABC, abstractmethod

from app.github.models import Repository
from app.verification.model import RepoVerificationResult


class VerificationInterface(ABC):

    @classmethod
    @abstractmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        """Deve retornar um RepoVerificationResult indicando a regra e se foi ou não aprovado"""
        pass
