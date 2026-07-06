from DataAccess.DnD.DnDMonster import DnDMonster
from pathlib import Path
import json

    #read in from https://api.open5e.com/
class DnDMonsterReader:
    #toDo: Move this to ENV file
    MonsterFileLocation:str = "./data/monster.data.txt"
    monsterList:list[DnDMonster] = []

    def __init__(self, monsterList:list[DnDMonster] = []):
        self.monsterList = monsterList
        if Path(self.MonsterFileLocation).exists():
            self.ReadInMonsters()

    def ReadInMonsters(self) -> None:
        with open(self.MonsterFileLocation,'r') as file:
            reader = file.readlines()
            for row in reader:
                jsonRow = json.loads(row)
                self.monsterList.append(DnDMonster(jsonRow))
        pass

