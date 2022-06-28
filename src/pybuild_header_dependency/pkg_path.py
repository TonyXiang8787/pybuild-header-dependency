from pathlib import Path
from tempfile import gettempdir

DEFAULT_PKG_PATH = Path(gettempdir()) / "pybuild-header-dependency"
