from ParsePackage import ParseStrategy

__author__ = 'thomasmeijers'

import re
import time
from pyelasticsearch import ElasticSearch


class ItjobboardParseStrategy(ParseStrategy.ParseStrategy):
    def __init__(self):
        self.website = "itjobboard"
        # elasticsearch binden aan es
        self.es = ElasticSearch('http://localhost:9200/')

    def parseTitel(self, soup):
        titel = soup.head.title.string
        return titel

    def parseWerkgever(self, soup):
        info = soup.find("td", {"id": "ContactOffice"})
        p = re.compile(r'<.*?>')
        werkgever = p.sub('', str(info))
        return werkgever

    def parseLocatie(self, soup):
        p = re.compile(r'<.*?>')
        infoLocatie = soup.find("td", {"id": "FreeLocation"})
        infoLocatie = p.sub('', str(infoLocatie))
        locatie = infoLocatie.strip()
        return locatie

    def parseInhoud(self, soup):
        body = soup.find(class_="jobText")
        inhoud = body.text
        return inhoud

    def parse(self, websiteUrl):
        soup = self.getSoup(websiteUrl)

        #parsen
        titel = self.parseTitel(soup)
        werkgever = self.parseWerkgever(soup)
        locatie = self.parseLocatie(soup)
        inhoud = self.parseInhoud(soup)
        websiteUrl = re.sub(r'(?s)/\*.*\*/', '', websiteUrl)
        datum = time.strftime("%d-%m-%Y")
        # generate id for website (string)
        id = self.website + "-" + re.sub(r'\W+', '', titel)

        # make document to be send to elasticsearch database
        document = self.makeDocument(id, titel, websiteUrl, self.website, datum, werkgever, locatie, "-", inhoud)

        #indexeren (stoppen) van vacaturen in esDb
        self.es.index('vacature-index', 'vacature', document, id=document['id'])
        print "Es: " + titel
