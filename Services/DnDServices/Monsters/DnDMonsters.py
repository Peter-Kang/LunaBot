from enum import Enum
from DataAccess.DnD.DnDMonsterReader import DnDMonsterReader
from DataAccess.DnD.DnDMonster import DnDMonster
import random

#enums for the environment array
#discord options limit count is 25 cut 5?
class DnDEnvironments(Enum):
    All         = 0
    Arctic      = 1
    Coastal     = 2
    Desert      = 3
    Forest      = 4
    Grassland   = 5
    Hills       = 6
    Jungle      = 7
    Mountain    = 8
    Swamp       = 9
    Underdark   = 10
    Underwater  = 11
    Urban       = 12
    Sewer       = 13
    Ruin        = 14
    Feywild     = 15
    Hell        = 16
    EarthPlane  = 17
    FirePlane   = 18
    WaterPlane  = 19
    AirPlane    = 20
    AstralPlane = 21
    EtherealPlane = 22
    Laboratory  = 23
    ShadowFell  = 24
    Abyss       = 25
    Caves       = 26
    Temple      = 27
    Volcano     = 28
    Flexible    = 29

class DnDMonsters:
    #monster location Enum

    #monsters by environment
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
    Sewer:list[DnDMonster] = []
    Ruin:list[DnDMonster] = []
    Feywild:list[DnDMonster] = []
    Hell:list[DnDMonster] = []
    EarthPlane:list[DnDMonster] = []
    FirePlane:list[DnDMonster] = []
    WaterPlane:list[DnDMonster] = []
    AirPlane:list[DnDMonster] = []
    AstralPlane:list[DnDMonster] = []
    EtherealPlane:list[DnDMonster] = []
    Laboratory:list[DnDMonster] = []
    ShadowFell:list[DnDMonster] = []
    Abyss:list[DnDMonster] = []
    Caves:list[DnDMonster] = []
    Temple:list[DnDMonster] = []
    Volcano:list[DnDMonster] = []
    Flexible:list[DnDMonster] = []

    Environments:list[list[DnDMonster]] = [ All, Arctic, Coastal, Desert, Forest, Grassland, Hills, Jungle, Mountain, Swamp, Underdark, Underwater,Urban,Sewer, Ruin, Feywild, Hell, EarthPlane, FirePlane, WaterPlane, AirPlane, AstralPlane, EtherealPlane, Laboratory, ShadowFell, Abyss, Caves, Temple, Volcano, Flexible]

    def __init__(self):
        self.Reader:DnDMonsterReader = DnDMonsterReader()
        self.__populateEnvironment()

    def __populateEnvironment(self):
        for monster in self.Reader.monsterList:
            self.All.append(monster)
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
            if monster.Sewer is True : self.Sewer.append(monster)
            if monster.Ruin is True : self.Ruin.append(monster)
            if monster.Feywild is True : self.Feywild.append(monster)
            if monster.Hell is True : self.Hell.append(monster)
            if monster.EarthPlane is True : self.EarthPlane.append(monster)
            if monster.FirePlane is True : self.FirePlane.append(monster)
            if monster.WaterPlane is True : self.WaterPlane.append(monster)
            if monster.AirPlane is True : self.AirPlane.append(monster)
            if monster.AstralPlane is True : self.AstralPlane.append(monster)
            if monster.EtherealPlane is True : self.EtherealPlane.append(monster)
            if monster.Laboratory is True : self.Laboratory.append(monster)
            if monster.ShadowFell is True : self.ShadowFell.append(monster)
            if monster.Abyss is True : self.Abyss.append(monster)
            if monster.Caves is True : self.Caves.append(monster)
            if monster.Temple is True : self.Temple.append(monster)
            if monster.Volcano is True : self.Volcano.append(monster)
            if monster.Flexible is True : self.Flexible.append(monster)
        print("DnD Monsters Populated")
        
    def Encounter(self, ChallengeRating:float = -1.0, Environment:DnDEnvironments = DnDEnvironments.All):
        result:DnDMonster = None
        environmentToUse = self.Environments[Environment.value]
        if( ChallengeRating >= 0 ): #look for cr CR
            environmentToUse = [x for x in environmentToUse if x.ChallengeRating == ChallengeRating]
        result = environmentToUse[random.randrange(0, len(environmentToUse), 1)]
        return result


        