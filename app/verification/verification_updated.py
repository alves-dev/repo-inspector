from datetime import datetime, timezone

from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


class ProjectUpdatedVerification(VerificationInterface):
    KEY = 'git.project.updated'
    DESCRIPTION = 'Verifica se projeto tem muitos dias sem atualização'
    DAYS = 100

    PASSED = [RepoVerificationResult.of_passed(KEY, '')]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        # Converte pra datetime (formato ISO 8601 com Zulu time)
        data = datetime.strptime(repository.updated_at, '%Y-%m-%dT%H:%M:%SZ')
        data = data.replace(tzinfo=timezone.utc)

        today = datetime.now(timezone.utc)
        diff = (today - data).days

        if diff > cls.DAYS:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Repo a mais de 100 dias sem atualização')]

        return cls.PASSED
