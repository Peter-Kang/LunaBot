from DataAccess.DnD.DnDMonster import DnDMonster
import json

    #read in from https://api.open5e.com/
class DnDMonsterReader:
    MonsterFileLocation:str = "./data/monster.data.txt"
    monsterList:list[DnDMonster] = []

    def __init__(self):
        self.ReadInMonsters()
        pass

    def ReadInMonsters(self) -> None:
        with open(self.MonsterFileLocation,'r') as file:
            reader = file.readlines()
            for row in reader:
                jsonRow = json.loads(row)
                self.monsterList.append(DnDMonster(jsonRow))
        pass

