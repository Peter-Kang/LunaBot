from .components.champions import Champions 
import random

class league:

    def __init__(self, riotAPIKey):
        self.RIOT_API_KEY = riotAPIKey
        self.ChampionData = Champions(riotAPIKey)
        self.UserToSummoner = {}
        
    def randomChampion(self):
        champ_count = len(self.ChampionData.ChampionList)-1
        result = "No Data"
        if champ_count != 0:
            index = random.randrange(0, champ_count, 1)
            result = self.ChampionData.ChampionList[index]
        return result

    def register(self, user:str , summoner:str):
        if( not user in self.userToSummonerList):
            self.userToSummonerList[user] = [summoner]
        elif( not summoner in self.userToSummonerList[user]):
            self.userToSummonerList[user].push(summoner)
        
    def unregister(self, user: str, summoner:str):
        return None


        