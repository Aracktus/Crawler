from ParsePackage import ParseStrategy

__author__ = 'thomasmeijers'

import re
import time
from pyelasticsearch import ElasticSearch


class ItvacaturesParseStrategy(ParseStrategy.ParseStrategy):
    def __init__(self):
        self.website = "it-vacatures"
        # elasticsearch binden aan es
        self.es = ElasticSearch('http://localhost:9200/')

    def parseTitel(self, soup):
        titel = soup.head.title.string
        return titel

    def parseWerkgever(self, soup):
        info = soup.find("td")
        infoTwee = info.find_next_sibling()
        p = re.compile(r'<.*?>')
        werkgever = p.sub('', str(infoTwee))
        return werkgever

    def parseLocatie(self, soup):
        info = soup.find("td")
        infoTwee = info.find_next_sibling()
        locatieEen = infoTwee.find_next()
        p = re.compile(r'<.*?>')
        locatieTwee = p.sub('', str(locatieEen))
        p = re.compile(r'Locatie')
        locatie = p.sub('', str(locatieTwee))
        locatie = locatie.strip()
        return locatie

    def parseInhoud(self, soup):
        body = soup.find("div", {"id": "job-description"})
        p = re.compile(r'<.*?>')
        inhoud = p.sub('', str(body))
        return inhoud

    def parse(self, websiteUrl):
        soup = self.getSoup(websiteUrl)

        # parsen
        titel = self.parseTitel(soup)
        try:
            werkgever = self.parseWerkgever(soup)
        except:
            werkgever = "-"
        try:
            locatie = self.parseLocatie(soup)
        except:
            locatie = "-"
        inhoud = self.parseInhoud(soup)
        websiteUrl = re.sub(r'(?s)/\*.*\*/', '', websiteUrl)
        datum = time.strftime("%d-%m-%Y")
        # generate id (string)
        id = self.website + "-" + re.sub(r'\W+', '', titel)

        # make document to be send to elasticsearch database
        document = self.makeDocument(id, titel, websiteUrl, self.website, datum, werkgever, locatie, "-", inhoud)

        #indexeren (stoppen) van vacaturen in esDb
        self.es.index('vacature-index', 'vacature', document, id=document['id'])
        print "Es: " + titel