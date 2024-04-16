from .components.champions import Champions 
from .components.summoners import Summoners, SummonerStat
from discord.emoji import Emoji
import random

class league:

    def __init__(self, riotAPIKey):
        self.RIOT_API_KEY = riotAPIKey
        self.ChampionData = Champions(riotAPIKey)
        self.UserSummonerData = Summoners(riotAPIKey)
        
    def randomChampion(self):
        champ_count = len(self.ChampionData.ChampionList)-1
        result = "No Data"
        if champ_count >= 0:
            index = random.randrange(0, champ_count, 1)
            result = self.ChampionData.ChampionList[index][0]
        return result

    def register(self, user:str , summoner:str):
        return self.UserSummonerData.register(user, summoner)

    async def getUserStatus(self, userID:str):
        sumStats:SummonerStat = await self.UserSummonerData.getStatus(userID)
        result = f''':milk: In the past 7 Days:milk:
        Total Games: {sumStats.TotalGames}
        WinRate: {sumStats.WinRate}
        Time Spent: {sumStats.TotalTimeSpent}
        Gold Gained: {sumStats.TotalGold}
        Minions Merked: {sumStats.MinionsKilled}
        Flash Count: {sumStats.FlashCount}
        KDA: {(sumStats.Kills+sumStats.Assists)/sumStats.Deaths}
        Deaths: {sumStats.Deaths}
        :milk:Cheers:milk:'''
        return result

        