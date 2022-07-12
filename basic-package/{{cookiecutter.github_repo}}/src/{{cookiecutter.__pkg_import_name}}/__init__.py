"""`{{cookiecutter.__pkg_name}}`:
_A {{cookiecutter.organization}} Workflow for {{cookiecutter.package_name}}_
"""

import logging


def get_names() -> tuple[str, str]:
    """Get the package name and import name for the current package.

    Returns:
        tuple[str, str]: The package name and import name, respectively.
    """
    import_name: str = __package__ or "{{cookiecutter.__pkg_import_name}}"
    package: str = import_name.replace("_", "-")
    return package, import_name


def get_version() -> str:
    """Get the version number for the current package.

    Returns:
        str: Version number taken from the installed package version or `version.py`.
    """
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

    __version__: str = "unknown"

    try:
        # Replace `version(__name__)` if project does not equal the package name
        __version__ = version(__pkg_name__)
    except PackageNotFoundError:  # pragma: no cover
        from .version import __version__
    finally:
        del version, PackageNotFoundError

    return __version__


__pkg_name__: str
__pkg_import_name__: str
__pkg_name__, __pkg_import_name__ = get_names()


__version__: str = get_version()
version: str = __version__


# fmt: off
# Root level logger for the '{{cookiecutter.__pkg_import_name}}' namespace
logging.getLogger(__pkg_import_name__).addHandler(logging.NullHandler())
