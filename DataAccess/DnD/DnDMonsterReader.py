import csv
from DataAccess.DnD.DnDMonster import DnDMonster

    
class DnDMonsterReader:
    MonsterStats:str = "./data/DnDMonsters.csv"
    MonsterLocationCSV:str = "./data/DnDMonsterLocation.csv"
    monsterList:list[DnDMonster] = []

    def __init__(self):
        self.ReadInCSV()
        pass

    def ReadInCSV(self) -> None:
        monsterNameMapping:dict[str,DnDMonster] = {}
        with open(self.MonsterLocationCSV,'r') as file:
            reader = csv.reader(file)
            for _ in range(3): next(reader) # clear the header
            for row in reader:
                monster:DnDMonster = DnDMonster(row)
                monsterNameMapping[monster.Name.lower().strip()] = monster
                
        with open(self.MonsterStats,'r') as file:
            reader = csv.reader(file)
            for _ in range(2): next(reader) #header
            for row in reader:
                #get monster
                if str(row[1].lower().strip()) in monsterNameMapping:
                    monsterNameMapping[row[1].lower().strip()].setMonsterInfo(row)
        self.monsterList:list[DnDMonster] = list(monsterNameMapping.values())
        pass

