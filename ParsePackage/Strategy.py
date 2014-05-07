from ParsePackage import ParseStrategyIitjobs, ParseStrategyItjobboard, ParseStrategyItvacatures, ParseStrategyLinkedIn, \
    ParseStrategyIctergezocht, ParseStrategyBonque

__author__ = 'thomasmeijers'

#Strategy Pattern:
class ParseStrategy():
    def __init__(self, parseStrategy):
        if parseStrategy == "bonque":
            self.strategy = ParseStrategyBonque.BonqueParseStrategy()
        elif parseStrategy == "itjobboard":
            self.strategy = ParseStrategyItjobboard.ItjobboardParseStrategy()
        elif parseStrategy == "it-vacatures":
            self.strategy = ParseStrategyItvacatures.ItvacaturesParseStrategy()
        elif parseStrategy == "ictergezocht":
            self.strategy = ParseStrategyIctergezocht.IctergezochtParseStrategy()
        elif parseStrategy == "iitjobs":
            self.strategy = ParseStrategyIitjobs.IitjobsParseStrategy()
        elif parseStrategy == "linkedin":
            self.strategy = ParseStrategyLinkedIn.LinkedInParseStrategy()

    def parse(self, websiteurl):
        self.strategy.parse(websiteurl)