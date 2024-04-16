from dataclasses import dataclass
from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta
from .matches import matches
import asyncio

@dataclass
class SummonerStat:
    TotalGames:int
    WinRate:float
    TotalGold:int 
    TotalTimeSpent:str
    MinionsKilled:int
    FlashCount:int

class Summoners: 

    def __init__(self, riotAPIKey ):
        self.RIOT_API_KEY = riotAPIKey
        self.userToSummonerPUUID = {}

#Changes to the user to summoner PUUID list
    def getSummonerPUUID(self, summoner):
        api_url:str = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner.lower().strip()}"
        result = ""
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }
        try:
            response = requests.get(api_url, params=urlencode(url_params))
            if(response.status_code == 200):
                result = response.json()['puuid']
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return result

    def register(self, userID, summoner ):
        PUUID:str = self.getSummonerPUUID(summoner)
        if(PUUID != ""):
            self.userToSummonerPUUID[userID] = PUUID
            return True
        return False
    
#Get
    async def getStatus(self, userID):
        daysToSubtract = 7
        puuid = self.userToSummonerPUUID[userID]
        stop_epoch_time = int(datetime.now().timestamp())
        start_epoch_time = int((datetime.now() - timedelta(days=daysToSubtract)).timestamp())
        api_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        url_params:dict = {
            "startTime":start_epoch_time,
            "endTime":stop_epoch_time,
            #"type":"ranked",
            "stop":"0",
            "count":"100",
            "api_key":self.RIOT_API_KEY,
            }
        response = requests.get(api_url, params=urlencode(url_params))
        if(response.status_code == 200):
            matchesList = []
            for match in response.json():
                matchesList.append(matches(self.RIOT_API_KEY,match))
            await asyncio.gather( *[matchItem.getMatchData() for matchItem in matchesList])
            #things to track
            totalMinionsKilled:float = 0
            goldEarned:float = 0
            totalWins:float = 0
            totalLoss:float = 0
            totalTimeS:float = 0.0
            flashCount:int = 0
            #get results
            for match in matchesList:
                totalTimeS+=match.durationMS
                player = match.getPlayerPUUIDIfExists(puuid)
                if(player != None):
                    if(bool(player["win"])):
                        totalWins+=1
                    else:
                        totalLoss+=1
                    totalMinionsKilled += int(player["totalMinionsKilled"])
                    goldEarned += int(player["goldEarned"])
                    #get flash count
                    if(int(player["summoner1Id"]) == 4):
                        flashCount += int(player["summoner1Casts"]) 
                    elif (int(player["summoner2Id"]) == 4):
                        flashCount += int(player["summone2Casts"]) 
            formatted:str = str(timedelta(seconds=int( totalTimeS/1000)))
            return SummonerStat(TotalGames=(totalLoss+totalWins),WinRate = (totalWins/(totalWins+totalLoss)), TotalGold=goldEarned, TotalTimeSpent=formatted, MinionsKilled=totalMinionsKilled, FlashCount=flashCount)
        return None