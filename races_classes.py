# Race descriptions.
dwarves = {
    "Hit Die": 8,
    "Weapons": {
        "Large Weapons": "two hands",
        "2-Handed Sword": False,
        "Pole Arm": False,
        "Longbow": False,
    },
    "Special": ["Darkvision 60'",
                "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6"],
    "Save Bonuses": {
        "Death Ray or Poison": 4,
        "Magic Wands": 4,
        "Paralysis or Petrify": 4,
        "Dragon Breath": 3,
        "Spells": 4,
    },
    "Languages": ["Common", "Dwarvish"],
}


elves = {
    "Hit Die": 6,
    "Weapons": {
        "Large Weapons": "two hands",
    },
    "Special": ["Darkvision 60'",
                "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                "Immune to paralyzing attack from ghouls",
                "Range reduction by 1 for surprise checks"],
    "Save Bonuses": {
        "Magic Wands": 2,
        "Paralysis or Petrify": 1,
        "Spells": 2,
    },
    "Languages": ["Common", "Elvish"],
}


halflings = {
    "Hit Die": 6,
    "Weapons": {
        "Large Weapons": False,
        "Medium Weapons": "two hands",
    },
    "Special": ["+1 attack bonus on ranged weapons",
                "+2 bonus to AC when attacked in melee by creatures larger than man-sized",
                "+1 to initiative die rolls",
                "Hide (10% change to be detected outdoors, 30% chance to be detected indoors"],
    "Save Bonuses": {
        "Death Ray or Poison": 4,
        "Magic Wands": 4,
        "Paralysis or Petrify": 4,
        "Dragon Breath": 3,
        "Spells": 4,
    },
    "Languages": ["Common", "Halfling"],
}


humans = {
    "Hit Die": 8,
    "Weapons": {
        "Large Weapons": "two hands",
    },
    "Special": ["+10% to all earned XP"],
    "Save Bonuses": False,
    "Languages": ["Common"],
}


# Class descriptions.
class_template = {
    "Hit Die": 0,
    "Weapons": 0,
    "Armor": 0,
    "XP for 2nd level": 0,
    "Spells": 0,
    "Specials": 0,
    "Saving Throws at 1st level": 0,
}