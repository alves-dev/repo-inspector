from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


class ProjectLicenseVerification(VerificationInterface):
    KEY = 'git.project.license'
    DESCRIPTION = "Verifica se existe uma licença para repos públicos"

    PASSED = [RepoVerificationResult.of_passed(KEY, '')]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        repo: dict = GithubClient.get_repo_by_url(repository.url)
        repo_license = repo.get('license', '')

        if repository.private:
            return cls.PASSED

        if repo_license is None:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Repo sem licença.')]

        return cls.PASSED
