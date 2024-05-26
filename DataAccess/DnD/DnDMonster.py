import discord
import json

class DnDMonster:                         

    def __init__(self, row:list[str]=[]):
        self.Name:str = ""                           
        self.Size:str = ""                           
        self.Type:str = ""                                         
        self.Alignment:str = ""
        self.HitDice:str = ""                      
    #defense
        self.AC:int = 0
        self.ArmorDescription:str = ""                              
        self.HP:int = 0                             
    #Movement
        self.SpeedNormal:str = ""                    
        self.SpeedFlying:str = ""                   
        self.SpeedSwimming:str = ""                  
        self.SpeedBurrowing:str = ""                 
        self.SpeedClimb:str = ""
        self.SpeedHover:str = ""
        self.SpeedLightWalk:str = ""
        self.SpeedNotes:str = ""                     
    #stats
        self.Strength:int = 0                        
        self.Dexterity:int = 0                       
        self.Constitution:int = 0                    
        self.Intelligence:int = 0                    
        self.Wisdom:int = 0                          
        self.Charisma:int = 0                        
    #details
        self.SavingThrows:str = ""                   
        self.Skills:str = ""                         
        self.Senses:str=""                           
        self.Languages:str=""                        
    #Challenge
        self.ChallengeRating:float=0.0            
    #Environments
        self.AllEnvironments:bool = True            
        self.Arctic:bool = False                     
        self.Costal:bool = False                     
        self.Desert:bool = False                    
        self.Forest:bool = False                     
        self.Grassland:bool = False                  
        self.Hills:bool = False                      
        self.Jungle:bool = False                     
        self.Mountain:bool = False                   
        self.Swamp:bool = False                      
        self.Underdark:bool = False                  
        self.Underwater:bool = False                 
        self.Urban:bool = False
        self.Sewer:bool = False
        self.Ruin:bool = False
        self.Feywild:bool = False
        self.Hell:bool = False
        self.EarthPlane:bool = False
        self.FirePlane:bool = False
        self.WaterPlane:bool = False
        self.AirPlane:bool = False
        self.AstralPlane:bool = False
        self.EtherealPlane:bool = False
        self.Laboratory:bool=False
        self.ShadowFell:bool = False
        self.Abyss:bool = False
        self.Caves:bool = False
        self.Temple:bool = False
        self.Volcano:bool = False
        self.Flexible:bool = False
    #WRI
        self.Weaknesses:str = ""
        self.Resistances:str = ""
        self.DamageImmunities:str =""
        self.ConditionImmunities:str = ""
    #actions
        self.Actions:list[str] = []
        self.BonusActions:list[str] = []
        self.Reactions:list[str] = []
        self.LegendaryActions:list[str] = []
        self.SpecialAbilities:list[str] = []
        self.SpellList:list[str] = []
    #Extra info
        self.Additional:str = ""                     
        self.Source:str= "" 
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
        #WRI
        self.Weaknesses = row["damage_vulnerabilities"]
        self.Resistances = row["damage_resistances"]
        self.DamageImmunities = row["damage_immunities"]
        self.ConditionImmunities = row["condition_immunities"]
        #actions
        if row["actions"] != None:
            for action in row["actions"]:
                self.Actions.append(f"{action['name']}")#: {action['desc'] if 'desc' in action else action['description']}")
        #bonus_actions
        if row["bonus_actions"] != None:
            for bonus in row["bonus_actions"]:
                self.BonusActions.append(f"{bonus['name']}")#: {bonus['desc'] if 'desc' in bonus else bonus['description']}")
        #reactions
        if row["reactions"] != None:
            for reaction in row["reactions"]:
                self.Reactions.append(f"{reaction['name']}")#: {reaction['desc'] if 'desc' in reaction else reaction['description']}")
        #legendary_actions
        if row["legendary_actions"] != None:
            for legendary in row["legendary_actions"]:
                self.LegendaryActions.append(f"{legendary['name']}")#: {legendary['desc'] if 'desc' in legendary else legendary['description']}")
        #special_abilities
        if row["special_abilities"] != None:
            for spec in row["special_abilities"]:
                self.SpecialAbilities.append(f"{spec['name']}")#: {spec['desc'] if 'desc' in spec else spec['description']}")
        #spell_list, remove https://api.open5e.com/v1/spells/,-, and /, then make title
        if row["spell_list"] != None:
            for spell in row["spell_list"]:
                self.SpellList.append(spell.replace("https://api.open5e.com/v1/spells/","").replace("-"," ").replace("/",""))

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
        embed.add_field(name = chr(173), value = chr(173),inline=False)
        #environment
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
            embed.add_field(name="Environment", value=f">  {envStr}", inline=False)
        #WRI
        if(self.Weaknesses != ""):
            embed.add_field(name="Vulnerabilities", value=f">  {self.Weaknesses}", inline=False)
        if(self.Resistances != ""):
            embed.add_field(name="Resistances", value=f">  {self.Resistances}", inline=True)
        if(self.DamageImmunities != ""):
            embed.add_field(name="Damage Immunities", value=f">  {self.DamageImmunities}", inline=True)
        if(self.ConditionImmunities != ""):
            embed.add_field(name="Conditional Immunities", value=f">  {self.ConditionImmunities}", inline=True)
        #details
        embed.add_field(name = chr(173), value = chr(173),inline=False)
        embed.add_field(name="Details",
                        value=f"\n>  **Senses:** {self.Senses}\n>  **Languages:** {self.Languages}",
                        inline=False)
        
        #Actions
        if len(self.Actions) != 0:
            embed.add_field(name="Actions", value="- "+"\n- ".join(self.Actions), inline=False)
        #BonusActions
        if len(self.BonusActions) != 0:
            embed.add_field(name="Bonus Actions", value="- "+"\n- ".join(self.BonusActions), inline=False)
        #Reactions
        if len(self.Reactions) != 0:
            embed.add_field(name="Reactions", value="- "+"\n- ".join(self.Reactions), inline=False)
        #LegendaryActions
        if len(self.LegendaryActions) != 0:
            embed.add_field(name="Legendary Actions", value="- "+"\n- ".join(self.LegendaryActions), inline=False)
        #SpecialAbilities
        if len(self.SpecialAbilities) != 0:
            embed.add_field(name="Special Abilities", value="- "+"\n- ".join(self.SpecialAbilities), inline=False)
        #SpellList
        if len(self.SpellList) != 0:
            embed.add_field(name="Spell List", value=", ".join(self.SpellList), inline=False)
        return embed
