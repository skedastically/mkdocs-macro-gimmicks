# Installation

Most scripts here requires the [mkdocs-macro-plugin](https://github.com/fralau/mkdocs-macros-plugin) which involves some setting up

## Install macros

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

## Create `main.py`:

In your project's root directory (**not** the docs directory), create a `main.py` file and copy the contents of main.py into it. 

Now you can start using commands such as `{{ "{{ listfiles() }}" }}`

If you already used macros with the file, simply append the scripts inside `def define_env(env):` to your file.

## Further resources

- mkdocs-macro-plugin's [website](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)
