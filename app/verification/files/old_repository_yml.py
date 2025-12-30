from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryOldFileRepositoryYMLVerification(VerificationInterface):
    KEY = 'git.repository.file.repository-yml'
    RULE_DESCRIPTION = "Verifica se existe o repository.yml na raiz do repo, falha se existir"
    SEVERITY = Severity.WARNING

    PASSED = RepoVerificationResult.passed(
        KEY,
        RULE_DESCRIPTION,
        SEVERITY
    )

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        file_name = 'repository.yml'
        file_data: str | None = GithubClient.get_file(repository.url, file_name)

        if file_data is None:
            return cls.PASSED

        return RepoVerificationResult.failure(
            cls.KEY,
            cls.RULE_DESCRIPTION,
            cls.SEVERITY,
            f'Repo com o {file_name}')
