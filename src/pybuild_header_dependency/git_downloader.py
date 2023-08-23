import re
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .package_downloader import PackageDownloader


class GitDownloader(PackageDownloader):
    include_base_dir: Path
    include_files: List[Path]
    extra_strip: Optional[str]
    releases: Dict[str, Any]

    def __init__(self, include_base_dir: str, include_files: List[str], extra_strip=None, **_kwargs):
        super().__init__()
        self.include_base_dir = Path(include_base_dir)
        self.include_files = [Path(x) for x in include_files]
        self.extra_strip = extra_strip
        self.releases = {}

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
            # extra strip
            if self.extra_strip is not None:
                # skip if extra strip is not found
                if not (tag.startswith(self.extra_strip) or tag.endswith(self.extra_strip)):
                    continue
                tag = tag.strip(self.extra_strip).strip()
            # only add official release
            if self.is_official_release(release):
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

    @abstractmethod
    def is_official_release(self, release: dict) -> bool:
        pass
