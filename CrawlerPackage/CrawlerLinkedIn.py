from CrawlerPackage import Crawler
from DatabasePackage import Database

__author__ = 'thomasmeijers'

import Queue
import urllib3
from bs4 import BeautifulSoup
from urlparse import urljoin

alfabet = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']

class LinkedInCrawler(Crawler.Crawler):
    def __init__(self, websiteUrl, baseUrl, database):
        self.websiteUrl = websiteUrl
        self.baseUrl = baseUrl
        self.linksQueue = Queue.Queue()
        self.parseQueue = Queue.Queue()
        self.vulQueue()
        self.http = urllib3.PoolManager()
        self.database = Database.Database(database)

    def vulQueue(self):
        for z in alfabet:
            for x in range(98):
                for y in range(98):
                    self.linksQueue.put("http://nl.linkedin.com/directory/people-"+ z +"-" + str(x+1) + "-" + str(y+1))

    def getLinks(self):
        #blijft links in de que stoppen totdat die empty is.
        key = 0
        while True:
            page = self.linksQueue.get()
            r = self.http.request('GET', page)
            soup = BeautifulSoup(r.data)
            links = soup('a')
            for link in links:
                if ('href' in dict(link.attrs)):
                    url=urljoin(page,link['href'])
                    if url[0:4]=='http':
                        if not self.database.isLinkInDb(url):
                            if url.startswith("http://nl.linkedin.com/pub/") or url.startswith("http://nl.linkedin.com/directory/"):
                                if url.startswith("http://nl.linkedin.com/pub/dir/"):
                                    self.linksQueue.put(url)
                                elif url.startswith("http://nl.linkedin.com/pub/") or url.startswith("http://nl.linkedin.com/in/"):
                                    self.parseQueue.put(url)
                                    self.database.addToDb(url)



