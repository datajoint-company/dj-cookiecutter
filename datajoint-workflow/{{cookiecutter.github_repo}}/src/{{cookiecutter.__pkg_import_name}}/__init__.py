"""`{{cookiecutter.__pkg_import_name}}`: A {{cookiecutter.organization}} Workflow for {{cookiecutter.workflow}}."""

import logging

__version__: str
__pkg_name__: str
__pkg_import_name__: str


def get_names() -> tuple[str, str]:
    """Get the distribution and import name for the top-level package.

    Returns:
        tuple[str, str]: The distribution name and import name, respectively.
    """
    import_name = __package__ or "{{cookiecutter.__pkg_import_name}}"
    package = import_name.replace("_", "-")
    return package, import_name


__pkg_name__, __pkg_import_name__ = get_names()


logging.getLogger(__pkg_import_name__).addHandler(logging.NullHandler())


def get_version() -> str:
    """Get the version number for the current package.

    Returns:
        str: Version number taken from the installed package version found in
            the file `pyproject.toml`.
    """
    from importlib.metadata import PackageNotFoundError, version

    __version__ = "unknown"

    try:
        __version__ = version(__pkg_name__)
    except PackageNotFoundError:
        from .version import __version__
    finally:
        del version, PackageNotFoundError

    return __version__


__version__ = get_version()
VERSION = __version__
