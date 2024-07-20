"""Dictionaries on races and classes to check for allowed armor/weapon."""


# Race descriptions.
dwarves = {
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
    "Weapons": {
        "Large Weapons": "two hands",
    },
    "Special": ["+10% to all earned XP"],
    "Save Bonuses": False,
    "Languages": ["Common"],
}


# Class descriptions.
cleric = {
    "Weapons": ["Club",
                "Mace",
                "Maul",
                "Quarterstaff",
                "Sling",
                "Warhammer"],
    "Armor": ["Any"],
    "Spells": False,
    "Special": ["Turn the Undead"],
    "Saving Throws at 1st level": {
        "Death Ray or Poison": 11,
        "Magic Wands": 12,
        "Paralysis or Petrify": 14,
        "Dragon Breath": 16,
        "Spells": 15,
    },
}


magic_user = {
    "Weapons": ["Cudgel",
                "Dagger",
                "Walking Staff"],
    "Armor": [False],
    "Spells": "1 first-level spell",
    "Special": [False],
    "Saving Throws at 1st level": {
        "Death Ray or Poison": 13,
        "Magic Wands": 14,
        "Paralysis or Petrify": 13,
        "Dragon Breath": 16,
        "Spells": 15,
    },
}


fighter = {
    "Weapons": ["Any"],
    "Armor": ["Any"],
    "Spells": False,
    "Special": [False],
    "Saving Throws at 1st level": {
        "Death Ray or Poison": 12,
        "Magic Wands": 13,
        "Paralysis or Petrify": 14,
        "Dragon Breath": 15,
        "Spells": 17,
    },
}


thief = {
    "Weapons": ["Any"],
    "Armor": ["Leather",
              "No Shield"],
    "Spells": False,
    "Special": ["Sneak Attack",
                "Thief Abilities"],
    "Saving Throws at 1st level": {
        "Death Ray or Poison": 13,
        "Magic Wands": 14,
        "Paralysis or Petrify": 13,
        "Dragon Breath": 16,
        "Spells": 15,
    },
}
