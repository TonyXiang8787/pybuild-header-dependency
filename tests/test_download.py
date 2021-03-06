from pathlib import Path

from pybuild_header_dependency import HeaderResolver


def test_all_pkgs():
    resolver = HeaderResolver.all_latest(use_cache=False)
    include = resolver.get_include()

    # test boost
    assert (include / "boost").exists()
    # test eigen
    assert (include / "Eigen").exists()
