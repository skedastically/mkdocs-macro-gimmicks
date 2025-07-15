# List navigations

To list navigations[^1] within a page's section, use

```
{{ "{{ listnavs() }}" }}
```

This function will attempt to find a page's parent, and iterate through its children list to find sibling links. It is useful e.g. for an index of subcontents, especially when you wish not to use the built-in navigation table.

!!! note "This function should not be called inside a paragraph/another element block as it won't render properly."

!!! warning "Nested listings are not supported (yet?)"


## Usage with awesome-nav

`listnavs()` can be used with [awesome-nav](https://github.com/lukasgeiter/mkdocs-awesome-nav) with some tweaks:

1. Add an mkdocs[hook](https://www.mkdocs.org/user-guide/configuration/#hooks) e.g. `hooks.py` in your project's root directory (**not** the docs directory) with the following content:
   
=== "./hooks.py"

    ```python
    def on_nav(nav, config, files):
        # overrides config.nav for macros use
        config.nav = nav
        return nav
    ```

Then you can configure both the plugins and this hook in `mkdocs.yml`. Remember to put macros **after** awesome-nav so the generated navigation can certainly pass through in order.

=== "./mkdocs.yml"

    ```yml
    hooks:
      - hooks.py
    plugins:
      - search
      - awesome-nav
      - macros
    ```

## Flags

You can also include these flags inside listnavs i.e. with `{{ "listnavs(excludeCurrentPage = False)"}}`

| Name                 | Default value | Description                                                                                                                                                     |
| -------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`              | `False`        | Title of the files list inside an `#!html <h2>` element, provided as a string. Also defaults to "Navigation" if `True`, and no title if `False`                 |
| `findSectionIndex`   | `True`        | Attempt to find and use `index.md` or `README.md` as a subsection's index file, instead of whatever is the first file provided for that subsection's items list |
| `excludeCurrentPage` | `True`        | Whether to exclude current page from nav list                                                                                                                   |
| `squeeze`            | `False`       | Whether to render single-spaced lists (`True`) that looks squeezed rather than double-spaced lists (`False`)                                                    |


## Caveats

If no `config.nav` object is found, `listnavs()` employs various heuristics to get a section's pages, as the `Navigation` object returned by `get_navigation` is very incomplete (see these issues: [mkdocs-macros-plugin#156](https://github.com/fralau/mkdocs-macros-plugin/issues/156), [mkdocs-macro-plugin#198](https://github.com/fralau/mkdocs-macros-plugin/discussions/198)).


[^1]: links to other objects like Sections and Pages