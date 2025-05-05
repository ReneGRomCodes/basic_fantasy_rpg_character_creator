import pygame
import gui.screen_objects as so
from core.character_model import Character
from gui.screen_objects import TextField
from gui.ui_helpers import draw_screen_title

"""Helper class to organize and access character sheet objects as attributes."""


class CharacterSheet:
    """A class to store and manage character sheet elements."""

    def __init__(self, screen, character: Character, gui_elements: dict) -> None:
        """Initialize the CharacterSheet object with elements.
        ARGS:
            screen: PyGame window.
            character: Instance of class 'Character'.
            gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        """
        # Assign character object to attribute.
        self.character: Character = character

        # Assign screen rect attributes.
        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.screen_height: int = self.screen_rect.height
        self.screen_width: int = self.screen_rect.width

        # Size and spacing variables from dict 'gui_elements' that are calculated based on screen size for scalability.
        self.gui_elements: dict = gui_elements
        self.text_standard: int = gui_elements["text_standard"]
        self.text_large: int = gui_elements["text_large"]
        self.text_medium: int = gui_elements["text_medium"]
        self.text_small: int = gui_elements["text_small"]
        self.title_spacing: int = gui_elements["menu_title_spacing"]
        self.default_spacing: int = gui_elements["default_edge_spacing"]


        # Following character sheet elements are paired, with attributes having no suffix representing the field label
        # which serves as 'anchor' object for positioning, while '_char' suffix represents the value from the 'Character'
        # class object.

        # Initialize character sheet elements.
        self.title: TextField = so.TextField(screen, "- CHARACTER SHEET -", self.text_medium)

        # Character sheet base info elements.
        self.name: TextField = so.TextField(screen, "Name: ", self.text_standard)  # ANCHOR
        self.name_char: TextField = so.TextField(screen, character.name, self.text_standard)
        self.xp: TextField = so.TextField(screen, "XP: ", self.text_standard)  # ANCHOR
        self.xp_char: TextField = so.TextField(screen, str(character.xp), self.text_standard)
        self.race: TextField = so.TextField(screen, "Race: ", self.text_standard)  # ANCHOR
        self.race_char: TextField = so.TextField(screen, character.race_name, self.text_standard)
        self.cls: TextField = so.TextField(screen, "Class: ", self.text_standard)  # ANCHOR
        self.cls_char: TextField = so.TextField(screen, character.class_name, self.text_standard)
        self.level: TextField = so.TextField(screen, "Level: ", self.text_standard)  # ANCHOR
        self.level_char: TextField = so.TextField(screen, str(character.level), self.text_standard)
        self.next_lvl_xp: TextField = so.TextField(screen, "XP to next level: ", self.text_standard)  # ANCHOR
        self.next_lvl_xp_char: TextField = so.TextField(screen, str(character.next_level_xp), self.text_standard)

        # Combat related info elements.
        self.armor_class: TextField = so.TextField(screen, "Armor Class: ", self.text_standard)  # ANCHOR
        self.armor_class_char: TextField = so.TextField(screen, str(character.armor_class), self.text_standard)
        self.health_points: TextField = so.TextField(screen, "Health Points: ", self.text_standard)  # ANCHOR
        self.health_points_char: TextField = so.TextField(screen, str(character.hp), self.text_standard)
        self.attack_bonus: TextField = so.TextField(screen, "Attack Bonus: +", self.text_standard)  # ANCHOR
        self.attack_bonus_char: TextField = so.TextField(screen, str(character.attack_bonus), self.text_standard)

        # Abilities info elements.
        # Suffixes '_score' and '_bonus_penalty' indicate objects with values from the 'Character' class object.
        self.abilities: TextField = so.TextField(screen, "ABILITIES", self.text_standard)  # ANCHOR
        self.str_label: TextField = so.TextField(screen, "str", self.text_standard)
        self.str_score: TextField = so.TextField(screen, str(character.abilities["str"][0]), self.text_standard)
        self.str_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["str"][1]), self.text_standard)
        self.dex_label: TextField = so.TextField(screen, "dex", self.text_standard)
        self.dex_score: TextField = so.TextField(screen, str(character.abilities["dex"][0]), self.text_standard)
        self.dex_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["dex"][1]), self.text_standard)
        self.con_label: TextField = so.TextField(screen, "con", self.text_standard)
        self.con_score: TextField = so.TextField(screen, str(character.abilities["con"][0]), self.text_standard)
        self.con_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["con"][1]), self.text_standard)
        self.int_label: TextField = so.TextField(screen, "int", self.text_standard)
        self.int_score: TextField = so.TextField(screen, str(character.abilities["int"][0]), self.text_standard)
        self.int_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["int"][1]), self.text_standard)
        self.wis_label: TextField = so.TextField(screen, "wis", self.text_standard)
        self.wis_score: TextField = so.TextField(screen, str(character.abilities["wis"][0]), self.text_standard)
        self.wis_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["wis"][1]), self.text_standard)
        self.cha_label: TextField = so.TextField(screen, "cha", self.text_standard)
        self.cha_score: TextField = so.TextField(screen, str(character.abilities["cha"][0]), self.text_standard)
        self.cha_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["cha"][1]), self.text_standard)
        # Array of ability groups for cleaner positioning/drawing in class methods.
        self.ability_groups: tuple[tuple[TextField, TextField, TextField], ...] = (
            (self.str_label, self.str_score, self.str_bonus_penalty),
            (self.dex_label, self.dex_score, self.dex_bonus_penalty),
            (self.con_label, self.con_score, self.con_bonus_penalty),
            (self.int_label, self.int_score, self.int_bonus_penalty),
            (self.wis_label, self.wis_score, self.wis_bonus_penalty),
            (self.cha_label, self.cha_score, self.cha_bonus_penalty),
        )
        # Format ability bonus/penalty output. See method docstring for details.
        self.format_ability_bonus_penalty()

        # Saving throws info elements.
        self.saving_throws: TextField = so.TextField(screen, "SAVING THROWS", self.text_standard)  # ANCHOR
        self.saving_throw_0_field: TextField = so.TextField(screen, "Death Ray or Poison:", self.text_standard)
        self.saving_throw_0_score: TextField = so.TextField(screen, str(character.saving_throws["Death Ray or Poison"]), self.text_standard)
        self.saving_throw_1_field: TextField = so.TextField(screen, "Magic Wands:", self.text_standard)
        self.saving_throw_1_score: TextField = so.TextField(screen, str(character.saving_throws["Magic Wands"]), self.text_standard)
        self.saving_throw_2_field: TextField = so.TextField(screen, "Paralysis or Petrify:", self.text_standard)
        self.saving_throw_2_score: TextField = so.TextField(screen, str(character.saving_throws["Paralysis or Petrify"]), self.text_standard)
        self.saving_throw_3_field: TextField = so.TextField(screen, "Dragon Breath:", self.text_standard)
        self.saving_throw_3_score: TextField = so.TextField(screen, str(character.saving_throws["Dragon Breath"]), self.text_standard)
        self.saving_throw_4_field: TextField = so.TextField(screen, "Spells:", self.text_standard)
        self.saving_throw_4_score: TextField = so.TextField(screen, str(character.saving_throws["Spells"]), self.text_standard)
        # Array of saving throws groups for cleaner positioning/drawing in class methods.
        self.saving_throw_groups: tuple[tuple[TextField, TextField], ...] = (
            (self.saving_throw_0_field, self.saving_throw_0_score),
            (self.saving_throw_1_field, self.saving_throw_1_score),
            (self.saving_throw_2_field, self.saving_throw_2_score),
            (self.saving_throw_3_field, self.saving_throw_3_score),
            (self.saving_throw_4_field, self.saving_throw_4_score),
        )
        # Format saving throw score output. See method docstring for details.
        self.format_saving_throw_scores()

        # Special abilities info elements.
        self.special_abilities: TextField = so.TextField(screen, "SPECIAL ABILITIES", self.text_standard)  # ANCHOR
        # 'special_ability' object has its text dynamically modified in method 'draw_format_dynamic_field()' to account
        # for the fact that number of abilities in 'character.specials' is unpredictable at the start of the character
        # creation.
        self.special_ability: TextField = so.TextField(screen, "", self.text_standard, multi_line=True,
                                                       surface_width=int(self.screen_width / 3))
        # Create list to store y-position values for each state of 'self.special_ability'.
        self.specials_pos_y_list: list[int] = (
            self.get_position_dynamic_field(self.special_ability, self.character.specials, self.special_abilities,
                                            text_prefix=" - "))

        # Spell elements for classes 'Magic-User', 'Cleric' or combination classes.
        self.spells: TextField = so.TextField(screen, "SPELLS", self.text_standard)  # ANCHOR
        self.spell: TextField = so.TextField(screen, str(character.spells), self.text_standard)

        # Class specials elements.
        self.class_specials: TextField = so.TextField(screen, character.class_name.upper() + " SPECIALS",
                                                            self.text_standard)  # ANCHOR
        # 'class_special' object has its text and position dynamically modified in method 'draw_format_dynamic_field()'
        # to account for the fact that number of specials in 'character.class_specials' is unpredictable at the start of
        # the character creation.
        self.class_special: TextField = so.TextField(screen, "", self.text_standard)
        # Create list to store y-position values for each state of 'self.class_special'.
        self.class_special_pos_y_list: list[int] =(
            self.get_position_dynamic_field(self.class_special, self.character.class_specials, self.class_specials))

        # TODO ignore me... I am just a marker so the idiot coding this knows where he is at right now.
        self.TEMP_RETURN_TO_MAIN_MESSAGE: TextField = so.TextField(
            screen, "WORK IN PROGRESS - Press any key to return to main menu.", self.text_large, bg_color="red")
        # TODO ignore me... I am just a marker so the idiot coding this knows where he is at right now.

        # Inventory elements.
        self.money: TextField = so.TextField(screen, "Money:", self.text_standard)  # ANCHOR
        self.carrying_capacity: TextField = so.TextField(screen, "Carrying Capacity:", self.text_standard)  # ANCHOR
        self.weight_carried: TextField = so.TextField(screen, "Weight Carried:", self.text_standard)  # ANCHOR
        self.inventory: TextField = so.TextField(screen, "Inventory:", self.text_standard)  # ANCHOR

        # Weapons and armor elements.
        self.weapons: TextField = so.TextField(screen, "Weapons:", self.text_standard)  # ANCHOR
        self.armor: TextField = so.TextField(screen, "Armor:", self.text_standard)  # ANCHOR
        self.armor_ac: TextField = so.TextField(screen, "AC:", self.text_standard) # Armor class for worn armor only, not including
                                                                        # base armor class for character.  # ANCHOR

        # Screen grid for positioning of anchor elements. Further elements that belong to anchors are then positioned
        # via helper methods.
        self.screen_grid_array: tuple[tuple, ...] = (
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, self.name, False, self.xp, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False),
        )
        # Set following attribute to 'True' to show grid on screen for layout design.
        self.show_grid = True


    """Main method to show character sheet. Called from main loop in 'main.py'."""

    def show_character_sheet_screen(self) -> None:
        """Draw character sheet elements on screen."""
        # TODO Draw temporary 'return to main' message.
        self.TEMP_RETURN_TO_MAIN_MESSAGE.draw_text()

        # Draw layout grid on screen if 'self.show_grid' is set to 'True'.
        if self.show_grid:
            self.draw_grid()

        # Draw screen title.
        draw_screen_title(self.screen, self.title, self.gui_elements)

        # Draw character sheet elements.
        # Basic character info fields.
        self.name.draw_text()
        self.xp.draw_text()
        self.race.draw_text()
        self.cls.draw_text()
        self.level.draw_text()
        self.next_lvl_xp.draw_text()
        # Draw combat info fields.
        self.armor_class.draw_text()
        self.health_points.draw_text()
        self.attack_bonus.draw_text()


    """Positioning method for use in 'initialize_character_sheet()' function in 'core/state_manager.py' when the final
    character sheet is initialized."""

    def position_cs_elements(self) -> None:
        """Position instances of class 'TextField' on screen."""
        self.position_anchors()


    """Helper methods for use within this class."""

    def position_anchors(self) -> None:
        """Assign screen positions to elements in 'self.screen_grid_array' based on their grid index.
        Elements can then be used as reference objects to position other related elements."""
        grid_cell_width: int = int(self.screen_width / len(self.screen_grid_array[0]))
        grid_cell_height: int = int(self.screen_height / len(self.screen_grid_array))

        for row_index, row in enumerate(self.screen_grid_array):
            for element_index, element in enumerate(row):
                if element:
                    element.text_rect.top = self.screen_rect.top + (row_index * grid_cell_height)
                    element.text_rect.left = self.screen_rect.left + (element_index * grid_cell_width)


    def format_ability_bonus_penalty(self) -> None:
        """Format output for 0/positive values of ability score's bonus and penalty. Remove value if it is '0' or add '+'
        if value is positive."""
        for group in self.ability_groups:
            if int(group[2].text) == 0:
                group[2].text = ""
            elif int(group[2].text) > 0:
                group[2].text = "+" + group[2].text

            # Update 'group[2].text_surface' and get new rect.
            group[2].render_new_text_surface()

    def format_saving_throw_scores(self) -> None:
        """Format output for saving throws by adding a '+' to the score."""
        for group in self.saving_throw_groups:
            group[1].text = "+" + group[1].text

            # Update 'group[1].text_surface' and get new rect.
            group[1].render_new_text_surface()

    def get_position_dynamic_field(self, field_object: TextField, char_attr_list: list[str] | tuple[str, ...],
                                   anchor: TextField, text_prefix: str = "") -> list[int]:
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
        pos_y_list: list[int] = []

        for index, char_attr_item in enumerate(char_attr_list):
            # Assign text to and expand 'field_object.text', update 'field_object.text_surface' and get new rect.
            field_object.text = text_prefix + char_attr_item
            field_object.render_new_text_surface()

            # Append default position for first 'field_object' to list.
            if index == 0:
                pos_y_list.append(pos_y)
            # Calculate and append new 'pos_y' in subsequent iterations.
            else:
                pos_y: int = pos_y_list[index - 1] + pos_y_list[index]
                pos_y_list[index] = pos_y

            # Append height of current 'text_rect' to list for use in following iteration where it will then be overwritten
            # with the newly calculated 'pos_y'.
            pos_y_list.append(field_object.text_rect.height)

            # Create object with default values to 'hard reset' 'field_object'. Quick and dirty fix for 'field_object'
            # refusing to be reset any other way if 'multi_line' is 'True'.
            if field_object.multi_line:
                default_object: TextField = so.TextField(self.screen, "", self.text_standard, multi_line=True,
                                              surface_width=int(self.screen_width / 3))
                field_object: TextField = default_object

        return pos_y_list

    def draw_format_dynamic_field(self, field_object: TextField, char_attr_list: list[str] | tuple[str, ...],
                                  anchor: TextField, pos_y_list: list[int], text_prefix: str = "") -> None:
        """
        Dynamically change 'text' attribute for 'field_object' based on list/tuple 'char_attr_list', and position/draw
        it on screen.
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
            # Assign text to and expand 'field_object.text', update 'field_object.text_surface' and get new rect.
            field_object.text = text_prefix + char_attr_item
            field_object.render_new_text_surface()

            # Position and draw 'field_object'.
            field_object.text_rect.top, field_object.text_rect.left = pos_y_list[index], anchor.text_rect.left
            field_object.draw_text()

    def draw_grid(self) -> None:
        """Draw layout grid on screen based on size of 'self.screen_grid_array'.
        NOTE: 'self.show_grid' has to be set to 'True' for the grid to appear on screen."""
        grid_cell_width: int = int(self.screen_width / len(self.screen_grid_array[0]))
        grid_cell_height: int = int(self.screen_height / len(self.screen_grid_array))
        grid_pos: list[int] = [0, 0]

        # Draw lines for each row and column on screen.
        for row in self.screen_grid_array:
            pygame.draw.line(self.screen, "black", tuple(grid_pos), (self.screen_rect.right, grid_pos[1]))

            for column in row:
                pygame.draw.line(self.screen, "black", tuple(grid_pos), (grid_pos[0], self.screen_rect.bottom))
                # Set new x-position for next column.
                grid_pos[0] += grid_cell_width

            # Reset x-position to '0' and set new y-position for next row.
            grid_pos[0] = 0
            grid_pos[1] += int(grid_cell_height)
