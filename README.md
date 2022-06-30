# pybuild-header-dependency

`pybuild-header-dependency` is a helper package to resolve C/C++ header-only libraries for Python build with native extensions.

# Why this project?

# Installation

You rarely need to install it manually. If you do, you can directly install it from PyPI:

```bash
pip install pybuild-header-dependency
```

# Usage

## Build dependency

## Get headers

## Limitation

As the name of this project suggests, this project supports header-only C/C++ libraries.
If you project depends on some static/dynamic libraries, you need to use a full build system like `cmake`.

The default way of downloading packages from GitLab/GitHub is based on releases.

# License

This project is licensed under the BSD-3-Clause license, see [LICENSE](LICENSE) for details.

## Licenses of the libraries

Each supported head-only library is licensed under its own terms. Please consult them individually.

# Contribution

You are more than welcome to make contributions to this project. 
Please have a look at the [`pkg.json`](src/pybuild_header_dependency/pkgs.json) for 
some examples about how to add new packages. 
Also refer to [`boost.py`](src/pybuild_header_dependency/custom_sources/boost.py) for 
an example of custom sources.
