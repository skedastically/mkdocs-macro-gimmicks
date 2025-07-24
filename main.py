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
