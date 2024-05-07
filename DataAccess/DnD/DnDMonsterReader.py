import csv
from DataAccess.DnD.DnDMonster import DnDMonster

    
class DnDMonsterReader:
    Location:str = "./data/DnDMonsters.csv"
    monsterList:list[DnDMonster] = []

    def __init__(self):
        self.ReadInCSV()
        pass

    def ReadInCSV(self):
        with open(self.Location,'r') as file:
            reader = csv.reader(file)
            for _ in range(2): next(reader) # clear the header
            for row in reader:
                self.monsterList.append(DnDMonster(row))


