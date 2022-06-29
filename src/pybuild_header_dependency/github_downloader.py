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

    def download(self, version: str, base_dir: Path):
        release = self.releases[version]
        url = release["tarball_url"]
        response = requests.get(url, stream=True)
        response.raise_for_status()
        self.unpack_files(
            response,
            has_root_dir=True,
            base_dir=base_dir,
            include_base_dir=self.include_base_dir,
            include_files=self.include_files,
        )

    def download_url(self, version: str) -> str:
        return self.releases[version]["tarball_url"]
