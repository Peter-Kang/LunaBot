from DataAccess.Util.LeagueDBCommandBase import LeagueDBCommandBase as base
import sqlite3

class SummonerDB(base):
    def __init__(self, sqliteConnection:sqlite3.Connection):
        super().__init__(sqliteConnection)

    def InitUserToSummonerMapping(self):
        query:str = ''' CREATE TABLE IF NOT EXISTS UserToSummonerMapping (
discordUserID TEXT PRIMARY KEY,
summonerName TEXT NOT NULL,
PUUID TEXT);'''
        super().sendVoidCommand(query)

    def addOrUpdateUserToSummonerMapping(self, discordID:str, summonerName:str, PUUID:str):
        query:str="INSERT OR REPLACE INTO UserToSummonerMapping(discordUserID, summonerName, PUUID) VALUES(?,?,?);"
        args:tuple = (str(discordID),str(summonerName),str(PUUID))
        super().sendVoidCommand(query, args)

    def getUserPUUID(self, discordID:str):
        query:str = "SELECT discordUserID, summonerName, PUUID FROM UserToSummonerMapping WHERE discordUserID = ?;"
        args:tuple = (str(discordID))
        return super().sendScalarCommand(query, args)

    def getAllUsers(self):
        query:str = "SELECT discordUserID, PUUID FROM UserToSummonerMapping;"
        return super().sendQueryCommand(query)