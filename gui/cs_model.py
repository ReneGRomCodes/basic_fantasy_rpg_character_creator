import gui.screen_objects as so
"""Helper class to organize and access character sheet objects as attributes."""


class CharacterSheet:
    """A class to store and manage character sheet elements."""

    def __init__(self, screen, character, gui_elements):
        """Initialize the CharacterSheet object with elements."""

        # Assign screen rect attributes.
        self.screen_rect = screen.get_rect()
        self.screen_height, self.screen_width = self.screen_rect.height, self.screen_rect.width

        # Size and spacing variables from dict 'gui_elements' that are calculated based on screen size for scalability.
        self.text_standard = gui_elements["text_standard"]
        self.text_large = gui_elements["text_large"]
        self.text_medium = gui_elements["text_medium"]
        self.text_small = gui_elements["text_small"]
        self.title_spacing = gui_elements["menu_title_spacing"]
        self.spacing_screen_edge = gui_elements["default_edge_spacing"]

        # Following character sheet elements are paired, with attributes having the suffix '_field' representing the
        # field label, while '_char' represent the value from the 'Character' class object.

        # Initialize character sheet elements.
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

    def position_cs_elements(self):
        """Position instances of class 'TextField' on screen."""

        # Position screen title.
        self.title.text_rect.top, self.title.text_rect.centerx = (self.screen_rect.top + self.spacing_screen_edge,
                                                                  self.screen_rect.centerx)

        # Positioning for basic character info fields. Primary 'anchor' object for positioning all elements is 'name_field'.
        self.name_field.text_rect.top, self.name_field.text_rect.left =(
            self.title.text_rect.bottom + self.title_spacing, self.screen_rect.left + self.spacing_screen_edge)
        self.name_char.text_rect.top, self.name_char.text_rect.left =(
            self.name_field.text_rect.top, self.name_field.text_rect.right)
        self.xp_field.text_rect.top, self.xp_field.text_rect.left =(
            self.name_field.text_rect.top, self.screen_width * 0.75)
        self.xp_char.text_rect.top, self.xp_char.text_rect.left = self.xp_field.text_rect.top, self.xp_field.text_rect.right
        self.race_field.text_rect.top, self.race_field.text_rect.left =(
            self.name_field.text_rect.bottom, self.name_field.text_rect.left)
        self.race_char.text_rect.top, self.race_char.text_rect.left =(
            self.race_field.text_rect.top, self.race_field.text_rect.right)
        self.class_field.text_rect.top, self.class_field.text_rect.left =(
            self.race_char.text_rect.top, self.screen_width * 0.25)
        self.class_char.text_rect.top, self.class_char.text_rect.left =(
            self.class_field.text_rect.top, self.class_field.text_rect.right)
        self.level_field.text_rect.top, self.level_field.text_rect.left =(
            self.class_char.text_rect.top, self.screen_width * 0.5)
        self.level_char.text_rect.top, self.level_char.text_rect.left =(
            self.level_field.text_rect.top, self.level_field.text_rect.right)
        self.next_lvl_xp_field.text_rect.top, self.next_lvl_xp_field.text_rect.left =(
            self.level_char.text_rect.top, self.screen_width * 0.75)
        self.next_lvl_xp_char.text_rect.top, self.next_lvl_xp_char.text_rect.left =(
            self.next_lvl_xp_field.text_rect.top, self.next_lvl_xp_field.text_rect.right)

    def show_character_sheet_screen(self):
        # Draw screen title.
        self.title.draw_text()

        # Draw character sheet elements.
        # Basic character info fields.
        self.name_field.draw_text()
        self.name_char.draw_text()
        self.xp_field.draw_text()
        self.xp_char.draw_text()
        self.race_field.draw_text()
        self.race_char.draw_text()
        self.class_field.draw_text()
        self.class_char.draw_text()
        self.level_field.draw_text()
        self.level_char.draw_text()
        self.next_lvl_xp_field.draw_text()
        self.next_lvl_xp_char.draw_text()
