from pathlib import Path

import requests

from .git_downloader import GitDownloader


class GitLabDownloader(GitDownloader):
    gitlab_id: int

    def __init__(self, gitlab_id: int, **_kwargs):
        super().__init__(**_kwargs)
        self.gitlab_id = gitlab_id

    def release_url(self) -> str:
        return f"https://gitlab.com/api/v4/projects/{self.gitlab_id}/releases"

    def download_url(self, version: str) -> str:
        release = self.releases[version]
        source = [x for x in release["assets"]["sources"] if x["format"] == "tar.gz"][0]
        return source["url"]
