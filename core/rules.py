"""
Look-ups, helper- and check-functions representing the game rules.
"""
import random

import core.items.item_instances as item_inst


CLASS_CATEGORIES: dict = {
    "spell_using_classes": {"Cleric", "Magic-User", "Fighter/Magic-User", "Magic-User/Thief"},  # ALL spell casters.
    "magic_classes": {"Magic-User", "Fighter/Magic-User", "Magic-User/Thief"},  # Only 'true' magic users.
    "no_armor_classes": {"Magic-User"}  # Classes that are not allowed to wear armor.
}

CARRY_RULES: dict = {  # Carrying capacities. Each entry is (strength_threshold, light_load, heavy_load).
    "default": (
        (3, 25, 60),
        (5, 35, 90),
        (8, 50, 120),
        (12, 60, 150),
        (15, 65, 165),
        (17, 70, 180),
        (18, 80, 195),
    ),
    "halfling": (
        (3, 20, 40),
        (5, 30, 60),
        (8, 40, 80),
        (12, 50, 100),
        (15, 55, 110),
        (17, 60, 120),
        (18, 65, 130),
    )
}

MOVEMENT_RULES: dict = {  # Movement rates based on encumbrance and worn armor.
    "light_load": {
        "no_armor": 40,
        "leather_armor": 30,
        "other": 20
    },
    "heavy_load": {
        "no_armor": 30,
        "leather_armor": 20,
        "other": 10
    },
}

SAVING_THROWS: dict = {
    "categories": ("Death Ray or Poison", "Magic Wands", "Paralysis or Petrify", "Dragon Breath", "Spells"),

    "cleric_saves": (11, 12, 14, 16, 15),
    "fighter_saves": (12, 13, 14, 15, 17),
    "magic_user_saves": (13, 14, 13, 16, 15),
    "thief_saves": (13, 14, 13, 16, 15),
    "fighter_magic_user_saves": (13, 14, 14, 16, 17),
    "magic_user_thief_saves": (13, 14, 13, 16, 15),

    "dwarf_bonuses": (4, 4, 4, 3, 4),
    "elf_bonuses": (0, 2, 1, 0, 2),
    "halfling_bonuses": (4, 4, 4, 3, 4),
    "human_bonuses": (0, 0, 0, 0, 0),
}

RACE_DATA: dict = {
    "dwarf": {
        "race_hit_die": False,
        "race_specials": ("Darkvision 60'",
                          "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6"),
        "race_bonuses": SAVING_THROWS["dwarf_bonuses"],
        "languages": {"Common", "Dwarvish"},
        "carrying_cap": CARRY_RULES["default"],
    },
    "elf": {
        "race_hit_die": 6,
        "race_specials": ("Darkvision 60'", "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                          "Range reduction by 1 for surprise checks"),
        "race_bonuses": SAVING_THROWS["elf_bonuses"],
        "languages": {"Common", "Elvish"},
        "carrying_cap": CARRY_RULES["default"],
    },
    "halfling": {
        "race_hit_die": 6,
        "race_specials": ("+1 attack bonus on ranged weapons", "+1 to initiative die rolls",
                          "Hide (10% chance to be detected outdoors, 30% chance to be detected indoors"),
        "race_bonuses": SAVING_THROWS["halfling_bonuses"],
        "languages": {"Common", "Halfling"},
        "carrying_cap": CARRY_RULES["halfling"],
    },
    "human": {
        "race_hit_die": False,
        "race_specials": ("+10% to all earned XP", ),
        "race_bonuses": SAVING_THROWS["human_bonuses"],
        "languages": {"Common"},
        "carrying_cap": CARRY_RULES["default"],
    },
}

CLASS_DATA: dict = {
    "cleric": {
        "class_hit_die": 6,
        "next_level_xp": 1500,
        "class_specials": ("Turn the Undead", ),
        "class_saving_throws": SAVING_THROWS["cleric_saves"],
        "spells": ["No Spells"],
        "inventory": [],
        "weight_carried": 0,
    },
    "fighter": {
        "class_hit_die": 8,
        "next_level_xp": 2000,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["fighter_saves"],
        "spells": [],
        "inventory": [],
        "weight_carried": 0,
    },
    "magic-user": {
        "class_hit_die": 4,
        "next_level_xp": 2500,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["magic_user_saves"],
        "spells": ["Read Magic"],
        "inventory": [item_inst.SPELLBOOK],
        "weight_carried": item_inst.SPELLBOOK.weight,
    },
    "thief": {
        "class_hit_die": 4,
        "next_level_xp": 1250,
        "class_specials": ("Sneak Attack", "Thief Abilities"),
        "class_saving_throws": SAVING_THROWS["thief_saves"],
        "spells": [],
        "inventory": [],
        "weight_carried": 0,
    },
    "fighter/magic-user": {
        "class_hit_die": 6,
        "next_level_xp": 4500,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["fighter_magic_user_saves"],
        "spells": ["Read Magic"],
        "inventory": [item_inst.SPELLBOOK],
        "weight_carried": item_inst.SPELLBOOK.weight,
    },
    "magic-user/thief": {
        "class_hit_die": 4,
        "next_level_xp": 3750,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["magic_user_thief_saves"],
        "spells": ["Read Magic"],
        "inventory": [item_inst.SPELLBOOK],
        "weight_carried": item_inst.SPELLBOOK.weight,
    },
}


"""General functions."""

def dice_roll(n: int, m: int) -> int:
    """Roll an n number of m-sided dice and return the result.
    ARGS:
        n: amount of dice to roll.
        m: number of sides on the dice.
    RETURNS:
        result: int value for the dice roll.
    """
    result: int = 0

    for i in range(n):
        result += random.randint(1, m)

    return result


"""Ability scores."""

def get_ability_score() -> list[int]:
    """Generate random value for base ability score, get bonus/penalty based on this and return list with both values.
    base score at index 0 and the bonus/penalty at index 1.
    RETURNS:
        List with ability score values. 'base_score' at index 0 and 'bonus_penalty' at index 1.
    """
    base_score: int = dice_roll(3, 6)
    bonus_penalty: int = 0

    if base_score <= 3:
        bonus_penalty = -3
    elif base_score <= 5:
        bonus_penalty = -2
    elif base_score <= 8:
        bonus_penalty = -1
    elif base_score <= 12:
        pass  # Bonus/penalty of '0' in this range.
    elif base_score <= 15:
        bonus_penalty = 1
    elif base_score <= 17:
        bonus_penalty = 2
    else:
        bonus_penalty = 3

    return [base_score, bonus_penalty]


"""Race and class selection."""

def get_race_list(character: object) -> list[str]:
    """Check instance 'character' ability scores for possible races to choose and return them in list 'race_list'.
    ARGS:
        character: Instance of class 'Character'.
    RETURNS:
        race_list: list of possible races.
    """
    race_list: list[str] = ["Human"]  # Humans have no minimum requirements.

    # Variables to store ability scores from 'character.abilities' for if-checks.
    con_score: int = character.abilities["con"][0]  # Constitution.
    cha_score: int = character.abilities["cha"][0]  # Charisma.
    int_score: int = character.abilities["int"][0]  # Intelligence.
    dex_score: int = character.abilities["dex"][0]  # Dexterity.
    str_score: int = character.abilities["str"][0]  # Strength.

    # Check ability scores for minimum/maximum values for different races.
    if con_score >= 9 and cha_score <= 17:
        race_list.append("Dwarf")
    if int_score >= 9 and con_score <= 17:
        race_list.append("Elf")
    if dex_score >= 9 and str_score <= 17:
        race_list.append("Halfling")

    return race_list


def get_class_list(character: object) -> list[str]:
    """Check abilities from instance 'character' for possible classes to choose and return them in list 'class_list'.
    ARGS:
        character: Instance of class 'Character'.
    RETURNS:
        class_list: list of possible classes.
    """
    class_list: list[str] = []

    # Variables to store ability scores from 'character.abilities' for if-checks.
    wis_score: int = character.abilities["wis"][0]  # Wisdom.
    str_score: int = character.abilities["str"][0]  # Strength.
    int_score: int = character.abilities["int"][0]  # Intelligence.
    dex_score: int = character.abilities["dex"][0]  # Dexterity.

    if wis_score >= 9:
        class_list.append("Cleric")
    if str_score >= 9:
        class_list.append("Fighter")
        # Additional check for combination class.
        if int_score >= 9:
            class_list.append("Fighter/Magic-User")
    if int_score >= 9:
        class_list.append("Magic-User")
        # Additional check for combination class.
        if dex_score >= 9:
            class_list.append("Magic-User/Thief")
    if dex_score >= 9:
        class_list.append("Thief")

    return class_list


def check_valid_race_class(character: object) -> bool:
    """Create 'race_list' and 'class_list', check if 'class_list' is empty, return 'False' if so. If not check for valid
    race-class combinations and remove invalid races from 'race_list'. Return 'False' if 'race_list' is empty, 'True'
    if items remain in 'race_list' afterward.

    If you ever have the same thought a friend of mine had:
    'I need to see a Halfling Berserk-Assassin in action. Just a tiny, rage-filled murder gremlin trying to stab ankles
    while everyone else casually holds them back with one hand.
    And the Gnome Barbarian-Wizard… oh man. Just picture this tiny, bearded rage monster, dual-wielding a great axe and a
    spellbook, screaming, "I CAST FIST!" right before getting launched across the battlefield like a football.'
    This the function you want to edit.

    ARGS:
        character: Instance of class 'Character'.
    RETURNS:
        True: 'race_list' (still) contains available races and 'class_list' contains available classes.
        False: 'race_list' OR 'class_list' are empty after valid race-class-combinations have been checked.
    """

    # Create race and class lists for checks.
    race_list: list[str] = get_race_list(character)
    class_list: list[str] = get_class_list(character)

    # Check if class list is empty.
    if not class_list:
        return False

    # Check if 'Magic-User' is the only class available, therefor excluding Dwarves and Halflings from race selection.
    if class_list == ["Magic-User"] and "Dwarf" in race_list:
        race_list.remove("Dwarf")
    if class_list == ["Magic-User"] and "Halfling" in race_list:
        race_list.remove("Halfling")

    # Check if race list is empty after 'Magic-User' check above and return 'False' or modified 'race_list'.
    # NOTE: unnecessary with the current rule set as 'race_list' will always contain at least "Humans". If-statement
    # left in place to ensure that function still works should that change in the future.
    if not race_list:
        return False
    else:
        return True


def build_possible_characters_list(character: object) -> list[str]:
    """Create lists of possible races and classes and return list 'possible_characters' with valid race-class
    combinations.
    ARGS:
        character: Instance of class 'Character'.
    RETURNS:
        possible_characters: list containing possible characters as strings.
    """
    # Create race and class lists for checks.
    race_list: list[str] = get_race_list(character)
    class_list: list[str] = get_class_list(character)
    # Empty list to be returned with possible characters.
    possible_characters: list[str] = []

    for char_race in race_list:
        for char_class in class_list:
            # Exclude Dwarves and Halflings from class 'Magic-User'.
            if char_race in {"Dwarf", "Halfling"} and char_class == "Magic-User":
                pass
            # Assure that combination classes are only shown for Elves.
            elif char_race != "Elf" and char_class in {"Fighter/Magic-User", "Magic-User/Thief"}:
                pass
            else:
                race_class = char_race + " " + char_class
                possible_characters.append(race_class)

    return possible_characters


"""Language selection."""

def set_language_flag(character: object) -> bool:
    """Check minimum intelligence bonus required for character to learn additional languages and return 'True' if
    requirements are met.
    RETURNS:
        True: character meets minimum requirements for additional languages.
        False: character does not meet minimum requirements for additional languages.
    """
    # Set minimum intelligence bonus.
    minimum_int_bonus: int = 1

    if character.abilities["int"][1] >= minimum_int_bonus:
        return True
    else:
        return False


"""Starting Money functions."""

def roll_starting_money() -> int:
    """Generate and return random amount of starting money.
    RETURNS:
        starting_money: random int value for starting money.
    """
    starting_money: int = dice_roll(3, 6) * 10

    return starting_money
