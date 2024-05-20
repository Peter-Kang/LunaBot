from DataAccess.DnD.DnDMonster import DnDMonster
import json

    
class DnDMonsterReader:
    MonsterFileLocation:str = "./data/monster.data.txt"
    monsterList:list[DnDMonster] = []

    def __init__(self):
        self.ReadInCSV()
        pass

    def ReadInCSV(self) -> None:
        with open(self.MonsterFileLocation,'r') as file:
            reader = file.readlines()
            for row in reader:
                jsonRow = json.loads(row)
                self.monsterList.append(DnDMonster(jsonRow))
        pass

