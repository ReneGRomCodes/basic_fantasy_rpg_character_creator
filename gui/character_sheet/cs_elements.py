import gui.screen_objects as so
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_cs_elements(screen, character, gui_elements):
    """Initialize instances of classes from 'screen_objects.py' for use in character sheet in addition to default size
    and spacing values for automatic scalability of screen objects. Return dict of instances 'cs_elements'.
    NOTE: Instances created have to be then added manually to dict 'cs_elements'!


    Class overview (imported as 'so'):
    TextField(screen, text, size, bg_color=False, text_color="default", multi_line=False, image_width=0, text_pos=(0,0):
        Basic text field.
    """

    # Size and spacing variables from dict 'gui_elements' that are calculated based on screen size for scalability.
    text_standard = gui_elements["text_standard"]
    text_large = gui_elements["text_large"]
    text_medium = gui_elements["text_medium"]
    text_small = gui_elements["text_small"]

    # Initialize screen elements.
    title = so.TextField(screen, "- CHARACTER SHEET -", text_medium)
    # Character sheet base info elements.
    name_field = so.TextField(screen, "Name: ", text_standard)
    name_char = so.TextField(screen, character.name, text_standard)
    xp_field = so.TextField(screen, "XP: ", text_standard)
    xp_char = so.TextField(screen, str(character.xp), text_standard)
    race_field = so.TextField(screen, "Race: ", text_standard)
    race_char = so.TextField(screen, character.race_name, text_standard)
    class_field = so.TextField(screen, "Class: ", text_standard)
    class_char = so.TextField(screen, character.class_name, text_standard)
    level_field = so.TextField(screen, "Level: ", text_standard)
    level_char = so.TextField(screen, str(character.level), text_standard)
    next_lvl_xp_field = so.TextField(screen, "XP to next level: ", text_standard)
    next_lvl_xp_char = so.TextField(screen, str(character.next_level_xp), text_standard)
    # Abilities and combat related info elements.
    armor_class = so.TextField(screen, "Armor Class:", text_standard)
    health_points = so.TextField(screen, "Health Points:", text_standard)
    attack_bonus = so.TextField(screen, "Attack Bonus:", text_standard)
    abilities = so.TextField(screen, "Abilities:", text_standard)
    saving_throws = so.TextField(screen, "Saving Throws:", text_standard)
    special_abilities = so.TextField(screen, "Special Abilities:", text_standard)
    # Spell element for classes 'Magic-User', 'Cleric' or combination classes.
    spells = so.TextField(screen, "Spells:", text_standard)
    # Inventory elements.
    money = so.TextField(screen, "Money:", text_standard)
    carrying_capacity = so.TextField(screen, "Carrying Capacity:", text_standard)
    weight_carried = so.TextField(screen, "Weight Carried:", text_standard)
    weapons = so.TextField(screen, "Weapons:", text_standard)
    armor = so.TextField(screen, "Armor:", text_standard)
    armor_ac = so.TextField(screen, "AC:", text_standard) # Armor class for worn armor only, not including base armor class for character.
    inventory = so.TextField(screen, "Inventory:", text_standard)

    # Dict to be returned containing instances and size/spacing values (for positioning) for GUI objects.
    cs_elements = {
        # Screen title.
        "title": title,
        # Basic info elements.
        "name": (name_field, name_char),
        "xp": (xp_field, xp_char),
        "level": (level_field, level_char),
        "next_level_xp": (next_lvl_xp_field, next_lvl_xp_char),
        "race": (race_field, race_char),
        "class": (class_field, class_char),
        # Abilities and combat elements.
        "armor_class": armor_class,
        "health_points": health_points,
        "attack_bonus": attack_bonus,
        "abilities": abilities,
        "saving_throws": saving_throws,
        "special_abilities": special_abilities,
        # Spells.
        "spells": spells,
        # Inventory elements.
        "money": money,
        "carrying_capacity": carrying_capacity,
        "weight_carried": weight_carried,
        "weapons": weapons,
        "armor": armor,
        "armor_ac": armor_ac,
        "inventory": inventory,
    }

    return cs_elements
