__author__ = 'thomasmeijers'

import urllib2
from bs4 import BeautifulSoup
import re

class ParseStrategy:
    def makeDocument(self, id, titel, url, aanbieder, datum, werkgever, locatie, werktijd, inhoud):
        document = {'id' : id, 'titel': titel, 'url': url, 'aanbieder': aanbieder, 'datum': datum, 'werkgever': werkgever,
                       'locatie': locatie, 'werktijd':werktijd, 'inhoud': inhoud}
        return document

    def getSoup(self, websiteUrl):
        websiteUrl = websiteUrl
        websiteFile = urllib2.urlopen(websiteUrl)
        websiteHtml = websiteFile.read()
        websiteFile.close()
        soup = BeautifulSoup("".join(websiteHtml))
        return soup

    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)
