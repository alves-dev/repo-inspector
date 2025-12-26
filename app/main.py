from datetime import datetime

from app.config.inspector_config import InspectorConfigLoader
from app.config.setting import setting
from app.github.client import GithubClient as gitClient
from app.github.models import Repository
from app.output import manager as output
from app.repository.store import get_store
from app.verification.model import RepoVerificationResult
from app.verification.verification_branch import RepositoryBranchVerification
from app.verification.verification_description import RepositoryDescriptionVerification
from app.verification.verification_license import RepositoryLicenseVerification
from app.verification.verification_name import RepositoryNameVerification
from app.verification.verification_topics import RepositoryTopicsVerification
from app.verification.verification_updated import RepositoryUpdatedVerification
from app.verification.verification_old_repository_yml import RepositoryOldFileRepositoryYMLVerification
from app.verification.verification_repository_yml import RepositoryFileRepositoryYMLVerification

if __name__ == "__main__":
    inspect_loader = InspectorConfigLoader(setting.INSPECTOR_GET_URL,
                                           setting.INSPECTOR_API_KEY,
                                           setting.INSPECTOR_YAML_PATH
                                           )
    inspect_config = inspect_loader.load()

    repositories: list[Repository] = gitClient.get_repos_by_token()

    verifications = [RepositoryNameVerification, RepositoryDescriptionVerification, RepositoryUpdatedVerification,
                     RepositoryBranchVerification, RepositoryLicenseVerification, RepositoryTopicsVerification,
                     RepositoryOldFileRepositoryYMLVerification, RepositoryFileRepositoryYMLVerification]

    repo_map: dict[str: list[RepoVerificationResult]] = {}

    for repo in repositories:
        repo_verifications: list[RepoVerificationResult] = []
        if (repo.name in inspect_config.ignored_rules_by_repo.keys()
                and '*' in inspect_config.ignored_rules_by_repo[repo.name]):
            repo_map[repo.name] = repo_verifications
            continue

        for verification in verifications:
            result: RepoVerificationResult = verification.verify(repo, inspect_config)
            repo_verifications.append(result)

        repo_map[repo.name] = repo_verifications

    output.save_report_repo(repo_map, repositories)
    output.post_report(repo_map, repositories)

    store = get_store()
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M'))
    key = 'last-inspection'
    store.add(key, time)
    print(store.get(key))
