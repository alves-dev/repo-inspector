import re

from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


def is_kebab_case(text: str) -> bool:
    """
    Retorna True se a string estiver no formato kebab-case.
    Exemplo de válido: "meu-exemplo-de-string"
    """
    return bool(re.fullmatch(r"[a-z]+(-[a-z]+)*", text))


class ProjectNameVerification(VerificationInterface):
    KEY = 'git.project.name'
    DESCRIPTION = 'Verifica se segue o padrão de nomenclatura'

    PASSED = [RepoVerificationResult.of_passed(KEY, DESCRIPTION)]
    FAILURE = [RepoVerificationResult.of_failure(KEY, DESCRIPTION)]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        if is_kebab_case(repository.name):
            return cls.PASSED
        else:
            return cls.FAILURE
