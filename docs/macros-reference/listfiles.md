# List directory files

To list files of a page's current directory, simply call 

```
{{ "{{ listfiles() }}" }}
```

As a feature, this function also match ignore patterns in mkdocs.yml's `exclude_docs:` parameter, so hidden files can stay outside of the list.

!!! note "This function should not be called inside a paragraph/another element block as it won't render properly."

!!! warning "Nested listings are not supported (yet?)"

## Flags

You can also include these flags inside listfiles e.g. with `{{ "listfiles(title = True, squeeze = False)"}}`

| Name              | Default value | Description                                                                                                                                                  |
| ----------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `title`           | `False`        | Title of the files list inside an `#!html <h2>` element, provided as a string. Also defaults to "Files in this directory" if `True`, and no title if `False` |
| `excludeMarkdown` | `True`        | Whether to exclude Markdown files from list                                                                                                                  |
| `squeeze`         | `False`       | Whether to render single-spaced lists (`True`) that looks squeezed rather than double-spaced lists (`False`)                                                 |
