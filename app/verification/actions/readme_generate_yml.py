from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class WorkflowsFileReadmeGenerateYMLVerification(VerificationInterface):
    KEY = 'git.workflows.file.readme_generate_yml'
    RULE_DESCRIPTION = "Verifica o arquivo .github/workflows/readme-generate.yml"
    SEVERITY = Severity.ERROR

    PASSED = RepoVerificationResult.passed(
        KEY,
        RULE_DESCRIPTION,
        SEVERITY
    )

    @classmethod
    def failure(cls, message: str) -> RepoVerificationResult:
        return RepoVerificationResult.failure(
            cls.KEY,
            cls.RULE_DESCRIPTION,
            cls.SEVERITY,
            message
        )

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        file_name = '.github/workflows/readme-generate.yml'
        file_data: str | None = GithubClient.get_file(repository.url, file_name)

        if file_data is None:
            return cls.failure(f'Repo sem o {file_name}')

        return cls.PASSED
