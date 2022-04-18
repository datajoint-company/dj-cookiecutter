"""Generate the api reference content and navigation from docstrings."""

from pathlib import Path

import mkdocs_gen_files as mkgen


def generate_api_docs(
    module_parent: str,
    rel_api_path: str,
    *,
    files_stems_to_skip: list[str] = None,
    show_source_list: list[str] = None,
) -> None:
    """Generate files with autodoc expressions processed by the mkdocstrings plugin.

    Args:
        module_parent (str): The parent folder where API content lives.
        rel_api_path (str): The path inside 'docs' where files should be generated.
            This should be the same as the 'Package Documentation' path in mkdocs.yml.
        files_stems_to_skip (list[str]): Skip these files.
        show_source_list (list[str]): Show source content for these modules.
    """
    nav: mkgen.Nav = mkgen.Nav()
    paths = sorted(Path(module_parent).rglob("*.py"))
    for path in paths:
        rel_path = path.relative_to(module_parent)
        module_path = rel_path.with_suffix("")
        api_doc_path = rel_path.with_suffix(".md")
        rel_api_path = Path(rel_api_path)
        full_api_doc_path = rel_api_path / api_doc_path

        parts = list(module_path.parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]
            api_doc_path = api_doc_path.with_name("index.md")
            full_api_doc_path = full_api_doc_path.with_name("index.md")
        elif files_stems_to_skip and parts[-1] in files_stems_to_skip:
            continue

        nav[parts] = api_doc_path

        with mkgen.open(full_api_doc_path, "w") as fd:
            ident: str = ".".join(parts)
            file_txt: str = "::: " + ident
            if show_source_list and ident in show_source_list:
                file_txt += "\n\trendering:"
                file_txt += "\n\t  show_source: true"
            print(file_txt, file=fd)

        mkgen.set_edit_path(full_api_doc_path, path)

    with mkgen.open(rel_api_path / "SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


generate_api_docs(
    module_parent="src",
    rel_api_path="api",
    files_stems_to_skip=["__main__", "version"],
    show_source_list=["brainwf.entrypoint"],
)
