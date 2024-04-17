from .components.champions import Champions 
from .components.summoners import Summoners, SummonerStat
from discord.emoji import Emoji
import random
from DatabaseLayer.LeagueDatabase import LeagueDatabase

class league:

    def __init__(self, riotAPIKey:str,db:LeagueDatabase):
        self.RIOT_API_KEY = riotAPIKey
        self.ChampionData = Champions(riotAPIKey)
        self.UserSummonerData = Summoners(riotAPIKey)
        self.db:LeagueDatabase = db
        self.userToSummonerPUUID = {}
        self.__initUserToSummonerPUUID()

    def __initUserToSummonerPUUID(self):
        result = self.db.getAllUsers()
        for row in result:
            self.userToSummonerPUUID[row[0]] = row[1]
        
    def randomChampion(self):
        champ_count = len(self.ChampionData.ChampionList)-1
        result = "No Data"
        if champ_count >= 0:
            index = random.randrange(0, champ_count, 1)
            result = self.ChampionData.ChampionList[index][0]
        return result

    def register(self, user:str , summoner:str):
        puuid = self.UserSummonerData.getSummonerPUUID( summoner )
        if(puuid != ""):
            self.userToSummonerPUUID[str(user)] = puuid
            self.db.addOrUpdateUserToSummonerMapping(user, summoner, puuid)
        return puuid

    async def getUserStatus(self, userID:str):
        if( not (userID in self.userToSummonerPUUID)):
            return ""
        puuid = self.userToSummonerPUUID[userID]
        sumStats:SummonerStat = await self.UserSummonerData.getStatus(puuid)
        result = f''':milk: In the past 7 Days:milk:
        Total Games: {sumStats.TotalGames}
        WinRate: {sumStats.WinRate}
        Time Spent: {sumStats.TotalTimeSpent}
        Gold Gained: {sumStats.TotalGold}
        Minions Merked: {sumStats.MinionsKilled}
        Flash Count: {sumStats.FlashCount}
        KDA: {'{0:.2f}'.format(((sumStats.Kills+sumStats.Assists)/sumStats.Deaths)) if sumStats.Deaths != 0 else "Undead" }
        Deaths: {sumStats.Deaths}
:milk:Cheers:milk:'''
        return result

        