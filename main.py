import os
import pathlib
from mrkdwn_analysis import MarkdownAnalyzer
import frontmatter

def squeezeItem(content, squeeze):
    """
    Return <p>item content</p> if squeeze is False
    """
    if not squeeze:
        return f"<p>{content}</p>"
    else:
        return content

def resolveListStyle(listStyle):
    """
    Determines list-style-type CSS attribute
    """
    if listStyle[0:4] == "css:":
        return listStyle[4:]
    else:
        return f"'{listStyle} '"


def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """

    @env.macro
    def lsnav(
        depth=0,
        navIndex=True,
        excludeCurrentPage=True,
        rootNav=False,
        squeeze=True,
        listStyle="css:square",
    ):
        """
        List the navigation tree
        """

        def findSectionIndex(section):
            """
            Get a Section's index page and first page

            Return None if none is detected
            """
            sectionIndexCandidates = [
                child for child in section.children if child.is_page
            ]
            if sectionIndexCandidates == []:
                return None, None
            else:
                sectionFirstPage = sectionIndexCandidates[0]
                for child in sectionIndexCandidates:
                    try:
                        sectionIndexPage = [
                            child
                            for child in sectionIndexCandidates
                            if str(os.path.basename(child.file.src_uri)) == "index.md"
                        ][0]
                    except IndexError:
                        try:
                            sectionIndexPage = [
                                child
                                for child in sectionIndexCandidates
                                if str(os.path.basename(child.file.src_uri))
                                == "README.md"
                            ][0]
                        except IndexError:
                            sectionIndexPage = None
                return sectionIndexPage, sectionFirstPage

        def getPageInfo(page):
            """
            Fetches info of a Page object

            Returns derived title of section/page as pageTitle
            and relative Url (compared to env.page.url) as pageUrl
            """

            def findPageTitle(page):
                """
                find a Page object's title using the frontmatter, first header and filename
                """

                pagePath = env.conf["docs_dir"] + "/" + page.file.src_uri
                if page.title is not None:
                    return page.title
                else:
                    try:
                        pageTitle = frontmatter.load(pagePath)["title"]
                    except KeyError:
                        try:
                            pageTitle = MarkdownAnalyzer(pagePath).identify_headers()[
                                "Header"
                            ][0]["text"]
                        except KeyError:
                            pageTitle = str(
                                os.path.basename(pagePath)[:-3].capitalize()
                            )

                return pageTitle

            def findPageUrl(page):
                pageUrl = os.path.relpath("/" + page.url, "/" + env.page.url)
                pageUrl = pathlib.PurePath(pageUrl).as_posix()
                return pageUrl

            pageTitle = findPageTitle(page)
            pageUrl = findPageUrl(page)

            return pageTitle, pageUrl

        def gennav(
            siblings,
            excludePage=env.page,
            navIndex=True,
            depth=depth,
            currentDepth=0,
            squeeze=squeeze,
            listStyle=listStyle,
        ):
            content = ""

            for item in siblings:
                if depth >= currentDepth:
                    # Terminate links first
                    if item.is_link:
                        itemContent = squeezeItem(
                            f'<a href="{item.url}">{item.title}</a>', squeeze
                        )

                    elif item.is_section:
                        # collect section info
                        sectionContent = ""
                        sectionTitle = f"<b>{item.title}</b>"
                        sectionIndexPage, sectionFirstPage = findSectionIndex(item)

                        # fetch index page or first page to serve as the representative section page
                        if sectionIndexPage is not None:
                            sectionPage = sectionIndexPage
                            sectionPageTitle, sectionPageUrl = getPageInfo(sectionPage)

                        elif sectionFirstPage is not None:
                            sectionPage = sectionFirstPage
                            sectionPageTitle, sectionPageUrl = getPageInfo(sectionPage)
                        else:
                            sectionPage = None

                        # only link to a section's representative page if last depth level reached
                        if depth == currentDepth:
                            if sectionPage is None:
                                sectionHeading = f"{sectionTitle}"
                            elif sectionIndexPage is None or not navIndex:
                                sectionHeading = f'{sectionTitle} > <a href="{sectionPageUrl}">{sectionPageTitle}</a>'
                            else:
                                sectionHeading = (
                                    f'<a href="{sectionPageUrl}">{sectionTitle}</a>'
                                )

                        elif sectionIndexPage is not None and navIndex:
                            sectionHeading = (
                                f'<a href="{sectionPageUrl}">{sectionTitle}</a>'
                            )
                            sectionContent = f"<ul>{
                                gennav(
                                    item.children,
                                    excludePage=sectionIndexPage,
                                    depth=depth,
                                    listStyle=listStyle,
                                    currentDepth=currentDepth + 1,
                                )
                            }</ul>"

                        elif (
                            sectionIndexPage is None
                            or sectionFirstPage is None
                            or not navIndex
                        ):
                            sectionHeading = f"{sectionTitle}"
                            sectionContent = f"<ul>{gennav(item.children, excludePage=None, depth=depth, currentDepth=currentDepth + 1, navIndex=navIndex)}</ul>"

                        itemContent = (
                            squeezeItem(sectionHeading, squeeze=squeeze)
                            + sectionContent
                        )

                    elif item.is_page:
                        if item == excludePage:
                            continue
                        pageTitle, pageUrl = getPageInfo(item)
                        itemContent = squeezeItem(
                            f'<a href="{pageUrl}">{pageTitle}</a>', squeeze
                        )

                else:
                    break
                content = (
                    content
                    + f'<li style="list-style-type: {listStyle}">{itemContent}</li>'
                )
            return content

        page = env.page
        nav = env.conf.nav
        listStyle = resolveListStyle(listStyle)

        # if page is at root dir (hence no parent)
        if page.parent is None or rootNav:
            siblings = nav.items
        else:
            siblings = env.page.parent.children

        excludePage = page
        if not excludeCurrentPage:
            excludePage = None

        content = gennav(
            siblings,
            depth=depth,
            navIndex=navIndex,
            excludePage=excludePage,
            squeeze=squeeze,
            listStyle=listStyle,
        )

        if content != "":
            content = f"<ul>{content}</ul>"
            return content
        else:
            return ""

    @env.macro
    def lsdir(
        depth=0,
        targetDir=None,
        showEmptyDirs=False,
        squeeze=True,
        listStyle="└─",
    ):
        """
        List all files in a page's current directory
        """

        def gendir(
            dirEntry,
            depth=0,
            showEmptyDirs=showEmptyDirs,
            listStyle=listStyle,
            specMatch=None,
            currentDepth=0,
        ):
            content = ""

            for item in dirEntry:
                itemSubcontent = ""
                if depth >= currentDepth:
                    # eliminate Markdowns or exclude_docs items
                    if (
                        (specMatch is not None and specMatch.match_file(item.name))
                        or item.name[-3:] == ".md"
                        or item.name[-9:] == ".markdown"
                    ):
                        continue

                    elif item.is_dir():
                        # collect info
                        itemHeading = "📁 " + item.name
                        itemSubcontent = gendir(
                            dirEntry=os.scandir(item.path),
                            depth=depth,
                            showEmptyDirs=showEmptyDirs,
                            listStyle=listStyle,
                            specMatch=specMatch,
                            currentDepth=currentDepth + 1,
                        )

                        if showEmptyDirs and (
                            itemSubcontent == "" or currentDepth == depth
                        ):
                            itemContent = itemHeading
                        elif not showEmptyDirs and (
                            itemSubcontent == "" or currentDepth == depth
                        ):
                            continue
                        else:
                            itemContent = (
                                squeezeItem(itemHeading, squeeze=squeeze)
                                + f"<ul>{itemSubcontent}</ul>"
                            )
                    elif item.is_file():
                        itemUrl = pathlib.PurePath(
                            os.path.relpath(item.path, os.path.dirname(pagePath))
                        ).as_posix()
                        itemContent = squeezeItem(
                            f'<a href="{itemUrl}">{item.name}</a>', squeeze=squeeze
                        )
                else:
                    break
                content = (
                    content
                    + f'<li style="list-style-type: {listStyle}">{itemContent}</li>'
                )
            return content

        page = env.page
        pagePath = (
            pathlib.PurePath(env.conf["docs_dir"]).as_posix() + "/" + page.file.src_uri
        )
        listStyle = resolveListStyle(listStyle)

        # ignore pages if exclude_docs exists
        specMatch = None
        if env.conf["exclude_docs"] is not None:
            specMatch = env.conf["exclude_docs"]

        # find targetDir if specified
        if isinstance(targetDir, str):
            targetDir = (
                pathlib.PurePath(env.conf["docs_dir"]).as_posix() + "/" + targetDir
            )
        else:
            targetDir = (
                pathlib.PurePath(env.conf["docs_dir"]).as_posix()
                + "/"
                + os.path.dirname(env.page.file.src_uri)
            )

        dirEntry = os.scandir(targetDir)
        content = gendir(
            dirEntry,
            depth=depth,
            specMatch=specMatch,
            showEmptyDirs=showEmptyDirs,
            listStyle=listStyle,
        )

        if content != "":
            content = f"<ul>{content}</ul>"
            return content
        else:
            return ""

    @env.macro
    def tabnav(
        # common vars
        features="nav,files",
        depth=0,
        navTitle="🔗 - Navigation",
        dirTitle="📂 - Directory listing",
        squeeze=True,
        # nav vars
        navDepth=None,
        navIndex=True,
        excludeCurrentPage=True,
        rootNav=False,
        # files vars
        dirDepth=None,
        targetDir=None,
        showEmptyDirs=False,
    ):
        content = ""

        if navDepth is None:
            navDepth = depth
        if dirDepth is None:
            dirDepth = depth

        for feature in features.split(","):
            if feature == "nav":
                nav = lsnav(
                    depth=navDepth,
                    navIndex=navIndex,
                    excludeCurrentPage=excludeCurrentPage,
                    rootNav=rootNav,
                    squeeze=squeeze,
                )
                content = content + f'=== "{navTitle}"\n\n\t{nav}\n\n\t---\n'
            elif feature == "files":
                files = lsdir(
                    depth=dirDepth,
                    targetDir=targetDir,
                    showEmptyDirs=showEmptyDirs,
                    squeeze=squeeze,
                )
                content = content + f'=== "{dirTitle}"\n\n\t{files}\n\n\t---\n'

        return content
