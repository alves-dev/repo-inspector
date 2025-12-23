import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import requests

from app.config.setting import setting
from app.github.commit import Commit
from app.github.models import Repository
from app.output import file_html as html
from app.output import file_image_graphic as graphic
from app.output import file_markdown as markdown
from app.output import type_json
from app.verification.model import RepoVerificationResult


# DEPRECIADO
def save_reports(results: dict[str: list[RepoVerificationResult]]):
    root_path = Path(__file__).parent.parent.parent.resolve()
    time_history = str(datetime.now().strftime("%Y-%m-%d"))
    base_path = root_path / "output-results"
    base_history = root_path / "output-results" / time_history

    base_history.mkdir(parents=True, exist_ok=True)

    markdown.save_grouped_by_repository(results, f'{base_path}/inspector-report.md')
    markdown.save_grouped_by_repository(results, f'{base_history}/inspector-report.md')

    markdown.save_grouped_by_verification(results, f'{base_path}/inspector-grouped-report.md')
    markdown.save_grouped_by_verification(results, f'{base_history}/inspector-grouped-report.md')

    markdown.save_summary(results, f'{base_path}/inspector-summary.md')
    markdown.save_summary(results, f'{base_history}/inspector-summary.md')

    graphic.generate_summary_charts(base_path)
    graphic.generate_summary_charts(base_history)

    html.generate_dashboard(f'{base_path}/inspector-dashboard.html')
    html.generate_dashboard(f'{base_history}/inspector-dashboard.html')


def save_report_repo(results: dict[str: list[RepoVerificationResult]], repositories: list[Repository]):
    summary: dict = type_json.inspector_summary(results, repositories)
    detailed: list = type_json.inspector_detailed(results, repositories)

    commit = Commit()

    detailed_json = json.dumps(detailed, indent=4, ensure_ascii=False)
    commit.write_file('inspector-detailed.json', detailed_json)

    summary_json = json.dumps(summary, indent=4, ensure_ascii=False)
    commit.write_file('inspector-summary.json', summary_json)

    commit.commit_and_push('inspector-reports')


def post_report(results: dict[str, list[RepoVerificationResult]], repositories: list[Repository]) -> None:
    if setting.INSPECTOR_POST_URL is None or setting.INSPECTOR_POST_URL == "":
        logging.warning("INSPECTOR_POST_URL not set")
        return

    # Indexa os dados dos repositórios por nome
    repo_map : dict[str, Repository] = {repo.name: repo for repo in repositories}

    payload = []

    headers = {
        "x-api-key": setting.INSPECTOR_API_KEY
    }

    for repo_name, verifications in results.items():
        repo :Repository = repo_map.get(repo_name)
        if not repo:
            continue  # Pula se o repositório não estiver na lista

        payload.extend([
            {
                "id": repo.id,
                "name": repo.name,
                "url": repo.url,
                "private": repo.private,
                "updated_at": repo.updated_at,
                "language": repo.language,
                "repository": repo_name,
                **asdict(result),
                "severity": result.severity.value  # Enum -> str
            }
            for result in verifications
        ])

    response = requests.post(
        setting.INSPECTOR_POST_URL,
        json=payload,
        timeout=10,
        headers=headers
    )

    response.raise_for_status()
