from pathlib import Path
from typing import Dict, Optional

from .package_downloader import PackageDownloader
from .pkg_path import DEFAULT_PKG_PATH


class HeaderResolver:
    def __init__(self, dependencies: Dict[str, Optional[str]], pkg_path: Path = DEFAULT_PKG_PATH):
        pass
