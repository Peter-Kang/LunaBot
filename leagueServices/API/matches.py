from dataclasses import dataclass
from urllib.parse import urlencode
import asyncio
import aiohttp
import time
import json

class Match:
    RIOT_API_KEY:str = ""
    matchID:str = ""
    results:json = None
    durationMS:int = 0
    LastPlayerGot:json = None
    Status:int = None
    Participants:list[str] = []
    EndEpoch:int = 0

    def __init__(self, riotAPIKey:str, matchID:str ,data:json=None):
        self.RIOT_API_KEY:str = riotAPIKey
        self.matchID:str = matchID
        if(data != None):
            self.__setResult(data)

#setResult stack
    def __setDuration(self) -> None:
        if self.results != None:
            self.durationMS = self.results['gameEndTimestamp'] - self.results['gameStartTimestamp']
            self.EndEpoch = int(self.results['gameEndTimestamp'])

    def __setParticipants(self) -> None:
        if self.results != None:
            for player in self.results['participants']:
                self.Participants.append(player['puuid'])
    
    def setResult(self, result:json) -> None:
        self.results = result
        self.__setDuration()
        self.__setParticipants()
        if self.Status == 0:
            self.Status = 200
    
    async def getMatchData(self) -> None:
        api_url:str = f'https://americas.api.riotgames.com/lol/match/v5/matches/{self.matchID}'
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url,params=urlencode(url_params) ) as rep:
                    data = await rep.json()
                    self.Status = rep.status
                    if( rep.status == 200 ):
                        if("info" in data ):
                            self.setResult( (data['info']) )
                            
        except Exception as e:
            print(e)

    def getPlayerPUUIDIfExists(self, PUUID:str) -> json:
        if(self.results is None or PUUID is None or PUUID == ""):
            print(f"Match:{self.matchID} not loaded or PUUID not present")
            return None
        for player in self.results['participants'] :
            if player['puuid'] == PUUID:
                self.LastPlayerGot = player
                return player
        print(f"Could not find player: {PUUID} in match: {self.matchID}")
        return None
    
class Matches:

    def __init__(self, riotAPIKey):
          self.RIOT_API_KEY:str = riotAPIKey

    async def getMatchesFromList(self, stringListOfMatches:list) -> list[Match]:
        matchesList:list[Match] = []
        if len(stringListOfMatches) != 0:
            for match in stringListOfMatches:
                matchesList.append(Match(self.RIOT_API_KEY,match))
            keepCalling:bool = True
            while ( keepCalling ):
                await asyncio.gather( *[matchItem.getMatchData() for matchItem in matchesList if (matchItem.Status == None or matchItem.Status == 429)])
                keepCalling = False
                for matchItem in matchesList:
                    if(matchItem.Status == None or matchItem.Status == 429):
                        keepCalling = True
                        time.sleep(1) #wait until rate limit is freed
        return matchesList