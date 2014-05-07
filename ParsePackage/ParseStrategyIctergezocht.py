from ParsePackage import ParseStrategy

__author__ = 'thomasmeijers'

import re
import time
from pyelasticsearch import ElasticSearch

class IctergezochtParseStrategy(ParseStrategy.ParseStrategy):
    def __init__(self):
        self.website = "ictergezocht"
        # elasticsearch binden aan es
        self.es = ElasticSearch('http://localhost:9200/')

    def parseWerkgever(self, soup):
        info = soup.find(class_="highlight")
        p = re.compile(r'<.*?>')
        werkgever = p.sub('', str(info))
        return werkgever

    def parseLocatie(self, soup):
        infoTwee = soup.find(class_="bf")
        locatieEen = infoTwee.find_next()
        locatieTwee = locatieEen.find_next()
        locatieDrie = locatieTwee.find_next()
        locatieVier = locatieDrie.find_next()
        p = re.compile(r'<.*?>')
        locatieVijf = p.sub('', str(locatieVier))
        p = re.compile(r'Locatie')
        locatie = p.sub('', str(locatieVijf))
        locatie = locatie.strip()
        return locatie

    def parseInhoud(self, soup):
        body = soup.find(class_="vacancybody")
        p = re.compile(r'<.*?>')
        inhoud = p.sub('', str(body))
        return inhoud

    def parseTitel(self, soup):
        titel = soup.head.title.string
        return titel

    def parse(self, websiteUrl):
        soup = self.getSoup(websiteUrl)

        titel = self.parseTitel(soup)
        if titel.startswith("Vacature"):
            #parsen
            werkgever = self.parseWerkgever(soup)
            locatie = self.parseLocatie(soup)
            inhoud = self.parseInhoud(soup)
            websiteUrl = re.sub(r'(?s)/\*.*\*/', '', websiteUrl)
            datum = time.strftime("%d-%m-%Y")
            # generate id website (string)
            id = self.website + "-" + re.sub(r'\W+', '', titel)

            #make document
            document = self.makeDocument(id, titel, websiteUrl, self.website, datum, werkgever, locatie, "-", inhoud)
            #indexeren (stoppen) van vacaturen in esDb
            self.es.index('vacature-index', 'vacature', document, id=document['id'])
            print "Es: " + titel
