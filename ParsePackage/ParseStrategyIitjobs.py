from ParsePackage import ParseStrategy

__author__ = 'thomasmeijers'

import re
import time
from pyelasticsearch import ElasticSearch


class IitjobsParseStrategy(ParseStrategy.ParseStrategy):
    def __init__(self):
        self.website = "iitjobs"
        # elasticsearch binden aan es
        self.es = ElasticSearch('http://localhost:9200/')

    def parseTitel(self, soup):
        titel = soup.head.title.string
        titel = titel.strip()
        return titel

    def parseWerkgever(self, soup):
        body = soup.find("span", {"id": "ctl00_middleContent_idShowJobDetails_lblCompanyName"})
        p = re.compile(r'<.*?>')
        werkgever = p.sub('', str(body))
        werkgever = werkgever.strip()
        return werkgever

    def parseLocatie(self, soup):
        body = soup.find("span", {"id": "ctl00_middleContent_idShowJobDetails_lblCountryID"})
        p = re.compile(r'<.*?>')
        locatie = p.sub('', str(body))
        locatie = locatie.strip()
        return locatie

    def parseInhoud(self, soup):
        body = soup.find("div", {"id": "divJobDescrip"})
        p = re.compile(r'<.*?>')
        inhoud = p.sub('', str(body))
        inhoud = inhoud.strip()
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
        print('Es: ' + titel)