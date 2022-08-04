from pathlib import Path

import requests

from ..package_downloader import PackageDownloader


class Boost(PackageDownloader):
    name = "boost"
    release_url = "https://boostorg.jfrog.io/artifactory/api/storage/main/release"
    file_base_url = "https://boostorg.jfrog.io/artifactory/main/release"

    def __init__(self):
        super().__init__()

    def get_releases(self):
        self.all_versions = []
        response = requests.get(self.release_url)
        response.raise_for_status()
        # loop all versions
        children = response.json()["children"]
        for child in reversed(children):
            version_uri = child["uri"]
            # get all files
            response = requests.get(f"{self.release_url}{version_uri}/source")
            response.raise_for_status()
            all_files = [x["uri"] for x in response.json()["children"]]
            version = version_uri.split("/")[1]
            # only add to version list if it has official release
            version_underscore = version.replace(".", "_")
            if f"/boost_{version_underscore}.tar.gz" in all_files:
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
