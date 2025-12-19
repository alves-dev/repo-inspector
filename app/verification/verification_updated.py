from datetime import datetime, timezone

from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryUpdatedVerification(VerificationInterface):
    KEY = 'git.repository.updated'
    RULE_DESCRIPTION = 'Verifica se o repositorio tem muitos dias sem atualização'
    SEVERITY = Severity.WARNING

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        # Converte pra datetime (formato ISO 8601 com Zulu time)
        data = datetime.strptime(repository.updated_at, '%Y-%m-%dT%H:%M:%SZ')
        data = data.replace(tzinfo=timezone.utc)

        today = datetime.now(timezone.utc)
        diff = (today - data).days

        if diff > config.max_days_without_update:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Repo a mais de 100 dias sem atualização"
            )

        return RepoVerificationResult.passed(
            cls.KEY,
            cls.RULE_DESCRIPTION,
            cls.SEVERITY
        )
