# Installation

Assuming you're inside your mkdocs project directory...

## 1. Install macros

Install **macros** via [mkdocs-macro-plugin](https://mkdocs-macros-plugin.readthedocs.io/en/latest/#installation) as well as required packages

```bash
pip install mkdocs-macro-plugin mrkdwn_analysis pathspec python-frontmatter
```

And include it in your `mkdocs.yml` file:

```yml
plugins:
  - search
  - macros
```

## 2. Create an mkdocs hook

Add an mkdocs [hook](https://www.mkdocs.org/user-guide/configuration/#hooks) e.g. `hooks.py` in your project's root directory (**not** the docs directory) with the following content:
   
```python title="hooks.py"
def on_nav(nav, config, files):
    # overrides config.nav for macros use
    config.nav = nav
    return nav
```

This is important for use in [lsnav()](macros-reference/lsnav.md), as it allows the macro to receive nav events from mkdocs/other plugins.

## 3. Create `main.py`:

Copy the contents of [main.py](https://github.com/skedastically/mkdocs-macro-gimmicks/blob/main/main.py) into the project directory.

With wget:

```bash
wget https://raw.githubusercontent.com/skedastically/mkdocs-macro-gimmicks/main/main.py
```

Now you can start using commands such as `{{ "{{ lsdir() }}" }}` and see their results during `mkdocs serve`

## Further resources

- mkdocs-macro-plugin's [website](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)
