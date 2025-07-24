# List navigations

To list navigations[^1] within a page's section, use

```
{{ "{{ listnav() }}" }}
```

This function will iterate through a page's siblings and their descendants. It'll return a tree-like nested list of navigations with 

!!! note "This function should not be called inside a paragraph/another element block as it won't render properly."

## Usage with awesome-nav

`listnav()` can be used with [awesome-nav](https://github.com/lukasgeiter/mkdocs-awesome-nav), provided that you configured the hook and list the `macros` plugin **after** `awesome-nav`:

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

| Name                 | Default value | Description                                                                                                                                                                                                    |
| -------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `depth`              | `0`           | Depth of navigation tree. 0 means only the current siblings are listed                                                                                                                                                                                       |
| `navIndex`           | `True`        | Attach `index.md` or `README.md` to a section's bulletpoint. Similar to mkdocs-material's [`navigation.indexes`](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/#section-index-pages) |
| `excludeCurrentPage` | `True`        | Whether to exclude current page from nav list                                                                                                                                                                  |
| `rootNav`            | `False`       | If `True`, returns navigation from root dir regardless of current page |
| `squeeze`            | `True`        | If `False`, rendered lists are more vertically spaced. Works better in `mkdocs` and `readthedocs` themes                                                                                                       |

## Caveats

`listnav()` tries its best to mimic Mkdocs-material's navigation sidebar, hence these opinionated setups..

- Page titles are derived from the following order:
    - `page.title` as found in the Page object if exists
    - Their frontmatter's `title` field if exists
    - Their first heading if exists
    - Their filename
- Section listings are **bolded**
- When `navIndex=True`, section titles are used in lieu of the section index page's title.
- When `navIndex=True` and on final depth level, any section without an index page will link to its first available page. The listing will be written as "**Section** > Page title"
- Furthermore, links to other pages are _relatively resolved_ from current page. This is to accommodate both subpaths and root-path mkdocs deployments.

[^1]: links to other objects like Sections and Pages