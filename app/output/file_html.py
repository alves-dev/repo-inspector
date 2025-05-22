def generate_dashboard(filepath: str):
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Repo Inspector Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: auto;
            padding: 2rem;
            background-color: #f9f9f9;
        }}
        h1, h2 {{
            color: #333;
        }}
        .chart {{
            margin-bottom: 40px;
        }}
        img {{
            max-width: 100%;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        ul {{
            list-style: none;
            padding-left: 0;
        }}
        li {{
            margin: 6px 0;
        }}
        a {{
            text-decoration: none;
            color: #0077cc;
        }}
    </style>
</head>
<body>
    <h1>📊 Repo Inspector Dashboard</h1>

    <h2>📂 Relatórios</h2>
    <ul>
        <li><a href="inspector-report.md" target="_blank">🔍 Relatório por Repositório</a></li>
        <li><a href="inspector-grouped-report.md" target="_blank">📎 Relatório Agrupado por Verificação</a></li>
        <li><a href="inspector-summary.md" target="_blank">🧾 Sumário em Markdown</a></li>
        <li><a href="inspector-summary.json" target="_blank">🗂️ Sumário em JSON</a></li>
    </ul>

    <h2>📈 Gráficos</h2>

    <div class="chart">
        <h3>📊 Resultados por Regra</h3>
        <img src="chart_rules_bar.png" alt="Gráfico de barras por regra">
    </div>

    <div class="chart">
        <h3>🥧 Distribuição Geral das Verificações</h3>
        <img src="chart_overall_pie.png" alt="Gráfico de pizza geral">
    </div>

    <div class="chart">
        <h3>🚨 Repositórios com Mais de uma Falha</h3>
        <img src="chart_repo_failures.png" alt="Gráfico de barras horizontal">
    </div>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
