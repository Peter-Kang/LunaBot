import aiohttp
from urllib.parse import urlencode

class matches:

    def __init__(self, riotAPIKey, matchID):
        self.RIOT_API_KEY = riotAPIKey
        self.matchID = matchID
        self.results = None
        self.durationMS = 0

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
                            end = data['info']['gameEndTimestamp'] 
                            start = data['info']['gameStartTimestamp']
                            self.durationMS = end-start
        except Exception as e:
            print(e)