import re

from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


def is_kebab_case(text: str) -> bool:
    """
    Retorna True se a string estiver no formato kebab-case.
    Exemplo de válido: "meu-exemplo-de-string"
    """
    return bool(re.fullmatch(r"[a-z]+(-[a-z]+)*", text))


class RepositoryNameVerification(VerificationInterface):
    KEY = 'git.repository.name'
    RULE_DESCRIPTION = 'Verifica se segue o padrão de nomenclatura'
    SEVERITY = Severity.ERROR

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        if is_kebab_case(repository.name):
            return RepoVerificationResult.passed(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY
            )
        else:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Fora do kebab-case, Exemplo válido: meu-exemplo-de-string"
            )
