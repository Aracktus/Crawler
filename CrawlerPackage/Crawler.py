from DatabasePackage import Database

__author__ = 'Thomas Meijers'
import urllib3
from bs4 import BeautifulSoup
from urlparse import urljoin
import Queue
import re

_digits = re.compile('\d')

class Crawler():
    def __init__(self, websiteUrl, dataBase):
        self.websiteUrl = websiteUrl
        self.linksQueue = Queue.Queue()
        self.parseQueue = Queue.Queue()
        self.linksQueue.put(websiteUrl)
        self.http = urllib3.PoolManager()
        self.database = Database.Database(dataBase)

    def putInParseQue(self, page):
        if (page.find("/jobs/") != -1 and bool(_digits.search(page)) == True):
            self.parseQueue.put(page)

    def saveLinks(self, links, page):
        for link in links:
            if ('href' in dict(link.attrs)):
                url = urljoin(page, link['href'])
                if url[0:4] == 'http':
                    if url.startswith(self.websiteUrl) and not self.database.isLinkInDb(url):
                        self.linksQueue.put(url)
                        self.database.addToDb(url)

    def getLinks(self):
        while True:
            page = self.linksQueue.get()
            print page
            self.putInParseQue(page)
            try:
                # pagina openen met urllib2 library
                r = self.http.request('GET', page)
            except:
                # wanneer geen html pagina is
                print "Kan pagina niet openen: %s" % page
                continue
            # soup maken van de pagina
            try:
                soup = BeautifulSoup(r.data)
            except:
                print "Kan pagina niet lezen als soup"
                continue
            #zoek allen links op <a href...
            try:
                links = soup('a')
            except:
                print "Kan pagina niet tot een soup maken"
                continue
            self.saveLinks(links, page)

