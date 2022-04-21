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
        parts = {"api_nav": list(module_path.parts), "doc_nav": list(module_path.parts)}
        stem = parts["api_nav"][-1]
        rendering = ["show_signature: true"]
        write_mode = "w"
        pretext = ""

        if files_stems_to_skip and (stem in files_stems_to_skip):
            continue
        elif stem == "__init__":
            parts["api_nav"] = parts["api_nav"][:-1]
            parts["doc_nav"] = parts["doc_nav"][:-1]
            api_doc_path = api_doc_path.with_name("index.md")
            full_api_doc_path = full_api_doc_path.with_name("index.md")
            rendering.append("show_submodules: false")
        elif stem == "__main__":
            pretext = "\n## `command-line interface`\n"
            api_doc_path = None
            full_api_doc_path = full_api_doc_path.with_name("index.md")
            write_mode = "a"
            rendering.append("show_root_heading: false")
            rendering.append("heading_level: 3")

        if api_doc_path:
            nav[parts["doc_nav"]] = api_doc_path

        with mkgen.open(full_api_doc_path, write_mode) as fd:
            ident: str = ".".join(parts["api_nav"])
            file_txt: str = pretext + "::: " + ident
            file_txt += "\n\trendering:"
            if show_source_list and ident in show_source_list:
                rendering.append("show_source: true")
            file_txt += "".join([f"\n\t\t{r}" for r in rendering])
            print(file_txt, file=fd)

        mkgen.set_edit_path(full_api_doc_path, path)

    with mkgen.open(rel_api_path / "SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


generate_api_docs(
    module_parent="src",
    rel_api_path="api",
    files_stems_to_skip=["version"],
    show_source_list=["{{cookiecutter.__pkg_import_name}}.entrypoint"],
)
