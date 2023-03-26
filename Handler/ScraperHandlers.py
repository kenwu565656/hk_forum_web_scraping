from factory.scraperFactory import ScraperFactory


def scraperHandler(forum):
    factory = ScraperFactory()
    factory.makeScraper(forum)
    factory.findPosts("1")
    factory.getComments("")


