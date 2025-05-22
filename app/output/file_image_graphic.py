import json
from pathlib import Path

import matplotlib.pyplot as plt


def generate_summary_charts(base_path: Path):
    json_path = f'{base_path}/inspector-summary.json'
    output_dir = base_path

    with open(json_path, encoding="utf-8") as f:
        summary = json.load(f)

    # Gráfico 1 - Barras por regra
    rules = summary["rules"]
    rule_names = list(rules.keys())
    passed = [rules[r]["passed"] for r in rule_names]
    failed = [rules[r]["failed"] for r in rule_names]

    plt.figure(figsize=(10, 6))
    bar_width = 0.4
    x = range(len(rule_names))

    plt.bar(x, passed, width=bar_width, label='Passaram', color='green')
    plt.bar([i + bar_width for i in x], failed, width=bar_width, label='Falharam', color='red')

    plt.xticks([i + bar_width / 2 for i in x], rule_names, rotation=45, ha='right')
    plt.ylabel("Número de repositórios")
    plt.title("Resultados por Regra")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "chart_rules_bar.png")
    plt.close()

    # Gráfico 2 - Pizza geral (pass x fail)
    total_pass = sum(passed)
    total_fail = sum(failed)

    plt.figure(figsize=(6, 6))
    plt.pie(
        [total_pass, total_fail],
        labels=["Passaram", "Falharam"],
        colors=["green", "red"],
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title("Distribuição Geral das Verificações")
    plt.savefig(output_dir / "chart_overall_pie.png")
    plt.close()

    # Gráfico 3 - Barras horizontais (falhas por repo)
    failed_repos = summary["repos_multiple_failures"]
    if failed_repos:
        repos = [item["repo"] for item in failed_repos]
        fail_counts = [item["fail_count"] for item in failed_repos]

        plt.figure(figsize=(8, 5))
        plt.barh(repos, fail_counts, color="orange")
        plt.xlabel("Número de falhas")
        plt.title("Repositórios com Mais de uma Falha")
        plt.tight_layout()
        plt.savefig(output_dir / "chart_repo_failures.png")
        plt.close()
