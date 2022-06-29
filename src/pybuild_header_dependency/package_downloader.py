import shutil
import tarfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import requests


class PackageDownloader(ABC):
    """
    Abstract class to download header-only package
    """

    # all versions, latest at first
    all_versions: List[str]

    def get_latest_version(self) -> str:
        return self.all_versions[0]

    def check_version(self, version: str):
        if version not in self.all_versions():
            raise ValueError(f"Unknown version {version} for package {self.name}!")

    def unpack_files(
        self,
        response: requests.Response,
        has_root_dir: bool,
        base_dir: Path,
        include_base_dir: Path,
        include_files: List[Path],
    ):
        tmp_dir = base_dir / "pkgs" / "tmp"
        tf = tarfile.open(fileobj=response.raw, mode="r|gz")
        tf.extractall(tmp_dir)
        if has_root_dir:
            root_dir_name = next(tmp_dir.glob("*")).name
            pkg_dir = tmp_dir / root_dir_name
        else:
            pkg_dir = tmp_dir
        for file in include_files:
            shutil.copytree(pkg_dir / include_base_dir / file, base_dir / "include" / file)
        shutil.rmtree(tmp_dir)

    @abstractmethod
    def download(self, version: str, base_dir: Path):
        pass
