from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta
import time

class Summoners: 

    def __init__(self, riotAPIKey ):
        self.RIOT_API_KEY = riotAPIKey

#Changes to the user to riot PUUID list
    def getPUUIDFromRiotID(self, riotid) -> str:
        riotTag = riotid.split('#')
        if(len(riotTag) != 2):
            return ""
        gameName = riotTag[0]
        tagName = riotTag[1]
        api_url:str = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagName}"
        result = ""
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }
        try:
            response = None
            while response == None or response.status_code == 429:
                response = requests.get(api_url, params=urlencode(url_params))
                if(response.status_code == 200):
                    result = response.json()['puuid']
                else:
                    time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return result
    
#Get List of matches played
    async def getMatchesFromSummoner(self, puuid:str) -> list[str]:
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