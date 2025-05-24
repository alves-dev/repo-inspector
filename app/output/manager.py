import json
from datetime import datetime
from pathlib import Path

from app.github.commit import Commit
from app.github.models import Repository
from app.output import file_html as html
from app.output import file_image_graphic as graphic
from app.output import file_json
from app.output import file_markdown as markdown
from app.verification.model import RepoVerificationResult


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

    file_json.save_summary(results, f'{base_path}/inspector-summary.json')
    file_json.save_summary(results, f'{base_history}/inspector-summary.json')

    graphic.generate_summary_charts(base_path)
    graphic.generate_summary_charts(base_history)

    html.generate_dashboard(f'{base_path}/inspector-dashboard.html')
    html.generate_dashboard(f'{base_history}/inspector-dashboard.html')


def save_report_repo(results: dict[str: list[RepoVerificationResult]], repositories: list[Repository]):
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
        for v in verifications:
            repo_entry[v.key] = v.passed

        full_data.append(repo_entry)

    commit = Commit()
    json_str = json.dumps(full_data, indent=4, ensure_ascii=False)
    commit.write_file('inspector-detailed.json', json_str)
    commit.commit_and_push('inspector-detailed')
