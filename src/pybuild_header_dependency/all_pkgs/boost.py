from ..package_downloader import PackageDownloader
import requests
from typing import List


class Boost(PackageDownloader):
    name = 'boost'
    
    def get_latest_version(self):
        return self._all_versions[-1]


    def download(version: str, base_dir: Path):
        pass

    
    def all_versions(self) -> List[str]:
        response = requests.get("https://boostorg.jfrog.io/artifactory/api/storage/main/release/")
        response.raise_for_status()
        return [x['uri'].split('/')[1] for x in response.json()['children']]
