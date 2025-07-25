# Non-index.md navs and files

lsdir() and lsnavs() can work here too

## lsdir()

```
{{ "{{ lsdir() }}" }}
```

### Result

{{ lsdir() }}

---

## lsnav()

    ```
    {{ "{{ lsnav(excludeCurrentPage = True) }}" }}
    ```

### Result

{{ lsnav(excludeCurrentPage = True) }}

!!! note
    With `excludeCurrentPage = True`, `bar.md` is now excluded and `index.md` (titled "*Examples*") is now included

---