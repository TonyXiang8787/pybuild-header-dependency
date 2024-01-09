from pathlib import Path
import re

import requests

from ..package_downloader import PackageDownloader


class Boost(PackageDownloader):
    name = "boost"
    release_url = "https://archives.boost.io/release/"
    file_base_url = "https://archives.boost.io/release"

    def __init__(self):
        super().__init__()

    def get_releases(self):
        self.all_versions = []
        response = requests.get(self.release_url)
        response.raise_for_status()
        # loop all versions
        versions = re.findall(r"\d+\.\d+\.\d+", response.content.decode(response.encoding))
        for version in reversed(versions):
            # get all files
            response = requests.get(f"{self.release_url}/{version}/source")
            response.raise_for_status()
            version_underscore = version.replace(".", "_")
            # only add to version list if it has official release
            if re.search(f"boost_{version_underscore}.tar.gz", response.content.decode(response.encoding)):
                self.all_versions.append(version)

    def download(self, version: str, base_dir: Path):
        version_underscore = version.replace(".", "_")
        file_name = Path(f"boost_{version_underscore}.tar.gz")
        response = requests.get(f"{self.file_base_url}/{version}/source/{file_name}", stream=True)
        response.raise_for_status()
        self.unpack_files(
            response,
            has_root_dir=True,
            base_dir=base_dir,
            include_base_dir=Path(),
            include_files=[Path("boost")],
        )
