import json
from dataclasses import dataclass
from datetime import timedelta

@dataclass
class SummonerStatSummaryResults:
    TotalGames:int = 0
    WinRate:str = ""
    TotalGold:int = ""
    TotalTimeSpent:str = ""
    MinionsKilled:int = 0
    FlashCount:int = 0
    Kills:int = 0
    Deaths:int = 0
    Assists:int =0

    def __format__(self, format_spec: str) -> str:
        return f''':milk: In the past 7 Days:milk:
    Total Games: {self.TotalGames}
    WinRate: {self.WinRate}
    Time Spent: {self.TotalTimeSpent}
    Gold Gained: {self.TotalGold}
    Minions Merked: {self.MinionsKilled}
    Flash Count: {self.FlashCount}
    KDA: {'{0:.2f}'.format(((self.Kills+self.Assists)/self.Deaths)) if self.Deaths != 0 else "Undead" }
    Deaths: {self.Deaths}
:milk:Cheers:milk:'''

class SummonerStatSummary:

    def __init__(self):
        self.FLASH_SUMMONER_ID = 4
        self.GHOST_SUMMONER_ID = 6

    def ListOfMatchesToSummonerStat(self,matchesList:list, puuid:str) -> SummonerStatSummaryResults:
        if len(matchesList) !=0 and puuid:
         #things to track
            totalMinionsKilled:float = 0
            goldEarned:float = 0
            totalWins:float = 0
            totalLoss:float = 0
            totalTimeS:float = 0.0
            flashCount:int = 0
            totalKills:int = 0
            totalDeaths:int = 0
            totalAssists:int = 0
            #get results
            for match in matchesList:
                totalTimeS+=match.durationMS
                player = match.getPlayerPUUIDIfExists(puuid)
                if(player != None):
                    if(bool(player["win"])):
                        totalWins+=1
                    else:
                        totalLoss+=1
                    totalMinionsKilled += int(player["totalMinionsKilled"])
                    goldEarned += int(player["goldEarned"])
                    #get flash count
                    if(int(player["summoner1Id"]) == self.FLASH_SUMMONER_ID):
                        flashCount += int(player["summoner1Casts"]) 
                    elif (int(player["summoner2Id"]) == self.FLASH_SUMMONER_ID):
                        flashCount += int(player["summoner2Casts"]) 
                    #KDA
                    totalKills+=int(player["kills"])
                    totalDeaths+=int(player["deaths"])
                    totalAssists+=int(player["assists"])
            formattedTimeSpent:str = str(timedelta(seconds=int( totalTimeS/1000)))
            totalGames=(totalLoss+totalWins)
            winRate = int((totalWins/totalGames)*100) if totalGames != 0 else 100
            return SummonerStatSummaryResults(TotalGames=totalGames, WinRate = str(winRate)+"%", TotalGold=goldEarned, TotalTimeSpent=formattedTimeSpent, MinionsKilled=totalMinionsKilled, FlashCount=flashCount, Kills=totalKills, Deaths=totalDeaths, Assists=totalAssists)
        return SummonerStatSummaryResults()