import time
from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta
from .Matches import Matches
import asyncio



class Summoners: 

    def __init__(self, riotAPIKey ):
        self.RIOT_API_KEY = riotAPIKey

#Changes to the user to summoner PUUID list
    def getSummonerPUUID(self, summoner) -> str:
        api_url:str = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner.lower().strip()}"
        result = ""
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }
        try:
            response = None
            while response == None or response.status_code == 429:
                response = requests.get(api_url, params=urlencode(url_params))
                time.wait(1)
            if(response.status_code == 200):
                result = response.json()['puuid']
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return result
    
#Get List of matches played
    async def getMatchesFromSummoner(self, puuid:str) -> list:
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
            matchesList:list = []
            for match in response.json():
                matchesList.append(match)
            return matchesList
        return []
    
    async def getMatchesFromList(self, stringListOfMatches:list):
        matchesList:list = []
        if len(stringListOfMatches) != 0:
            for match in stringListOfMatches:
                matchesList.append(Matches(self.RIOT_API_KEY,match))
            keepCalling:bool = True
            while ( keepCalling ):
                await asyncio.gather( *[matchItem.getMatchData() for matchItem in matchesList if (matchItem.Status == None or matchItem.Status == 429)])
                keepCalling = False
                for matchItem in matchesList:
                    if(matchItem.Status == None or matchItem.Status == 429):
                        keepCalling = True
                        time.sleep(1) #wait until rate limit is freed
        return matchesList