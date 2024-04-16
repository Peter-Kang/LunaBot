import aiohttp
from urllib.parse import urlencode

class matches:

    def __init__(self, riotAPIKey, matchID):
        self.RIOT_API_KEY = riotAPIKey
        self.matchID = matchID
        self.results = None
        self.durationMS = 0
        self.LastPlayerGot = None

    async def getMatchData(self):
        api_url:str = f'https://americas.api.riotgames.com/lol/match/v5/matches/{self.matchID}'
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url,params=urlencode(url_params) ) as rep:
                    data = await rep.json()
                    if( rep.status == 200 ):
                        if("info" in data ):
                            self.results = data['info']
                            #get gameEndTimestamp - gameStartTimestamp
                            self.durationMS = data['info']['gameEndTimestamp'] - data['info']['gameStartTimestamp']
        except Exception as e:
            print(e)

    def getPlayerPUUIDIfExists(self, PUUID:str):
        if(self.results is None or PUUID is None or PUUID == ""):
            return None
        for player in self.results['participants'] :
            if player['puuid'] == PUUID:
                self.LastPlayerGot = player
                return player
        return None
    