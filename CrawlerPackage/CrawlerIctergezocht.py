from CrawlerPackage import Crawler

__author__ = 'thomasmeijers'


class CrawlerIctergezocht(Crawler.Crawler):
    #override
    def putInParseQue(self, page):
        if page.find("/ict-vacatures/")!=-1:
            self.parseQueue.put(page)