from cookiecutter.utils import simple_filter


@simple_filter
def words(string: str, n: int = 1) -> str:
    split = string.split()
    return " ".join(split[: min(len(split), n)])
