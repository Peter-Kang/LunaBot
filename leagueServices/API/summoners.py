from dataclasses import dataclass
import time
from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta
from .Matches import Matches
import asyncio

@dataclass
class SummonerStat:
    TotalGames:int
    WinRate:str
    TotalGold:int 
    TotalTimeSpent:str
    MinionsKilled:int
    FlashCount:int
    Kills:int
    Deaths:int
    Assists:int

class Summoners: 

    def __init__(self, riotAPIKey ):
        self.RIOT_API_KEY = riotAPIKey
        self.FLASH_SUMMONER_ID = 4
        self.GHOST_SUMMONER_ID = 6

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
    
#Get List of matches played
    async def getStatus(self, puuid:str):
        daysToSubtract = 7
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
                matchesList.append(Matches(self.RIOT_API_KEY,match))
            keepCalling:bool = True
            while ( keepCalling ):
                await asyncio.gather( *[matchItem.getMatchData() for matchItem in matchesList if (matchItem.Status == None or matchItem.Status == 429)])
                keepCalling = False
                for matchItem in matchesList:
                    if(matchItem.Status == None or matchItem.Status == 429):
                        keepCalling = True
                        time.sleep(1)
            #things to track
            totalMinionsKilled:float = 0
            goldEarned:float = 0
            totalWins:float = 0
            totalLoss:float = 0
            totalTimeS:float = 0.0
            flashCount:int = 0
            totalKills:int = 0
            totalDeaths:int = 0
            totalAssists:int = 0
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
                    if(int(player["summoner1Id"]) == self.FLASH_SUMMONER_ID):
                        flashCount += int(player["summoner1Casts"]) 
                    elif (int(player["summoner2Id"]) == self.FLASH_SUMMONER_ID):
                        flashCount += int(player["summoner2Casts"]) 
                    #KDA
                    totalKills+=int(player["kills"])
                    totalDeaths+=int(player["deaths"])
                    totalAssists+=int(player["assists"])
            formatted:str = str(timedelta(seconds=int( totalTimeS/1000)))
            totalGames=(totalLoss+totalWins)
            winRate = int((totalWins/totalGames)*100) if totalGames != 0 else 100
            return SummonerStat(TotalGames=(totalGames),WinRate = str(winRate)+"%", TotalGold=goldEarned, TotalTimeSpent=formatted, MinionsKilled=totalMinionsKilled, FlashCount=flashCount, Kills=totalKills, Deaths=totalDeaths, Assists=totalAssists)
        return None