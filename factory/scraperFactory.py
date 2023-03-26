from Scraper.LihkgScraper import LihkgScraper
from Scraper.BabyDiscussScraper import BabyDiscussScraper
from Scraper.GoldenScraper import GoldenScraper
from Scraper.BabyKingdomScraper import BabyKingdomScraper

class ScraperFactory():
    def __init__(self):
        self.scraper = None

    def makeScraper(self, forum):
        match forum:
            case "lihkg":
                self.scraper = LihkgScraper()
            case "babyDiscuss":
                self.scraper = BabyDiscussScraper()
            case "golden":
                self.scraper = GoldenScraper()
            case "babyKingdom":
                self.scraper = BabyKingdomScraper()

    def findPosts(self, source):
        if self.scraper is not None:
            self.scraper.getPosts(source)

    def getComments(self, post):
        if self.scraper is not None:
            self.scraper.getCommentsInPosts(post)


