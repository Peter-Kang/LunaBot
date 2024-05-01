from enum import Enum
from DataAccess.CSV.DnDMonsterReader import DnDMonsterReader
from DataAccess.CSV.DnDMonster import DnDMonster
import random

#enums for the environment array
class DnDEnvironments(Enum):
    Unknown     = 0
    All         = 1
    Arctic       = 2
    Coastal = 3
    Desert = 4
    Forest = 5
    Grassland = 6
    Hills = 7
    Jungle = 8
    Mountain = 9
    Swamp = 10
    Underdark = 11
    Underwater = 12
    Urban = 13

class DnDMonsters:
    #monster location Enum

    #monsters by environment
    Unknown:list[DnDMonster] = []
    All:list[DnDMonster] = []
    Arctic:list[DnDMonster] = []
    Coastal:list[DnDMonster] = []
    Desert:list[DnDMonster] = []
    Forest:list[DnDMonster] = []
    Grassland:list[DnDMonster] = []
    Hills:list[DnDMonster] = []
    Jungle:list[DnDMonster] = []
    Mountain:list[DnDMonster] = []
    Swamp:list[DnDMonster] = []
    Underdark:list[DnDMonster] = []
    Underwater:list[DnDMonster] = []
    Urban:list[DnDMonster] = []

    Environments:list[list[DnDMonster]] = [Unknown, All, Arctic, Coastal, Desert, Forest, Grassland, Hills, Jungle, Mountain, Swamp, Underdark, Underwater,Urban]

    def __init__(self):
        self.CSVReader:DnDMonsterReader = DnDMonsterReader()
        self.__populateEnvironment()

    def __populateEnvironment(self):
        for monster in self.CSVReader.monsterList:
            if monster.Unknown: self.Unknown.append(monster)
            if monster.AllEnvironments: self.All.append(monster)
            if monster.Arctic: self.Arctic.append(monster)
            if monster.Costal: self.Coastal.append(monster)
            if monster.Desert: self.Desert.append(monster)
            if monster.Forest: self.Forest.append(monster)
            if monster.Grassland: self.Grassland.append(monster)
            if monster.Hills: self.Hills.append(monster)
            if monster.Jungle: self.Jungle.append(monster)
            if monster.Mountain: self.Mountain.append(monster)
            if monster.Swamp: self.Swamp.append(monster)
            if monster.Underdark: self.Underdark.append(monster)
            if monster.Underwater: self.Underwater.append(monster)
            if monster.Urban: self.Urban.append(monster)
        
    def Encounter(self, ChallengeRating:float = -1.0, Environment:DnDEnvironments = DnDEnvironments.All):
        result:DnDMonster = None
        environmentToUse = self.Environments[Environment.value]
        if( ChallengeRating >= 0 ): #look for cr CR
            environmentToUse = [x for x in environmentToUse if x.ChallengeRating == ChallengeRating]
        result = environmentToUse[random.randrange(0, len(environmentToUse), 1)]
        return result


        