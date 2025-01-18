import gui.screen_objects as so
"""Helper class to organize and access character sheet objects as attributes."""


class CharacterSheet:
    """A class to store and manage character sheet elements."""

    def __init__(self, screen, character, gui_elements):
        """Initialize the CharacterSheet object with elements."""

        # Size and spacing variables from dict 'gui_elements' that are calculated based on screen size for scalability.
        self.text_standard = gui_elements["text_standard"]
        self.text_large = gui_elements["text_large"]
        self.text_medium = gui_elements["text_medium"]
        self.text_small = gui_elements["text_small"]

        # Initialize screen elements.
        self.title = so.TextField(screen, "- CHARACTER SHEET -", self.text_medium)
        # Character sheet base info elements.
        self.name_field = so.TextField(screen, "Name: ", self.text_standard)
        self.name_char = so.TextField(screen, character.name, self.text_standard)
        self.xp_field = so.TextField(screen, "XP: ", self.text_standard)
        self.xp_char = so.TextField(screen, str(character.xp), self.text_standard)
        self.race_field = so.TextField(screen, "Race: ", self.text_standard)
        self.race_char = so.TextField(screen, character.race_name, self.text_standard)
        self.class_field = so.TextField(screen, "Class: ", self.text_standard)
        self.class_char = so.TextField(screen, character.class_name, self.text_standard)
        self.level_field = so.TextField(screen, "Level: ", self.text_standard)
        self.level_char = so.TextField(screen, str(character.level), self.text_standard)
        self.next_lvl_xp_field = so.TextField(screen, "XP to next level: ", self.text_standard)
        self.next_lvl_xp_char = so.TextField(screen, str(character.next_level_xp), self.text_standard)
        # Abilities and combat related info elements.
        self.armor_class = so.TextField(screen, "Armor Class:", self.text_standard)
        self.health_points = so.TextField(screen, "Health Points:", self.text_standard)
        self.attack_bonus = so.TextField(screen, "Attack Bonus:", self.text_standard)
        self.abilities = so.TextField(screen, "Abilities:", self.text_standard)
        self.saving_throws = so.TextField(screen, "Saving Throws:", self.text_standard)
        self.special_abilities = so.TextField(screen, "Special Abilities:", self.text_standard)
        # Spell element for classes 'Magic-User', 'Cleric' or combination classes.
        self.spells = so.TextField(screen, "Spells:", self.text_standard)
        # Inventory elements.
        self.money = so.TextField(screen, "Money:", self.text_standard)
        self.carrying_capacity = so.TextField(screen, "Carrying Capacity:", self.text_standard)
        self.weight_carried = so.TextField(screen, "Weight Carried:", self.text_standard)
        self.weapons = so.TextField(screen, "Weapons:", self.text_standard)
        self.armor = so.TextField(screen, "Armor:", self.text_standard)
        self.armor_ac = so.TextField(screen, "AC:", self.text_standard) # Armor class for worn armor only, not including base armor class for character.
        self.inventory = so.TextField(screen, "Inventory:", self.text_standard)
