from packaging.version import Version
import requests


class Champions:

    def __init__(self, riotAPIKey):
        self.ChampionList:list[tuple[str,dict[str:str]]] = []
        self.RIOT_API_KEY:str = riotAPIKey
        self.version:Version = None
        self.Update()
        
#macro Call
    def Update(self) -> list[tuple[str,dict[str:str]]] :
        self.getLatestVersion()
        return self.repopulateChampionList()

#network calls
    def getLatestVersion(self):
        api_url:str = "https://ddragon.leagueoflegends.com/api/versions.json"
        try:
            rep = requests.get(api_url)
            data = rep.json()
            if( rep.status_code == 200 and len(data) != 0):
                self.version = Version(data[0])
        except requests.exceptions.RequestException as e:
            print(e.strerror)

    def repopulateChampionList(self):
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
                    return self.ChampionList
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        return None