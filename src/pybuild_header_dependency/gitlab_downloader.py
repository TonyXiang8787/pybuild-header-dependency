import re
from pathlib import Path
from typing import Any, Dict, List

import requests

from .package_downloader import PackageDownloader


class GitLabDownloader(PackageDownloader):
    gitlab_id: int
    include_base_dir: Path
    include_files: List[Path]
    releases: Dict[str, Any]

    def __init__(self):
        response = requests.get(f"https://gitlab.com/api/v4/projects/{self.gitlab_id}/releases")
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
        release = self.releases[version]
        source = [x for x in release["assets"]["sources"] if x["format"] == "tar.gz"][0]
        url = source["url"]
        file_name = url.split("/")[-1]
        source_dir = file_name.strip(".tar.gz")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        self.unpack_files(
            response,
            base_dir=base_dir,
            include_base_dir=source_dir / self.include_base_dir,
            include_files=self.include_files,
        )
