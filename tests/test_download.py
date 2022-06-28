from pybuild_header_dependency import HeaderResolver
from pathlib import Path


def test_all_pkgs():
    resolver = HeaderResolver.all_latest()
    include = resolver.get_include()
    