from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryDescriptionVerification(VerificationInterface):
    KEY = "git.repository.description"
    RULE_DESCRIPTION = "Verifica se o repositório possui uma descrição válida"
    SEVERITY = Severity.ERROR

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        repo: dict = GithubClient.get_repo_by_url(repository.url)

        description = repo.get('description', "")

        if description is None:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Repositório sem descrição"
            )

        if len(description) < 15:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Descrição com menos de 15 caracteres"
            )

        return RepoVerificationResult.passed(
            cls.KEY,
            cls.RULE_DESCRIPTION,
            cls.SEVERITY
        )
