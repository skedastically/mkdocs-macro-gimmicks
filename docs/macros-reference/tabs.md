# Files + Navs content tabs

The `{{ "{{ tabnav() }}" }}` function provides selectable [content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/) that can view both files and navigations. For instance, the tabnav() of this directory has no files:

```
{{ "{{ tabnav(excludeCurrentPage = False) }}" }}
```

{{ tabnav(excludeCurrentPage = False) }}

!!! note "This function should not be called inside a paragraph/another element block as it won't render properly."

!!! note "Content tabs are an mkdocs-material only feature"

## Flags

| Name                 | Default value        | Description                                                                                              |
| -------------------- | -------------------- | -------------------------------------------------------------------------------------------------------- |
| `features`           | `nav,files`          | Comma-separated feature list, of which valid variables are `nav` and `files`                             |
| `depth`              | `0`                  | Depth of directory and nav trees                                                                         |
| `navTitle`           | `"📂 - Directory"`  | Title for the navigation content tab                                                                     |
| `dirTitle`           | `"🔗 - Navigation"` | Title for the directory content tab                                                                      |
| `squeeze`            | `True`               | If `False`, rendered lists are more vertically spaced. Works better in `mkdocs` and `readthedocs` themes |
| `navDepth`           | None                 | Depth level for navigation tree. Overrides `depth` if set                                                |
| `navIndex`           | `True`               | Attach `index.md` or `README.md` to a section's bulletpoint.                                             |
| `excludeCurrentPage` | `True`               | Whether to exclude current page from nav list                                                            |
| `dirDepth`           | None                 | Depth level for directory tree. Overrides `depth` if set                                                 |
| `rootNav`            | `False`              | If `True`, returns navigation from root dir regardless of current page                                   |
| `targetDir`          | `None`               | Directory to list in string format, relative to docs_dir                                                 |
| `showEmptyDirs`      | `False`              | Show dirs without any files and dirs at final depth                                                      |
