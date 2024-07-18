"""This file contains code in development and is meant to try out concepts or just play around with ideas."""
import random
import functions as func


# Races.
race_template = {
    "Hit Die": 0,
    "Weapons": 0,
    "Special": 0,
    "Save Bonuses": 0,
    "Languages": 0,
    "Description": 0,
}

dwarves = {
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
    "Hit Die": 0,
    "Weapons": 0,
    "Armor": 0,
    "XP for 2nd level": 0,
    "Spells": 0,
    "Specials": 0,
    "Saving Throws at 1st level": 0,
}

cleric = {
    "Hit Die": "D6",
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

func.show_race_descriptions()
