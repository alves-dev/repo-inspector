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

        required_keys: list = config.repo_yml.get('required_keys', [])

        repository_licenses = config.repo_yml.get('repository', {}).get('licenses', [])
        repository_types = config.repo_yml.get('repository', {}).get('types', [])

        project_status = config.repo_yml.get('project', {}).get('status', [])
        project_language = config.repo_yml.get('project', {}).get('language', [])
        project_framework = config.repo_yml.get('project', {}).get('framework', [])
        project_database = config.repo_yml.get('project', {}).get('database', [])
        project_protocols = config.repo_yml.get('project', {}).get('protocols', [])

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

        language = metadata['project']['stack']['language']
        if language is not None and language not in project_language:
            return cls.failure(f"Linguagem {language} invalida")

        framework = metadata['project']['stack']['framework']
        if framework is not None and framework not in project_framework:
            return cls.failure(f"Framework {framework} invalido")

        database = metadata['project']['stack']['database']
        if database is not None and database not in project_database:
            return cls.failure(f"Banco {database} invalido")

        invalids = set(metadata['project']['stack']['protocols']) - set(project_protocols)
        if invalids:
            return cls.failure(f"Protocolos invalidos: {', '.join(invalids)}")

        return cls.PASSED
