from packaging.version import Version
import requests
import asyncio
import aiohttp
from urllib.parse import urlencode

class Champions:

    def __init__(self, riotAPIKey):
        self.ChampionList:list[tuple[str,dict[str:str]]] = []
        self.RIOT_API_KEY:str = riotAPIKey
        self.version:Version = None
        self.Update()
        
#macro Call
    def Update(self) -> list[tuple[str,dict[str:str]]] :
        result:Version = self.getLatestVersion()
        if self.version is not None or result > self.version:
            self.version = result
            return asyncio.run(self._repopulateChampionList())
        return None

#network calls
    def getLatestVersion(self)-> Version:
        api_url:str = "https://ddragon.leagueoflegends.com/api/versions.json"
        try:
            rep = requests.get(api_url)
            data = rep.json()
            if( rep.status_code == 200 and len(data) != 0):
                return Version(data[0])
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return self.version

    async def _repopulateChampionList(self):
        #make the request and get the response
        api_url:str = f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json"
        try:
            rep = requests.get(api_url)
            if( rep.status_code == 200 ):
                #Data filtering
                data = rep.json()
                versionChanged:bool = self.version == None or self.version < Version(data['version'])
                championListEmpty:bool = len(self.ChampionList) ==0
                if(championListEmpty or versionChanged):
                    self.version = Version(data['version'])
                    self.ChampionList = []
                    for i in data["data"]:
                        self.ChampionList.append((i,data["data"][i]))
                    await self._updateAllChampionDetails()
                    return self.ChampionList
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return None
    
    async def _updateAllChampionDetails(self):
        try:
            #Data filtering
            self.ChampionList = await asyncio.gather( *[self._requestChampionDetails(championID[0]) for championID in self.ChampionList])
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return None
    
    async def _requestChampionDetails(self, id:str):
        api_url:str = f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion/{id}.json"
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url,params=urlencode(url_params) ) as rep:
                    response = await rep.json()
                    self.Status = rep.status
                    if( rep.status == 200 ):
                        return (id,response['data'][id])
        except Exception as e:
            print(e)