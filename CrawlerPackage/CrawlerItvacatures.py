from CrawlerPackage import Crawler
from DatabasePackage import Database

__author__ = 'thomasmeijers'
import urllib3
import Queue


class CrawlerItvacatures(Crawler.Crawler):
    #override init due to baseUrl
    def __init__(self, websiteUrl, baseUrl, dataBase):
        self.websiteUrl = websiteUrl
        self.baseUrl = baseUrl
        self.linksQueue = Queue.Queue()
        self.parseQueue = Queue.Queue()
        self.linksQueue.put(websiteUrl)
        self.http = urllib3.PoolManager()
        self.database = Database.Database(dataBase)

    #override
    def putInParseQue(self, page):
        if page.startswith(self.baseUrl):
                self.parseQueue.put(page)