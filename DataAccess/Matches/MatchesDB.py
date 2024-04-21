from DataAccess.Util.LeagueDBCommandBase import LeagueDBCommandBase as base
import sqlite3

class MatchesDB(base):
    def __init__(self, sqliteConnection:sqlite3.Connection):
        super().__init__(sqliteConnection)

    def initMatchesTable(self) -> None:
        query:str = "CREATE TABLE IF NOT EXISTS MatchCache ( MatchID TEXT PRIMARY KEY, EndTimeSecondsPastEpoch INTEGER NOT NULL ,Data TEXT NOT NULL )"
        super().sendVoidCommand(query)

    def addMatches(self, matchID:str, EndTimeSecondsPastEpoch:int, Data:str):
        query:str="INSERT OR REPLACE INTO MatchCache(discordUserID, summonerName, PUUID) VALUES(?,?,?);"
        args:tuple = (matchID,EndTimeSecondsPastEpoch,Data)
        super().sendVoidCommand(query, args)

    def clearPastDays(self, days:int) -> None:
        pass

    def getMatches(self, listOfMatches:tuple) -> list:
        pass