from typing import Optional

import requests
import yaml

from app.verification.model import InspectorConfig


class InspectorConfigLoader:

    def __init__(
            self,
            api_url: Optional[str],
            api_key: Optional[str],
            yaml_path: Optional[str]
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.yaml_path = yaml_path

    def load(self) -> InspectorConfig:
        if self.api_url:
            return self._load_from_api()

        return self._load_from_yaml()

    def _load_from_api(self) -> InspectorConfig:
        headers = {
            "x-api-key": self.api_key
        }

        response = requests.get(self.api_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        return InspectorConfig(
            github_topics=data.get("github_topics", []),
            ignored_rules_by_repo={
                k: set(v) for k, v in data.get("ignored_rules_by_repo", {}).items()
            },
            max_days_without_update=data.get("max_days_without_update", 90),
            repo_yml=data.get("repo_yml", {})
        )

    def _load_from_yaml(self) -> InspectorConfig:
        if not self.yaml_path:
            raise RuntimeError(
                "Nenhuma configuração encontrada: api_url e yaml_path estão nulos"
            )

        with open(self.yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return InspectorConfig(
            github_topics=data.get("github_topics", []),
            ignored_rules_by_repo={
                k: set(v) for k, v in data.get("ignored_rules_by_repo", {}).items()
            },
            max_days_without_update=data.get("max_days_without_update", 90),
            repo_yml=data.get("repo_yml", {})
        )
