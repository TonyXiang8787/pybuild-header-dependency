import json
import shutil
from pathlib import Path
from typing import Dict, Optional

from . import all_pkgs as _
from .package_downloader import PackageDownloader
from .pkg_path import DEFAULT_PKG_PATH


class HeaderResolver:
    pkg_path: Path
    pkgs: Dict[str, Optional[str]]
    downloaders: Dict[str, PackageDownloader]

    @staticmethod
    def all_latest(pkg_path: Path = DEFAULT_PKG_PATH, use_cache: bool = True) -> "HeaderResolver":
        pkgs = {x: None for x in PackageDownloader.all_downloaders.keys()}
        return HeaderResolver(pkgs=pkgs, pkg_path=pkg_path, use_cache=use_cache)

    def __init__(self, pkgs: Dict[str, Optional[str]], pkg_path: Path = DEFAULT_PKG_PATH, use_cache: bool = True):
        self.pkg_path = pkg_path
        self.pkgs = pkgs
        self.downloaders = {}
        self._resolve_version()
        # skip if we already has cache
        if use_cache and self._has_cache():
            pass
        else:
            self._resolve_pkgs()

    def get_include(self) -> Path:
        return self.pkg_path / "include"

    def _resolve_version(self):
        pkgs = {}
        for name, version in self.pkgs.items():
            if name not in PackageDownloader.all_downloaders:
                raise ValueError(f"Unknown package: {name}. Consider make a PR to add it.")
            downloader = PackageDownloader.all_downloaders[name]()
            self.downloaders[name] = downloader
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

    def _resolve_pkgs(self):
        self._create_folder()
        # download
        for name, version in self.pkgs.items():
            print(f"Download package: {name}, version: {version} ...")
            self.downloaders[name].download(version, self.pkg_path)
        # save to json for the cache
        with open(self.pkg_path / "pkgs.json", "w") as f:
            json.dump(self.pkgs, f, indent=2)

    def _create_folder(self):
        shutil.rmtree(self.pkg_path, ignore_errors=True)
        (self.pkg_path / "include").mkdir(parents=True, exist_ok=True)
        (self.pkg_path / "pkgs").mkdir(parents=True, exist_ok=True)
