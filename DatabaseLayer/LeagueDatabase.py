import sqlite3

class LeagueDatabase:

    def __init__(self, dataPath:str, fileName:str):
        fileNameAndPath:str = ""; 
        if(dataPath.endswith("\\") or dataPath.endswith("/")):
            fileNameAndPath = dataPath+fileName
        else:
            fileNameAndPath = dataPath+"/"+fileName
        self.Path:str = fileNameAndPath
        self.sqliteConnection = sqlite3.connect(self.Path)
        self.InitTables()
        
    def __del__(self):
        if self.sqliteConnection:
            self.sqliteConnection.close()

    def InitTables(self):
        self.InitUserToSummonerMapping()

    def InitUserToSummonerMapping(self):
        query:str = ''' CREATE TABLE IF NOT EXISTS UserToSummonerMapping (
discordUserID TEXT PRIMARY KEY,
summonerName TEXT NOT NULL,
PUUID TEXT);'''
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query)
        cursor.close()

    def sendVoidCommand(self, query:str, args:tuple):
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query,args)
        cursor.close()
        self.sqliteConnection.commit()

    def addOrUpdateUserToSummonerMapping(self, discordID:str, summonerName:str, PUUID:str):
        query:str="INSERT OR REPLACE INTO UserToSummonerMapping(discordUserID, summonerName, PUUID) VALUES(?,?,?);"
        args:tuple = (str(discordID),str(summonerName),str(PUUID))
        self.sendVoidCommand(query, args)

    def getUserPUUID(self, discordID:str):
        query:str = "SELECT discordUserID, summonerName, PUUID FROM UserToSummonerMapping WHERE discordUserID = ?;"
        args = (discordID)
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchone()
        cursor.close()
        return result

    def getAllUsers(self):
        query:str = "SELECT discordUserID, PUUID FROM UserToSummonerMapping"
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query)
        results = cursor.fetchmany()
        cursor.close()
        return results