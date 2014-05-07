from ParsePackage import ParseStrategy

__author__ = 'thomasmeijers'

import re
import time
from pyelasticsearch import ElasticSearch


class BonqueParseStrategy(ParseStrategy.ParseStrategy):
    def __init__(self):
        self.website = "bonque"
        # elasticsearch binden aan es
        self.es = ElasticSearch('http://localhost:9200/')

    def parseTitel(self, soup):
        titel = soup.head.title.string
        return titel

    def parseWerkgever(self, soup):
        info = soup.find(class_="info")
        p = re.compile(r'<.*?>')
        infoText = p.sub('', str(info))
        p2 = re.compile(r'Werkgever ')
        werkgeverText = p2.sub('', infoText)
        p3 = re.compile(r'Locatie.*')
        werkgever = p3.sub('', werkgeverText)
        werkgever = werkgever.strip()
        return werkgever

    def parseLocatie(self, soup):
        info = soup.find(class_="info")
        p = re.compile(r'<.*?>')
        infoText = p.sub('', str(info))
        p2 = re.compile(r'Werkgever ')
        werkgeverText = p2.sub('', infoText)
        p4 = re.compile(r'(?s).*?Locatie ')
        locatie = p4.sub('', werkgeverText)
        locatie = locatie.strip()
        return locatie

    def parseInhoud(self, soup):
        body = soup.findAll('p')
        inhoud = ""
        for i in body:
            text = i.text
            text = re.sub('\'', '', text)
            text = text.strip()
            inhoud = inhoud + text.encode('utf8')
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
        #make id (str)
        id = self.website + "-" + re.sub(r'\W+', '', titel)

        # make document for elasticsearch db
        document = self.makeDocument(id, titel, websiteUrl, self.website, datum, werkgever, locatie, "-", inhoud)

        #indexeren (stoppen) van vacaturen in esDb
        self.es.index('vacature-index', 'vacature', document, id=document['id'])
        print "Es: " + titel
