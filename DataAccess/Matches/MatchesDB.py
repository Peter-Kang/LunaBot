from DataAccess.Util.LeagueDBCommandBase import LeagueDBCommandBase as base
from datetime import datetime, timedelta
import sqlite3

class MatchesDB(base):
    def __init__(self, sqliteConnection:sqlite3.Connection):
        super().__init__(sqliteConnection)

    def initMatchesTable(self) -> None:
        query:str = "CREATE TABLE IF NOT EXISTS MatchCache ( MatchID TEXT PRIMARY KEY, EndTimeSecondsPastEpoch INTEGER NOT NULL, Data TEXT NOT NULL );"
        super().sendVoidCommand(query)

    def addMatches(self, matchID:str, EndTimeSecondsPastEpoch:int, Data:str):
        query:str="INSERT OR REPLACE INTO MatchCache(MatchID, EndTimeSecondsPastEpoch, Data) VALUES(?,?,?);"
        args:tuple = (matchID,EndTimeSecondsPastEpoch,Data)
        super().sendVoidCommand(query, args)

    def clearPastDays(self, days:int) -> None:
        epoch = int((datetime.now() - timedelta(days=days)).timestamp())
        query:str = "DELETE FROM MatchCache WHERE EndTimeSecondsPastEpoch < ?;"
        args:tuple = (epoch)
        super().sendVoidCommand(query, args)

    def getMatches(self) -> list:
        query:str = "SELECT MatchID, EndTimeSecondsPastEpoch, Data FROM MatchCache;"
        return super().sendQueryCommand(query)