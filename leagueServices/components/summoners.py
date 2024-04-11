from urllib.parse import urlencode
import requests
import time    
from datetime import datetime, timedelta

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
    def getStatus(self, userID):
        daysToSubtract = 7
        puuid = self.userToSummonerPUUID[userID]
        stop_epoch_time = datetime.now().strftime('%s')
        start_epoch_time = (datetime.now() - timedelta(days=daysToSubtract)).strftime('%s')
        api_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        url_params:dict = {
            
            "startTime":start_epoch_time,
            "endTime":stop_epoch_time,
            "type":"ranked",
            "stop":"0",
            "count":"100",
            "api_key":self.RIOT_API_KEY,
            }
        response = requests.get(api_url, params=urlencode(url_params))
        if(response.status_code == 200):
            totalTime:time = 0;
            for match in response.json():
                #get gameEndTimestamp - gameStartTimestamp
                print(match)