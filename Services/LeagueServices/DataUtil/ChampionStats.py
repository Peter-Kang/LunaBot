import discord
import random
from packaging.version import Version
from dataclasses import dataclass

@dataclass
class ChampionDisplay:
    ChampionVersion:Version = None
    data:dict[str:str] = None
    id:str =""
    Name:str = ""
    Lore:str = ""
    Tags:list[str] = None
    ImageUrl:str = ""
    Title:str =""
    TeamTips:str=""
    EnemyTips:str=""

    def __init__(self,version:Version,data:dict[str:str]):
        self.ChampionVersion = version
        self.__processData(data)

    def __processData(self, data:dict[str:str]):
        self.data = data
        self.Name = str(self.data["name"])
        self.id = str(self.data["id"])
        self.Lore = str(self.data["lore"])
        self.Tags = self.data["tags"]
        self.Title = self.data["title"]
        self.ImageUrl = f"https://ddragon.leagueoflegends.com/cdn/{self.ChampionVersion}/img/champion/{self.id}.png"
        self.TeamTips = "- "+"\n- ".join(self.data["allytips"])
        self.EnemyTips = "- "+"\n- ".join(self.data["enemytips"])

    def getEmbed(self) -> str:
        embed = discord.Embed(title=f"{self.Name} - {self.Title}")
        embed.description = self.Lore
        embed.add_field(name="Team Tips", value=self.TeamTips, inline=False)
        embed.add_field(name="Enemy Tips", value=self.EnemyTips, inline=False)
        embed.set_thumbnail(url=self.ImageUrl)
        return embed

class ChampionStats:
    
    ChampionData:list[ChampionDisplay] = []
    ChampionVersion:Version = None
    ChampionTags:set[str] = set()

    def __init__(self, version:Version, dictionaryFromAPI:list[tuple[str,dict[str:str]]]):
        self.ChampionVersion:Version = version
        for champTuple in dictionaryFromAPI:
            resultObject:ChampionDisplay = ChampionDisplay(self.ChampionVersion,champTuple[1])
            for tag in resultObject.Tags:
                self.ChampionTags.add(tag)
            self.ChampionData.append(resultObject)

    def randomChampion(self):
        champ_count:int = len(self.ChampionData)-1
        result:str = "No Data"
        if champ_count >= 0:
            index:int = random.randrange(0, champ_count, 1)
            result = self.ChampionData[index].getEmbed()
        return result