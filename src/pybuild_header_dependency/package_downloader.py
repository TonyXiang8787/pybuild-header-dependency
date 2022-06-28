import shutil
import tarfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Type

import requests


class PackageDownloader(ABC):
    """
    Abstract class to download header-only package
    """

    # name of the package, to be overridden
    name: str
    # dict of all packages
    all_downloaders: Dict[str, Type["PackageDownloader"]] = {}

    # all versions, latest at first
    all_versions: List[str]

    def __init_subclass__(cls, **kwargs):
        if "name" in dir(cls):
            PackageDownloader.all_downloaders[cls.name] = cls

    def get_latest_version(self) -> str:
        return self.all_versions[0]

    def check_version(self, version: str):
        if version not in self.all_versions():
            raise ValueError(f"Unknown version {version} for package {self.name}!")

    def unpack_files(
        self, response: requests.Response, base_dir: Path, include_base_dir: Path, include_files: List[Path]
    ):
        tf = tarfile.open(fileobj=response.raw, mode="r|gz")
        tf.extractall(base_dir / "pkgs")
        for file in include_files:
            shutil.copytree(base_dir / "pkgs" / include_base_dir / file, base_dir / "include" / file)

    @abstractmethod
    def download(self, version: str, base_dir: Path):
        pass
