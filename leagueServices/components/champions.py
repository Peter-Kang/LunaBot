from packaging.version import Version
from urllib.parse import urlencode
import requests

class Champions:

    def __init__(self, riotAPIKey):
        self.ChampionList = []
        self.RIOT_API_KEY = riotAPIKey
        self.version = None
        self.repopulateChampionList()

#network calls
    def repopulateChampionList(self):
        #make the request and get the response
        api_url = f"https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion.json"
        try:
            rep = requests.get(api_url)
            if( rep.status_code == 200 ):
                #Data filtering
                data = rep.json()
                if(self.version == None or self.version < Version(data['version'])):
                    self.version = Version(data['version'])
                    self.ChampionList = []
                    for i in data["data"]:
                        self.ChampionList.append(i)
        except requests.exceptions.RequestException as e:
            print(e.strerror)