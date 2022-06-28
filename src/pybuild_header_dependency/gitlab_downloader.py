from pathlib import Path
from .package_downloader import PackageDownloader
import requests
from pathlib import Path
from typing import List


class GitLabDownloader(PackageDownloader):
    gitlab_id: str
    include_base_dir: Path
    include_files: List[Path]

    