import re
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, List

import requests

from .package_downloader import PackageDownloader


class GitDownloader(PackageDownloader):
    include_base_dir: Path
    include_files: List[Path]
    releases: Dict[str, Any]

    def __init__(self, include_base_dir: str, include_files: List[str], **_kwargs):
        super().__init__()
        self.include_base_dir = Path(include_base_dir)
        self.include_files = [Path(x) for x in include_files]

    def get_releases(self):
        # retrieve
        response = requests.get(self.release_url())
        response.raise_for_status()
        releases: List[Dict] = response.json()
        self.releases = {}
        for release in releases:
            tag = release["tag_name"]
            # strip leading v
            tag = tag.strip("v")
            # skip for versions containing letters
            if re.search("[a-zA-Z]", tag):
                continue
            self.releases[tag] = release
        self.all_versions = list(self.releases.keys())

    def download(self, version: str, base_dir: Path):
        response = requests.get(self.download_url(version), stream=True)
        response.raise_for_status()
        self.unpack_files(
            response,
            has_root_dir=True,
            base_dir=base_dir,
            include_base_dir=self.include_base_dir,
            include_files=self.include_files,
        )

    @abstractmethod
    def release_url(self) -> str:
        pass

    @abstractmethod
    def download_url(self, version: str) -> str:
        pass
