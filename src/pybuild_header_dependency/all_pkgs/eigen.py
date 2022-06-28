from pathlib import Path

from ..gitlab_downloader import GitLabDownloader


class Eigen(GitLabDownloader):
    name = "eigen"
    gitlab_id = 15462818
    include_base_dir = Path()
    include_files = [Path("Eigen")]
