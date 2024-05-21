import discord
import json

class DnDMonster:
    Name:str = ""                           
    Size:str = ""                           
    Type:str = ""                                         
    Alignment:str = ""
    HitDice:str = ""                      
    #defense
    AC:int = 0
    ArmorDescription:str = ""                              
    HP:int = 0                             
    #Movement
    SpeedNormal:str = ""                    
    SpeedFlying:str = ""                   
    SpeedSwimming:str = ""                  
    SpeedBurrowing:str = ""                 
    SpeedClimb:str = ""
    SpeedHover:str = ""
    SpeedLightWalk:str = ""
    SpeedNotes:str = ""                     
    #stats
    Strength:int = 0                        
    Dexterity:int = 0                       
    Constitution:int = 0                    
    Intelligence:int = 0                    
    Wisdom:int = 0                          
    Charisma:int = 0                        
    #details
    SavingThrows:str = ""                   
    Skills:str = ""                         
    WeaknessResistanceImmunities:str = ""   
    Senses:str=""                           
    Languages:str=""                        
    #Challenge
    ChallengeRating:float=0.0            
    #Environments
    AllEnvironments:bool = True            
    Arctic:bool = False                     
    Costal:bool = False                     
    Desert:bool = False                    
    Forest:bool = False                     
    Grassland:bool = False                  
    Hills:bool = False                      
    Jungle:bool = False                     
    Mountain:bool = False                   
    Swamp:bool = False                      
    Underdark:bool = False                  
    Underwater:bool = False                 
    Urban:bool = False
    Sewer:bool = False
    Ruin:bool = False
    Feywild:bool = False
    Hell:bool = False
    EarthPlane:bool = False
    FirePlane:bool = False
    WaterPlane:bool = False
    AirPlane:bool = False
    AstralPlane:bool = False
    EtherealPlane:bool = False
    Laboratory:bool=False
    ShadowFell:bool = False
    Abyss:bool = False
    Caves:bool = False
    Temple:bool = False
    Volcano:bool = False
    Flexible:bool = False
    #Extra info
    Additional:str = ""                     
    Source:str= ""                          

    def __init__(self, row:list[str]=[]):
        #set the location and monster names
        self.setMonsterLocationAndCR(row)
        self.setMonsterInfo(row)

    def setMonsterLocationAndCR(self, row:dict):
        #this is separated out since it is what we search by
        self.Name:str = str(row['name'])
        #environments
        for env in row['environments']:
            match env.lower():
                case 'arctic' | 'tundra' | 'ice':
                    self.Arctic = True
                case 'coastal':
                    self.Costal = True
                case 'desert':
                    self.Desert = True
                case 'forest':
                    self.Forest = True
                case 'grassland':
                    self.Grassland = True
                case 'hill' | 'hills':
                    self.Hills = True
                case 'jungle':
                    self.Jungle = True
                case 'mountain'|'mountains':
                    self.Mountain = True
                case 'swamp':
                    self.Swamp = True
                case 'underdark':
                    self.Underdark = True
                case 'water' | 'underwater' | 'ocean' | 'lake':
                    self.Underwater = True
                case 'urban' | 'settlement':
                    self.Urban = True
                case 'sewer':
                    self.Sewer = True
                case 'ruin'|'ruins'|'tomb':
                    self.Ruin = True
                case 'hell':
                    self.Hell = True
                case 'plane of earth':
                    self.EarthPlane = True
                case 'plane of fire':
                    self.FirePlane = True
                case 'plane of water':
                    self.WaterPlane = True
                case 'plane of air':
                    self.AirPlane = True
                case 'astral plane':
                    self.AstralPlane = True
                case 'ethereal plane':
                    self.EtherealPlane = True
                case 'laboratory':
                    self.Laboratory = True
                case 'shadowfell':
                    self.ShadowFell = True
                case 'feywild':
                    self.Feywild = True
                case 'abyss':
                    self.Abyss = True
                case 'caves' | 'caverns':
                    self.Caves = True
                case 'temple':
                    self.Temple = True
                case 'any': #flexible
                    self.Flexible = True
                case 'volcano':
                    self.Volcano = True
                case _:
                    print(f"Missing Environment {env}")
        #stats
        self.ChallengeRating = float(row['cr'])

    def setMonsterInfo(self, row:list[str]):                  
        self.Size:str = row['size']                    
        self.Type:str = f"{row['type']}"
        self.HitDice:str = row['hit_dice']
        if(row['subtype'] != ''):
            self.Type += f" - {row['subtype']}"
        self.Alignment:str = row['alignment']                   
        #defense
        self.AC:int = int(row['armor_class'])
        self.ArmorDescription:str = f" {str(row['armor_desc'])}"                      
        self.HP:int = int(row['hit_points'])                     
        #Movement
        for speed in row['speed']:
            match speed:
                case 'walk':
                    self.SpeedNormal = str(row['speed']['walk'])+" ft"
                case 'burrow':
                    self.SpeedBurrowing = str(row['speed']['burrow'])+" ft"
                case 'bur.':
                    self.SpeedBurrowing = str(row['speed']['bur.'])+" ft"
                case 'fly':
                    self.SpeedFlying = str(row['speed']['fly'])+" ft"
                case 'climb':
                    self.SpeedClimb = str(row['speed']['climb'])+" ft"
                case 'swim':
                    self.SpeedSwimming = str(row['speed']['swim'])+" ft"
                case 'hover':
                    self.SpeedHover = str(row['speed']['hover'])+" ft"
                case 'lightwalking':
                    self.SpeedLightWalk = str(row['speed']['lightwalking'])+" ft"
                case 'notes':
                    self.SpeedNotes = str(row['speed']['notes'])
                case _:
                    print(f"Missing Speed {speed}")
        #stats
        self.Strength:int = int(row['strength'])                     
        self.Dexterity:int =  int(row['dexterity'])                   
        self.Constitution:int =  int(row['constitution'])                
        self.Intelligence:int =  int(row['intelligence'])               
        self.Wisdom:int =  int(row['wisdom'])                      
        self.Charisma:int =  int(row['charisma'])  

        #saving throws
        saves:list[str] = []
        if(row['strength_save'] != None):
            saves.append(f">  :person_lifting_weights:**Strength:** {row['strength_save']}")
        if(row['dexterity_save'] != None):
            saves.append(f">  :pinched_fingers:**Dexterity:** {row['dexterity_save']}")
        if(row['constitution_save'] != None):
            saves.append(f">  :anatomical_heart:**Constitution:** {row['constitution_save']}")
        if(row['intelligence_save'] != None):
            saves.append(f">  :nerd:**Intelligence:** {row['intelligence_save']}")
        if(row['wisdom_save'] != None):
            saves.append(f">  :woman_in_lotus_position:**Wisdom:** {row['wisdom_save']}")
        if(row['charisma_save'] != None):
            saves.append(f">  :lips:**Charisma:** {row['charisma_save']}")
        if(row['perception'] != None):
            saves.append(f">  :nazar_amulet:**Perception:** {row['perception']}")
        self.SavingThrows:str = "\n".join(saves)
        #abilities
        self.Languages:str=row['languages']
        self.Senses:str=row['senses']
        #Skills
        skills:list[str] = []
        for skill in row['skills']:
            skills.append(f"**{skill.capitalize()}**: {row['skills'][skill]}")
        self.Skills:str = "\n>  ".join(skills)
        if self.Skills != '':
            self.Skills = "\n>  "+self.Skills
        '''         
        #details                                       
        self.WeaknessResistanceImmunities:str = row[20]        
        #Extra info
        self.Additional:str = row[39]                        
        self.Source:str = row[40]                           
        '''

    def __format__(self, format_spec: str) -> str:
        return self.Name

    def getEmbedding(self) ->discord.Embed:
        embed = discord.Embed(title=f"{self.Name}")
        if self.Alignment != '':
            self.Size = f"{self.Alignment.title()} {self.Size}"
        embed.description = f"{self.Size} {self.Type}\n**Challenge Rating:** {self.ChallengeRating}\n**AC:** {str(self.AC) + self.ArmorDescription.title()} **HP:** {self.HP}\n **Hit Dice:** {self.HitDice}"

        movementList:list[str] = []
        if self.SpeedNormal != "": movementList.append(f">  **Normal:** {self.SpeedNormal}")
        if self.SpeedFlying != "": movementList.append(f">  **Flying:** {self.SpeedFlying}")
        if self.SpeedSwimming != "": movementList.append(f">  **Swimming:** {self.SpeedSwimming}")
        if self.SpeedBurrowing != "": movementList.append(f">  **Burrow:** {self.SpeedBurrowing}")
        if self.SpeedClimb != "": movementList.append(f">  **Climbing:** {self.SpeedClimb}")
        if self.SpeedHover != "": movementList.append(f">  **Hovering:** {self.SpeedHover}")
        if self.SpeedLightWalk != "": movementList.append(f">  **Light Walking:** {self.SpeedLightWalk}")
        if self.SpeedNotes != "": movementList.append(f">  **Notes:** {self.SpeedNotes}")

        embed.add_field(name="Movement", 
                        value="\n".join(movementList),
                        inline=False)
        embed.add_field(name="Stats",
                        value=f">  :mechanical_arm:**Strength:** {self.Strength}\n>  :pinched_fingers:**Dexterity:** {self.Dexterity}\n>  :sparkling_heart:**Constitution:** {self.Constitution}\n>  :brain:**Intelligence:** {self.Intelligence}\n>  :person_in_lotus_position:**Wisdom:** {self.Wisdom}\n>  :kiss:**Charisma:** {self.Charisma}",
                        inline=True)
        if(self.SavingThrows != ""):
            embed.add_field(name="Saving Throws",
                            value=self.SavingThrows,
                            inline=True)
        if(self.Skills != ""):
            embed.add_field(name="Skills", value=self.Skills, inline=True)
        embed.add_field(name="Details",
                        value=f"\n>  **Senses:** {self.Senses}\n>  **Languages:** {self.Languages}",
                        inline=False)
        environmentList:list[str] = []
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
        if self.Sewer is True : environmentList.append("Sewer")
        if self.Ruin is True : environmentList.append("Ruin")
        if self.Feywild is True : environmentList.append("Feywild")
        if self.Hell is True : environmentList.append("Hell")
        if self.EarthPlane is True : environmentList.append("Earth Plane")
        if self.FirePlane is True : environmentList.append("Fire Plane")
        if self.WaterPlane is True : environmentList.append("Water Plane")
        if self.AirPlane is True : environmentList.append("Air Plane")
        if self.AstralPlane is True : environmentList.append("Astral Plane")
        if self.EtherealPlane is True : environmentList.append("Ethereal Plane")
        if self.Laboratory is True : environmentList.append("Laboratory")
        if self.ShadowFell is True : environmentList.append("ShadowFell")
        if self.Abyss is True : environmentList.append("Abyss")
        if self.Caves is True : environmentList.append("Caves")
        if self.Temple is True : environmentList.append("Temple")
        if self.Volcano is True : environmentList.append("Volcano")
        if self.Flexible is True : environmentList.append("Flexible")

        if len(environmentList) != 0 :
            envStr:str = ", ".join(environmentList)
            embed.add_field(name="Environment", value=">  "+envStr, inline=False)

        embed.add_field(name="Extra",value=f">  **Actions:** {self.Additional}")
        return embed
