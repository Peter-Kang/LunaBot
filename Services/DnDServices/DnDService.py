import random
from Services.DnDServices.Monsters.DnDMonsters import DnDMonsters 

class DnD:

    def __init__(self):
        self.DnDMonster:DnDMonsters = DnDMonsters()

    def roll(self, input:str)->str:
        diceInfo:list[int] = input.lower().replace(" ","").split('d') #ie 2d8
        inputParsed:str = input.lower().replace(" ","")
        result:str = "Please enter valid dice format. ie: 2d8 is 2 eight sided dice."
        if(len(diceInfo) == 2 and diceInfo[0].isnumeric() and diceInfo[1].isnumeric() and int(diceInfo[0]) > 0 and int(diceInfo[1]) >0 ):
            count:int = int(diceInfo[0])
            diceSide:int = int(diceInfo[1])
            rollResults:list[int] = []
            total:int = 0
            for _ in range(0,count):
                roll:int = random.randrange(1, diceSide, 1)
                rollResults.append(roll)
                total += roll
            rollResultsString = ' , '.join([str(i) for i in rollResults])
            
            result=f"You Rolled {inputParsed}\n[{rollResultsString}]\nTotal:{total}"
        return result
