from datetime import datetime

from app.github.client import GithubClient as gitClient
from app.github.models import Repository
from app.output import manager as output
from app.repository.store import get_store
from app.verification.model import RepoVerificationResult
from app.verification.verification_branch import ProjectBranchVerification
from app.verification.verification_description import ProjectDescriptionVerification
from app.verification.verification_license import ProjectLicenseVerification
from app.verification.verification_name import ProjectNameVerification
from app.verification.verification_topics import ProjectTopicsVerification
from app.verification.verification_updated import ProjectUpdatedVerification

if __name__ == "__main__":
    repositories: list[Repository] = gitClient.get_repos_by_token()

    verifications = [ProjectNameVerification, ProjectDescriptionVerification, ProjectUpdatedVerification,
                     ProjectBranchVerification, ProjectLicenseVerification, ProjectTopicsVerification]

    repo_map: dict[str: list[RepoVerificationResult]] = {}

    for repo in repositories:
        repo_verifications: list[RepoVerificationResult] = []
        for verification in verifications:
            result: list[RepoVerificationResult] = verification.verify(repo)
            repo_verifications.extend(r for r in result)

        repo_map[repo.name] = repo_verifications

    output.save_report_repo(repo_map, repositories)

    store = get_store()
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M'))
    key = 'last-inspection'
    store.add(key, time)
    print(store.get(key))
