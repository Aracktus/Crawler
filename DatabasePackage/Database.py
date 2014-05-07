
__author__ = 'thomasmeijers'

import sqlite3

class Database():
    def __init__(self, naam):
        self.naam = "DatabasePackage/" + naam
        self.initDb()

    def initDb(self):
        conn = sqlite3.connect(self.naam)
        conn.execute('''DROP TABLE IF EXISTS LINKS''')
        conn.execute('''CREATE TABLE LINKS (LINK TEXT NOT NULL);''')
        print "Succesvol " + self.naam + " aangemaakt.";

        conn.close()
    def isLinkInDb(self, url):
        conn = sqlite3.connect(self.naam)
        cursor = conn.execute("SELECT LINK FROM LINKS WHERE LINK = (?)", (url,))
        cursor = list(cursor.fetchall())
        if len(cursor) > 0:
            conn.close()
            return True
        else:
            conn.close()
            return False

    def addToDb(self, url):
        conn = sqlite3.connect(self.naam)
        conn.execute("INSERT INTO LINKS (LINK) VALUES (?)", (url,));
        conn.commit()
        conn.close()
