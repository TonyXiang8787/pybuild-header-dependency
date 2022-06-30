import os
import re
import requests


def get_version() -> str:
    with open("VERSION") as f:
        version = f.read().strip().strip("\n")
    major, minor = (int(x) for x in version.split("."))
    latest_major, latest_minor, latest_patch = get_pypi_latest()
    # get version
    version = get_new_version(major, minor, latest_major, latest_minor, latest_patch)
    # mutate version in GitHub Actions
    if ("GITHUB_SHA" in os.environ) and ("GITHUB_REF" in os.environ) and ("GITHUB_RUN_NUMBER" in os.environ):
        sha = os.environ["GITHUB_SHA"]
        ref = os.environ["GITHUB_REF"]
        build_number = os.environ["GITHUB_RUN_NUMBER"]
        # short hash number in numeric
        short_hash = f'{int(f"0x{sha[0:6]}", base=16):08}'

        if "main" in ref:
            # main branch
            # major.minor.patch
            # do nothing
            pass
        else:
            # feature branch
            # major.minor.patch a 1 build_number short_hash
            version += f"a1{build_number}{short_hash}"
    with open("VERSION", "w") as f:
        f.write(version)
    return version


def get_pypi_latest():
    r = requests.get("https://pypi.org/pypi/pybuild-header-dependency/json")
    data = r.json()
    version: str = data["info"]["version"]
    versions = [int(x) for x in version.split(".")]
    if len(versions) < 3:
        versions.append(0)
    return versions


def get_new_version(major, minor, latest_major, latest_minor, latest_patch):
    if (major > latest_major) or ((major == latest_major) and minor > latest_minor):
        # brand-new version with patch zero
        return f"{major}.{minor}.0"
    elif major == latest_major and minor == latest_minor:
        # current version, increment path
        return f"{major}.{minor}.{latest_patch + 1}"
    else:
        # does not allow building older version
        raise ValueError(
            "Invalid version number!\n"
            f"latest version: {latest_major}.{latest_minor}.{latest_patch}\n"
            f"to be built version: {major}.{minor}\n"
        )


def convert_long_description():
    with open("README.md", "r") as f:
        raw_readme = f.read()
    if "GITHUB_SHA" not in os.environ:
        readme = raw_readme
    else:
        sha = os.environ["GITHUB_SHA"].lower()
        url = f"https://github.com/TonyXiang8787/pybuild-header-dependency/blob/{sha}/"
        readme = re.sub(r"(\[[^\(\)\[\]]+\]\()((?!http)[^\(\)\[\]]+\))", f"\\1{url}\\2", raw_readme)
    with open("README.md", 'w') as f:
        f.write(readme)


if __name__ == "__main__":
    get_version()
    convert_long_description()
