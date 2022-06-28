from multiprocessing.sharedctypes import Value
from pathlib import Path
from typing import Dict, Optional
import json

from .package_downloader import PackageDownloader
from .pkg_path import DEFAULT_PKG_PATH


class HeaderResolver:
    pkg_path: Path
    pkgs: Dict[str, Optional[str]]

    @staticmethod
    def all_latest(pkg_path: Path = DEFAULT_PKG_PATH) -> "HeaderResolver":
        pkgs = {x: None for x in PackageDownloader.all_pkgs.keys()}
        return HeaderResolver(pkgs=pkgs, pkg_path=pkg_path)

    def __init__(self, pkgs: Dict[str, Optional[str]], pkg_path: Path = DEFAULT_PKG_PATH):
        self.pkg_path = pkg_path
        self.pkgs = pkgs
        self._resolve_version()

    def get_include(self) -> Path:
        return self.pkg_path / "include"

    def _resolve_version(self):
        pkgs = {}
        for name, version in self.pkgs.items():
            if name not in PackageDownloader.all_pkgs:
                raise ValueError(f"Unknown package: {name}. Consider make a PR to add it.")
            downloader = PackageDownloader.all_pkgs[name]
            if version is None:
                pkgs[name] = downloader.get_latest_version()
            else:
                downloader.check_version(version)
                pkgs[name] = version
        # overwrite
        self.pkgs = pkgs

    def _has_cache(self) -> bool:
        if (self.pkg_path / "pkgs.json").exists():
            with open(self.pkg_path / "pkgs.json", "r") as f:
                pkgs = json.load(f)
                if pkgs == self.pkgs:
                    return True
        return False
