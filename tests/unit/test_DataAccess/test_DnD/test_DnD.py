import json
import os
import tempfile
import unittest

from src.DataAccess.DnD.DnDMonster import DnDMonster
from src.DataAccess.DnD.DnDMonsterReader import DnDMonsterReader


class TestDnDMonster(unittest.TestCase):
    def setUp(self):
        self.monster_data = {
            "name": "Goblin",
            "environments": ["forest", "caves"],
            "cr": 0.25,
            "size": "Small",
            "type": "humanoid",
            "subtype": "goblinoid",
            "alignment": "neutral evil",
            "hit_dice": "2d6",
            "armor_class": 15,
            "armor_desc": "leather armor",
            "hit_points": 7,
            "speed": {
                "walk": 30,
                "burrow": 0,
                "fly": 0,
                "climb": 0,
                "swim": 0,
                "hover": 0,
                "lightwalking": 0,
                "notes": ""
            },
            "strength": 8,
            "dexterity": 14,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 8,
            "charisma": 8,
            "strength_save": None,
            "dexterity_save": None,
            "constitution_save": None,
            "intelligence_save": None,
            "wisdom_save": None,
            "charisma_save": None,
            "perception": None,
            "languages": "Common, Goblin",
            "senses": "darkvision 60 ft.",
            "skills": {"stealth": "+6"},
            "damage_vulnerabilities": "",
            "damage_resistances": "",
            "damage_immunities": "",
            "condition_immunities": "",
            "actions": [{"name": "Scimitar"}],
            "bonus_actions": None,
            "reactions": None,
            "legendary_actions": None,
            "special_abilities": None,
            "spell_list": None
        }

    def test_monster_init_parses_expected_fields(self):
        monster = DnDMonster(self.monster_data)

        self.assertEqual(monster.Name, "Goblin")
        self.assertTrue(monster.Forest)
        self.assertTrue(monster.Caves)
        self.assertEqual(monster.ChallengeRating, 0.25)
        self.assertEqual(monster.Size, "Small")
        self.assertEqual(monster.Type, "humanoid - goblinoid")
        self.assertEqual(monster.Alignment, "neutral evil")
        self.assertEqual(monster.HitDice, "2d6")
        self.assertEqual(monster.AC, 15)
        self.assertEqual(monster.ArmorDescription.strip(), "leather armor")
        self.assertEqual(monster.HP, 7)
        self.assertEqual(monster.SpeedNormal, "30 ft")
        self.assertEqual(monster.Strength, 8)
        self.assertEqual(monster.Dexterity, 14)
        self.assertEqual(monster.Languages, "Common, Goblin")
        self.assertIn("**Stealth**: +6", monster.Skills)
        self.assertEqual(monster.Actions, ["Scimitar"])
        self.assertEqual(monster.SpellList, [])

    def test_monster_embed_contains_core_values(self):
        monster = DnDMonster(self.monster_data)
        embed = monster.getEmbedding()

        self.assertEqual(embed.title, "Goblin")
        self.assertIn("Challenge Rating", embed.description)
        self.assertIn("AC:** 15", embed.description)
        self.assertEqual(embed.fields[0].name, "Movement")
        self.assertEqual(embed.fields[1].name, "Stats")
        self.assertTrue(any(field.name == "Details" for field in embed.fields))

if __name__ == "__main__":
    unittest.main()
