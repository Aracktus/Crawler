import threading

from CrawlerPackage import CrawlerBonque
from CrawlerPackage import CrawlerLinkedIn
from CrawlerPackage import CrawlerItjobboard
from CrawlerPackage import CrawlerIctergezocht
from CrawlerPackage import CrawlerItvacatures
from CrawlerPackage import Crawler
from ParsePackage import Parser
from ParsePackage import Strategy

# variables for string for website

bonque = "bonque"
itjobboard = "itjobboard"
itvacatures = "it-vacatures"
ictergezocht = "ictergezocht"
iitjobs = "iitjobs"
linkedin = "linkedin"

# The start method which starts the crawling when called
def start():
    crawlerLinkedIn = CrawlerLinkedIn.LinkedInCrawler("http://nl.linkedin.com/", "http://nl.linkedin.com/pub/", "databaseLinkedIn.db")
    parserlinkedIn = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInTwee = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInDrie = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInVier = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInVijf = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInZes = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInZeven = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInAcht = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))
    parserlinkedInNegen = Parser.Parser(crawlerLinkedIn.parseQueue, Strategy.ParseStrategy(linkedin))

    crawlerBonque = CrawlerBonque.BonqueCrawler("http://www.bonque.nl/", "http://www.bonque.nl/vacature/", "databaseBonque.db")
    parserBonque = Parser.Parser(crawlerBonque.parseQueue, Strategy.ParseStrategy(bonque))

    crawlerItjobboard = CrawlerItjobboard.ItjobboardCrawler("http://www.itjobboard.nl/", "http://www.itjobboard.nl/ICT-baan/", "databaseItjobboard.db")
    parserItjobboard = Parser.Parser(crawlerItjobboard.parseQueue, Strategy.ParseStrategy(itjobboard))

    crawlerIctergezocht = CrawlerIctergezocht.CrawlerIctergezocht("http://www.ictergezocht.nl/", "databaseIctergezocht.db")
    parserIctergezocht = Parser.Parser(crawlerIctergezocht.parseQueue, Strategy.ParseStrategy(ictergezocht))

    crawlerItvacatures = CrawlerItvacatures.CrawlerItvacatures("http://www.it-vacatures.nl/","http://www.it-vacatures.nl/job/", "databaseItvacatures.db")
    parserItvacatures = Parser.Parser(crawlerItvacatures.parseQueue, Strategy.ParseStrategy(itvacatures))

    crawlerIttjobs = Crawler.Crawler("http://www.iitjobs.com/", "databaseIttjobs.db")
    parserIitjobs = Parser.Parser(crawlerIttjobs.parseQueue, Strategy.ParseStrategy(iitjobs))


    tasks = [

        crawlerBonque.getLinks, parserBonque.parse,

        crawlerItjobboard.getLinks, parserItjobboard.parse,

        crawlerIctergezocht.getLinks, parserIctergezocht.parse,

        crawlerItvacatures.getLinks, parserItvacatures.parse,

    ]

    # is going to do every task in tasks next to each other -> new threads
    for task in tasks:
        t = threading.Thread(target=task)
        t.start()

#starts up the application
if __name__ == '__main__':
    start()
