from pathlib import Path

import requests

from .git_downloader import GitDownloader


class GitHubDownloader(GitDownloader):
    repository_name: str

    def __init__(self, repository_name: str, **_kwargs):
        super().__init__(**_kwargs)
        self.repository_name = repository_name

    def release_url(self) -> str:
        return f"https://api.github.com/repos/{self.repository_name}/releases"

    def download_url(self, version: str) -> str:
        return self.releases[version]["tarball_url"]

    def is_official_release(self, release: dict) -> bool:
        return not release["prerelease"]
