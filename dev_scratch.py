"""This file contains code in development and is meant to try out concepts or just play around with ideas."""
import random
import functions as func


# Races.
race_template = {
    "Race": 0,
    "Ability Requirements": 0,
    "Classes": 0,
    "Hit Dice": 0,
    "Weapons": 0,
    "Special": 0,
    "Save Bonuses": 0,
    "Languages": 0,
    "Description": 0,
}

dwarves = {
    "Race": "Dwarf",
    "Ability Requirements": "CON 9 or higher, CHA 17 or lower.",
    "Classes": "Cleric, Fighter, Thief",
    "Hit Die": "Any",
    "Weapons": "Large weapons require two hands."
               "No 2-handed swords, pole-arms or longbows.",
    "Special": "Darkvision 60'."
               "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6.",
    "Save Bonuses": "+4 vs Death Ray or Poison,"
                    "+4 vs Magic Wands,"
                    "+4 vs Paralysis,"
                    "+3 vs Dragon Breath,"
                    "+4 vs Spells",
    "Languages": "Common, Dwarvish."
                 "+1 Point of INT bonus.",
    "Description": "Typically about 4' tall, stocky, lifespan of 300-400 years. Thick hair and beards.",
}

# Character classes.
class_template = {
    "Class": 0,
    "Prime Requisite": 0,
    "Hit Dice": 0,
    "Weapons": 0,
    "Armor": 0,
    "XP for 2nd level": 0,
    "Spells": 0,
    "Specials": 0,
    "Saving Throws at 1st level": 0,
}

cleric = {
    "Class": "Cleric",
    "Prime Requisite": "WIS (must be 9+)",
    "Hit Dice": "D6",
    "Weapons": "Blunt weapons only.",
    "Armor": "Any, shields allowed.",
    "XP for 2nd level": 1500,
    "Spells": "None at first level.",
    "Specials": "Turn the undead (Clerics may be able to turn the undead or drive away undead monsters by means of faith"
                "alone. The Cleric brandishes their holy symbol and calls upon the power of their divine patron. The"
                "player rolls 1d20 and tells the GM the result).",
    "Saving Throws at 1st level": "Death Ray or Poison: 11"
                                  "Magic Wands: 12"
                                  "Paralysis or Petrify: 14"
                                  "Dragon Breath: 16"
                                  "Spells: 15",
}
