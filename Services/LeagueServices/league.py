from .API.Champions import Champions as ChampionsAPI 
from .API.Summoners import Summoners as SummonersAPI
from .API.Matches import Matches as MatchesAPI, Match

from DataAccess.LeagueDatabase import LeagueDatabase
from .DataUtil.SummonerStatSummary import SummonerStatSummary, SummonerStatSummaryResults
from .DataUtil.ChampionStats import ChampionStats, ChampionDisplay
import json

class league:
    #database
    db:LeagueDatabase

    #apis
    ChampionAPI:ChampionsAPI
    UserSummonerAPI:SummonersAPI
    SummonerMatchAPI:MatchesAPI

    #business logic
    ChampionData:ChampionStats
    SummonerStat:SummonerStatSummary

    #cache
    userToSummonerPUUID:dict[str:str] #discordUser:string to summonerPUUID:string
    matchCache:dict[str:Match]  #matchName:string to json
  
    def __init__(self, riotAPIKey:str,db:LeagueDatabase):
        self.RIOT_API_KEY:str = riotAPIKey
    #Database
        self.db:LeagueDatabase = db
    #Champion Data
        #API call objects
        self.ChampionAPI:ChampionsAPI = ChampionsAPI(riotAPIKey)
        #Features/DataModels
        self.ChampionData:ChampionStats = ChampionStats(self.ChampionAPI.version, self.ChampionAPI.ChampionList)
    #Summoner Data
        #API call objects
        self.UserSummonerAPI:SummonersAPI = SummonersAPI(riotAPIKey)
        self.SummonerMatchAPI:MatchesAPI = MatchesAPI(riotAPIKey)
        #Features/DataModels
        self.SummonerStat:SummonerStatSummary = SummonerStatSummary()
    #Cache and mappings
        self.userToSummonerPUUID:dict[str:str] = {} #discordUser:string to summonerPUUID:string
        self.matchCache:dict[str:Match] = {}#matchName:string to json
    #inits
        self.__initUserToSummonerPUUID()
        self.__initMatchCache()
#inits
    def __initUserToSummonerPUUID(self) -> None:
        userIDIndex:int = 0
        summonerPUUIDIndex:int = 1
        result:list[tuple[str]] = self.db.SummonerDB.getAllUsers()
        #populate
        for row in result:
            self.userToSummonerPUUID[row[userIDIndex]] = row[summonerPUUIDIndex]

    def __initMatchCache(self) -> None:
        matchIDIndex:int = 0
        jsonIndex:int = 2
        result:list[tuple[str]] = self.db.MatchesDB.getMatches()
        for row in result:
            self.matchCache[row[matchIDIndex]] = Match(self.RIOT_API_KEY,row[matchIDIndex],json.loads(row[jsonIndex]))
        
#update Champion Lists, cron call
    def UpdateChampionList(self):
        result = self.ChampionAPI.Update()
        if result is not None:
            self.ChampionData = ChampionStats(self.ChampionAPI.version.result)
            print(f"Champion Data updated to {self.ChampionAPI.version}")
       
#champion Data
    def randomChampion(self):
        return self.ChampionData.randomChampion()

    def register(self, user:str , riotid:str) -> str:
        puuid:str = self.UserSummonerAPI.getPUUIDFromRiotID( riotid )
        if(puuid != ""):
            self.userToSummonerPUUID[str(user)] = puuid
            self.db.SummonerDB.addOrUpdateUserToSummonerMapping(user, riotid, puuid)
        return puuid

#summoner stats
    def updateMissingMatchesData(self, matchList:list[Match]) -> None:
        for match in matchList:
            self.matchCache[match.matchID] = match
            self.db.MatchesDB.addMatches(match.matchID,match.EndEpoch,json.dumps(match.results))

    def getListOfMatches(self, matchListString:list[str]) -> list[Match]:
        result:list[Match] = []
        for matchID in matchListString:
            result.append(self.matchCache[matchID])
        return result
    
    async def populateMissingMatches(self, matchListString:list[str])-> None:
        matchListStringMissing:list[str] = []
        #filter out the list of ids we already have
        for matchStr in matchListString :
            if not matchStr in self.matchCache:
                matchListStringMissing.append(matchStr)
        # get the matches missing
        matchMissingListMatch:list[Match] = await self.SummonerMatchAPI.getMatchesFromList(matchListStringMissing) # turn list of match ids to list of completed matches
         # save the matches to db and add to match cache
        self.updateMissingMatchesData(matchMissingListMatch)

    async def getUserStatus(self, userID:str) -> str:
        if( not (userID in self.userToSummonerPUUID)):
            return "Not Registered"
        puuid:str = self.userToSummonerPUUID[userID]
        matchStringList:list[str] = await self.UserSummonerAPI.getMatchesFromSummoner(puuid) # list of match ids
        await self.populateMissingMatches(matchStringList)
        matchList = self.getListOfMatches(matchStringList)
        #report stats
        res:SummonerStatSummaryResults = self.SummonerStat.ListOfMatchesToSummonerStat(matchList,puuid)
        return format(res)