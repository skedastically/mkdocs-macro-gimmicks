import os
import pathlib
import pathspec

from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation
from mrkdwn_analysis import MarkdownAnalyzer
import frontmatter

def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """

    @env.macro
    def listfiles(
            excludeMarkdown = True,
            squeeze = True
            ):

        """
        List all files in a page's current directory

        - excludeMarkdown: do not include Markdown as files, defaults to True
        """
        
        pagePath = env.page.file.src_uri
        pageDir = env.conf['docs_dir'] + "/" + os.path.dirname(pagePath)
        pageDirFiles = [f for f in os.listdir(pageDir) if os.path.isfile(os.path.join(pageDir, f))]

        # filter Markdown
        if excludeMarkdown == True:
            pageDirFiles = [f for f in pageDirFiles if f[-3:] != ".md"]

        # Filter by exclude_docs list which is a pathspec.gitignore.GitIgnoreSpec object
        matches = pageDirFiles
        if env.conf['exclude_docs'] != None:
            spec = env.conf['exclude_docs']
            matches = list(spec.match_files(pageDirFiles,negate=True))
        
        content = ""
        
        # Content list logic
        if squeeze == False:
            for match in matches:
                content = content + f"<ul><li><a href='{match}'>{match}</a></li></ul>"
        else:
            for match in matches:
                content = content + f"<li><a href='{match}'>{match}</a></li>"
            content = "<ul>" + content + "</ul>"
        return content
   
    @env.macro
    def listnav(
        depth=0,
        navIndex=True,
        excludeCurrentPage = True,
        rootNav = False,
        squeeze = True
        ):
        """
        List the navigation tree
        """

        def findSectionIndex(section):
            """
            Get a Section's index page and first page

            Return None if none is detected
            """
            sectionIndexCandidates = [child for child in section.children if child.is_page == True]
            sectionFirstPage = sectionIndexCandidates[0]
            for child in sectionIndexCandidates:
                try:
                    sectionIndexPage = [child for child in sectionIndexCandidates if str(os.path.basename(child.file.src_uri)) == "index.md"][0]
                except IndexError:
                    try:
                        sectionIndexPage = [child for child in sectionIndexCandidates if str(os.path.basename(child.file.src_uri)) == "README.md"][0]
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

                pagePath = env.conf['docs_dir'] + "/" + page.file.src_uri
                if page.title != None:
                    return page.title
                else:
                    try:
                        pageTitle = frontmatter.load(pagePath)['title']
                    except KeyError:
                        try:
                            pageTitle = MarkdownAnalyzer(pagePath).identify_headers()['Header'][0]['text']
                        except KeyError:
                            pageTitle = str(os.path.basename(pagePath)[:-3].capitalize())

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
            excludePage = env.page,
            navIndex = True,
            depth=depth,
            currentDepth=0,
            squeeze=squeeze
            ):
            
            content = ""

            for item in siblings:

                if depth >= currentDepth:

                    # Terminate links first
                    if item.is_link:
                        pageHeading = f'<a href="{item.url}">{item.title}</a>'
                        if squeeze == False:
                            pageHeading = f'<p>{pageHeading}</p>'
                        content = content + "<li>" + pageHeading + "</li>" 

                    elif item.is_section:
                        sectionTitle = f'<b>{item.title}</b>'
                        sectionIndexPage, sectionFirstPage = findSectionIndex(item)

                        # fetch index page or first page to serve as the representative section page
                        if sectionIndexPage != None:
                            sectionPageTitle, sectionPageUrl = getPageInfo(sectionIndexPage)
                        else:
                            sectionPageTitle, sectionPageUrl = getPageInfo(sectionFirstPage)

                        # only link to a section's representative page if last depth level reached
                        if depth == currentDepth:
                            sectionContent = ""
                            sectionHeading =  f'<a href="{sectionPageUrl}">{sectionTitle}</a>'
                            if sectionIndexPage == None or navIndex == False:
                                sectionHeading = f'{sectionTitle} > <a href="{sectionPageUrl}">{sectionPageTitle}</a>'

                        elif sectionIndexPage != None and navIndex == True:
                            sectionHeading = f'<a href="{sectionPageUrl}">{sectionTitle}</a>'
                            sectionContent = f'<ul>{gennav(item.children, excludePage = sectionIndexPage, depth=depth, currentDepth = currentDepth + 1)}</ul>'

                        elif sectionIndexPage == None or navIndex == False:
                            
                            sectionHeading = f'{sectionTitle}'
                            sectionContent = f'<ul>{gennav(item.children, excludePage = None, depth=depth, currentDepth = currentDepth + 1, navIndex = navIndex)}</ul>'
                        
                        if squeeze == False:
                            sectionHeading = f'<p>{sectionHeading}</p>'
                        content = content + '<li>' + sectionHeading + sectionContent + "</li>"
                            
                    elif item.is_page:
                        if item == excludePage:
                            continue
                        pageTitle, pageUrl = getPageInfo(item)
                        pageHeading = f'<a href="{pageUrl}">{pageTitle}</a>'
                        if squeeze == False:
                            pageHeading = f'<p>{pageHeading}</p>'
                        content = content + "<li>" + pageHeading + "</li>" 
                else:
                    break
            
            return content


        page = env.page
        nav = env.conf.nav
        
        # if page is at root dir (hence no parent)
        if page.parent == None or rootNav == True:
            siblings = nav.items
        else:
            siblings = env.page.parent.children
        
        excludePage = page
        if excludeCurrentPage == False:
            excludePage = None
        
        content = "<ul>" + gennav(siblings, depth=depth, navIndex=navIndex, excludePage=excludePage, squeeze=squeeze) + "</ul>"
        
        return content

    @env.macro
    def tabnav(        

        features = "nav,files",

        # content tab vars
        navTitle = "🔗 - Navigation",
        filesTitle = "📄 - Files",

        # nav vars
        navDepth = 0,
        navIndex = True,
        excludeCurrentPage = True,
        rootNav = False,

        # files vars
        excludeMarkdown = True,
        squeeze = True
    ):
        nav = listnav(
            depth=navDepth,
            navIndex=navIndex,
            excludeCurrentPage = excludeCurrentPage,
            rootNav = rootNav,
            squeeze=squeeze
            )

        files = listfiles(
            squeeze=squeeze,
            excludeMarkdown=excludeMarkdown)

        content = ""

        for feature in features.split(","):
            if feature == "nav":
                content = content + f'=== "{navTitle}"\n\n' + "\t" + nav + "\n\n\t---\n"
            elif feature == "files":
                content = content + f'=== "{filesTitle}"\n\n' + "\t" + files + "\n\n\t---\n"

        return content


    @env.macro
    def lsdir(
            depth = 0,
            targetDir = None,
            showEmptyDirs = True,
            squeeze = True,
            ):

        """
        List all files in a page's current directory
        """
        def squeezeItem(content,squeeze):
            if squeeze == False:
                print('unsqueeze')
                return f'<p>{content}</p>'
            else:
                return content        
        def gendir(
            dirEntry,
            depth=0,
            specMatch=None,
            showEmptyDirs=showEmptyDirs,
            currentDepth=0
            ):
            content = ""

            for item in dirEntry:
                itemSubcontent = ""
                if depth >= currentDepth:

                    # eliminate Markdowns or exclude_docs items
                    if (specMatch != None and specMatch.match_file(item.name) == True) or item.name[-3:] == ".md" or item.name[-9:] == ".markdown":
                        continue

                    elif item.is_dir():
                        
                        # collect info
                        itemHeading = squeezeItem("📁 " + item.name, squeeze=squeeze)
                        itemSubcontent = gendir(
                            dirEntry = os.scandir(item.path),
                            depth=depth,
                            specMatch = specMatch,
                            showEmptyDirs=showEmptyDirs,
                            currentDepth=currentDepth+1
                            )

                        if showEmptyDirs == True and (itemSubcontent == "" or currentDepth==depth ):
                            itemContent = itemHeading
                        elif showEmptyDirs == False and (itemSubcontent == "" or currentDepth==depth ):
                            continue
                        else:
                            itemContent = itemHeading + f'<ul>{itemSubcontent}</ul>'
                    elif item.is_file():
                        itemUrl = pathlib.PurePath(os.path.relpath(item.path,pagePath)).as_posix()
                        itemContent = squeezeItem(f'<a href="{itemUrl}">{item.name}</a>',squeeze=squeeze)
                else:
                    break
                content = content + f'<li>{itemContent}</li>'
            return content

        page = env.page
        pagePath = pathlib.PurePath(env.conf["docs_dir"]).as_posix() + "/" + env.page.file.src_uri
        
        # ignore pages if exclude_docs exists
        specMatch = None
        if env.conf['exclude_docs'] != None:
            specMatch = env.conf['exclude_docs']        

        # find targetDir if specified
        if isinstance(targetDir, str):
            targetDir = pathlib.PurePath(env.conf["docs_dir"]).as_posix() + "/" + targetDir
        else:
            targetDir = pathlib.PurePath(env.conf["docs_dir"]).as_posix() + "/" + os.path.dirname(env.page.file.src_uri)

        dirEntry = os.scandir(targetDir)        
        content = gendir(dirEntry, depth=depth,specMatch=specMatch, showEmptyDirs = showEmptyDirs)
        if content != "":
            content = f'<ul>{content}</ul>'
            return content
        else:
            return ""