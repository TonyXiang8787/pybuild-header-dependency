from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from .pkg_path import DEFAULT_PKG_PATH


class PackageDownloader(ABC):
    """
    Abstract class to download header-only package
    """

    # name of the package, to be overridden
    name: str
    # dict of all packages
    all_pkgs: Dict[str, "PackageDownloader"] = {}

    def __init_subclass__(cls, **kwargs):
        if "name" in dir(cls):
            PackageDownloader.all_pkgs[cls.name] = cls()

    @abstractmethod
    def get_latest_version(self) -> str:
        pass

    @abstractmethod
    def download(version: str, base_dir: Path = DEFAULT_PKG_PATH):
        pass
