import random
from Services.DnDServices.Monsters.DnDMonsters import DnDMonsters, DnDEnvironments
from DataAccess.DnD.DnDMonster import DnDMonster
import discord

class DnD:

    def __init__(self):
        self.DnDMonsters:DnDMonsters = DnDMonsters()

    def roll(self, input:str)->str:
        diceInfo:list[str] = input.lower().replace(" ","").split('d') #ie 2d8
        inputParsed:str = input.lower().replace(" ","")
        result:str = "Please enter valid dice format. ie: 2d8 is 2 eight sided dice."
        if(len(diceInfo) == 2 and diceInfo[0].isnumeric() and int(diceInfo[0]) > 0):
            count:int = int(diceInfo[0])
            diceSide:int = 0
            flatAdd:int = 0
            secondHalf:list[str] = diceInfo[1].split('+')
            if((len(secondHalf) == 1 and secondHalf[0].isnumeric() and int(secondHalf[0])>0) or (len(secondHalf) == 2 and secondHalf[0].isnumeric() and secondHalf[1].isnumeric() and int(secondHalf[0]) >0 )):
                diceSide = int(secondHalf[0])+1
                if(len(secondHalf) == 2):
                    flatAdd = int(secondHalf[1])
                rollResults:list[int] = []
                total:int = 0
                for _ in range(0,count):
                    roll:int = random.randrange(1, diceSide, 1) + flatAdd
                    rollResults.append(roll)
                    total += roll 
                rollResultsString = ' , '.join([str(i) for i in rollResults])
                if len(rollResultsString) < 1900:
                    rollResultsString = f"\n[{rollResultsString}]"
                else:
                    rollResultsString = ""
                result=f"You Rolled {inputParsed}{rollResultsString}\nTotal:{total}"
        return result

    def Encounter(self, ChallengeRating:float =-1.0, Environment:DnDEnvironments=DnDEnvironments.All) -> discord.Embed:
        result:DnDMonster = self.DnDMonsters.Encounter(ChallengeRating,Environment)
        if(result == None):
            return discord.Embed(title="No result")
        return result.getEmbedding()