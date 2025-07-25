## These functions are just helpers
import os


def on_pre_page_macros(env):
    @env.macro
    def cwd(trailSlash=True):
        pagePath = os.path.dirname(env.conf["docs_dir"] + "/" + env.page.file.src_uri)
        trailingSlash = ""
        if trailSlash:
            trailingSlash = "/"
        return os.path.relpath(pagePath, os.getcwd()) + trailingSlash

    env.variables.cwd = cwd()
