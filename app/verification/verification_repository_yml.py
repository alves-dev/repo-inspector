import yaml

from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


class RepositoryFileRepositoryYMLVerification(VerificationInterface):
    KEY = 'git.repository.file.repository-yml'
    DESCRIPTION = "Verifica se existe o repository.yml na raiz do repo e se é valido"

    PASSED = [RepoVerificationResult.of_passed(KEY, '')]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        file_name = 'repository.yml'
        file_data: str | None = GithubClient.get_file(repository.url, file_name)

        if file_data is None:
            return [RepoVerificationResult.of_failure(cls.KEY, f'Repo sem o {file_name}')]

        metadata: dict = yaml.safe_load(file_data)

        # Validações da versão: V1
        required_keys = ['repository']
        repository_licenses = ['GPL-3', 'MIT', 'NOT-LICENSE']
        repository_types = ['code', 'infra', 'documentation', 'data', 'profile']
        project_status = ['development', 'maintenance', 'deprecated', 'archived']
        project_protocols = ['http', 'mqtt', 'amqp']

        for key in required_keys:
            if key not in metadata:
                return [RepoVerificationResult.of_failure(cls.KEY, f"{file_name} sem a key '{key}'")]

        if metadata['repository']['license'] not in repository_licenses:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Licença invalida')]

        if metadata['repository']['type'] not in repository_types:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Tipo invalido')]

        if metadata['repository']['type'] != 'code':
            return cls.PASSED

        if metadata['project']['status'] not in project_status:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Status do projeto invalido')]

        protocols = set(metadata['project']['protocols']) - set(project_protocols)
        if protocols:
            return [RepoVerificationResult.of_failure(cls.KEY, f"Protocolos invalidos: {', '.join(protocols)}")]

        return cls.PASSED
