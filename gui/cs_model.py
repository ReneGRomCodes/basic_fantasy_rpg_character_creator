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

        # Initialize character sheet elements.
        self.title: TextField = so.TextField(screen, "- CHARACTER SHEET -", self.text_medium)

        """
        Character sheet elements are positioned using a grid-based system. Each 'anchor' field (usually just the field
        label) is placed into 'self.screen_grid_array' at the bottom of '__init__()', which drives the initial layout
        logic.

        Any related elements (like '_char', '_score', etc.) are positioned relative to their anchor using section-specific
        methods. These value elements are grouped into arrays used by those methods to handle layout based on the anchor's
        grid position.

        NOTE: Each section of the screen may handle positioning a bit differently. '# ANCHOR' comments indicate the anchor
        object, but that object isn't usually part of the group array itself.
        TL;DR: if you're tweaking layout logic, check if the anchor is included in the group array or not, and peek at
        the related method to see how it's doing its thing ;)
        """

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
        self.money: TextField = so.TextField(screen, "Money: ", self.text_standard)  # ANCHOR
        self.money_char: so.TextField = so.TextField(screen, str(self.character.money) + " gold pieces", self.text_standard)
        # Combat related basic info elements.
        self.armor_class: TextField = so.TextField(screen, "Armor Class: ", self.text_standard)  # ANCHOR
        self.armor_class_char: TextField = so.TextField(screen, str(character.armor_class), self.text_standard)
        self.health_points: TextField = so.TextField(screen, "Health Points: ", self.text_standard)  # ANCHOR
        self.health_points_char: TextField = so.TextField(screen, str(character.hp), self.text_standard)
        self.attack_bonus: TextField = so.TextField(screen, "Attack Bonus: +", self.text_standard)  # ANCHOR
        self.attack_bonus_char: TextField = so.TextField(screen, str(character.attack_bonus), self.text_standard)
        # Array of basic info and combat info groups for cleaner positioning/drawing in class methods.
        self.basic_info_groups: tuple[tuple[TextField, TextField], ...] = (
            (self.name, self.name_char),
            (self.xp, self.xp_char),
            (self.race, self.race_char),
            (self.cls, self.cls_char),
            (self.level, self.level_char),
            (self.next_lvl_xp, self.next_lvl_xp_char),
            (self.money, self.money_char),
            (self.armor_class, self.armor_class_char),
            (self.health_points, self.health_points_char),
            (self.attack_bonus, self.attack_bonus_char),
        )

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

        # Saving throws info elements.
        self.saving_throws: TextField = so.TextField(screen, "SAVING THROWS", self.text_standard)  # ANCHOR
        self.saving_throw_0_label: TextField = so.TextField(screen, "Death Ray or Poison:", self.text_standard)
        self.saving_throw_0_score: TextField = so.TextField(screen, str(character.saving_throws["Death Ray or Poison"]), self.text_standard)
        self.saving_throw_1_label: TextField = so.TextField(screen, "Magic Wands:", self.text_standard)
        self.saving_throw_1_score: TextField = so.TextField(screen, str(character.saving_throws["Magic Wands"]), self.text_standard)
        self.saving_throw_2_label: TextField = so.TextField(screen, "Paralysis or Petrify:", self.text_standard)
        self.saving_throw_2_score: TextField = so.TextField(screen, str(character.saving_throws["Paralysis or Petrify"]), self.text_standard)
        self.saving_throw_3_label: TextField = so.TextField(screen, "Dragon Breath:", self.text_standard)
        self.saving_throw_3_score: TextField = so.TextField(screen, str(character.saving_throws["Dragon Breath"]), self.text_standard)
        self.saving_throw_4_label: TextField = so.TextField(screen, "Spells:", self.text_standard)
        self.saving_throw_4_score: TextField = so.TextField(screen, str(character.saving_throws["Spells"]), self.text_standard)
        # Array of saving throws groups for cleaner positioning/drawing in class methods.
        self.saving_throw_groups: tuple[tuple[TextField, TextField], ...] = (
            (self.saving_throw_0_label, self.saving_throw_0_score),
            (self.saving_throw_1_label, self.saving_throw_1_score),
            (self.saving_throw_2_label, self.saving_throw_2_score),
            (self.saving_throw_3_label, self.saving_throw_3_score),
            (self.saving_throw_4_label, self.saving_throw_4_score),
        )

        # Special abilities info elements.
        self.special_abilities: TextField = so.TextField(screen, "SPECIAL ABILITIES", self.text_standard)  # ANCHOR
        # 'special_ability' object has its text dynamically modified in method 'draw_format_dynamic_field()' to account
        # for the fact that number of abilities in 'character.specials' is unpredictable at the start of the character
        # creation.
        self.special_ability: TextField = so.TextField(screen, "", self.text_standard, multi_line=True,
                                                       surface_width=int(self.screen_width / 3))
        # Create empty list to store y-position values for each state of 'self.special_ability'.
        self.specials_pos_y_list: list[int] = []

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
        # Create empty list to store y-position values for each state of 'self.class_special'.
        self.class_special_pos_y_list: list[int] = []

        # Weight/carrying capacity elements.
        unit: str = " lbs"
        self.carrying_cap: TextField = so.TextField(screen, "CARRYING CAPACITY", self.text_standard)  # ANCHOR
        self.carrying_cap_light_label: TextField = so.TextField(screen, "Light Load:", self.text_standard)
        self.carrying_cap_light_char: TextField = so.TextField(screen, str(self.character.carrying_capacity["Light Load"]) + unit,
                                                               self.text_standard)
        self.carrying_cap_heavy_label: TextField = so.TextField(screen, "Heavy Load:", self.text_standard)
        self.carrying_cap_heavy_char: TextField = so.TextField(screen, str(self.character.carrying_capacity["Heavy Load"]) + unit,
                                                               self.text_standard)
        self.weight_carried_label: TextField = so.TextField(screen, "Weight Carried:", self.text_standard)
        self.weight_carried_char: TextField = so.TextField(screen, str(self.character.weight_carried) + unit, self.text_standard)
        # Array of weight/carrying capacity groups for cleaner positioning/drawing in class methods.
        self.weight_group: tuple[tuple[TextField, TextField], ...] = (
            (self.carrying_cap_light_label, self.carrying_cap_light_char),
            (self.carrying_cap_heavy_label, self.carrying_cap_heavy_char),
            (self.weight_carried_label, self.weight_carried_char),
        )

        # Inventory
        self.inventory: TextField = so.TextField(screen, "Inventory: ", self.text_standard)  # ANCHOR

        # Weapons and armor elements.
        self.weapons: TextField = so.TextField(screen, "Weapons: ", self.text_standard)  # ANCHOR
        self.armor: TextField = so.TextField(screen, "Armor: ", self.text_standard)  # ANCHOR
        self.armor_ac: TextField = so.TextField(screen, "AC: ", self.text_standard) # Armor class for worn armor only, not including
                                                                        # base armor class for character.  # ANCHOR

        """
        16x24 screen grid for positioning of anchor elements. Further elements that belong to anchors are then positioned
        dynamically via helper methods if value elements are added to their corresponding group array above.
        """
        # Set following attribute to 'True' to show grid on screen for layout design.
        self.show_grid = True

        # Assign attributes to shorter variables for use in 'self.screen_grid_array' to allow for better readability.
        name, xp, race, cls, level, nxtxp, money, arcls, hp, atbns, ablts, svgth, spabl, spls, clssp, crcap = (
            self.name, self.xp, self.race, self.cls, self.level, self.next_lvl_xp, self.money, self.armor_class,
            self.health_points, self.attack_bonus, self.abilities, self.saving_throws, self.special_abilities, self.spells,
            self.class_specials, self.carrying_cap)

        self.screen_grid_array: tuple[tuple[False | TextField, ...], ...] = (
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, name , False, xp   , False, race , False, cls  , False, level, False, nxtxp, False, False, False, False),
            (False, arcls, False, hp   , False, atbns, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, ablts, False, False, False, svgth, False, False, False, False, spabl, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, money, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, crcap, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, spls , False, False, False, clssp, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
        )

        # TODO Temporary 'return to main' message.
        self.TEMP_RETURN_TO_MAIN_MESSAGE: TextField = so.TextField(
            screen, "WORK IN PROGRESS - Press any key to return to main menu.", self.text_large, bg_color="red")


    """Main method to show character sheet. Called from function 'character_sheet_state_manager()' in
    'core/state_manager.py'."""

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
        self.draw_basic_info()
        self.draw_ability_scores()
        self.draw_saving_throws()
        self.draw_special_abilities()
        self.draw_weight_carrying_capacity()

        # Draw 'spells' section if character is of a magic related class (Magic-User, Cleric, etc.).
        if self.character.spells:
            self.draw_spells()
        # Draw 'class specials' section if character class has special abilities.
        if self.character.class_specials:
            self.draw_class_specials()


    """Main positioning method for use in 'character_sheet_state_manager()' function in 'core/state_manager.py' when the
    final character sheet is initialized."""

    def position_cs_elements(self) -> None:
        """Position instances of class 'TextField' on screen."""
        # Position anchor objects based on entry in 'self.screen_grid_array'.
        self.position_anchors()

        # Position further elements.
        self.position_basic_info()
        self.position_ability_scores()
        self.position_saving_throws()
        self.position_weight_carrying_capacity()

        # Get lists for dynamically positioned elements.
        self.specials_pos_y_list: list[int] = self.get_position_dynamic_field(self.special_ability, self.character.specials,
                                                                              self.special_abilities, text_prefix=" - ")
        self.class_special_pos_y_list: list[int] = self.get_position_dynamic_field(self.class_special, self.character.class_specials,
                                                                                   self.class_specials)

        # Position 'spells' section if character is of a magic related class (Magic-User, Cleric, etc.).
        if self.character.spells:
            self.position_spells()


    """Helper methods for use within this class.
    
    Each section of the character sheet has its own dedicated methods for formatting, positioning, and drawing. 
    Some of these methods may be similar or even identical, but they've been kept separate for the sake of clarity 
    and easier future modification of individual sections."""

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

    def position_basic_info(self) -> None:
        """Position values for basic character info (name, race, etc.) to corresponding anchor elements as grouped in
        'self.basic_info_groups'."""
        # Position value rects 'topleft' position to anchors 'topright'.
        for info_pair in self.basic_info_groups:
            info_pair[1].text_rect.topleft = info_pair[0].text_rect.topright

    def draw_basic_info(self) -> None:
        """Draw info pairs from 'self.basic_info_groups' on screen."""
        for info_pair in self.basic_info_groups:
            for field in info_pair:
                field.draw_text()

    def format_ability_scores(self) -> None:
        """Format output for 0/positive values of ability score's bonus and penalty. Remove value if it is '0' or add '+'
        if value is positive."""
        for group in self.ability_groups:
            if int(group[2].text) == 0:
                group[2].text = ""
            elif int(group[2].text) > 0:
                group[2].text = "+" + group[2].text

            # Update 'group[2].text_surface' and get new rect.
            group[2].render_new_text_surface()

    def position_ability_scores(self) -> None:
        """Format and position ability score labels and values on screen."""
        # Format ability bonus/penalty output.
        self.format_ability_scores()

        # Values for spacing between elements.
        score_spacing: int = int(self.screen_width / 15)
        bonus_penalty_spacing: int = int(self.screen_width / 40)

        # Position label, score and bonus/penalty fields.
        for index, group in enumerate(self.ability_groups):
            self.position_first_group_element(index, group, self.ability_groups, self.abilities)
            group[1].text_rect.top, group[1].text_rect.right = (group[0].text_rect.top,
                                                                group[0].text_rect.left + score_spacing)
            group[2].text_rect.top, group[2].text_rect.right = (group[1].text_rect.top,
                                                               group[1].text_rect.right + bonus_penalty_spacing)

    def draw_ability_scores(self) -> None:
        """Draw ability score section on screen."""
        # Draw sections anchor object 'self.abilities'.
        self.abilities.draw_text()
        # Draw ability score section.
        self.draw_grouped_fields(self.ability_groups)

    def format_saving_throws(self) -> None:
        """Format output for saving throws by adding a '+' to the score."""
        for group in self.saving_throw_groups:
            group[1].text = "+" + group[1].text

            # Update 'group[1].text_surface' and get new rect.
            group[1].render_new_text_surface()

    def position_saving_throws(self) -> None:
        """Format and position saving throw labels and values on screen."""
        # Format saving throws output.
        self.format_saving_throws()

        # Values for spacing between elements.
        score_spacing: int = int(self.screen_width / 5)

        # Position label and value fields.
        for index, group in enumerate(self.saving_throw_groups):
            self.position_first_group_element(index, group, self.saving_throw_groups, self.saving_throws)
            group[1].text_rect.top, group[1].text_rect.right = (group[0].text_rect.top,
                                                                group[0].text_rect.left + score_spacing)

    def draw_saving_throws(self) -> None:
        """Draw saving throw section on screen."""
        # Draw sections anchor object 'self.saving_throws'.
        self.saving_throws.draw_text()
        # Draw saving throws section.
        self.draw_grouped_fields(self.saving_throw_groups)

    def draw_special_abilities(self) -> None:
        """Format, position and draw special abilities elements on screen."""
        # Draw sections anchor object 'self.special_abilities'.
        self.special_abilities.draw_text()
        # Format, position and draw special abilities.
        self.format_and_draw_dynamic_field(self.special_ability, self.character.specials, self.special_abilities,
                                           self.specials_pos_y_list, text_prefix=" - ")

    def position_spells(self) -> None:
        """Position spells elements on screen."""
        self.spell.text_rect.topleft = self.spells.text_rect.bottomleft

    def draw_spells(self) -> None:
        """Position and draw spells elements on screen."""
        # Draw sections anchor object 'self.spells'.
        self.spells.draw_text()
        # Draw spells.
        self.spell.draw_text()

    def draw_class_specials(self) -> None:
        """Format, position and draw special abilities elements on screen."""
        # Draw sections anchor object 'self.class_specials'.
        self.class_specials.draw_text()
        # Format, position and draw special abilities.
        self.format_and_draw_dynamic_field(self.class_special, self.character.class_specials, self.class_specials,
                                           self.class_special_pos_y_list, text_prefix=" - ")

    def position_weight_carrying_capacity(self) -> None:
        """Position weight/carrying capacity elements on screen."""
        # Value for spacing between elements.
        cap_spacing: int = int(self.screen_width / 5)

        # Position label and value fields.
        for index, group in enumerate(self.weight_group):
            self.position_first_group_element(index, group, self.weight_group, self.carrying_cap)
            group[1].text_rect.top, group[1].text_rect.right = (group[0].text_rect.top,
                                                                group[0].text_rect.left + cap_spacing)

    def draw_weight_carrying_capacity(self) -> None:
        """Draw weight/carrying capacity elements on screen."""
        # Draw sections anchor object 'self.carrying_cap'.
        self.carrying_cap.draw_text()
        # Draw weight/carrying capacity section.
        self.draw_grouped_fields(self.weight_group)

    @staticmethod
    def position_first_group_element(index: int, group: tuple[TextField, ...],
                                     array: tuple[tuple[TextField, ...], ...], anchor: TextField) -> None:
        """Position the first element of a group within a vertically stacked section.
        If it's the first group in the section (index 0), align its top-left corner to the bottom-left of the section's
        anchor. Otherwise, stack it below the previous group's first element.
        ARGS:
            index: index of the current group in the array, passed from enumerate()
            group: tuple of TextField elements (e.g. label + value) to position
            array: full tuple containing all grouped elements in the section
            anchor: anchor TextField that marks the top of this section (e.g. section label)
        """
        if index == 0:
            group[0].text_rect.topleft = anchor.text_rect.bottomleft
        else:
            group[0].text_rect.topleft = array[index - 1][0].text_rect.bottomleft

    @staticmethod
    def draw_grouped_fields(array: tuple[tuple[TextField, ...], ...]) -> None:
        """Draw grouped character sheet elements from array.
        ARGS:
            array: tuple containing all grouped elements in the section.
        """
        for group in array:
            for item in group:
                item.draw_text()

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

    @staticmethod
    def format_and_draw_dynamic_field(field_object: TextField, char_attr_list: list[str] | tuple[str, ...],
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
