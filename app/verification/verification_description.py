from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


class ProjectDescriptionVerification(VerificationInterface):
    KEY = 'git.project.description'
    DESCRIPTION = 'Verifica se tem uma boa descrição'

    PASSED = [RepoVerificationResult.of_passed(KEY, '')]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        repo: dict = GithubClient.get_repo_by_url(repository.url)

        description = repo.get('description', "")

        if description is None:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Sem descrição.')]

        if len(description) < 15:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Descrição com menos de 15 caracteres.')]

        return cls.PASSED
