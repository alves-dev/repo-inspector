import base64

import requests

from app.config.setting import setting
from app.github.models import Repository

headers = {"Authorization": f"token {setting.GITHUB_TOKEN}"}


class GithubClient:
    """
    Age como um cache durante o script
    Caso seja solicitado um repositório, eu verifico aqui antes de ir no github
    """
    repo_dict: dict[str, dict] = {}

    @classmethod
    def get_repos_by_token(cls) -> list[Repository]:
        page_size = setting.GITHUB_PAGE_SIZE
        url = f'{setting.GITHUB_BASE_URL}/user/repos?per_page={page_size}'

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            cls.__log_info(page_size, response.json())
            return cls.__transform_to_repository_list(response.json())
        else:
            print(f'status_code {response.status_code}, body: Error: Erro na requisição {url}')
            return []

    @classmethod
    def get_repo_by_url(cls, repo_url) -> dict:
        cache = cls.repo_dict.get(repo_url, None)
        if cache is not None:
            return cache

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_user = repo_url.split("/")[-2]

        url = f'{setting.GITHUB_BASE_URL}/repos/{repo_user}/{repo_name}'

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            cls.repo_dict[repo_url] = response.json()
            return response.json()
        else:
            print(f'status_code {response.status_code}, body: Error: Erro na requisição {url}')
            return {}

    @classmethod
    def get_file(cls, repo_url: str, file_path: str) -> str | None:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_user = repo_url.split("/")[-2]

        url = f'{setting.GITHUB_BASE_URL}/repos/{repo_user}/{repo_name}/contents/{file_path}'

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return base64.b64decode(data['content']).decode('utf-8')
        else:
            print(f'File not found in: {url}')
            return None

    @staticmethod
    def __log_info(page_size: int, response: dict):
        response_size = len(response)
        is_all = response_size < page_size
        message = f'Amount of repositories: {response_size}'
        if not is_all:
            message = f'{message} -- NOT ALL LISTED'
        print(message)

    @staticmethod
    def __transform_to_repository_list(response: list) -> list[Repository]:
        repos = []
        for e in response:
            repos.append(Repository.from_dict(e))

        return repos
