import requests

class matches:

    def __init__(self, riotAPIKey, matchID):
        self.RIOT_API_KEY = riotAPIKey
        self.matchID = matchID

    def getMatchData(self):
        api_url:str = 'https://americas.api.riotgames.com/lol/match/v5/matches/'
        url_params:dict = {
            "api_key":self.RIOT_API_KEY
            }