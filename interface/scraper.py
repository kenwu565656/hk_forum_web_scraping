from abc import ABC, abstractmethod


class Scraper(ABC):

    @abstractmethod
    def getPosts(self, source):
        pass

    @abstractmethod
    def getCommentsInPosts(self, postUrl):
        pass
