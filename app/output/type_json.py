from collections import defaultdict

from app.github.models import Repository
from app.verification.model import RepoVerificationResult


def inspector_detailed(results: dict[str, list[RepoVerificationResult]], repositories: list[Repository]) -> list:
    # Indexa os dados dos repositórios por nome
    repo_map = {repo.name: repo for repo in repositories}

    full_data = []

    for repo_name, verifications in results.items():
        repo = repo_map.get(repo_name)
        if not repo:
            continue  # Pula se o repositório não estiver na lista

        repo_entry = {
            "id": repo.id,
            "name": repo.name,
            "url": repo.url,
            "private": repo.private,
            "updated_at": repo.updated_at,
            "language": repo.language,
            "visibility": repo.visibility
        }

        # Adiciona as verificações como chaves booleanas
        failed_count = 0
        failure_description = ''
        for v in verifications:
            repo_entry[v.key] = v.passed

            if not v.passed:
                failed_count += 1
                failure_description += v.rule_description + ' --- '

        repo_entry['total_not_passed'] = failed_count
        repo_entry['failure_description'] = failure_description

        full_data.append(repo_entry)

    return full_data


def inspector_summary(results: dict[str, list[RepoVerificationResult]], repositories: list[Repository]) -> dict:
    rule_summary = defaultdict(lambda: {"passed": 0, "failed": 0})
    repos_passed_all = []
    repos_multiple_failures = []
    rules = set()

    for repo, verifications in results.items():
        failed_count = 0
        all_passed = True
        for v in verifications:
            rules.add(v.key)

            if v.passed:
                rule_summary[v.key]["passed"] += 1
            else:
                rule_summary[v.key]["failed"] += 1
                failed_count += 1
                all_passed = False

        if all_passed:
            repos_passed_all.append(repo)
        if failed_count > 1:
            repos_multiple_failures.append({"repo": repo, "fail_count": failed_count})

    count = {'total': 0, 'private': 0, 'public': 0}
    for repo in repositories:
        count['total'] += 1
        if repo.private:
            count['private'] += 1
        else:
            count['public'] += 1

    rule_summary_list = [
        {"rule": key, **value}
        for key, value in rule_summary.items()
    ]

    summary = {
        "repos_count": count,
        "rules": list(rules),
        "rules_detail": rule_summary_list,
        "repos_passed_all": repos_passed_all,
        "repos_multiple_failures": repos_multiple_failures
    }

    return summary
