from .API.Champions import Champions as ChampionsAPI 
from .API.Summoners import Summoners as SummonersAPI, SummonerStat
import random
from DataAccess.LeagueDatabase import LeagueDatabase

class league:

    def __init__(self, riotAPIKey:str,db:LeagueDatabase):
        self.RIOT_API_KEY:str = riotAPIKey
        #API calls
        self.ChampionData:ChampionsAPI = ChampionsAPI(riotAPIKey)
        self.UserSummonerAPI:SummonersAPI = SummonersAPI(riotAPIKey)
        #Features/DataModels

        #Database
        self.db:LeagueDatabase = db
        self.userToSummonerPUUID:dict = {}
        self.__initUserToSummonerPUUID()

    def __initUserToSummonerPUUID(self):
        result:list = self.db.SummonerDB.getAllUsers()
        for row in result:
            self.userToSummonerPUUID[row[0]] = row[1]
        
    def randomChampion(self):
        champ_count:int = len(self.ChampionData.ChampionList)-1
        result:str = "No Data"
        if champ_count >= 0:
            index:int = random.randrange(0, champ_count, 1)
            result:str = self.ChampionData.ChampionList[index][0]
        return result

    def register(self, user:str , summoner:str):
        puuid:str = self.UserSummonerAPI.getSummonerPUUID( summoner )
        if(puuid != ""):
            self.userToSummonerPUUID[str(user)] = puuid
            self.db.SummonerDB.addOrUpdateUserToSummonerMapping(user, summoner, puuid)
        return puuid

    async def getUserStatus(self, userID:str):
        if( not (userID in self.userToSummonerPUUID)):
            return "Not Registered"
        puuid:str = self.userToSummonerPUUID[userID]
        sumStats:SummonerStat = await self.UserSummonerAPI.getStatus(puuid)
        return f''':milk: In the past 7 Days:milk:
        Total Games: {sumStats.TotalGames}
        WinRate: {sumStats.WinRate}
        Time Spent: {sumStats.TotalTimeSpent}
        Gold Gained: {sumStats.TotalGold}
        Minions Merked: {sumStats.MinionsKilled}
        Flash Count: {sumStats.FlashCount}
        KDA: {'{0:.2f}'.format(((sumStats.Kills+sumStats.Assists)/sumStats.Deaths)) if sumStats.Deaths != 0 else "Undead" }
        Deaths: {sumStats.Deaths}
:milk:Cheers:milk:'''