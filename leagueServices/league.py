from .API.Champions import Champions as ChampionsAPI 
from .API.Summoners import Summoners as SummonersAPI
import random
from DataAccess.LeagueDatabase import LeagueDatabase
from .DataUtil.SummonerStatSummary import SummonerStatSummary, SummonerStatSummaryResults

class league:

    def __init__(self, riotAPIKey:str,db:LeagueDatabase):
        self.RIOT_API_KEY:str = riotAPIKey
        #API calls
        self.ChampionData:ChampionsAPI = ChampionsAPI(riotAPIKey)
        self.UserSummonerAPI:SummonersAPI = SummonersAPI(riotAPIKey)

        #Features/DataModels
        self.SummonerStat = SummonerStatSummary()

        #Database
        self.db:LeagueDatabase = db
        self.userToSummonerPUUID:dict = {}
        self.__initUserToSummonerPUUID()

    def __initUserToSummonerPUUID(self):
        result:list = self.db.SummonerDB.getAllUsers()
        for row in result:
            self.userToSummonerPUUID[row[0]] = row[1]
        
    def randomChampion(self) -> str:
        champ_count:int = len(self.ChampionData.ChampionList)-1
        result:str = "No Data"
        if champ_count >= 0:
            index:int = random.randrange(0, champ_count, 1)
            result:str = self.ChampionData.ChampionList[index][0]
        return result

    def register(self, user:str , summoner:str) -> str:
        puuid:str = self.UserSummonerAPI.getSummonerPUUID( summoner )
        if(puuid != ""):
            self.userToSummonerPUUID[str(user)] = puuid
            self.db.SummonerDB.addOrUpdateUserToSummonerMapping(user, summoner, puuid)
        return puuid

    async def getUserStatus(self, userID:str) -> str:
        if( not (userID in self.userToSummonerPUUID)):
            return "Not Registered"
        puuid:str = self.userToSummonerPUUID[userID]
        matchList:list = await self.UserSummonerAPI.getMatchesFromSummoner(puuid)
        res:SummonerStatSummaryResults = self.SummonerStat.ListOfMatchesToSummonerStat(matchList,puuid)
        return format(res)