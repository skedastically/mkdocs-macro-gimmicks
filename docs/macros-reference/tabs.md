# Files + Navs content tabs

The `{{ "{{ tabnav() }}" }}` function provides selectable [content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/) to view both files and navigations. For instance, the tabnav() of this directory has no files:

{{ tabnav(excludeCurrentPage = False) }}

!!! note "This function should not be called inside a paragraph/another element block as it won't render properly."

!!! warning "Nested listings are not supported (yet?)"


## Flags

| Name                 | Default value        | Description                                                                                                                                                     |
| -------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `navTitle`           | `"📄 - Files"`      | Title for the navigation content tab                                                                                                                            |
| `filesTitle`         | `"🔗 - Navigation"` | Title for the files content tab                                                                                                                            |
| `findSectionIndex`   | `True`               | (from `listnavs()`) Attempt to find and use `index.md` or `README.md` as a subsection's index file, and fallback to whatever is the first file provided for that subsection's items list if nothing's found |
| `excludeCurrentPage` | `True`               | (from `listnavs()`) Whether to exclude current page from nav list                                                                                                                   |
| `excludeMarkdown`    | `True`               | (from `listfiles()`) Whether to exclude Markdown files from list                                                                                                                     |
| `squeeze`            | `True`              | Whether to render single-spaced lists (`True`) that looks squeezed rather than double-spaced lists (`False`)                                                    |
