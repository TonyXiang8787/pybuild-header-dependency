import json
from pathlib import Path
from typing import Any, Dict, List, Type

from .custom_sources.boost import Boost
from .github_downloader import GitHubDownloader
from .gitlab_downloader import GitLabDownloader
from .package_downloader import PackageDownloader

CUSTOM_PKGS: Dict[str, Type[PackageDownloader]] = {"boost": Boost}


def _get_all_pkgs() -> Dict[str, Dict[str, Any]]:
    with open(Path(__file__).parent / "pkgs.json", "r") as f:
        pkgs = json.load(f)

    # make a dictionary
    pkgs = {x["name"]: x for x in pkgs}
    return pkgs


# load meta data of all packages into memory
_all_pkgs_meta: Dict[str, Dict[str, Any]] = _get_all_pkgs()


def all_pkgs() -> List[str]:
    return list(_all_pkgs_meta.keys())


def fetch_downloader(pkg_name: str) -> PackageDownloader:
    if pkg_name not in _all_pkgs_meta:
        raise TypeError(f"Unknown package: {pkg_name}. Consider make a PR to add it.")
    meta_data: dict = _all_pkgs_meta[pkg_name]

    if meta_data["source"] == "gitlab":
        return GitLabDownloader(**meta_data)
    elif meta_data["source"] == "github":
        return GitHubDownloader(**meta_data)
    elif meta_data["source"] == "custom":
        return CUSTOM_PKGS[pkg_name]()
    else:
        raise TypeError(f"Unknown source type: {meta_data['source']}")


def get_downloader(pkg_name: str) -> PackageDownloader:
    downloader = fetch_downloader(pkg_name=pkg_name)
    downloader.get_releases()
    return downloader
