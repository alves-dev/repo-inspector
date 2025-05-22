import json
from collections import defaultdict
from pathlib import Path

from app.verification.model import RepoVerificationResult


def save_summary_json(results: dict[str, list[RepoVerificationResult]]):
    root_path = Path(__file__).parent.parent.parent.resolve()
    filepath = root_path / "output-results" / "inspector-summary.json"

    rule_summary = defaultdict(lambda: {"passed": 0, "failed": 0})
    repos_passed_all = []
    repos_multiple_failures = []

    for repo, verifications in results.items():
        failed_count = 0
        all_passed = True
        for v in verifications:
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

    summary = {
        "rules": rule_summary,
        "repos_passed_all": repos_passed_all,
        "repos_multiple_failures": repos_multiple_failures
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
