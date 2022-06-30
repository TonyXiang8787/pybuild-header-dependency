[![PyPI version](https://badge.fury.io/py/pybuild-header-dependency.svg)](https://badge.fury.io/py/pybuild-header-dependency)
[![Build python](https://github.com/TonyXiang8787/pybuild-header-dependency/actions/workflows/build.yml/badge.svg)](https://github.com/TonyXiang8787/pybuild-header-dependency/actions/workflows/build.yml)

# pybuild-header-dependency

`pybuild-header-dependency` is a helper package to resolve C/C++ header-only libraries for Python build with native extensions.

# Why this project?

Are you developing a Python project with C/C++ extensions? You are likely to have some dependencies on C/C++ libraries. Managing C/C++ dependencies can be tricky in this case because `setuptools`, the standard build system for Python extension module, does not have a proper package management for C/C++ libraries.

In many cases, your C/C++ dependencies are header-only libraries. You need to then tell `setuptools` the path to the needed header files. Some header-only libraries, e.g. [`pybind11`](https://github.com/pybind/pybind11), are directly installable from PyPI and you can resolve the header location by calling the function `get_include`. This is however not universally applicable for all header-only libraries.

This project is a helper package aiming to facilitate the build process by automatically downloading the needed C/C++ header-only libraries and providing a include path to the build system (`setuptools`).

## Alternatives to this project

[`pybind11`](https://github.com/pybind/pybind11) also provides a way to build C/C++ extensions using full `cmake` build system. In this way, all the C/C++ dependencies can be resolved in `cmake`. Please refer to their [documentation](https://pybind11.readthedocs.io/en/stable/compiling.html#building-with-cmake). This project, however, aims at the developers using `setuptools` to build the extensions.

# Installation

You rarely need to install it manually. If you do, you can directly install it from PyPI:

```bash
pip install pybuild-header-dependency
```

# Usage

The usage below is under the assumption that you develop your project according to [PEP518](https://peps.python.org/pep-0518/) with `pyproject.toml`.

## Build dependency

Specify `pybuild-header-dependency` as a build dependency in your `pyproject.toml`. It should include something like below:

```toml
[build-system]
requires = [
    "setuptools",
    "wheel",
    "pybuild-header-dependency"
    # your other build dependencies
]
build-backend = "setuptools.build_meta"
```

## Get headers

## Limitation

As the name of this project suggests, this project supports header-only C/C++ libraries.
If you project depends on some static/dynamic libraries, you need to use a full build system like `cmake`.

The default way of downloading packages from GitLab/GitHub is based on releases. You can of course make a custom downloader.

# License

This project is licensed under the BSD-3-Clause license, see [LICENSE](LICENSE) for details.

## Licenses of the libraries

Each supported head-only library is licensed under its own terms. Please consult them individually.

# Contribution

You are more than welcome to make contributions to this project. 
Please have a look at the [`pkg.json`](src/pybuild_header_dependency/pkgs.json) for 
some examples about how to add new packages. 
Also refer to [`boost.py`](src/pybuild_header_dependency/custom_sources/boost.py) for 
an example of custom downloader.
