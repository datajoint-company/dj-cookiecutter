"""Generate the api reference content and navigation from docstrings."""

from pathlib import Path

import mkdocs_gen_files as mkgen


def generate_api_docs(
    module_parent: str,
    nav: mkgen.nav.Nav,
    *,
    files_stems_to_skip: list[str] = None,
    show_source_list: list[str] = None,
) -> None:
    paths = sorted(Path(module_parent).rglob("*.py"))
    for path in paths:
        rel_path = path.relative_to(module_parent)
        module_path = rel_path.with_suffix("")
        doc_path = rel_path.with_suffix(".md")
        full_doc_path = Path("api", doc_path)

        parts = list(module_path.parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif files_stems_to_skip and parts[-1] in files_stems_to_skip:
            continue

        nav[parts] = doc_path

        with mkgen.open(full_doc_path, "w") as fd:
            ident: str = ".".join(parts)
            file_txt: str = "::: " + ident
            if show_source_list and ident in show_source_list:
                file_txt += "\n\tshow_source: true"
            print(file_txt, file=fd)

        mkgen.set_edit_path(full_doc_path, path)

    with mkgen.open("api/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


generate_api_docs(
    "src",
    mkgen.Nav(),
    files_stems_to_skip=["__main__", "version"],
    show_source_list=["{{cookiecutter.__pkg_import_name}}.entrypoint"],
)
