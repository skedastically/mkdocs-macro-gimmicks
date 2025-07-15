# Non-index.md navs and files

listfiles() and listnavs() can work here too

=== "Code"

    ```
    {{ "{{ listfiles() }}" }}
    ```

=== "Result"

    {{ listfiles() }}

---

=== "Code"

    ```
    {{ "{{ listnavs(excludeCurrentPage = True) }}" }}
    ```

=== "Result"

    {{ listnavs(excludeCurrentPage = True) }}

    !!! note
        With `excludeCurrentPage = True`, `bar.md` is now excluded and `index.md` (titled "*Examples*") is now included
---