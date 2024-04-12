from .components.champions import Champions 
from .components.summoners import Summoners
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
        
    def unregister(self, user: str, summoner:str):
        return None

    async def getUserStatus(self, userID:str):
        return await self.UserSummonerData.getStatus(userID)

        