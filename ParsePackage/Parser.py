
__author__ = 'Thomas Meijers'

class Parser:
    def __init__(self, parseQueue, parseStrategy):
        self.parseQueue = parseQueue # queue met alle links voor parsen
        self.parseStrategy = parseStrategy #strategy object

    #Main parse functie, word ook in task opgeroepen.
    def parse(self):
        while True:
            self.parseStrategy.parse(self.parseQueue.get())







