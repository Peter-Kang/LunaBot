
class league:

    def __init__(self):
        self.OPGG = OPGG()
        self.userToSummonerList = {}

    def randomChampion(self):
        print("Random")
        


    def register(self, user:str , summoner:str):
        if( not user in self.userToSummonerList):
            self.userToSummonerList[user] = [summoner]
        elif( not summoner in self.userToSummonerList[user]):
            self.userToSummonerList[user].push(summoner)
        
    def unregister(self, user: str, summoner:str):
        return None


        