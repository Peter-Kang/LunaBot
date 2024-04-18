import sqlite3
from .Summoner.SummonerDB import SummonerDB

class LeagueDatabase:

    def __init__(self, dataPath:str, fileName:str):
        fileNameAndPath:str = ""; 
        if(dataPath.endswith("\\") or dataPath.endswith("/")):
            fileNameAndPath = dataPath+fileName
        else:
            fileNameAndPath = dataPath+"/"+fileName
        self.Path:str = fileNameAndPath
        self.sqliteConnection = sqlite3.connect(self.Path)
        self.SummonerDB:SummonerDB = SummonerDB(self.sqliteConnection)
        self.InitTables()
        
    def __del__(self):
        if self.sqliteConnection:
            self.sqliteConnection.close()

    def InitTables(self):
        self.SummonerDB.InitUserToSummonerMapping()