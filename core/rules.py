"""
Look-ups, helper- and check-functions representing the game rules.
"""
import random

import core.items.item_instances as item_inst


ABILITIES: tuple[str, ...] = ("str", "dex", "con", "int", "wis", "cha")
STRENGTH: str = ABILITIES[0]
DEXTERITY: str = ABILITIES[1]
CONSTITUTION: str = ABILITIES[2]
INTELLIGENCE: str = ABILITIES[3]
WISDOM: str = ABILITIES[4]
CHARISMA: str = ABILITIES[5]

CLASS_CATEGORIES: dict = {
    "spell_using_classes": {"Cleric", "Magic-User", "Fighter/Magic-User", "Magic-User/Thief"},  # ALL spell casters.
    "magic_classes": {"Magic-User", "Fighter/Magic-User", "Magic-User/Thief"},  # Only 'true' magic users.
    "no_armor_classes": {"Magic-User"},  # Classes that are not allowed to wear armor.
    "no_shield_classes": {"Thief", "Magic-User/Thief"}  # Classes that are not allowed to use a shield.
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
    "Halfling": (
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
    "Dwarf": {
        "min_max_score": {"minimum": (CONSTITUTION, 9), "maximum": (CHARISMA, 17)},
        "race_hit_die": False,
        "race_specials": ("Darkvision 60'",
                          "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6"),
        "race_bonuses": SAVING_THROWS["dwarf_bonuses"],
        "classes": ("Cleric", "Fighter", "Thief"),
        "languages": {"Common", "Dwarvish"},
        "carrying_cap": CARRY_RULES["default"],
    },
    "Elf": {
        "min_max_score": {"minimum": (INTELLIGENCE, 9), "maximum": (CONSTITUTION, 17)},
        "race_hit_die": 6,
        "race_specials": ("Darkvision 60'", "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                          "Range reduction by 1 for surprise checks"),
        "race_bonuses": SAVING_THROWS["elf_bonuses"],
        "classes": ("Cleric", "Fighter", "Magic-User", "Thief", "Fighter/Magic-User", "Magic-User/Thief"),
        "languages": {"Common", "Elvish"},
        "carrying_cap": CARRY_RULES["default"],
    },
    "Halfling": {
        "min_max_score": {"minimum": (DEXTERITY, 9), "maximum": (STRENGTH, 17)},
        "race_hit_die": 6,
        "race_specials": ("+1 attack bonus on ranged weapons", "+1 to initiative die rolls",
                          "Hide (10% chance to be detected outdoors, 30% chance to be detected indoors"),
        "race_bonuses": SAVING_THROWS["halfling_bonuses"],
        "classes": ("Cleric", "Fighter", "Thief"),
        "languages": {"Common", "Halfling"},
        "carrying_cap": CARRY_RULES["Halfling"],
    },
    "Human": {
        "min_max_score": False,
        "race_hit_die": False,
        "race_specials": ("+10% to all earned XP", ),
        "race_bonuses": SAVING_THROWS["human_bonuses"],
        "classes": ("Cleric", "Fighter", "Magic-User", "Thief"),
        "languages": {"Common"},
        "carrying_cap": CARRY_RULES["default"],
    },
}

CLASS_DATA: dict = {
    "Cleric": {
        "min_score": ((WISDOM, 9), ),
        "class_hit_die": 6,
        "next_level_xp": 1500,
        "class_specials": ("Turn the Undead", ),
        "class_saving_throws": SAVING_THROWS["cleric_saves"],
        "spells": ["No Spells"],
        "inventory": [],
        "weight_carried": 0,
    },
    "Fighter": {
        "min_score": ((STRENGTH, 9), ),
        "class_hit_die": 8,
        "next_level_xp": 2000,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["fighter_saves"],
        "spells": [],
        "inventory": [],
        "weight_carried": 0,
    },
    "Magic-User": {
        "min_score": ((INTELLIGENCE, 9), ),
        "class_hit_die": 4,
        "next_level_xp": 2500,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["magic_user_saves"],
        "spells": ["Read Magic"],
        "inventory": [item_inst.SPELLBOOK],
        "weight_carried": item_inst.SPELLBOOK.weight,
    },
    "Thief": {
        "min_score": ((DEXTERITY, 9), ),
        "class_hit_die": 4,
        "next_level_xp": 1250,
        "class_specials": ("Sneak Attack", "Thief Abilities"),
        "class_saving_throws": SAVING_THROWS["thief_saves"],
        "spells": [],
        "inventory": [],
        "weight_carried": 0,
    },
    "Fighter/Magic-User": {
        "min_score": ((STRENGTH, 9), (INTELLIGENCE, 9)),
        "class_hit_die": 6,
        "next_level_xp": 4500,
        "class_specials": (),
        "class_saving_throws": SAVING_THROWS["fighter_magic_user_saves"],
        "spells": ["Read Magic"],
        "inventory": [item_inst.SPELLBOOK],
        "weight_carried": item_inst.SPELLBOOK.weight,
    },
    "Magic-User/Thief": {
        "min_score": ((INTELLIGENCE, 9), (DEXTERITY, 9)),
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
    # Threshold breakpoints for bonus/penalty calculation.
    threshold_00: int = 3
    threshold_01: int = 5
    threshold_02: int = 8
    threshold_03: int = 12
    threshold_04: int = 15
    threshold_05: int = 17

    base_score: int = dice_roll(3, 6)
    bonus_penalty: int = 0

    if base_score <= threshold_00:
        bonus_penalty = -3
    elif base_score <= threshold_01:
        bonus_penalty = -2
    elif base_score <= threshold_02:
        bonus_penalty = -1
    elif base_score <= threshold_03:
        pass  # Bonus/penalty of '0' in this range.
    elif base_score <= threshold_04:
        bonus_penalty = 1
    elif base_score <= threshold_05:
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
        race_list: list of possible races as strings.
    """
    race_list: list[str] = []

    for race, scores in RACE_DATA.items():

        if not scores["min_max_score"]:
            race_list.append(race)

        else:
            min_ability: str = scores["min_max_score"]["minimum"][0]
            min_score: int = scores["min_max_score"]["minimum"][1]
            max_ability: str = scores["min_max_score"]["maximum"][0]
            max_score: int = scores["min_max_score"]["maximum"][1]

            if character.abilities[min_ability][0] >= min_score and character.abilities[max_ability][0] <= max_score:
                race_list.append(race)

    return race_list


def get_class_list(character: object) -> list[str]:
    """Check abilities from instance 'character' for possible classes to choose and return them in list 'class_list'.
    ARGS:
        character: Instance of class 'Character'.
    RETURNS:
        class_list: list of possible classes as strings.
    """
    class_list: list[str] = []

    for cls, scores in CLASS_DATA.items():

        if not scores["min_score"][0]:  # Add class if it has no minimum score requirements.
            class_list.append(cls)

        else:
            class_list.append(cls)

            for requirement in scores["min_score"]:
                ability: str = requirement[0]
                min_score: int = requirement[1]
                char_ability_score: int = character.abilities[ability][0]
                last_or_only_req: tuple[str, int] = scores["min_score"][-1]

                if requirement == last_or_only_req and char_ability_score >= min_score:
                    break
                elif char_ability_score >= min_score:
                    pass
                else:
                    class_list.remove(cls)
                    break

    return class_list


def check_valid_race_class(character: object) -> bool:
    """Check if a character has at least one valid race/class combination.
    ARGS:
        character: Instance of class 'Character'.
    RETURNS:
        'True' if there's at least one valid race/class combo, 'False' otherwise.
    """
    race_check_list: list[str] = get_race_list(character)
    class_check_list: list[str] = get_class_list(character)

    if not class_check_list:
        return False

    # Exclude Dwarves and Halflings if 'Magic-User' is the only class available.
    if class_check_list == ["Magic-User"] and "Dwarf" in race_check_list:
        race_check_list.remove("Dwarf")
    if class_check_list == ["Magic-User"] and "Halfling" in race_check_list:
        race_check_list.remove("Halfling")

    # Check if race list is empty after 'Magic-User' check above.
    # NOTE: unnecessary with the current rule set as 'race_list' will always contain at least "Humans". If-statement
    # left in place to ensure that function still works should that change in the future.
    if not race_check_list:
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
    race_list: list[str] = get_race_list(character)
    class_list: list[str] = get_class_list(character)
    possible_characters: list[str] = []

    for char_race in race_list:
        for char_class in class_list:
            if char_race in {"Dwarf", "Halfling"} and char_class == "Magic-User":
                pass
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
