import discord
import json

class DnDMonster:
    Name:str = ""                           #index 1
    Size:str = ""                           #2
    Type:str = ""                           #3                   
    Alignment:str = ""                      #4
    #defense
    AC:int = 0                              #5
    HP:int = 0                              #6
    #Movement
    SpeedNormal:str = ""                    #7
    SpeedFlying:str = ""                    #8
    SpeedSwimming:str = ""                  #9
    SpeedBurrowing:str = ""                 #10
    SpeedClimb:str = ""                     #11
    #stats
    Strength:int = 0                        #12
    Dexterity:int = 0                       #13
    Constitution:int = 0                    #14
    Intelligence:int = 0                    #15
    Wisdom:int = 0                          #16
    Charisma:int = 0                        #17
    #details
    SavingThrows:str = ""                   #18
    Skills:str = ""                         #19
    WeaknessResistanceImmunities:str = ""   #20
    Senses:str=""                           #21
    Languages:str=""                        #22
    #Challenge
    ChallengeRating:float=0.0               #23
    Experience:int = 0                      #24
    #Environments
    Unknown:bool = False                    #25
    AllEnvironments:bool = False            #26
    Arctic:bool = False                     #27 #13 in locations csv 
    Costal:bool = False                     #28 #14
    Desert:bool = False                     #29 #15
    Forest:bool = False                     #30 #16
    Grassland:bool = False                  #31 #17
    Hills:bool = False                      #32 #18
    Jungle:bool = False                     #33 #19
    Mountain:bool = False                   #34 #20
    Swamp:bool = False                      #35 #21
    Underdark:bool = False                  #36 #22
    Underwater:bool = False                 #37 #23
    Urban:bool = False                      #38 #24
    #Extra info
    Additional:str = ""                     #39
    Source:str= ""                          #40

    def __init__(self, row:list[str]=[]):
        #set the location and monster names
        self.setMonsterLocation(row)
        pass

    def setMonsterLocation(self, row:dict):
        self.Name:str = str(row['name'])
        #environments
        for env in row['environments']:
            match env.lower():
                case 'arctic':
                    pass
                case 'tundra':
                    pass
                
                case 'coastal':
                    pass
                case 'desert':
                    pass
                case 'forest':
                    pass
                case 'grassland':
                    pass
                case 'hill' | 'hills':
                    pass
                case 'jungle':
                    pass
                case 'mountain'|'mountains':
                    pass
                case 'swamp':
                    pass
                case 'underdark':
                    pass
                case 'water' | 'underwater':
                    pass
                case 'urban':
                    pass
                case 'settlement':
                    pass
                case 'sewer':
                    pass
                case 'ruin'|'ruins':
                    pass
                case 'feywild':
                    pass
                case 'hell':
                    pass
                case 'plane of earth':
                    pass
                case 'plane of fire':
                    pass
                case 'plane of water':
                    pass
                case 'plane of air':
                    pass
                case 'laboratory':
                    pass
                case 'tomb':
                    pass
                case 'shadowfell':
                    pass
                
                case 'abyss':
                    pass
                

                case 'caves':
                    pass
                case 'caverns':
                    pass

                case 'temple':
                    pass
                case 'astral plane':
                    pass
                case 'ethereal plane':
                    pass
                case 'lake':
                    pass
                case 'ocean':
                    pass
                case 'ice':
                    pass
                case 'any':
                    pass
                case 'volcano':
                    pass
                case _:
                    print(f"Missing Environment {env}")
        
        #stats
        '''
        if('/' in row[5]):
            numerator, denominator = row[5].split('/')
            self.ChallengeRating:float = float(numerator)/float(denominator)
        else:
            self.ChallengeRating:float = float(row[5])
        '''
        pass

    def setMonsterInfo(self, row:list[str]):
        '''
        #self.Name:str = row[1]                         
        self.Size:str = row[2]                    
        self.Type:str = row[3]                                         
        self.Alignment:str = row[4]                   
        #defense
        self.AC:int = int(row[5])                           
        self.HP:int = int(row[6])                     
        #Movement
        self.SpeedNormal:str = row[7]                        #7
        self.SpeedFlying:str = row[8]                        #8
        self.SpeedSwimming:str = row[9]                      #9
        self.SpeedBurrowing:str = row[10]                    #10
        self.SpeedClimb:str = row[11]                        #11
        #stats
        self.Strength:int = int(row[12])                     #12
        self.Dexterity:int =  int(row[13])                   #13
        self.Constitution:int =  int(row[14])                #14
        self.Intelligence:int =  int(row[15])                #15
        self.Wisdom:int =  int(row[16])                      #16
        self.Charisma:int =  int(row[17])                    #17
        #details
        self.SavingThrows:str = row[18]                      #18
        self.Skills:str = row[19]                            #19
        self.WeaknessResistanceImmunities:str = row[20]      #20
        self.Senses:str=row[21]                              #21
        self.Languages:str=row[22]                           #22
        #Challenge
        self.ChallengeRating:float= float(row[23])           #23
        self.Experience:int =  int(row[24])                  #24
        #Extra info
        self.Additional:str = row[39]                        #39
        self.Source:str = row[40]                            #40
        '''
        pass

    def __format__(self, format_spec: str) -> str:
        return self.Name

    def getEmbedding(self) ->discord.Embed:
        embed = discord.Embed(title=f"{self.Name} - AC: {self.AC} HP: {self.HP}")
        embed.description = f">  Challenge Rating: {self.ChallengeRating}, Experience: {self.Experience}\n>  Alignment: {self.Alignment}, Type: {self.Type}, Size: {self.Size}"
        movementList:list[str] = []
        if self.SpeedNormal != "": movementList.append(f">  Normal: {self.SpeedNormal}")
        if self.SpeedFlying != "": movementList.append(f">  Flying: {self.SpeedFlying}")
        if self.SpeedSwimming != "": movementList.append(f">  Swimming: {self.SpeedSwimming}")
        if self.SpeedBurrowing != "": movementList.append(f">  Burrow: {self.SpeedBurrowing}")
        if self.SpeedClimb != "": movementList.append(f">  Climbing: {self.SpeedClimb}")
        embed.add_field(name="Movement", 
                        value="\n".join(movementList),
                        inline=False)
        embed.add_field(name="Stats",
                        value=f">  :mechanical_arm:Strength: {self.Strength}\n>  :pinched_fingers:Dexterity: {self.Dexterity}\n>  :sparkling_heart:Constitution: {self.Constitution}\n>  :brain:Intelligence: {self.Intelligence}\n>  :person_in_lotus_position:Wisdom: {self.Wisdom}\n>  :kiss:Charisma: {self.Charisma}",
                        inline=False)
        embed.add_field(name="Details",
                        value=f">  Saving Throws: {self.SavingThrows}\n>  Skills: {self.Skills}\n>  WRI: {self.WeaknessResistanceImmunities}\n>  Senses: {self.Senses}\n>  Languages: {self.Languages}",
                        inline=False)
        environmentList:list[str] = []
        if self.Unknown == True: environmentList.append("Unknown")
        if self.AllEnvironments == True: environmentList.append("All")
        if self.Arctic == True: environmentList.append("Arctic")
        if self.Costal == True: environmentList.append("Coastal")
        if self.Desert == True: environmentList.append("Desert")
        if self.Forest == True: environmentList.append("Forest")
        if self.Grassland == True: environmentList.append("Grassland")
        if self.Hills == True: environmentList.append("Hills")
        if self.Jungle == True: environmentList.append("Jungle")
        if self.Mountain == True: environmentList.append("Mountain")
        if self.Swamp == True: environmentList.append("Swamp")
        if self.Underdark == True: environmentList.append("Underdark")
        if self.Underwater == True: environmentList.append("Underwater")
        if self.Urban == True: environmentList.append("Urban")
        envStr:str = ", ".join(environmentList)
        embed.add_field(name="Environment", value=">  "+envStr, inline=False)

        embed.add_field(name="Extra",value=f">  Actions: {self.Additional}")
        return embed
