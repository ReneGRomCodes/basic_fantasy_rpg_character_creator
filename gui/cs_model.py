"""
Helper class to organize and access character sheet objects as attributes.
"""
import pygame

from core.character_model import Character
from core.shared_data import shared_data
from core.rules import CLASS_CATEGORIES, ABILITIES, SAVING_THROWS

from .screen_objects import TextField, Button
from .ui_helpers import draw_screen_title, draw_single_element_background_image
from .shared_data import ui_shared_data as uisd


class CharacterSheet:
    """A class to store and manage character sheet elements."""

    def __init__(self, screen) -> None:
        """Initialize the CharacterSheet object with elements.
        ARGS:
            screen: PyGame window.
        """
        self.character: Character = shared_data.character

        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.screen_height: int = self.screen_rect.height
        self.screen_width: int = self.screen_rect.width

        # Size attributes.
        self.edge_spacing: int = uisd.ui_registry["default_edge_spacing"]
        text_medium: int = uisd.ui_registry["text_medium"]
        self.text_standard: int = int(self.screen_height / 50)
        text_large: int = int(self.screen_height / 45)
        title_size: int = int(self.screen_height / 35)

        # Units of measurement used on character sheet.
        self.weight_unit: str = " lbs"
        self.money_unit: str = " gold pieces"
        self.distance_unit: str = "'"

        # General screen objects.
        self.title: TextField = TextField(screen, "- CHARACTER SHEET -", title_size)
        self.main_menu_button: Button = Button(screen, "Main Menu", text_medium)
        self.save_load_button: Button = Button(screen, "Save/Load", text_medium)
        self.button_group: tuple[Button, ...] = (self.main_menu_button, self.save_load_button)
        for button in self.button_group:
            button.button_rect.width = uisd.ui_registry["default_button_width"]

        # Attribute indicating if character has been saved to 'save/characters.json'. Contains 'slot_id' string if so.
        self.is_saved: str | bool = False
        # Confirmation message objects.
        self.confirmation_message: TextField = TextField(screen, "Exit without saving?", uisd.ui_registry["text_large"])
        self.exit_button: Button = Button(screen, "CONTINUE WITHOUT SAVING", self.text_standard)
        self.cancel_button: Button = Button(screen, "CANCEL", self.text_standard)
        self.save_button: Button = Button(screen, "SAVE CHARACTER", self.text_standard)
        self.confirmation_button_group: tuple[Button, ...] = (self.exit_button, self.cancel_button, self.save_button)
        for button in self.confirmation_button_group:
            button.button_rect.width = int(screen.get_rect().width / 5)
        self.position_exit_confirm_message()

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

        # Basic info elements.
        name: TextField = TextField(screen, f"Name: {self.character.name}", text_large)
        xp: TextField = TextField(screen, f"XP: {self.character.xp}", text_large)
        race: TextField = TextField(screen, f"Race: {self.character.race_name}", text_large)
        cls: TextField = TextField(screen, f"Class: {self.character.class_name}", text_large)
        level: TextField = TextField(screen, f"Level: {self.character.level}", text_large)
        next_lvl_xp: TextField = TextField(screen, f"XP to next level: {self.character.next_level_xp}", text_large)
        money: TextField = TextField(screen, f"Money: {self.character.money}", text_large)
        movement: TextField = TextField(screen, f"Movement: {self.character.movement}{self.distance_unit}", self.text_standard)
        # Combat related elements.
        armor_class: TextField = TextField(screen, f"Armor Class: {self.character.armor_class}", self.text_standard)
        health_points: TextField = TextField(screen, f"Health Points: {self.character.hp}", self.text_standard)
        attack_bonus: TextField = TextField(screen, f"Attack Bonus: +{self.character.attack_bonus}", self.text_standard)
        # Language elements.
        languages: TextField = TextField(screen, f"Languages: {self.build_languages_string()}", self.text_standard)

        self.basic_info_groups: tuple[TextField, ...] = (name, xp, race, cls, level, next_lvl_xp, money, movement,
                                                         armor_class, health_points, attack_bonus, languages)

        # Abilities elements.
        # Ability name strings as defined in 'core/rules.py' ABILITIES.
        str_name: str = ABILITIES[0]
        dex_name: str = ABILITIES[1]
        con_name: str = ABILITIES[2]
        int_name: str = ABILITIES[3]
        wis_name: str = ABILITIES[4]
        cha_name: str = ABILITIES[5]
        # Suffixes '_score' and '_bonus_penalty' indicate objects with values from the 'Character' class object.
        self.abilities: TextField = TextField(screen, "ABILITIES", text_large)  # ANCHOR
        str_label: TextField = TextField(screen, str_name, self.text_standard)
        str_score: TextField = TextField(screen, str(self.character.abilities[str_name][0]), self.text_standard)
        str_bonus_penalty: TextField = TextField(screen, str(self.character.abilities[str_name][1]), self.text_standard)
        dex_label: TextField = TextField(screen, dex_name, self.text_standard)
        dex_score: TextField = TextField(screen, str(self.character.abilities[dex_name][0]), self.text_standard)
        dex_bonus_penalty: TextField = TextField(screen, str(self.character.abilities[dex_name][1]), self.text_standard)
        con_label: TextField = TextField(screen, con_name, self.text_standard)
        con_score: TextField = TextField(screen, str(self.character.abilities[con_name][0]), self.text_standard)
        con_bonus_penalty: TextField = TextField(screen, str(self.character.abilities[con_name][1]), self.text_standard)
        int_label: TextField = TextField(screen, int_name, self.text_standard)
        int_score: TextField = TextField(screen, str(self.character.abilities[int_name][0]), self.text_standard)
        int_bonus_penalty: TextField = TextField(screen, str(self.character.abilities[int_name][1]), self.text_standard)
        wis_label: TextField = TextField(screen, wis_name, self.text_standard)
        wis_score: TextField = TextField(screen, str(self.character.abilities[wis_name][0]), self.text_standard)
        wis_bonus_penalty: TextField = TextField(screen, str(self.character.abilities[wis_name][1]), self.text_standard)
        cha_label: TextField = TextField(screen, cha_name, self.text_standard)
        cha_score: TextField = TextField(screen, str(self.character.abilities[cha_name][0]), self.text_standard)
        cha_bonus_penalty: TextField = TextField(screen, str(self.character.abilities[cha_name][1]), self.text_standard)

        self.ability_groups: tuple[tuple[TextField, TextField, TextField], ...] = (
            (str_label, str_score, str_bonus_penalty),
            (dex_label, dex_score, dex_bonus_penalty),
            (con_label, con_score, con_bonus_penalty),
            (int_label, int_score, int_bonus_penalty),
            (wis_label, wis_score, wis_bonus_penalty),
            (cha_label, cha_score, cha_bonus_penalty),
        )

        # Saving throws info elements.
        # Saving throw name strings as defined in 'core/rules.py' SAVING_THROWS.
        st_0_name: str = SAVING_THROWS["categories"][0]
        st_1_name: str = SAVING_THROWS["categories"][1]
        st_2_name: str = SAVING_THROWS["categories"][2]
        st_3_name: str = SAVING_THROWS["categories"][3]
        st_4_name: str = SAVING_THROWS["categories"][4]

        self.saving_throws: TextField = TextField(screen, "SAVING THROWS", text_large)  # ANCHOR
        saving_throw_0_label: TextField = TextField(screen, f"{st_0_name}:", self.text_standard)
        saving_throw_0_score: TextField = TextField(screen, str(self.character.saving_throws[st_0_name]), self.text_standard)
        saving_throw_1_label: TextField = TextField(screen, f"{st_1_name}:", self.text_standard)
        saving_throw_1_score: TextField = TextField(screen, str(self.character.saving_throws[st_1_name]), self.text_standard)
        saving_throw_2_label: TextField = TextField(screen, f"{st_2_name}:", self.text_standard)
        saving_throw_2_score: TextField = TextField(screen, str(self.character.saving_throws[st_2_name]), self.text_standard)
        saving_throw_3_label: TextField = TextField(screen, f"{st_3_name}:", self.text_standard)
        saving_throw_3_score: TextField = TextField(screen, str(self.character.saving_throws[st_3_name]), self.text_standard)
        saving_throw_4_label: TextField = TextField(screen, f"{st_4_name}:", self.text_standard)
        saving_throw_4_score: TextField = TextField(screen, str(self.character.saving_throws[st_4_name]), self.text_standard)

        self.saving_throw_groups: tuple[tuple[TextField, TextField], ...] = (
            (saving_throw_0_label, saving_throw_0_score),
            (saving_throw_1_label, saving_throw_1_score),
            (saving_throw_2_label, saving_throw_2_score),
            (saving_throw_3_label, saving_throw_3_score),
            (saving_throw_4_label, saving_throw_4_score),
        )

        # Special abilities info elements.
        self.special_abilities: TextField = TextField(screen, "SPECIAL ABILITIES", text_large)  # ANCHOR
        # 'special_ability' object has its text dynamically modified in method 'draw_format_dynamic_field()' to account
        # for the fact that number of abilities in 'character.specials' is unpredictable at the start of the character
        # creation.
        self.special_ability: TextField = TextField(screen, "", self.text_standard, multi_line=True,
                                                       surface_width=int(self.screen_width / 3))
        self.specials_pos_y_list: list[int] = []

        # Spell elements for classes 'Magic-User', 'Cleric' or combination classes.
        self.spells: TextField = TextField(screen, "SPELLS", text_large)  # ANCHOR
        # 'spell' object has its text and position dynamically modified in method 'draw_format_dynamic_field()' to
        # account for the fact that number of items in 'character.spells' is unpredictable at the start of the character
        # creation.
        self.spell: TextField = TextField(screen, str(self.character.spells), self.text_standard)
        self.spell_pos_y_list: list[int] = []

        # Class specials elements.
        # Set class special text to 'Thief' for all thief related classes.
        if "Thief" in self.character.class_name:
            class_text = "Thief"
        else:
            class_text = self.character.class_name

        self.class_specials: TextField = TextField(screen, class_text.upper() + " SPECIALS", text_large)  # ANCHOR
        # 'class_special' object has its text and position dynamically modified in method 'draw_format_dynamic_field()'
        # to account for the fact that number of specials in 'character.class_specials' is unpredictable at the start of
        # the character creation.
        self.class_special: TextField = TextField(screen, "", self.text_standard)
        self.class_special_pos_y_list: list[int] = []

        # Weight/carrying capacity elements.
        unit = self.weight_unit
        self.carrying_cap: TextField = TextField(screen, "CARRYING CAPACITY", text_large)  # ANCHOR
        carrying_cap_light_label: TextField = TextField(screen, "Light Load:", self.text_standard)
        carrying_cap_light_char: TextField = TextField(screen, f"{self.character.carrying_capacity["Light Load"]}{unit}",
                                                               self.text_standard)
        carrying_cap_heavy_label: TextField = TextField(screen, "Heavy Load:", self.text_standard)
        carrying_cap_heavy_char: TextField = TextField(screen, f"{self.character.carrying_capacity["Heavy Load"]}{unit}",
                                                               self.text_standard)
        weight_carried_label: TextField = TextField(screen, "Weight Carried:", self.text_standard)
        weight_carried_char: TextField = TextField(screen, f"{self.character.weight_carried}{unit}", self.text_standard)

        self.weight_group: tuple[tuple[TextField, TextField], ...] = (
            (carrying_cap_light_label, carrying_cap_light_char),
            (carrying_cap_heavy_label, carrying_cap_heavy_char),
            (weight_carried_label, weight_carried_char),
        )

        # Inventory elements.
        self.inventory: TextField = TextField(screen, "INVENTORY", text_large)  # ANCHOR
        # 'inventory_item' and 'inventory_item_weight' objects have their text and position dynamically modified in
        # methods 'draw_format_dynamic_field()' and 'position_and_draw_inventory_weight()' respectively to account for
        # the fact that number of items in 'character.inventory' is unpredictable at the start of the character creation.
        self.inventory_item: TextField = TextField(screen, "", self.text_standard)
        self.inventory_item_weight: TextField = TextField(screen, "", self.text_standard)
        self.inventory_item_list, self.inventory_item_weight_list = self.get_inventory_strings()
        self.inventory_pos_y_list: list[int] = []

        # Weapon elements.
        self.weapon_label: TextField = TextField(screen, "WEAPON", self.text_standard)  # ANCHOR
        self.weapon_header_size: TextField = TextField(screen, "Size", self.text_standard)
        self.weapon_header_damage: TextField = TextField(screen, "Dmg", self.text_standard)
        self.weapon_header_s: TextField = TextField(screen, "S +1", self.text_standard)
        self.weapon_header_m: TextField = TextField(screen, "M", self.text_standard)
        self.weapon_header_l: TextField = TextField(screen, "L -2", self.text_standard)
        # Characters weapon elements.
        self.weapon: TextField = TextField(screen, f"{self.character.weapon.name}", self.text_standard)

        self.weapon_header_group: tuple[TextField, ...] = (
            self.weapon_header_size, self.weapon_header_damage, self.weapon_header_s, self.weapon_header_m,
            self.weapon_header_l
        )
        self.weapon_group: tuple[TextField, ...] = (self.weapon, )

        # Armor elements.
        self.armor_label: TextField = TextField(screen, "ARMOR", self.text_standard)  # ANCHOR
        self.armor_header_ac: TextField = TextField(screen, "AC", self.text_standard)
        self.armor_char: TextField = TextField(screen, f"{self.character.armor.name}", self.text_standard)
        self.armor_char_ac: TextField = TextField(screen, f"{self.character.armor.armor_class}", self.text_standard)
        self.shield_char: TextField = TextField(screen, f"{self.character.shield.name}", self.text_standard)
        self.shield_char_ac: TextField = TextField(screen, f"{self.character.shield.armor_class}", self.text_standard)

        self.armor_header_group, self.armor_group = self.get_armor_groups()

        """
        16x24 screen grid for positioning of anchor elements. Further elements that belong to anchors are then positioned
        dynamically via helper methods if value elements are added to their corresponding group array above.
        
        The grid size can be modified without the need to edit other parts of the the class. Only thing to keep in mind
        is that each tuple within 'self.screen_grid_array' has to contain the same number of items.
        """
        # Set following attribute to 'True' to show grid on screen for layout design.
        self.show_grid = False

        # Assign attributes to shorter variables for use in 'self.screen_grid_array' to allow for better readability.
        name : TextField = name
        xp   : TextField = xp
        race : TextField = race
        cls  : TextField = cls
        level: TextField = level
        nxtxp: TextField = next_lvl_xp
        money: TextField = money
        mvmnt: TextField = movement
        arcls: TextField = armor_class
        hp   : TextField = health_points
        atbns: TextField = attack_bonus
        langs: TextField = languages
        ablts: TextField = self.abilities
        svgth: TextField = self.saving_throws
        spabl: TextField = self.special_abilities
        splss: TextField = self.spells
        clssp: TextField = self.class_specials
        crcap: TextField = self.carrying_cap
        invty: TextField = self.inventory
        weapn: TextField = self.weapon_label
        armor: TextField = self.armor_label

        self.screen_grid_array: tuple[tuple[False | TextField, ...], ...] = (
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, name , False, False, level, False, False, False, arcls, False, atbns, False, hp   , False, mvmnt, False),
            (False, race , False, False, cls  , False, False, False, weapn, False, False, False, False, armor, False, False),
            (False, xp   , False, False, nxtxp, False, False, False, False, False, False, False, False, False, False, False),
            (False, langs, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            (False, ablts, False, False, False, svgth, False, False, False, False, spabl, False, False, False, False, False),
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

        # TODO work in progress!
        # Background image attributes.
        bg_type = uisd.ui_registry["parchment_images"][2]
        bg_width: float = self.screen_width * 1.18
        bg_height: float = self.screen_height * 1.15
        bg_center: tuple[int, int] = self.screen_rect.center
        self.bg_image_loaded = pygame.transform.scale(bg_type, (bg_width, bg_height))
        self.bg_image_rect = self.bg_image_loaded.get_rect(center=bg_center)
        # List of character attribute categories as stored in 'self.screen_grid_array'.
        self.cs_categories = [col for row in self.screen_grid_array for col in row if col]


    """Main methods to position/display character sheet. Called from function 'character_sheet_state_manager()' in
    'core/state_manager.py'."""

    def show_character_sheet_screen(self, mouse_pos) -> None:
        """Draw character sheet elements on screen.
        ARGS:
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        if self.show_grid:
            self.draw_grid()

        self.draw_cs_background()

        draw_screen_title(self.screen, self.title)
        for button in self.button_group:
            draw_single_element_background_image(self.screen, button, "wood")
            button.draw_button(mouse_pos)

        for field in self.basic_info_groups:
            field.draw_text()

        self.draw_ability_scores()
        self.draw_saving_throws()
        self.draw_special_abilities()
        self.draw_weight_carrying_capacity()
        self.draw_inventory()
        self.draw_weapon()

        if self.character.class_name in CLASS_CATEGORIES["spell_using_classes"]:
            self.draw_spells()
        if self.character.class_specials:
            self.draw_class_specials()
        if self.character.class_name not in CLASS_CATEGORIES["no_armor_classes"]:
            self.draw_armor()

    def position_cs_elements(self) -> None:
        """Position character sheet elements on screen."""
        valinor = (-9999, self.screen_rect.centery)  # Off-screen position for unused elements based on race/class.
                                                     # can only be reached by sailing the Straight Road.
        self.position_anchors()

        self.main_menu_button.button_rect.bottomright = (self.screen_rect.right - self.edge_spacing,
                                                         self.screen_rect.bottom - self.edge_spacing)
        self.save_load_button.button_rect.bottomleft = (self.screen_rect.left + self.edge_spacing,
                                                        self.screen_rect.bottom - self.edge_spacing)

        self.position_ability_scores()
        self.position_saving_throws()
        self.position_weight_carrying_capacity()
        self.position_weapon()

        # Move anchor objects to valinor if irrelevant for character race/class.
        if self.character.class_name not in CLASS_CATEGORIES["spell_using_classes"]:
            self.spells.text_rect.center = valinor
        if not self.character.class_specials:
            self.class_specials.text_rect.center = valinor
        if self.character.class_name not in CLASS_CATEGORIES["no_armor_classes"]:
            self.position_armor()
        else:
            self.armor_label.text_rect.center = valinor

        self.specials_pos_y_list: list[int] = self.get_position_dynamic_field(self.special_ability, self.character.race_specials,
                                                                              self.special_abilities, text_prefix=" - ")
        self.class_special_pos_y_list: list[int] = self.get_position_dynamic_field(self.class_special, self.character.class_specials,
                                                                                   self.class_specials)
        self.inventory_pos_y_list: list[object] = self.get_position_dynamic_field(self.inventory_item, self.inventory_item_list,
                                                                                  self.inventory)
        self.spell_pos_y_list: list[int] = self.get_position_dynamic_field(self.spell, self.character.spells,
                                                                               self.spells)

    # TODO work in progress!
    def draw_cs_background(self):
        self.screen.blit(self.bg_image_loaded, self.bg_image_rect)


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

    def format_ability_scores(self) -> None:
        """Format output for 0/positive values of ability score's bonus and penalty. Remove value if it is '0' or add '+'
        if value is positive."""
        for group in self.ability_groups:
            if int(group[2].text) == 0:
                group[2].text = ""
            elif int(group[2].text) > 0:
                group[2].text = "+" + group[2].text

            group[2].render_new_text_surface()

    def position_ability_scores(self) -> None:
        """Format and position ability score labels and values on screen."""
        anchor = self.abilities
        self.format_ability_scores()

        score_spacing: int = int(self.screen_width / 15)
        bonus_penalty_spacing: int = int(self.screen_width / 40)

        for index, group in enumerate(self.ability_groups):
            self.position_first_group_element(index, group, self.ability_groups, anchor)
            group[1].text_rect.top, group[1].text_rect.right = (group[0].text_rect.top,
                                                                group[0].text_rect.left + score_spacing)
            group[2].text_rect.top, group[2].text_rect.right = (group[1].text_rect.top,
                                                               group[1].text_rect.right + bonus_penalty_spacing)

    def draw_ability_scores(self) -> None:
        """Draw ability score section on screen."""
        self.abilities.draw_text()
        self.draw_grouped_fields(self.ability_groups)

    def format_saving_throws(self) -> None:
        """Format output for saving throws by adding a '+' to the score."""
        for group in self.saving_throw_groups:
            group[1].text = "+" + group[1].text

            group[1].render_new_text_surface()

    def position_saving_throws(self) -> None:
        """Format and position saving throw labels and values on screen."""
        anchor = self.saving_throws
        self.format_saving_throws()

        score_spacing: int = int(self.screen_width / 5)

        for index, group in enumerate(self.saving_throw_groups):
            self.position_first_group_element(index, group, self.saving_throw_groups, anchor)
            group[1].text_rect.top, group[1].text_rect.right = (group[0].text_rect.top, group[0].text_rect.left + score_spacing)

    def draw_saving_throws(self) -> None:
        """Draw saving throw section on screen."""
        self.saving_throws.draw_text()
        self.draw_grouped_fields(self.saving_throw_groups)

    def draw_special_abilities(self) -> None:
        """Format, position and draw special abilities elements on screen."""
        self.special_abilities.draw_text()
        self.format_and_draw_dynamic_field(self.special_ability, self.character.race_specials, self.special_abilities,
                                           self.specials_pos_y_list, text_prefix=" - ")

    def draw_spells(self) -> None:
        """Position and draw spells elements on screen."""
        self.spells.draw_text()
        self.format_and_draw_dynamic_field(self.spell, self.character.spells, self.spells, self.spell_pos_y_list)

    def draw_class_specials(self) -> None:
        """Format, position and draw special abilities elements on screen."""
        self.class_specials.draw_text()
        self.format_and_draw_dynamic_field(self.class_special, self.character.class_specials, self.class_specials,
                                           self.class_special_pos_y_list, text_prefix=" - ")

    def position_weight_carrying_capacity(self) -> None:
        """Position weight/carrying capacity elements on screen."""
        anchor = self.carrying_cap

        cap_spacing: int = int(self.screen_width / 5)

        for index, group in enumerate(self.weight_group):
            self.position_first_group_element(index, group, self.weight_group, anchor)
            group[1].text_rect.top, group[1].text_rect.right = (group[0].text_rect.top,
                                                                group[0].text_rect.left + cap_spacing)

    def draw_weight_carrying_capacity(self) -> None:
        """Draw weight/carrying capacity elements on screen."""
        self.carrying_cap.draw_text()
        self.draw_grouped_fields(self.weight_group)

    def get_inventory_strings(self) -> tuple[list[str], list[str]]:
        """Create and populate lists of inventory item names and weight as strings. Values are retrieved from 'Item'
        instances in 'self.character.inventory'."""
        name_list: list[str] = []
        weight_list: list[str]= []

        for item in self.character.inventory:
            name_list.append(str(item.name))
            weight_list.append(str(item.weight))

        return name_list, weight_list

    def position_and_draw_inventory_weight(self) -> None:
        """Format, position and draw 'self.inventory_item_weight'.
        Specialized version of method 'format_and_draw_dynamic_field()' to account for additional 'weight' element in
        inventory section."""
        weight_spacing: int = int(self.screen_width / 4.5)

        for index, weight in enumerate(self.inventory_item_weight_list):
            self.inventory_item_weight.text = weight + self.weight_unit
            self.inventory_item_weight.render_new_text_surface()

            self.inventory_item_weight.text_rect.top, self.inventory_item_weight.text_rect.right = (
                self.inventory_pos_y_list[index], self.inventory.text_rect.left + weight_spacing)
            self.inventory_item_weight.draw_text()

    def draw_inventory(self) -> None:
        """Format, position and inventory elements on screen."""
        self.inventory.draw_text()
        self.format_and_draw_dynamic_field(self.inventory_item, self.inventory_item_list, self.inventory,
                                           self.inventory_pos_y_list)
        self.position_and_draw_inventory_weight()

    def position_weapon_header_elements(self) -> None:
        """Position weapon header elements."""
        anchor = self.weapon_label

        size_spacing: int = int(self.screen_width / 12)
        dmg_spacing: int = int(self.screen_width / 70)
        range_spacing: int = int(self.screen_width / 70)
        sml_spacing: int = int(self.screen_width / 100)

        for weapon_header in self.weapon_header_group:
            weapon_header.text_rect.bottom = anchor.text_rect.bottom

        self.weapon_header_size.text_rect.left = anchor.text_rect.right + size_spacing
        self.weapon_header_damage.text_rect.left = self.weapon_header_size.text_rect.right + dmg_spacing
        self.weapon_header_s.text_rect.left = self.weapon_header_damage.text_rect.right + range_spacing
        self.weapon_header_m.text_rect.left = self.weapon_header_s.text_rect.right + sml_spacing
        self.weapon_header_l.text_rect.left = self.weapon_header_m.text_rect.right + sml_spacing

    def position_weapon(self) -> None:
        """Position weapon elements."""
        anchor: TextField = self.weapon_label
        self.position_weapon_header_elements()

        for index, item in enumerate(self.weapon_group):
            if index == 0:
                item.text_rect.topleft = anchor.text_rect.bottomleft
            else:
                item.text_rect.topleft = self.weapon_group[index - 1].text_rect.bottomleft

    def draw_weapon(self) -> None:
        """Draw armor elements."""
        self.weapon_label.draw_text()

        for group in (self.weapon_header_group, self.weapon_group):
            for item in group:
                item.draw_text()

    def get_armor_groups(self) -> tuple[tuple[TextField, ...], tuple]:
        """Create, populate and return arrays 'armor_header_group' and 'armor_group' based on selected race/class.
        RETURNS:
            armor_header_group: 'tuple[TextField, ...]' containing armor header elements WITHOUT the section anchor.
            armor_group: 'tuple[TextField, ...]' containing armor value elements.
        """
        no_armor_classes: set[str] = CLASS_CATEGORIES["no_armor_classes"]
        no_shield_classes: set[str] = CLASS_CATEGORIES["no_shield_classes"]

        armor_header_group: tuple[TextField, ...] = (self.armor_header_ac, )

        if self.character.class_name in no_armor_classes:
            armor_header_group: tuple = ()
            armor_group: tuple = ()
        elif self.character.class_name in no_shield_classes:
            armor_group: tuple[tuple[TextField, TextField], ...] = (
                (self.armor_char, self.armor_char_ac),
            )
        else:
            armor_group: tuple[tuple[TextField, TextField], ...] = (
                (self.armor_char, self.armor_char_ac),
                (self.shield_char, self.shield_char_ac),
            )

        return armor_header_group, armor_group

    def position_armor_header_elements(self) -> None:
        """Position armor header elements."""
        anchor: TextField = self.armor_label

        spacing: int = int(self.screen_width / 18)

        for armor_header in self.armor_header_group:
            armor_header.text_rect.bottom = anchor.text_rect.bottom

        self.armor_header_ac.text_rect.left = anchor.text_rect.right + spacing

    def position_armor(self) -> None:
        """Position armor elements."""
        anchor: TextField = self.armor_label
        self.position_armor_header_elements()

        for index, group in enumerate(self.armor_group):
            self.position_first_group_element(index, group, self.armor_group, anchor)
            group[1].text_rect.top = group[0].text_rect.top
            group[1].text_rect.centerx = self.armor_header_group[0].text_rect.centerx

    def draw_armor(self) -> None:
        """Draw armor elements."""
        self.armor_label.draw_text()

        for element in self.armor_header_group:
            element.draw_text()

        self.draw_grouped_fields(self.armor_group)

    def build_languages_string(self) -> str:
        """Build and return string 'languages_str' to be used as value for attribute 'self.lang_str'."""
        languages_str: str = ""

        for index, language in enumerate(self.character.languages, start=1):
            # Format string with a ', ' for all elements except the last one.
            if index != len(self.character.languages):
                languages_str += f"{language}, "
            else:
                languages_str += language

        return languages_str

    @staticmethod
    def position_first_group_element(index: int, group: tuple[TextField, ...],
                                     array: tuple[tuple[TextField, ...], ...], anchor: TextField) -> None:
        """Position the first element of a group within a vertically stacked section.
        If it's the first group in the section (index 0), align its top-left corner to the bottom-left of the section's
        anchor. Otherwise, stack it below the previous group's first element.
        ARGS:
            index: index of the current group in the array, passed from enumerate().
            group: tuple of TextField elements (e.g. label + value) to position.
            array: full tuple containing all grouped elements in the section.
            anchor: anchor TextField that marks the top of this section (e.g. section label).
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
        pos_y = anchor.text_rect.bottom
        pos_y_list: list[int] = []

        for index, char_attr_item in enumerate(char_attr_list):
            field_object.text = text_prefix + char_attr_item
            field_object.render_new_text_surface()

            if index == 0:
                pos_y_list.append(pos_y)
            else:
                pos_y: int = pos_y_list[index - 1] + pos_y_list[index]
                pos_y_list[index] = pos_y

            # Append height of current 'text_rect' to list for use in following iteration where it will then be
            # overwritten with the newly calculated 'pos_y'.
            pos_y_list.append(field_object.text_rect.height)

            # Create object with default values to hard reset 'field_object'. Quick and dirty fix for 'field_object'
            # refusing to be reset any other way if 'multi_line' is 'True'.
            if field_object.multi_line:
                default_object: TextField = TextField(self.screen, "", self.text_standard, multi_line=True,
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
            field_object.text = text_prefix + char_attr_item
            field_object.render_new_text_surface()

            field_object.text_rect.top, field_object.text_rect.left = pos_y_list[index], anchor.text_rect.left
            field_object.draw_text()

    def draw_grid(self) -> None:
        """Draw layout grid on screen based on size of 'self.screen_grid_array'.
        NOTE: 'self.show_grid' has to be set to 'True' for the grid to appear on screen."""
        grid_cell_width: int = int(self.screen_width / len(self.screen_grid_array[0]))
        grid_cell_height: int = int(self.screen_height / len(self.screen_grid_array))
        grid_pos: list[int] = [0, 0]

        for row in self.screen_grid_array:
            pygame.draw.line(self.screen, "black", tuple(grid_pos), (self.screen_rect.right, grid_pos[1]))

            for column in row:
                pygame.draw.line(self.screen, "black", tuple(grid_pos), (grid_pos[0], self.screen_rect.bottom))
                grid_pos[0] += grid_cell_width

            # Reset x-position to '0' and set new y-position for next row.
            grid_pos[0] = 0
            grid_pos[1] += int(grid_cell_height)

    def show_exit_confirm_message(self, screen, mouse_pos) -> None:
        """Draw confirmation message when exiting character sheet screen.
        ARGS:
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        draw_single_element_background_image(screen, self.confirmation_message, "ornate_wood")
        self.confirmation_message.draw_text()

        for button in self.confirmation_button_group:
            draw_single_element_background_image(screen, button, "wood")
            button.draw_button(mouse_pos)

    def position_exit_confirm_message(self) -> None:
        """Position confirmation message objects."""
        edge_spacing = uisd.ui_registry["default_edge_spacing"]
        button_spacing = uisd.ui_registry["button_spacing"]

        self.confirmation_message.text_rect.bottom = self.screen_rect.centery - edge_spacing

        self.cancel_button.button_rect.centerx = self.screen_rect.centerx  # Position cancel button first as reference.
        for button in self.confirmation_button_group:
            button.button_rect.top = self.screen_rect.centery + edge_spacing
        self.exit_button.button_rect.left = self.cancel_button.button_rect.right + button_spacing
        self.save_button.button_rect.right = self.cancel_button.button_rect.left - button_spacing
