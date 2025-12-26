import yaml

from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryFileRepositoryYMLVerification(VerificationInterface):
    KEY = 'git.repository.file.repo_yml'
    RULE_DESCRIPTION = "Verifica se existe o .repo.yml na raiz do repo e se é valido"
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
        file_name = '.repo.yml'
        file_data: str | None = GithubClient.get_file(repository.url, file_name)

        if file_data is None:
            return cls.failure(f'Repo sem o {file_name}')

        metadata: dict = yaml.safe_load(file_data)

        # Validações da versão: V1
        required_keys = ['repository']

        repository_licenses = ['GPL-3', 'MIT', 'NOT-LICENSE']
        repository_types = ['code', 'infra', 'documentation', 'data', 'profile']

        project_status = ['development', 'maintenance', 'deprecated', 'archived']

        project_language = ['java', 'kotlin', 'go', 'csharp', 'python']
        project_framework = ['spring', 'quarkus', 'dotnet']
        project_database = ['mysql', 'postresql', 'redis', 'mongoDB']
        project_protocols = ['http', 'mqtt', 'amqp']

        for key in required_keys:
            if key not in metadata:
                return cls.failure(f"{file_name} sem a key '{key}'")

        if metadata['repository']['license'] not in repository_licenses:
            return cls.failure("Licença invalida")

        if metadata['repository']['type'] not in repository_types:
            return cls.failure("Tipo invalido")

        if metadata['repository']['type'] != 'code':
            return cls.PASSED

        if metadata['project']['status'] not in project_status:
            return cls.failure("Status do projeto invalido")

        invalids = set(metadata['project']['stack']['language']) - set(project_language)
        if invalids:
            return cls.failure(f"Linguagem invalida: {', '.join(invalids)}")

        invalids = set(metadata['project']['stack']['framework']) - set(project_framework)
        if invalids:
            return cls.failure(f"Framework invalido: {', '.join(invalids)}")

        invalids = set(metadata['project']['stack']['database']) - set(project_database)
        if invalids:
            return cls.failure(f"Banco invalido: {', '.join(invalids)}")

        invalids = set(metadata['project']['stack']['protocols']) - set(project_protocols)
        if invalids:
            return cls.failure(f"Protocolos invalidos: {', '.join(invalids)}")

        return cls.PASSED
