"""
Contains function for the character's ability score descriptions.
"""


def get_ability_descr() -> dict[str, str]:
    """Initialize variables containing characters ability score descriptions and return them in dict 'ability_descr'.
    NOTE: String variables created have to be then added manually to dict 'ability_descr'.
    RETURNS:
        ability_descr: dict containing each ability description text as strings.
    """

    strength: str = ("Measures the character's raw physical power. Strength is the prime requisite for FIGHTERS.\n"
                     "\nBonuses:\n"
                     " - Adds to attack roll when using melee weapons.\n"
                     " - Adds to the damage roll for melee weapons\n"
                     "    or thrown weapons.")
    dexterity: str = ("Measures the character's quickness and balance as well as aptitude with tools. Dexterity is the prime "
                      "requisite for THIEVES.\n"
                      "\nBonuses:\n"
                      " - Adds to attack roll when using ranged weapons.\n"
                      " - Armor Class (AC).\n"
                      " - Initiative die roll.")
    constitution: str = ("A combination of general health and vitality.\n"
                         "\nBonuses:\n"
                         " - Add to each Hit Die.\n"
                         " - Save vs. Poison.")
    intelligence: str = ("The ability to learn and apply knowledge. Intelligence is the prime requisite for MAGIC-USERS.\n"
                         "\nBonuses:\n"
                         " - Number of languages the character knows.\n"
                         " - Save vs. Illusion.\n"
                         " - May be useful for remembering spells and research.")
    wisdom: str = ("A combination of intuition, willpower and common sense. Wisdom is the prime requisite for CLERICS.\n"
                   "\nBonuses:\n"
                   " - Some saving throws vs. magical attacks.")
    charisma: str = ("The ability to influence or even lead people; those with high Charisma are well-liked, or at least "
                     "highly respected.\n"
                     "\nBonuses:\n"
                     " - Reaction rolls.\n"
                     " - Number of retainers a character may hire.")

    # Dict to be returned containing string variables with character ability score descriptions.
    ability_descr: dict[str, str] = {
        "str_descr": strength,
        "dex_descr": dexterity,
        "con_descr": constitution,
        "int_descr": intelligence,
        "wis_descr": wisdom,
        "cha_descr": charisma,
    }

    return ability_descr
