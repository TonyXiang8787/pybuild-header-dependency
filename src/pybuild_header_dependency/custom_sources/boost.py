from pathlib import Path

import requests

from ..package_downloader import PackageDownloader


class Boost(PackageDownloader):
    name = "boost"
    release_url = "https://boostorg.jfrog.io/artifactory/api/storage/main/release"
    file_base_url = "https://boostorg.jfrog.io/artifactory/main/release"

    def __init__(self):
        response = requests.get(self.release_url)
        response.raise_for_status()
        self.all_versions = [x["uri"].split("/")[1] for x in response.json()["children"]]
        self.all_versions.reverse()

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
