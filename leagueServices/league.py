from urllib.parse import urlencode
import requests

class league:

    def __init__(self, RiotAPIKey):
        self.RIOT_API_KEY = RiotAPIKey;
        self.ChampionList = []
        self.UserToSummoner = {}
        self.repopulateChampionList()

#Champion related
    def repopulateChampionList(self):
        self.ChampionList = []
        #make the request and get the reponse
        api_url = f"https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion.json"
        try:
            rep = requests.get(api_url)
            if( rep.status_code is 200 ):
                data = rep.json()
                print(data)
        except requests.exceptions.RequestException as e:
            print(e.strerror)
        
    def randomChampion(self):
        print("Random")

    def register(self, user:str , summoner:str):
        if( not user in self.userToSummonerList):
            self.userToSummonerList[user] = [summoner]
        elif( not summoner in self.userToSummonerList[user]):
            self.userToSummonerList[user].push(summoner)
        
    def unregister(self, user: str, summoner:str):
        return None


        