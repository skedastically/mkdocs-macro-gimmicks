# Non-index.md navs and files

listfiles() and listnavs() can work here too

## listfiles()

```
{{ "{{ listfiles() }}" }}
```

### Result

{{ listfiles() }}

---

## listnav()

    ```
    {{ "{{ listnav(excludeCurrentPage = True) }}" }}
    ```

### Result

{{ listnav(excludeCurrentPage = True) }}

!!! note
    With `excludeCurrentPage = True`, `bar.md` is now excluded and `index.md` (titled "*Examples*") is now included

---