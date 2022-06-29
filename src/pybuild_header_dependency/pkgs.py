from .gitlab_downloader import GitLabDownloader
from .package_downloader import PackageDownloader
from .custom_sources.boost import Boost
import json
from pathlib import Path
from typing import Dict, Any, List, Type


CUSTOM_PKGS: Dict[str, Type[PackageDownloader]] = {
    'boost': Boost
}


def _get_all_pkgs():
    with open(Path(__file__).parent / "pkgs.json", 'r') as f:
        pkgs = json.load(f)
    
    # make a dictionary
    pkgs = {x["name"]: x for x in pkgs}
    return pkgs

ALL_PKGS_META_DATA: Dict[str, Any] = _get_all_pkgs()


def all_pkgs() -> List[str]:
    return list(ALL_PKGS_META_DATA.keys())


def get_downloader(pkg_name: str) -> PackageDownloader:
    if pkg_name not in ALL_PKGS_META_DATA:
        raise TypeError(f"Unknown package: {pkg_name}. Consider make a PR to add it.")
    meta_data: dict = ALL_PKGS_META_DATA[pkg_name]

    if meta_data['source'] == 'gitlab':
        return GitLabDownloader(**meta_data)
    elif meta_data['source'] == 'custom':
        return CUSTOM_PKGS[pkg_name]()
    else:
        raise TypeError(f"Unknown source type: {meta_data['source']}")
