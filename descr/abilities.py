"""Contains function for the characters ability score descriptions."""


def get_ability_descr():
    """Initialize variables containing characters ability score descriptions and return them in dict 'ability_descr'.
    NOTE: String variables created have to be then added manually to dict 'ability_descr'!"""

    strength = ("Measures the character's raw physical power. Strength is the prime requisite for FIGHTERS.\n"
                "\nBonuses:\n"
                " - Adds to attack roll when using melee weapons.\n"
                " - Adds to the damage roll for melee weapons or thrown weapons.")
    dexterity = ("Measures the character's quickness and balance as well as aptitude with tools. Dexterity is the prime "
                 "requisite for THIEVES.\n"
                 "\nBonuses:\n"
                 " - Adds to attack roll when using ranged weapons.\n"
                 " - Armor Class (AC).\n"
                 " - Initiative die roll.")
    constitution = ("A combination of general health and vitality.\n"
                    "\nBonuses:\n"
                    " - Add to each Hit Die.\n"
                    " - Save vs. Poison.")
    intelligence = ("The ability to learn and apply knowledge. Intelligence is the prime requisite for MAGIC-USERS.\n"
                    "\nBonuses:\n"
                    " - Number of languages the character knows.\n"
                    " - Save vs. Illusion.\n"
                    " - May be useful for remembering spells and research.")
    wisdom = ("A combination of intuition, willpower and common sense. Wisdom is the prime requisite for CLERICS.\n"
              "\nBonuses:\n"
              " - Some saving throws vs. magical attacks.")
    charisma = ("The ability to influence or even lead people; those with high Charisma are well-liked, or at least "
                "highly respected.\n"
                "\nBonuses:\n"
                " - Reaction rolls.\n"
                " - Number of retainers a character may hire.")

    # Dict to be returned containing string variables with character ability score descriptions.
    ability_descr = {
        "str_descr": strength,
        "dex_descr": dexterity,
        "con_descr": constitution,
        "int_descr": intelligence,
        "wis_descr": wisdom,
        "cha_descr": charisma,
    }

    return ability_descr
