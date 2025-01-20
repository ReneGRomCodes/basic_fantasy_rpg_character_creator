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

        # Combat related info elements.
        self.armor_class_field = so.TextField(screen, "Armor Class: ", self.text_standard)
        self.armor_class_char = so.TextField(screen, str(character.armor_class), self.text_standard)
        self.health_points_field = so.TextField(screen, "Health Points: ", self.text_standard)
        self.health_points_char = so.TextField(screen, str(character.hp), self.text_standard)
        self.attack_bonus_field = so.TextField(screen, "Attack Bonus: +", self.text_standard)
        self.attack_bonus_char = so.TextField(screen, str(character.attack_bonus), self.text_standard)

        # Abilities info elements. Suffixes '_score' and '_bonus_penalty' indicate objects with values from the
        # 'Character' class object.
        self.abilities_title = so.TextField(screen, "ABILITIES", self.text_standard)
        self.str_field = so.TextField(screen, "str", self.text_standard)
        self.str_score = so.TextField(screen, str(character.abilities["str"][0]), self.text_standard)
        self.str_bonus_penalty = so.TextField(screen, str(character.abilities["str"][1]), self.text_standard)
        self.dex_field = so.TextField(screen, "dex", self.text_standard)
        self.dex_score = so.TextField(screen, str(character.abilities["dex"][0]), self.text_standard)
        self.dex_bonus_penalty = so.TextField(screen, str(character.abilities["dex"][1]), self.text_standard)
        self.con_field = so.TextField(screen, "con", self.text_standard)
        self.con_score = so.TextField(screen, str(character.abilities["con"][0]), self.text_standard)
        self.con_bonus_penalty = so.TextField(screen, str(character.abilities["con"][1]), self.text_standard)
        self.int_field = so.TextField(screen, "int", self.text_standard)
        self.int_score = so.TextField(screen, str(character.abilities["int"][0]), self.text_standard)
        self.int_bonus_penalty = so.TextField(screen, str(character.abilities["int"][1]), self.text_standard)
        self.wis_field = so.TextField(screen, "wis", self.text_standard)
        self.wis_score = so.TextField(screen, str(character.abilities["wis"][0]), self.text_standard)
        self.wis_bonus_penalty = so.TextField(screen, str(character.abilities["wis"][1]), self.text_standard)
        self.cha_field = so.TextField(screen, "cha", self.text_standard)
        self.cha_score = so.TextField(screen, str(character.abilities["cha"][0]), self.text_standard)
        self.cha_bonus_penalty = so.TextField(screen, str(character.abilities["cha"][1]), self.text_standard)
        # Array of ability groups for cleaner positioning/drawing in class methods.
        self.ability_groups = ((self.str_field, self.str_score, self.str_bonus_penalty),
                               (self.dex_field, self.dex_score, self.dex_bonus_penalty),
                               (self.con_field, self.con_score, self.con_bonus_penalty),
                               (self.int_field, self.int_score, self.int_bonus_penalty),
                               (self.wis_field, self.wis_score, self.wis_bonus_penalty),
                               (self.cha_field, self.cha_score, self.cha_bonus_penalty))

        # Further ability info elements.
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

        # Position screen title first.
        self.title.text_rect.top, self.title.text_rect.centerx = (self.screen_rect.top + self.spacing_screen_edge,
                                                                  self.screen_rect.centerx)

        # General position attributes for x-axis.
        x_column_0 = self.screen_rect.left + self.spacing_screen_edge
        x_column_1 = self.screen_width * 0.25
        x_column_2 = self.screen_width * 0.5
        x_column_3 = self.screen_width * 0.75

        # Position attribute for first row on y-axis based on screen title object.
        y_row_0 = self.title.text_rect.bottom + self.title_spacing

        # Positioning for basic character info fields group.
        # First row of group.
        self.name_field.text_rect.top, self.name_field.text_rect.left = y_row_0, x_column_0
        self.name_char.text_rect.top, self.name_char.text_rect.left = y_row_0, self.name_field.text_rect.right
        self.xp_field.text_rect.top, self.xp_field.text_rect.left = y_row_0, x_column_3
        self.xp_char.text_rect.top, self.xp_char.text_rect.left = y_row_0, self.xp_field.text_rect.right
        # Position attribute for second row on y-axis based on 'name_field' object.
        y_row_1 = self.name_field.text_rect.bottom
        # Second row of group.
        self.race_field.text_rect.top, self.race_field.text_rect.left = y_row_1, x_column_0
        self.race_char.text_rect.top, self.race_char.text_rect.left = y_row_1, self.race_field.text_rect.right
        self.class_field.text_rect.top, self.class_field.text_rect.left = y_row_1, x_column_1
        self.class_char.text_rect.top, self.class_char.text_rect.left = y_row_1, self.class_field.text_rect.right
        self.level_field.text_rect.top, self.level_field.text_rect.left = y_row_1, x_column_2
        self.level_char.text_rect.top, self.level_char.text_rect.left = y_row_1, self.level_field.text_rect.right
        self.next_lvl_xp_field.text_rect.top, self.next_lvl_xp_field.text_rect.left = y_row_1, x_column_3
        self.next_lvl_xp_char.text_rect.top, self.next_lvl_xp_char.text_rect.left = y_row_1, self.next_lvl_xp_field.text_rect.right

        # Position attribute for row on y-axis for combat info fields group.
        y_row_2 = y_row_1 + self.spacing_screen_edge
        # Group starting on 'x_column_1', 'y_row_2'.
        self.armor_class_field.text_rect.top, self.armor_class_field.text_rect.left = y_row_2, x_column_1
        self.armor_class_char.text_rect.top, self.armor_class_char.text_rect.left = y_row_2, self.armor_class_field.text_rect.right
        self.health_points_field.text_rect.top, self.health_points_field.text_rect.left = y_row_2, x_column_2
        self.health_points_char.text_rect.top, self.health_points_char.text_rect.left = y_row_2, self.health_points_field.text_rect.right
        self.attack_bonus_field.text_rect.top, self.attack_bonus_field.text_rect.left = y_row_2, x_column_3
        self.attack_bonus_char.text_rect.top, self.attack_bonus_char.text_rect.left = y_row_2, self.attack_bonus_field.text_rect.right

        # Ability scores group.
        # Using 'abilities_title' rect for reference and easier positioning.
        group_ref_rect = self.abilities_title.text_rect
        # Group starting on 'x_column_0', 'y_row_2' by positioning 'abilities_title' first. Further elements use separate
        # column system (ab_colum_x) specific to ability scores as assigned further down.
        group_ref_rect.top, group_ref_rect.left = y_row_2, x_column_0
        # Position attributes for ability scores.
        y_row_3 = group_ref_rect.bottom
        ab_column_0 = group_ref_rect.left
        ab_column_1 = ab_column_0 + group_ref_rect.width
        ab_column_2 = ab_column_1 + group_ref_rect.width
        # Ability scores positioning using array 'ability_groups'.
        for group in self.ability_groups:
            group[0].text_rect.top, group[0].text_rect.left = y_row_3, ab_column_0
            group[1].text_rect.top, group[1].text_rect.right = y_row_3, ab_column_1
            group[2].text_rect.top, group[2].text_rect.right = y_row_3, ab_column_2
            # Move row position down for next group.
            y_row_3 = group[0].text_rect.bottom
        # Reset 'y_row_3' to starting position.
        y_row_3 = group_ref_rect.bottom

    def show_character_sheet_screen(self):
        """Draw character sheet elements on screen."""
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
        # Draw combat info fields.
        self.armor_class_field.draw_text()
        self.armor_class_char.draw_text()
        self.health_points_field.draw_text()
        self.attack_bonus_field.draw_text()
        self.health_points_char.draw_text()
        self.attack_bonus_char.draw_text()
        # Draw ability scores fields.
        self.abilities_title.draw_text()
        for group in self.ability_groups:
            group[0].draw_text()
            group[1].draw_text()
            group[2].draw_text()

    def format_ability_bonus_penalty(self):
        """Format output for 0/positive values of ability score's bonus and penalty. Remove value if it is '0' or add '+'
        if value is positive."""
        for group in self.ability_groups:
            if int(group[2].text) == 0:
                group[2].text = ""
            elif int(group[2].text) > 0:
                group[2].text = "+" + group[2].text
