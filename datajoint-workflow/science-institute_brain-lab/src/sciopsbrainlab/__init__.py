"""`sciops-brain-lab`:
_A DataJoint SciOps Workflow for
Science Institute, Brain Lab_
"""

import logging


def get_version() -> str:
    """_Get version number for the package `sciops-brain-lab`._

    Returns:
        str: Version number taken from the installed package version or `version.py`.
    """
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

    __version__: str = "unknown"

    try:
        # Replace `version(__name__)` if project does not equal the package name
        __version__ = version("sciops-brain-lab")
    except PackageNotFoundError:  # pragma: no cover
        from .version import __version__
    finally:
        del version, PackageNotFoundError

    return __version__


__version__: str = get_version()
version: str = __version__


# fmt: off
# Root level logger for the 'sciopsbrainlab' namespace
logging.getLogger("sciopsbrainlab").addHandler(logging.NullHandler())
