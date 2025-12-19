import yaml

from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryFileRepositoryYMLVerification(VerificationInterface):
    KEY = 'git.repository.file.repository-yml'
    RULE_DESCRIPTION = "Verifica se existe o repository.yml na raiz do repo e se é valido"
    SEVERITY = Severity.ERROR

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
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                f'Repo sem o {file_name}')

        metadata: dict = yaml.safe_load(file_data)

        # Validações da versão: V1
        required_keys = ['repository']
        repository_licenses = ['GPL-3', 'MIT', 'NOT-LICENSE']
        repository_types = ['code', 'infra', 'documentation', 'data', 'profile']
        project_status = ['development', 'maintenance', 'deprecated', 'archived']
        project_protocols = ['http', 'mqtt', 'amqp']

        for key in required_keys:
            if key not in metadata:
                return RepoVerificationResult.failure(
                    cls.KEY,
                    cls.RULE_DESCRIPTION,
                    cls.SEVERITY,
                    f"{file_name} sem a key '{key}'")

        if metadata['repository']['license'] not in repository_licenses:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Licença invalida")

        if metadata['repository']['type'] not in repository_types:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Tipo invalido")

        if metadata['repository']['type'] != 'code':
            return cls.PASSED

        if metadata['project']['status'] not in project_status:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Status do projeto invalido")

        protocols = set(metadata['project']['protocols']) - set(project_protocols)
        if protocols:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                f"Protocolos invalidos: {', '.join(protocols)}")

        return cls.PASSED
