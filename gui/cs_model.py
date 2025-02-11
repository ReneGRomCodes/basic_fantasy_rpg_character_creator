import gui.screen_objects as so
"""Helper class to organize and access character sheet objects as attributes."""


class CharacterSheet:
    """A class to store and manage character sheet elements."""

    def __init__(self, screen, character, gui_elements):
        """Initialize the CharacterSheet object with elements."""

        # Assign character object to attribute.
        self.character = character

        # Assign screen rect attributes.
        self.screen = screen
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

        # Abilities info elements.
        # Suffixes '_score' and '_bonus_penalty' indicate objects with values from the 'Character' class object.
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
        # Format ability bonus/penalty output. See method docstring for details.
        self.format_ability_bonus_penalty()

        # Saving throws info elements.
        self.saving_throws_title = so.TextField(screen, "SAVING THROWS", self.text_standard)
        self.saving_throw_0_field = so.TextField(screen, "Death Ray or Poison:", self.text_standard)
        self.saving_throw_0_score = so.TextField(screen, str(character.saving_throws["Death Ray or Poison"]), self.text_standard)
        self.saving_throw_1_field = so.TextField(screen, "Magic Wands:", self.text_standard)
        self.saving_throw_1_score = so.TextField(screen, str(character.saving_throws["Magic Wands"]), self.text_standard)
        self.saving_throw_2_field = so.TextField(screen, "Paralysis or Petrify:", self.text_standard)
        self.saving_throw_2_score = so.TextField(screen, str(character.saving_throws["Paralysis or Petrify"]), self.text_standard)
        self.saving_throw_3_field = so.TextField(screen, "Dragon Breath:", self.text_standard)
        self.saving_throw_3_score = so.TextField(screen, str(character.saving_throws["Dragon Breath"]), self.text_standard)
        self.saving_throw_4_field = so.TextField(screen, "Spells:", self.text_standard)
        self.saving_throw_4_score = so.TextField(screen, str(character.saving_throws["Spells"]), self.text_standard)
        # Array of saving throws groups for cleaner positioning/drawing in class methods.
        self.saving_throw_groups = ((self.saving_throw_0_field, self.saving_throw_0_score),
                                    (self.saving_throw_1_field, self.saving_throw_1_score),
                                    (self.saving_throw_2_field, self.saving_throw_2_score),
                                    (self.saving_throw_3_field, self.saving_throw_3_score),
                                    (self.saving_throw_4_field, self.saving_throw_4_score))
        # Format saving throw score output. See method docstring for details.
        self.format_saving_throw_scores()

        # Special abilities info elements.
        self.special_abilities_title = so.TextField(screen, "SPECIAL ABILITIES", self.text_standard)
        # 'special_ability' object has its text dynamically modified in method 'draw_format_dynamic_field()' to account
        # for the fact that number of abilities in 'character.specials' is unpredictable at the start of the character
        # creation. 'draw_format_dynamic_field()' is called from 'show_character_sheet_screen()'.
        self.special_ability = so.TextField(screen, "", self.text_standard, multi_line=True, image_width=self.screen_width / 3)
        # List to store y-position values for each state of 'self.special_ability' as created in function
        # 'initialize_character_sheet()' in 'main_functions.py'.
        self.specials_pos_y_list = []

        # Spell elements for classes 'Magic-User', 'Cleric' or combination classes.
        self.spells_title = so.TextField(screen, "SPELLS", self.text_standard)
        self.spell = so.TextField(screen, str(character.spells), self.text_standard)

        # Class specials elements.
        self.class_specials_title = so.TextField(screen, character.class_name.upper() + " SPECIALS", self.text_standard)
        # 'class_special' object has its text dynamically modified in method 'draw_format_dynamic_field()' to account
        # for the fact that number of specials in 'character.class_specials' is unpredictable at the start of the
        # character creation. 'draw_format_dynamic_field()' is called from 'show_character_sheet_screen()'.
        self.class_special = so.TextField(screen, "", self.text_standard)
        # List to store y-position values for each state of 'self.class_special' as created in function
        # 'initialize_character_sheet()' in 'main_functions.py'.
        self.class_special_pos_y_list = []
        # TODO ignore me... I am just a marker so the idiot coding this knows where he is at right now.
        # Inventory elements.
        self.money = so.TextField(screen, "Money:", self.text_standard)
        self.carrying_capacity = so.TextField(screen, "Carrying Capacity:", self.text_standard)
        self.weight_carried = so.TextField(screen, "Weight Carried:", self.text_standard)
        self.inventory = so.TextField(screen, "Inventory:", self.text_standard)

        # Weapons and armor elements.
        self.weapons = so.TextField(screen, "Weapons:", self.text_standard)
        self.armor = so.TextField(screen, "Armor:", self.text_standard)
        self.armor_ac = so.TextField(screen, "AC:", self.text_standard) # Armor class for worn armor only, not including
                                                                        # base armor class for character.


    """Main method to show character sheet. Called from main loop in 'main.py'."""

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
        # Draw saving throw fields.
        self.saving_throws_title.draw_text()
        for group in self.saving_throw_groups:
            group[0].draw_text()
            group[1].draw_text()
        # Draw special abilities fields.
        self.special_abilities_title.draw_text()
        self.draw_format_dynamic_field(self.special_ability, self.character.specials, self.special_abilities_title,
                                       self.specials_pos_y_list, text_prefix=" - ")
        # Draw spells fields only if character is magic based, i.e. Magic-User, Cleric or combination class.
        if self.character.spells:
            self.spells_title.draw_text()
            self.spell.draw_text()
        # Draw class specials fields only if character is Thief, Cleric or Thief/Magic-User.
        if self.character.class_specials:
            self.class_specials_title.draw_text()
            self.draw_format_dynamic_field(self.class_special, self.character.class_specials, self.class_specials_title,
                                       self.class_special_pos_y_list)


    """Positioning methods for use in 'initialize_character_sheet()' function in 'core/main_functions.py' when the final
    character sheet is initialized."""

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

        # Saving throws group.
        # Using 'saving_throws_title' rect for reference and easier positioning.
        group_ref_rect = self.saving_throws_title.text_rect
        # Group starting on 'x_column_1', 'y_row_3' by positioning 'saving_throws_title' first.
        group_ref_rect.top, group_ref_rect.left = y_row_3, x_column_1
        # Position attribute for saving throw scores.
        y_row_4 = group_ref_rect.bottom
        for group in self.saving_throw_groups:
            group[0].text_rect.top, group[0].text_rect.left = y_row_4, x_column_1
            group[1].text_rect.top, group[1].text_rect.right = y_row_4, x_column_2 - self.screen_width / 16
            # Move row position down for next group.
            y_row_4 = group[0].text_rect.bottom

        # Special abilities group.
        # Only the group title object is positioned here, the other fields are handled by 'get_position_special_abilities()'
        # method.
        # Group starting on 'x_column_2', 'y_row_3'.
        self.special_abilities_title.text_rect.top, self.special_abilities_title.text_rect.left = y_row_3, x_column_2

        # Position 'y_row_5' at the center line of the screen.
        y_row_5 = self.screen_height / 2

        # Spells group.
        # Using 'spells' rect for reference and easier positioning.
        group_ref_rect = self.spells_title.text_rect
        # Group starting on 'x_column_2', 'y_row_5'
        group_ref_rect.top, group_ref_rect.left = y_row_5, x_column_2
        self.spell.text_rect.top, self.spell.text_rect.left = group_ref_rect.bottom, x_column_2

        # Class specials group.
        # Using 'class_specials_title' rect for reference and easier positioning.
        group_ref_rect = self.class_specials_title.text_rect
        # Group starting on 'x_column_3, 'y_row_5'
        group_ref_rect.top, group_ref_rect.left = y_row_5, x_column_3

    def get_position_dynamic_field(self, field_object, char_attr_list, anchor, text_prefix=""):
        """
        Create, populate and return list 'pos_y_list' with y-positions for each state of 'field_object'.
        ARGS:
            field_object: instance of class 'TextField' to be dynamically modified using values from 'char_attr_list'.
            char_attr_list: attribute of type LIST or TUPLE from instance of 'Character' containing strings to be
                            dynamically added to 'field_object'.
            anchor: anchor object for thematic group that 'field_object' belongs to. Used for positioning along x-axis.
            text_prefix: string with prefix to be added to 'field_object.text' together with 'char_attr_item', i.e. " - ".
                         Default is "".
        RETURNS:
            pos_y_list: list with y-positions for use in positioning of 'field_object' in method 'draw_format_dynamic_field()'
        """
        # Use 'anchor' rect as reference for starting row.
        pos_y = anchor.text_rect.bottom
        # Create list to be returned.
        pos_y_list = []

        for index, char_attr_item in enumerate(char_attr_list):
            # Assign text to and expand 'field_object.text', update 'field_object.text_image' and get new rect.
            field_object.text = text_prefix + char_attr_item
            field_object.render_new_text_image()

            # Append default position for first 'field_object' to list.
            if index == 0:
                pos_y_list.append(pos_y)
            # Calculate and append new 'pos_y' in subsequent iterations.
            else:
                pos_y = pos_y_list[index - 1] + pos_y_list[index]
                pos_y_list[index] = pos_y

            # Append height of current 'text_rect' to list for use in following iteration where it will then be overwritten
            # with the newly calculated 'pos_y'.
            pos_y_list.append(field_object.text_rect.height)

            # Create object with default values to 'hard reset' 'field_object'. Quick and dirty fix for 'field_object'
            # refusing to be reset any other way if 'multi_line' is 'True'.
            if field_object.multi_line:
                default_object = so.TextField(self.screen, "", self.text_standard, multi_line=True, image_width=self.screen_width / 3)
                field_object = default_object

        return pos_y_list


    """Helper methods for use within this class."""

    def format_ability_bonus_penalty(self):
        """Format output for 0/positive values of ability score's bonus and penalty. Remove value if it is '0' or add '+'
        if value is positive."""
        for group in self.ability_groups:
            if int(group[2].text) == 0:
                group[2].text = ""
            elif int(group[2].text) > 0:
                group[2].text = "+" + group[2].text

            # Update 'group[2].text_image' and get new rect.
            group[2].render_new_text_image()

    def format_saving_throw_scores(self):
        """Format output for saving throws by adding a '+' to the score."""
        for group in self.saving_throw_groups:
            group[1].text = "+" + group[1].text

            # Update 'group[1].text_image' and get new rect.
            group[1].render_new_text_image()

    def draw_format_dynamic_field(self, field_object, char_attr_list, anchor, pos_y_list, text_prefix=""):
        """
        Dynamically change 'text' attribute for 'field_object' based on list/tuple 'char_attr_list', and draw it on
        screen.
        ARGS:
            field_object: instance of class 'TextField' to be dynamically modified using values from 'char_attr_list'.
            char_attr_list: attribute of type LIST or TUPLE from instance of 'Character' containing strings to be
                            dynamically added to 'field_object'.
            anchor: anchor object for thematic group that 'field_object' belongs to. Used for positioning along x-axis.
            pos_y_list: list containing y-positions for 'field_object' as populated by function 'get_position_dynamic_field'
            text_prefix: string with prefix to be added to 'field_object.text' together with 'char_attr_item', i.e. " - ".
                         Default is "".
        """
        for index, char_attr_item in enumerate(char_attr_list):
            # Assign text to and expand 'field_object.text', update 'field_object.text_image' and get new rect.
            field_object.text = text_prefix + char_attr_item
            field_object.render_new_text_image()

            # Position and draw 'field_object'.
            field_object.text_rect.top, field_object.text_rect.left = pos_y_list[index], anchor.text_rect.left
            field_object.draw_text()
