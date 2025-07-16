import os
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
    def listnavs(
            findSectionIndex = True,
            excludeCurrentPage = True,
            squeeze = True
        ):
        """
        List navigation links of a Page's Section

        Returns bulletpointed hyperlinks with extracted titles
        """

        def findNavPage(
                nav,
                currentPage = env.page
                ):
            """
            Find current page to start navigation.
            Requires full Navigation object.

            - currentPage = Page variable
            """
            for navPage in nav.pages:
                # use Navigation.file.src_url as second checker
                if (
                    navPage.file.src_uri == currentPage.file.src_uri and
                    navPage.url == currentPage.url):
                    navPage = navPage
                    break
                else:
                    continue
            return navPage

        def findPageTitle(page):
            """
            find a Page object's title using the frontmatter, first header and filename
            """
            pagePath = env.conf['docs_dir'] + "/" + page.file.src_uri

            try:
                pageTitle = frontmatter.load(pagePath)['title']
            except KeyError:
                try:
                    pageTitle = MarkdownAnalyzer(pagePath).identify_headers()['Header'][0]['text']
                except KeyError:
                    pageTitle = str(os.path.basename(pagePath)[:-3].capitalize())

            return pageTitle

        def findSectionPage(
                sectionObject, 
                findSectionIndex = findSectionIndex
                ):
            """
            Get the default page of a section given a Section object

            - findSectionIndex: if True, finds section's index.md or README.md to use as default page. If False, returns first item in list if exists
            """
            sectionIndex = None 
            
            if findSectionIndex == True and len(sectionObject.children) > 0:
                sectionIndexCandidates = [child for child in sectionObject.children if child.is_section == False]
                try:
                    sectionIndex = [child for child in sectionIndexCandidates if str(os.path.basename(child.file.src_uri)) == "index.md"][0]
                except IndexError:
                    try:
                        sectionIndex = [child for child in sectionIndexCandidates if str(os.path.basename(child.file.src_uri)) == "README.md"][0]
                    except IndexError:
                        sectionIndex = navObject.children[0]
            
            else:
                sectionIndex = navObject.children[0]

            return sectionIndex
        
        def findObjectInfo(navObject):
            """
            Finds info of a Navigation object in the listnav context,
            Requires passing through the navObject in question.
            
            Returns derived title of section/page as resultTitle
            and derived Url as resultUrl
            """
            if navObject.is_section:
                resultTitle = navObject.title
                subsectionPage = findSectionPage(navObject, findSectionIndex = findSectionIndex)
                resultUrl = subsectionPage.url
            else:    
                resultTitle = findPageTitle(navObject)
                resultUrl = "/" + navObject.url
            return resultTitle, resultUrl

        nav = env.conf.nav
        if nav == None: # if not item exists
            files = get_files(env.conf)
            nav = get_navigation(files, env.conf)

        navPage = findNavPage(nav)
        
        try:
            navParentChildren = navPage.parent.children
        except AttributeError:
            # pages in root dir has no parent, use root nav list instead
            navParentChildren = nav.items

        navList = {}

        for navObject in navParentChildren:
            # raise excludeCurrentPage exception
            if (
                excludeCurrentPage and
                navObject.is_section == False and 
                navObject.url in ["./",""] # object is first index page
                
            ):
                continue
            if (
                excludeCurrentPage and
                navObject.is_section == False and 
                navObject.url == navPage.file.url
            ):
                continue


            resultTitle, resultUrl =  findObjectInfo(navObject)
            navList[resultTitle] = resultUrl
            

        content = ""
        contentTitle = ""
        
        # squeezed listing logic
        if squeeze == False:
            for navItem in navList:
                content = content + f"<ul><li><a href='{navList[navItem]}'>{navItem}</a></li></ul>"
        else:
            for navItem in navList:
                content = content + f"<li><a href='{navList[navItem]}'>{navItem}</a></li>"
            content = "<ul>" + content + "</ul>"
        
        return content

    @env.macro
    def tabnav(        

        # content tab vars
        navTitle = "🔗 - Navigation",
        filesTitle = "📄 - Files",

        # nav vars
        findSectionIndex = True,
        excludeCurrentPage = True,

        # files vars
        excludeMarkdown = True,
        squeeze = True
    ):
        nav = listnavs(findSectionIndex = findSectionIndex,excludeCurrentPage = excludeCurrentPage,squeeze=squeeze)

        files = listfiles(squeeze=squeeze,excludeMarkdown=excludeMarkdown)

        content = f'=== "{navTitle}"\n\n' + "    " + nav + "\n\n"
        content = content + f'=== "{filesTitle}"\n\n' + "    " + files + "\n\n"
        return content