from ParsePackage import ParseStrategy

__author__ = 'thomasmeijers'

import re
import time
from pyelasticsearch import ElasticSearch


class LinkedInParseStrategy(ParseStrategy.ParseStrategy):
    def __init__(self):
        self.website = "linkedin"
        # elasticsearch binden aan es
        self.es = ElasticSearch('http://95.85.28.128:9200/')

    def striphtml(self, data):
        try:
            p = re.compile(r'<.*?>')
            p = p.sub('', str(data))
            p = p.strip()
        except:
            None
        return p

    def parse(self, websiteUrl):
        try:
            soup = self.getSoup(websiteUrl)
        except Exception,e:
            print str(e)
            return

        # ----- Parsing Basis Info ----- #
        link = websiteUrl
        # Parsing naam
        naam = soup.find(class_="full-name")
        if naam != None:
            naam = self.striphtml(naam)

        else:
            return
        # Parsing titel
        titel = soup.find(class_="headline-title title")
        if titel != None:
            titel = self.striphtml(titel)

        else:
            return

        # Parsing locatie
        locatie = soup.find(class_="locality")
        if locatie != None:
            locatie = self.striphtml(locatie)
        else:
            locatie = "-"

        # Parsing industrie
        industrie = soup.find(class_="industry")
        if industrie != None:
            industrie = self.striphtml(industrie)
        else:
            industrie = "-"

        # ----- Parsing Overzicht ----- #

        # Parsing huidig
        huidig = soup.find(class_="current")
        if huidig != None:
            huidig = self.striphtml(huidig)
            huidig = re.sub(r'\W+', '', huidig)
            huidig = huidig.split("at", 3)
            try:
                huidigTitel = huidig[0]
                huidigInstelling = huidig[1]
            except:
                huidigTitel = "-"
                huidigInstelling = "-"
        else:
            huidigTitel = "-"
            huidigInstelling = "-"

        # Connecties
        connecties = soup.find(class_="overview-connections")
        if connecties != None:
            connecties = self.striphtml(connecties)
            connecties = re.findall(r'\d+', connecties)
            connecties = int(connecties[0])
        else:
            connecties = "-"

        # ----- Talen ----- #
        talen = soup.find_all("li", class_="competency language")
        inhoudTalen = []
        if talen != None:
            for taal in talen:
                t = taal.find('h3')
                t = t.text
                t = self.striphtml(t)
                t = re.sub(r'\W+', '', t)
                inhoudTalen.append(t)
        else:
            inhoudTalen = "-"

        # ----- Parsing vaardigheden ----- #
        vaardigheden = soup.find_all("span", class_="jellybean")
        inhoudVaardigheden = []
        if vaardigheden != None:
            for vaardigheid in vaardigheden:
                text = vaardigheid.text
                text = self.striphtml(text)
                inhoudVaardigheden.append(text)
        else:
            inhoudVaardigheden = ["-"]

        # ----- Parsing opleiding ----- #
        try:
            opleiding = soup.find(class_="position  first education vevent vcard")
            opleiding = opleiding.find("h4")
            opleiding = opleiding.text
            opleiding = self.striphtml(opleiding)
            if opleiding == "":
                opleiding = "-"
        except:
            opleiding = "-"

        # Datum van crawlen profiel
        datum = time.strftime("%d-%m-%Y")

        #ID is naam + functie + locatie tot 1 string
        id = naam + str(titel.__len__())
        id = re.sub(r'\W+', '', id)

        document = {'id' : id, 'datum': datum, 'link': link, 'basisinfo' : {'naam': naam, 'titel': titel, 'locatie': locatie,
                                                               'industrie': industrie},
                   'overzicht': {'huidig': {'titel' : huidigTitel, 'instelling' : huidigInstelling}, 'connecties': connecties},
                   'talen' : inhoudTalen, 'vaardigheden' : inhoudVaardigheden, 'opleiding': opleiding}

        #indexeren (stoppen) van vacaturen in esDb
        try:
            self.es.index('linkedin-index', 'linkedInProfiel', document, id=document['id'])
            print("Es: " + naam + " " + titel)
        except:
            print "opslaan in Es niet mogelijk"