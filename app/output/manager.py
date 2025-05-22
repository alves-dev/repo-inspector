from app.verification.model import RepoVerificationResult
from app.output import file_markdown as markdown
from app.output import file_json as json
from app.output import file_html as html
from app.output import file_image_graphic as graphic


def save_reports(results: dict[str: list[RepoVerificationResult]]):
    markdown.save_to_markdown(results)
    markdown.save_grouped_by_verification(results)
    markdown.save_summary(results)

    json.save_summary_json(results)

    graphic.generate_summary_charts()

    html.generate_dashboard_html()