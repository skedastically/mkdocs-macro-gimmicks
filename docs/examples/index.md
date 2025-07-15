# Examples

The directory details of `./example` is as below

=== "Tree"

    ```
    .
    ├── _hidden.md
    ├── another-section
    │   ├── firstpage.md
    │   ├── README.md
    │   └── .nav.yml
    ├── bar.md
    ├── foo.py
    └── index.md
    ```

=== "`./.nav.yml`"

    ```yaml
    nav:
      - index.md
      - "*"
    ```

=== "`./another-section/.nav.yml`"

    ```yaml
    nav:
    - firstpage.md
    - readme.md
    ```

---

## List all files including Markdown

```
{{ "{{ listfiles(excludeMarkdown = False, squeeze = True) }}" }}
```

### Result

{{ listfiles(excludeMarkdown = False, squeeze = True) }}

---

## List all files without Markdown and with larger list paddings

```
{{ "{{ listfiles(title = 'See all files here', squeeze = True) }}" }}
```

### Result

{{ listfiles(squeeze = False) }}

---

## List navigations unsqueezed and with current page

```
{{ "{{ listnavs(excludeCurrentPage = False, squeeze = False) }}" }}
```

### Result

{{ listnavs(excludeCurrentPage = False, squeeze = False) }}

---

## List navigations without finding section index

```
{{ "{{ listnavs(findSectionIndex = False) }}" }}
```

### Result

{{ listnavs(findSectionIndex = False) }}

!!! info
    The firstpage, as ordered in `example/another-section/.nav.yml` is now taken as the section's entrypoint page

---

## Content tab that shows the maximum of everything in this directory

```
{{ "{{ tabnav(excludeMarkdown = False, excludeCurrentPage = False) }}" }}
```

### Result

{{ tabnav(excludeMarkdown = False, excludeCurrentPage = False) }}