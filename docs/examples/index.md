# Examples

The directory details of `./example` is as below

=== "Directory tree"

    ```title="tree"
    .
    ├── _hidden.md
    ├── a-section
    │   ├── a-section.md
    │   ├── anotherdir
    │   │   ├── depth-2-page.md
    │   │   └── textfile.txt
    │   └── test.ipynb
    ├── another-section
    │   ├── README.md
    │   ├── example.toml
    │   └── firstpage.md
    ├── baz.md
    ├── foo.py
    ├── index.md
    └── non-index-page.md
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

## List all files in current directory


=== "Smaller paddings"
    ```
    {{ "{{ lsdir() }}" }}
    ```

    ### Result

    {{ lsdir() }}

=== "Larger paddings"
    ```
    {{ "{{ lsdir(squeeze=False) }}" }}
    ```
    
    ### Result

    {{ lsdir(squeeze=False) }}

---

## List directories and files at depth > 0

=== "`depth=1`"
    ```
    {{ "{{ lsdir(depth=1) }}" }}
    ```

    ### Result

    {{ lsdir(depth=1) }}

=== "`depth=2`"
    ```
    {{ "{{ lsdir(depth=2) }}" }}
    ```
    
    ### Result

    {{ lsdir(depth=2) }}

---

## List directories and files at depth > 0, but with `showEmptyDirs=True`

=== "`depth=1`"
    ```
    {{ "{{ lsdir(depth=1,showEmptyDirs=True) }}" }}
    ```

    ### Result

    {{ lsdir(depth=1,showEmptyDirs=True) }}

=== "`depth=2`"
    ```
    {{ "{{ lsdir(depth=2,showEmptyDirs=True) }}" }}
    ```
    
    ### Result

    {{ lsdir(depth=2,showEmptyDirs=True) }}

---


## List all non-Markdown, non-excluded files and folders from root path

```
{{ "{{ lsdir(depth=42,targetDir=\".\",showEmptyDirs=True) }}" }}
```

!!! tip
    Just use a big depth number e.g. **42** if you wanna walk every subdir

### Result

{{ lsdir(depth=42,targetDir=".",showEmptyDirs=True) }}

---

## List navigations

=== "With `navIndex=True`"
    ```
    {{ "{{ lsnav() }}" }}
    ```

    ### Result

    {{ lsnav() }}

    !!! info ""A File" is included as it was listed in `.nav.yml` as part of this section"

=== "With `navIndex=False`"
    ```
    {{ "{{ lsnav(navIndex=False) }}" }}
    ```
    
    ### Result

    {{ lsnav(navIndex=False) }}    

    !!! info ""A File" is included as it was listed in `.nav.yml` as part of this section"

    !!! info "The README.md page is now treated as a normal page inside the "Another section" section"

---

## List full-depth navigations starting from root and without navIndex

=== "Smaller paddings"

    ```
    {{ "{{ lsnav(depth=42, rootNav = True, navIndex = False) }}" }}
    ```

    ### Result

    {{ lsnav(depth=42, rootNav = True, navIndex = False) }}

=== "Larger paddings"

    ```
    {{ "{{ lsnav(depth=42, rootNav = True, navIndex = False, squeeze=False) }}" }}
    ```

    ### Result

    {{ lsnav(depth=42, rootNav = True, navIndex = False, squeeze=False) }}


---

## List navigations across multiple depths

=== "`depth=1`"
    ```
    {{ "{{ lsnav(depth = 1) }}" }}
    ```

    ### Result

    {{ lsnav(depth = 1) }}

=== "`depth=2`"
    ```
    {{ "{{ lsnav(depth = 2) }}" }}
    ```

    ### Result

    {{ lsnav(depth = 2) }}


---

## Content tab that shows files first, at full depth, and doesn't exclude anything

```
{{ "{{ tabnav(depth=42,features=\"files,nav\", excludeCurrentPage = False, showEmptyDirs=True) }}" }}
```

### Result

{{ tabnav(depth=42,features="files,nav",excludeCurrentPage = False, showEmptyDirs=True) }}