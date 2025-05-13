import pygame
import gui.screen_objects as so
from core.character_model import Character
from gui.screen_objects import TextField, Button
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

        # Size variables and elements from dict 'gui_elements'.
        self.gui_elements: dict = gui_elements
        self.edge_spacing: int = gui_elements["default_edge_spacing"]
        text_medium: int = gui_elements["text_medium"]

        # Class specific size variables.
        self.text_standard: int = int(self.screen_height / 50)
        text_large: int = int(self.screen_height / 45)
        title_size: int = int(self.screen_height / 35)

        # Strings for measurement units used on character sheet.
        self.weight_unit: str = " lbs"
        self.money_unit: str = " gold pieces"

        # General screen objects.
        self.title: TextField = so.TextField(screen, "- CHARACTER SHEET -", title_size)
        self.main_menu_button: Button = so.Button(screen, "Main Menu", text_medium)

        """
        INITIALIZE CHARACTER SHEET ELEMENTS.
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
        name: TextField = so.TextField(screen, "Name: ", text_large)  # ANCHOR
        name_char: TextField = so.TextField(screen, character.name, text_large)
        xp: TextField = so.TextField(screen, "XP: ", text_large)  # ANCHOR
        xp_char: TextField = so.TextField(screen, str(character.xp), text_large)
        race: TextField = so.TextField(screen, "Race: ", text_large)  # ANCHOR
        race_char: TextField = so.TextField(screen, character.race_name, text_large)
        cls: TextField = so.TextField(screen, "Class: ", text_large)  # ANCHOR
        cls_char: TextField = so.TextField(screen, character.class_name, text_large)
        level: TextField = so.TextField(screen, "Level: ", text_large)  # ANCHOR
        level_char: TextField = so.TextField(screen, str(character.level), text_large)
        next_lvl_xp: TextField = so.TextField(screen, "XP to next level: ", text_large)  # ANCHOR
        next_lvl_xp_char: TextField = so.TextField(screen, str(character.next_level_xp), text_large)
        money: TextField = so.TextField(screen, "Money: ", text_large)  # ANCHOR
        money_char: so.TextField = so.TextField(screen, str(self.character.money) + self.money_unit, text_large)
        # Combat related basic info elements.
        armor_class: TextField = so.TextField(screen, "Armor Class: ", self.text_standard)  # ANCHOR
        armor_class_char: TextField = so.TextField(screen, str(character.armor_class), self.text_standard)
        health_points: TextField = so.TextField(screen, "Health Points: ", self.text_standard)  # ANCHOR
        health_points_char: TextField = so.TextField(screen, str(character.hp), self.text_standard)
        attack_bonus: TextField = so.TextField(screen, "Attack Bonus: +", self.text_standard)  # ANCHOR
        attack_bonus_char: TextField = so.TextField(screen, str(character.attack_bonus), self.text_standard)
        # Array of basic info and combat info groups for cleaner positioning/drawing in class methods.
        self.basic_info_groups: tuple[tuple[TextField, TextField], ...] = (
            (name, name_char),
            (xp, xp_char),
            (race, race_char),
            (cls, cls_char),
            (level, level_char),
            (next_lvl_xp, next_lvl_xp_char),
            (money, money_char),
            (armor_class, armor_class_char),
            (health_points, health_points_char),
            (attack_bonus, attack_bonus_char),
        )

        # Abilities info elements.
        # Suffixes '_score' and '_bonus_penalty' indicate objects with values from the 'Character' class object.
        self.abilities: TextField = so.TextField(screen, "ABILITIES", text_large)  # ANCHOR
        str_label: TextField = so.TextField(screen, "str", self.text_standard)
        str_score: TextField = so.TextField(screen, str(character.abilities["str"][0]), self.text_standard)
        str_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["str"][1]), self.text_standard)
        dex_label: TextField = so.TextField(screen, "dex", self.text_standard)
        dex_score: TextField = so.TextField(screen, str(character.abilities["dex"][0]), self.text_standard)
        dex_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["dex"][1]), self.text_standard)
        con_label: TextField = so.TextField(screen, "con", self.text_standard)
        con_score: TextField = so.TextField(screen, str(character.abilities["con"][0]), self.text_standard)
        con_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["con"][1]), self.text_standard)
        int_label: TextField = so.TextField(screen, "int", self.text_standard)
        int_score: TextField = so.TextField(screen, str(character.abilities["int"][0]), self.text_standard)
        int_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["int"][1]), self.text_standard)
        wis_label: TextField = so.TextField(screen, "wis", self.text_standard)
        wis_score: TextField = so.TextField(screen, str(character.abilities["wis"][0]), self.text_standard)
        wis_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["wis"][1]), self.text_standard)
        cha_label: TextField = so.TextField(screen, "cha", self.text_standard)
        cha_score: TextField = so.TextField(screen, str(character.abilities["cha"][0]), self.text_standard)
        cha_bonus_penalty: TextField = so.TextField(screen, str(character.abilities["cha"][1]), self.text_standard)
        # Array of ability groups for cleaner positioning/drawing in class methods.
        self.ability_groups: tuple[tuple[TextField, TextField, TextField], ...] = (
            (str_label, str_score, str_bonus_penalty),
            (dex_label, dex_score, dex_bonus_penalty),
            (con_label, con_score, con_bonus_penalty),
            (int_label, int_score, int_bonus_penalty),
            (wis_label, wis_score, wis_bonus_penalty),
            (cha_label, cha_score, cha_bonus_penalty),
        )

        # Saving throws info elements.
        self.saving_throws: TextField = so.TextField(screen, "SAVING THROWS", text_large)  # ANCHOR
        saving_throw_0_label: TextField = so.TextField(screen, "Death Ray or Poison:", self.text_standard)
        saving_throw_0_score: TextField = so.TextField(screen, str(character.saving_throws["Death Ray or Poison"]), self.text_standard)
        saving_throw_1_label: TextField = so.TextField(screen, "Magic Wands:", self.text_standard)
        saving_throw_1_score: TextField = so.TextField(screen, str(character.saving_throws["Magic Wands"]), self.text_standard)
        saving_throw_2_label: TextField = so.TextField(screen, "Paralysis or Petrify:", self.text_standard)
        saving_throw_2_score: TextField = so.TextField(screen, str(character.saving_throws["Paralysis or Petrify"]), self.text_standard)
        saving_throw_3_label: TextField = so.TextField(screen, "Dragon Breath:", self.text_standard)
        saving_throw_3_score: TextField = so.TextField(screen, str(character.saving_throws["Dragon Breath"]), self.text_standard)
        saving_throw_4_label: TextField = so.TextField(screen, "Spells:", self.text_standard)
        saving_throw_4_score: TextField = so.TextField(screen, str(character.saving_throws["Spells"]), self.text_standard)
        # Array of saving throws groups for cleaner positioning/drawing in class methods.
        self.saving_throw_groups: tuple[tuple[TextField, TextField], ...] = (
            (saving_throw_0_label, saving_throw_0_score),
            (saving_throw_1_label, saving_throw_1_score),
            (saving_throw_2_label, saving_throw_2_score),
            (saving_throw_3_label, saving_throw_3_score),
            (saving_throw_4_label, saving_throw_4_score),
        )

        # Special abilities info elements.
        self.special_abilities: TextField = so.TextField(screen, "SPECIAL ABILITIES", text_large)  # ANCHOR
        # 'special_ability' object has its text dynamically modified in method 'draw_format_dynamic_field()' to account
        # for the fact that number of abilities in 'character.specials' is unpredictable at the start of the character
        # creation.
        self.special_ability: TextField = so.TextField(screen, "", self.text_standard, multi_line=True,
                                                       surface_width=int(self.screen_width / 3))
        # Create empty list to store y-position values for each state of 'self.special_ability'.
        self.specials_pos_y_list: list[int] = []

        # Spell elements for classes 'Magic-User', 'Cleric' or combination classes.
        self.spells: TextField = so.TextField(screen, "SPELLS", text_large)  # ANCHOR
        self.spell: TextField = so.TextField(screen, str(character.spells), self.text_standard)

        # Class specials elements.
        self.class_specials: TextField = so.TextField(screen, character.class_name.upper() + " SPECIALS",
                                                            text_large)  # ANCHOR
        # 'class_special' object has its text and position dynamically modified in method 'draw_format_dynamic_field()'
        # to account for the fact that number of specials in 'character.class_specials' is unpredictable at the start of
        # the character creation.
        self.class_special: TextField = so.TextField(screen, "", self.text_standard)
        # Create empty list to store y-position values for each state of 'self.class_special'.
        self.class_special_pos_y_list: list[int] = []

        # Weight/carrying capacity elements.
        unit = self.weight_unit
        self.carrying_cap: TextField = so.TextField(screen, "CARRYING CAPACITY", text_large)  # ANCHOR
        carrying_cap_light_label: TextField = so.TextField(screen, "Light Load:", self.text_standard)
        carrying_cap_light_char: TextField = so.TextField(screen, str(self.character.carrying_capacity["Light Load"]) + unit,
                                                               self.text_standard)
        carrying_cap_heavy_label: TextField = so.TextField(screen, "Heavy Load:", self.text_standard)
        carrying_cap_heavy_char: TextField = so.TextField(screen, str(self.character.carrying_capacity["Heavy Load"]) + unit,
                                                               self.text_standard)
        weight_carried_label: TextField = so.TextField(screen, "Weight Carried:", self.text_standard)
        weight_carried_char: TextField = so.TextField(screen, str(self.character.weight_carried) + unit, self.text_standard)
        # Array of weight/carrying capacity groups for cleaner positioning/drawing in class methods.
        self.weight_group: tuple[tuple[TextField, TextField], ...] = (
            (carrying_cap_light_label, carrying_cap_light_char),
            (carrying_cap_heavy_label, carrying_cap_heavy_char),
            (weight_carried_label, weight_carried_char),
        )

        # Inventory elements.
        self.inventory: TextField = so.TextField(screen, "INVENTORY: ", text_large)  # ANCHOR
        # 'inventory_item' and 'inventory_item_weight' objects have their text and position dynamically modified in
        # methods 'draw_format_dynamic_field()' and 'position_and_draw_inventory_weight()' respectively to account for
        # the fact that number of items in 'character.inventory' is unpredictable at the start of the character creation.
        self.inventory_item: TextField = so.TextField(screen, "", self.text_standard)
        self.inventory_item_weight: TextField = so.TextField(screen, "", self.text_standard)
        # Create and populate lists of inventory item names and weight as strings to position/format 'inventory_item'
        # and 'inventory_item_weight'.
        self.inventory_item_list, self.inventory_item_weight_list = self.get_inventory_strings()
        # Create empty list to store y-position values for each state of 'self.inventory'.
        self.inventory_pos_y_list: list[int] = []

        # Weapons and armor elements.
        # NOTE: While 'weapons' and 'armor' are two distinct sections, with their respective anchor elements being
        # separately positioned via 'self.screen_grid_array', they are using joint class methods for positioning/drawing
        # of each section's internal elements because of their similar structure and thematic relation.
        self.weapon: TextField = so.TextField(screen, "WEAPON", self.text_standard)  # ANCHOR
        self.armor: TextField = so.TextField(screen, "ARMOR", self.text_standard)  # ANCHOR
        # Further Header elements.
        self.weapon_header_size: TextField = so.TextField(screen, "Size", self.text_standard)
        self.weapon_header_damage: TextField = so.TextField(screen, "Dmg", self.text_standard)
        self.weapon_header_s: TextField = so.TextField(screen, "S", self.text_standard)
        self.weapon_header_m: TextField = so.TextField(screen, "M", self.text_standard)
        self.weapon_header_l: TextField = so.TextField(screen, "L", self.text_standard)
        self.armor_header_ac: TextField = so.TextField(screen, "AC", self.text_standard)
        # Characters weapon/armor/shield elements.
        weapon_item_str: str = f"{self.character.weapon.name}"
        armor_item_str: str = f"{self.character.armor.name}{self.character.armor.armor_class}"
        shield_item_str: str = f"{self.character.shield.name}"
        self.weapon_char: TextField = so.TextField(screen, weapon_item_str, self.text_standard)
        self.armor_char: TextField = so.TextField(screen, armor_item_str, self.text_standard)
        self.shield_char: TextField = so.TextField(screen, shield_item_str, self.text_standard)
        # Get arrays for weapon/armor groups for cleaner positioning/drawing in class methods.
        self.weapon_header_group, self.armor_header_group, self.weapon_armor_groups = self.get_weapon_armor_groups()

        """
        16x24 screen grid for positioning of anchor elements. Further elements that belong to anchors are then positioned
        dynamically via helper methods if value elements are added to their corresponding group array above.
        
        The grid size can be modified without the need to edit other parts of the the class. Only thing to keep in mind
        is that each tuple within 'self.screen_grid_array' has to contain the same number of items.
        """
        # Set following attribute to 'True' to show grid on screen for layout design.
        self.show_grid = False

        # Assign attributes to shorter variables for use in 'self.screen_grid_array' to allow for better readability.
        name: TextField = name
        xp: TextField = xp
        race: TextField = race
        cls: TextField = cls
        level: TextField = level
        nxtxp: TextField = next_lvl_xp
        money: TextField = money
        arcls: TextField = armor_class
        hp: TextField = health_points
        atbns: TextField = attack_bonus
        ablts: TextField = self.abilities
        svgth: TextField = self.saving_throws
        spabl: TextField = self.special_abilities
        splss: TextField = self.spells
        clssp: TextField = self.class_specials
        crcap: TextField = self.carrying_cap
        invty: TextField = self.inventory
        weapn: TextField = self.weapon
        armor: TextField = self.armor

        self.screen_grid_array: tuple[tuple[False | TextField, ...], ...] = (
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, name , False, False, level, False, False, False, arcls, False, atbns, False, hp   , False, False, False),
            (False, race , False, False, cls  , False, False, False, weapn, False, False, False, armor, False, False, False),
            (False, xp   , False, False, nxtxp, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, ablts, False, False, False, svgth, False, False, False, False, spabl, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, money, False, False, False, invty, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, splss, False, False, clssp, False, False),
            (False, crcap, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
        )


    """Main method to show character sheet. Called from function 'character_sheet_state_manager()' in
    'core/state_manager.py'."""

    def show_character_sheet_screen(self, mouse_pos) -> None:
        """Draw character sheet elements on screen.
        ARGS:
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        # Draw layout grid on screen if 'self.show_grid' is set to 'True'.
        if self.show_grid:
            self.draw_grid()

        # Draw general screen objects.
        draw_screen_title(self.screen, self.title, self.gui_elements)
        self.main_menu_button.draw_button(mouse_pos)

        # Draw character sheet elements.
        self.draw_basic_info()
        self.draw_ability_scores()
        self.draw_saving_throws()
        self.draw_special_abilities()
        self.draw_weight_carrying_capacity()
        self.draw_inventory()
        self.draw_armor_weapon()

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

        # Position basic screen elements.
        self.main_menu_button.button_rect.bottomright = (self.screen_rect.right - self.edge_spacing,
                                                         self.screen_rect.bottom - self.edge_spacing)

        # Position further elements.
        self.position_basic_info()
        self.position_ability_scores()
        self.position_saving_throws()
        self.position_weight_carrying_capacity()
        self.position_armor_weapon()

        # Get lists for dynamically positioned elements.
        self.specials_pos_y_list: list[int] = self.get_position_dynamic_field(self.special_ability, self.character.specials,
                                                                              self.special_abilities, text_prefix=" - ")
        self.class_special_pos_y_list: list[int] = self.get_position_dynamic_field(self.class_special, self.character.class_specials,
                                                                                   self.class_specials)
        self.inventory_pos_y_list: list[object] = self.get_position_dynamic_field(self.inventory_item, self.inventory_item_list,
                                                                                  self.inventory)

        # Position 'spells' section if character is of a magic related class (Magic-User, Cleric, etc.).
        if self.character.spells:
            self.position_spells()


    """Helper methods for use within this class.
    
    Each section of the character sheet has its own dedicated methods for formatting, positioning, and drawing. 
    Some of these methods may be similar or even identical, but they've been kept separate for the sake of clarity and
    easier future modification of individual sections."""

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
        self.draw_grouped_fields(self.basic_info_groups)

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

    def get_inventory_strings(self) -> tuple[list[str], list[str]]:
        """Create and populate lists of inventory item names and weight as strings. Values are retrieved from 'Item'
        instances in 'self.character.inventory'."""
        # Create empty lists to be populated and returned.
        name_list: list[str] = []
        weight_list: list[str]= []

        # Retrieve attributes from items in 'self.character.inventory' as strings and append them to lists.
        for item in self.character.inventory:
            name_list.append(str(item.name))
            weight_list.append(str(item.weight))

        return name_list, weight_list

    def position_and_draw_inventory_weight(self) -> None:
        """Format, position and draw 'self.inventory_item_weight'.
        Specialized version of method 'format_and_draw_dynamic_field()' to account for additional 'weight' element in
        inventory section."""
        # Value for spacing between elements.
        weight_spacing: int = int(self.screen_width / 4.5)

        for index, weight in enumerate(self.inventory_item_weight_list):
            # Assign text to and expand 'inventory_item_weight.text', update 'inventory_item_weight.text_surface' and
            # get new rect.
            self.inventory_item_weight.text = weight + self.weight_unit
            self.inventory_item_weight.render_new_text_surface()

            # Position and draw 'inventory_item_weight'.
            self.inventory_item_weight.text_rect.top, self.inventory_item_weight.text_rect.right = (
                self.inventory_pos_y_list[index], self.inventory.text_rect.left + weight_spacing)
            self.inventory_item_weight.draw_text()

    def draw_inventory(self) -> None:
        """Format, position and inventory elements on screen."""
        # Draw sections anchor object 'self.inventory'.
        self.inventory.draw_text()
        # Format, position and draw inventory item names and weight.
        self.format_and_draw_dynamic_field(self.inventory_item, self.inventory_item_list, self.inventory,
                                           self.inventory_pos_y_list)
        self.position_and_draw_inventory_weight()

    def get_weapon_armor_groups(self) -> tuple[tuple[TextField, ...], tuple[TextField, ...], tuple[tuple[TextField, ...], ...]]:
        """Create, populate and return arrays 'weapon_header_group', 'armor_header_group' and 'item_group' based on
        selected race/class.
        RETURNS:
            weapon_header_group: 'tuple[TextField, ...]' containing weapon header elements WITHOUT the section anchor.
            armor_header_group: 'tuple[TextField, ...]' containing armor header elements WITHOUT the section anchor.
            item_group: 'tuple[tuple[TextField, ...], ...]' containing item value elements and section anchors.
        """
        # Sets for class checks. 'Magic-User' can't use any armor, 'Thief' classes can't use shields.
        no_armor_classes: set[str] = {"Magic-User"}
        no_shield_classes: set[str] = {"Thief", "Magic-User/Thief"}

        # Tuples for weapon and armor header elements.
        weapon_header_group: tuple[TextField, ...] = (
                self.weapon_header_size, self.weapon_header_damage, self.weapon_header_s, self.weapon_header_m,
                self.weapon_header_l
            )
        armor_header_group: tuple[TextField, ...] = (self.armor_header_ac, )

        # Assign array of character sheet elements based on character class.
        if self.character.class_name in no_armor_classes:
            item_groups: tuple[tuple[TextField, ...], ...] = (
                (self.weapon, self.weapon_char),
            )
            # Empty armor header tuple for classes that can't use armor.
            armor_header_group = ()
        elif self.character.class_name in no_shield_classes:
            item_groups: tuple[tuple[TextField, ...], ...] = (
                (self.weapon, self.weapon_char),
                (self.armor, self.armor_char),
            )
        else:
            item_groups: tuple[tuple[TextField, ...], ...] = (
                (self.weapon, self.weapon_char),
                (self.armor, self.armor_char, self.shield_char),
            )

        return weapon_header_group, armor_header_group, item_groups

    def position_weapon_armor_header_elements(self) -> None:
        # Spacing values.
        spacing_1 = int(self.screen_width / 50)
        spacing_2 = int(self.screen_width / 50)
        spacing_3 = int(self.screen_width / 50)
        spacing_4 = int(self.screen_width / 50)
        spacing_5 = int(self.screen_width / 50)
        spacing_6 = int(self.screen_width / 50)

        # Assign y-positions based on anchor objects.
        for weapon_header in self.weapon_header_group:
            weapon_header.text_rect.bottom = self.weapon.text_rect.bottom
        for armor_header in self.armor_header_group:
            armor_header.text_rect.bottom = self.armor.text_rect.bottom

        self.weapon_header_size.text_rect.left = self.weapon.text_rect.right + spacing_1
        self.weapon_header_damage.text_rect.left = self.weapon_header_size.text_rect.right + spacing_2
        self.weapon_header_s.text_rect.left = self.weapon_header_damage.text_rect.right + spacing_3
        self.weapon_header_m.text_rect.left = self.weapon_header_s.text_rect.right + spacing_4
        self.weapon_header_l.text_rect.left = self.weapon_header_m.text_rect.right + spacing_5

        self.armor_header_ac.text_rect.left = self.armor.text_rect.right + spacing_6

    def position_armor_weapon(self) -> None:
        """Position weapon/armor elements from header groups and 'self.weapon_armor_groups'."""
        # Position header elements.
        self.position_weapon_armor_header_elements()
        # Position value rects 'topleft' position to 'bottomleft' of previous element.
        for info_pair in self.weapon_armor_groups:
            for index, item in enumerate(info_pair):
                # Explicit if-statement to make clear that anchor object (index 0) positioning is skipped, as this is
                # done via 'self.screen_grid_array'.
                if index == 0:
                    pass
                else:
                    item.text_rect.topleft = info_pair[index - 1].text_rect.bottomleft

    def draw_armor_weapon(self) -> None:
        """Draw elements from header groups and 'self.weapon_armor_groups' on screen."""
        # Draw header elements.
        for header_group in (self.weapon_header_group, self.armor_header_group):
            for header in header_group:
                header.draw_text()
        # Draw anchors and further weapon/armor elements.
        self.draw_grouped_fields(self.weapon_armor_groups)

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
            char_attr_list: attribute of type LIST or TUPLE containing strings to be dynamically added to 'field_object'.
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
            char_attr_list: attribute of type LIST or TUPLE containing strings to be dynamically added to 'field_object'.
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
