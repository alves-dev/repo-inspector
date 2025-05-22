from collections import defaultdict
from datetime import datetime
from pathlib import Path
import json
from app.verification.model import RepoVerificationResult


def save_to_markdown(results: dict[str: list[RepoVerificationResult]]):
    root_path = Path(__file__).parent.parent.parent.resolve()
    filepath = root_path / "output-results" / "inspector-report.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(__get_title())
        for repo, verifications in results.items():
            f.write(f"## {repo}\n\n")
            f.write("| Verificação | Descrição | Status |\n")
            f.write("|-------------|-----------|--------|\n")
            for v in verifications:
                status = "✅" if v.passed else "❌"
                f.write(f"| {v.key} | {v.description} | {status} |\n")
            f.write("\n")


def save_grouped_by_verification(results: dict[str, list[RepoVerificationResult]]):
    root_path = Path(__file__).parent.parent.parent.resolve()
    filepath = root_path / "output-results" / "inspector-grouped-report.md"

    grouped = defaultdict(list)

    for repo, verifications in results.items():
        for v in verifications:
            grouped[v.key].append((repo, v))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Repo Inspector - Visão por Verificação\n\n")
        for key, items in grouped.items():
            f.write(f"## {key}\n\n")
            f.write("| Repositório | Descrição | Status |\n")
            f.write("|-------------|-----------|--------|\n")
            for repo, v in items:
                status = "✅" if v.passed else "❌"
                f.write(f"| {repo} | {v.description} | {status} |\n")
            f.write("\n")


def save_summary(results: dict[str, list[RepoVerificationResult]]):
    root_path = Path(__file__).parent.parent.parent.resolve()
    filepath = root_path / "output-results" / "inspector-summary.md"

    rule_pass_count = defaultdict(int)
    rule_fail_count = defaultdict(int)
    repos_passed_all = []
    repos_multiple_failures = []

    for repo, verifications in results.items():
        failed_count = 0
        all_passed = True
        for v in verifications:
            if v.passed:
                rule_pass_count[v.key] += 1
            else:
                rule_fail_count[v.key] += 1
                failed_count += 1
                all_passed = False

        if all_passed:
            repos_passed_all.append(repo)
        if failed_count > 1:
            repos_multiple_failures.append((repo, failed_count))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 📋 Repo Inspector - Sumário Geral\n\n")

        f.write("## ✅ Visão Geral por Regra\n\n")
        all_keys = set(rule_pass_count.keys()) | set(rule_fail_count.keys())
        for key in sorted(all_keys):
            passed = rule_pass_count.get(key, 0)
            failed = rule_fail_count.get(key, 0)
            f.write(f"- `{key}`: {passed} passaram | {failed} falharam\n")
        f.write("\n")

        f.write("## 🏆 Repositórios que passaram em **todas** as regras\n\n")
        for repo in repos_passed_all:
            f.write(f"- {repo}\n")
        f.write(f"\nTotal: {len(repos_passed_all)}\n\n")

        f.write("## 🚨 Repositórios com **mais de uma falha**\n\n")
        for repo, count in repos_multiple_failures:
            f.write(f"- {repo} (falhou em {count} regras)\n")
        f.write(f"\nTotal: {len(repos_multiple_failures)}\n")


def __get_title() -> str:
    time = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
    return f'# Inspector - Resultados em {time}\n\n'
