"""
`{{cookiecutter.__project_name}}`: _{{cookiecutter.__short_description}}_
"""

import logging


def get_version() -> str:
    """_Get version number for the package `{{cookiecutter.__project_name}}`._

    Returns:
        str: Version number taken from the installed package version or `version.py`.
    """
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

    __version__: str = "unknown"

    try:
        # Replace `version(__name__)` if project does not equal the package name
        __version__ = version("{{cookiecutter.__project_name}}")
    except PackageNotFoundError:  # pragma: no cover
        from .version import __version__
    finally:
        del version, PackageNotFoundError

    return __version__


__version__: str = get_version()
version: str = __version__


# Root level logger for the '{{cookiecutter.__pkg_import_name}}' namespace
logging.getLogger("{{cookiecutter.__pkg_import_name}}").addHandler(
    logging.NullHandler()
)
