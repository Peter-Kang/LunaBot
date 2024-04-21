from DataAccess.Util.LeagueDBCommandBase import LeagueDBCommandBase as base
import sqlite3

class MatchesDB(base):
    def __init__(self, sqliteConnection:sqlite3.Connection):
        super().__init__(sqliteConnection)

    def initMatchesTable(self):
        query:str = "CREATE TABLE IF NOT EXISTS "
        pass

    def addOrIgnoreMatches(self):
        pass

    def clearPastDays(self, days:int):
        pass

    def getMatches(self, listOfMatches:tuple):
        pass