# List directory files

To list files of a page's current directory, simply call 

```
{{ "{{ lsdir() }}" }}
```

This function will walk current page's directory and list files/folders accordingly. With `depth > 0`, it'll also tries subdirectories and return them as nested listings.

!!! note "This function should not be called inside a paragraph/another element block as it won't render properly."

!!! tip "Note the differences"
    `lsdir()` walks a page's **current directory** to find siblings and niblings. `lsnav()` on the other hand walks a page's current Navigation, which is an [mkdocs-generated object](https://www.mkdocs.org/dev-guide/themes/#mkdocs.structure.nav.Navigation) that is **not representative** of the underlying files.

## Flags

You can also include these flags inside lsdir e.g. with `{{ "lsdir(depth = 2, squeeze = False)" }}`

| Name            | Default value | Description                                                                                              |
| --------------- | ------------- | -------------------------------------------------------------------------------------------------------- |
| `depth`         | `0`           | Depth of directory tree. 0 means only the current siblings are listed                                    |
| `targetDir`     | None          | Directory to list in string format, relative to docs_dir                                                 |
| `showEmptyDirs` | `False`        | Show dirs without any files and dirs at final depth |
| `squeeze`       | `True`        | If `False`, rendered lists are more vertically spaced. Works better in `mkdocs` and `readthedocs` themes |

## Caveats

- Instead of using the Files object, `lsdir()` walks the file directory on the current machine. This may be subject to filesystem quirks and features.