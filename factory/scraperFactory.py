from Scraper.LihkgScraper import LihkgScraper

class ScraperFactory():
    def __init__(self):
        self.scraper = None

    def makeScraper(self, forum):
        match forum:
            case "lihkg":
                self.scraper = LihkgScraper()

    def findPosts(self, source):
        if self.scraper is not None:
            self.scraper.getPosts(source)

    def getComments(self, post):
        if self.scraper is not None:
            self.scraper.getCommentsInPosts(post)


