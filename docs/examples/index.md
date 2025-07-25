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
      - A File: a-section/a-section.md
      - Example website: https://example.com
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
{{ "{{ lsdir() }}" }}
```

### Result

{{ lsdir() }}

---

## List all files without Markdown and with larger list paddings

```
{{ "{{ lsdir(squeeze = True) }}" }}
```

### Result

{{ lsdir(squeeze = False) }}

---

## List navigations unsqueezed and with current page

```
{{ "{{ lsnav(excludeCurrentPage = False, squeeze = False) }}" }}
```

### Result

{{ lsnav(excludeCurrentPage = False, squeeze = False) }}

---

## List navigations starting from root and without navIndex

```
{{ "{{ lsnav(rootNav = True, navIndex = False) }}" }}
```

### Result

{{ lsnav(rootNav = True, navIndex = False) }}

!!! info
    The README.md page is now taken as the section's representative page

---

## List navigations with depth=1

```
{{ "{{ lsnav(depth = 1) }}" }}
```

### Result

{{ lsnav(depth = 1) }}

---

## Content tab that shows files first and doesn't exclude current page

```
{{ "{{ tabnav(features=\"files,nav\", excludeCurrentPage = False) }}" }}
```

### Result

{{ tabnav(features="files,nav",excludeCurrentPage = False) }}