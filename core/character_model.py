"""
Class for character.
"""
import random
from typing import Any

from gui.screen_objects import InteractiveText
from gui.shared_data import ui_shared_data as uisd

import core.items.item_instances as item_inst
from .items import Armor
from .rules import RACE_DATA, CLASS_DATA, CLASS_CATEGORIES, SAVING_THROWS, MOVEMENT_RULES, dice_roll, get_ability_score
from .shared_data import shared_data as sd


class Character:
    """Represent a character."""

    def __init__(self) -> None:
        """Initialize race and class-specific attributes and character values."""
        # Race specific attributes.
        self.race_name: str = ""
        self.race_specials: tuple[str, ...] = ()
        self.bonuses: tuple[int, ...] = ()
        # Class specific attributes.
        self.class_name: str = ""
        self.class_specials: tuple[str, ...] = ()
        self.class_saving_throws: tuple[int, ...] = ()

        # Character attributes.
        self.name: str = ""
        self.abilities: dict[str, list[int]] = {}
        self.armor_class: int = 0
        self.attack_bonus: int = 1  # Default attack bonus of +1 for Lvl characters.
        self.specials: tuple[str, ...] = ()
        self.max_hit_die: int | False = False
        self.xp: int = 0
        self.level: int = 1
        self.next_level_xp: int = 0
        self.saving_throws: dict[str, int] = {}
        self.languages: list[str] = []
        self.spells: list[str] = []
        self.hp: int = 0
        self.movement: int = 0
        # Inventory attributes.
        self.carrying_capacity: dict[str, int] = {}
        self.weight_carried: int | float = 0
        self.money: int | float = 0
        self.inventory: list[object] = []
        self.armor: object = item_inst.ARMORS["no_armor"]
        self.shield: object = item_inst.ARMORS["no_shield"]
        self.weapon: object = item_inst.WEAPONS["no_weapon"]

    def set_race(self, race_selection: str) -> None:
        """Set race-specific values based on chosen race.
        ARGS:
            race_selection: string representing the race chosen by the player.
        """
        self.race_name = race_selection

        race_data: dict = RACE_DATA[race_selection.lower()]

        self.race_specials = race_data["race_specials"]
        self.bonuses = race_data["race_bonuses"]

    def set_class(self, class_selection: str) -> None:
        """Set class-specific values based on chosen class.
        ARGS:
            class_selection: string representing the class chosen by the player.
        """
        self.class_name = class_selection

        class_data: dict = CLASS_DATA[class_selection.lower()]

        self.next_level_xp = class_data["next_level_xp"]
        self.class_specials = class_data["class_specials"]
        self.class_saving_throws = class_data["class_saving_throws"]
        self.spells = class_data["spells"]
        self.inventory = class_data["inventory"]
        self.weight_carried = class_data["weight_carried"]

    def reset_character(self) -> None:
        """Reset values that may not be overwritten otherwise when creating a new character."""
        self.specials = ()

    def set_name(self, char_name: str) -> None:
        """Set name for character."""
        self.name = char_name

        # Reset value for name input field to empty string.
        uisd.ui_registry["character_name_input"][0].manager.value = ""

    def set_ability_dict(self) -> None:
        """Build attribute dictionary 'self.abilities' for character abilities. Values are lists with base score at
        index 0 and bonus/penalty at index 1."""
        ability_names: tuple[str, ...] = ("str", "dex", "con", "int", "wis", "cha")

        for item in ability_names:
            # Adding default INT bonus of +1.
            if item == "int":
                self.abilities[item] = get_ability_score()
                self.abilities[item][1] += 1
            else:
                self.abilities[item] = get_ability_score()

    def set_character_values(self) -> None:
        """Collected method calls to set multiple attributes."""
        self.set_max_hit_die()
        self.set_saving_throws()
        self.set_specials()
        self.set_hp()
        self.set_armor_class()
        self.set_carrying_capacity()
        self.set_movement_rate()

    def set_max_hit_die(self) -> None:
        """Set 'self.max_hit_die' based on chosen race and class."""
        race_hit_die: dict = RACE_DATA[self.race_name.lower()]["race_hit_die"]
        class_hit_die: dict = CLASS_DATA[self.class_name.lower()]["class_hit_die"]

        if race_hit_die and class_hit_die > race_hit_die:
            self.max_hit_die = race_hit_die
        else:
            self.max_hit_die = class_hit_die

    def set_specials(self) -> None:
        """Get special abilities and add them to attribute list 'self.specials'."""
        self.specials = self.race_specials + self.class_specials

    def set_saving_throws(self) -> None:
        """Get saving throw values and add them to attribute dict 'self.saving_throws'."""
        saving_throws = SAVING_THROWS["categories"]

        for index, item in enumerate(saving_throws):
            self.saving_throws[item] = self.bonuses[index] + self.class_saving_throws[index]

    def set_hp(self) -> None:
        """Set HP and adds constitution bonus/penalty."""
        self.hp = dice_roll(1, self.max_hit_die)

        # Adding constitution bonus/penalty to HP or set to minimum value of 1:
        if self.hp + self.abilities["con"][1] < 1:
            self.hp = 1
        else:
            self.hp += self.abilities["con"][1]

    def set_armor_class(self) -> None:
        """Set armor class based on equipped armor, shield and dexterity bonus/penalty."""
        self.armor_class = self.armor.armor_class + self.shield.armor_class + self.abilities["dex"][1]

    def set_carrying_capacity(self) -> None:
        """Set dict 'self.carrying_capacity' based on race and strength score."""
        carry_cap: tuple[tuple[int, int, int], ...] = RACE_DATA[self.race_name.lower()]["carrying_cap"]
        strength_threshold_index: int = 0
        cap_light_index: int = 1
        cap_heavy_index: int = 2
        strength: int = self.abilities["str"][0]
        cap_light_key: str = "Light Load"
        cap_heavy_key: str = "Heavy Load"

        for item in carry_cap:
            if strength > item[strength_threshold_index]:
                self.carrying_capacity = {cap_light_key: item[cap_light_index], cap_heavy_key: item[cap_heavy_index]}

    def set_movement_rate(self) -> None:
        """Set movement rate based on encumbrance and worn armor. Has to be called whenever changes to 'self.weight_carried'
        are made in other methods."""
        light_encumbrance: dict[str, int] = MOVEMENT_RULES["light_load"]
        heavy_encumbrance: dict[str, int] = MOVEMENT_RULES["heavy_load"]

        if self.weight_carried <= self.carrying_capacity["Light Load"]:
            if self.armor == item_inst.NO_ARMOR:
                self.movement: int = light_encumbrance["no_armor"]
            elif self.armor == item_inst.LEATHER_ARMOR:
                self.movement: int = light_encumbrance["leather_armor"]
            else:
                self.movement: int = light_encumbrance["other"]

        elif self.weight_carried <= self.carrying_capacity["Heavy Load"]:
            if self.armor == item_inst.NO_ARMOR:
                self.movement: int = heavy_encumbrance["no_armor"]
            elif self.armor == item_inst.LEATHER_ARMOR:
                self.movement: int = heavy_encumbrance["leather_armor"]
            else:
                self.movement: int = heavy_encumbrance["other"]

    def set_starting_spell(self, spell_list: tuple[InteractiveText, ...]) -> None:
        """Append 'text' attributes from instances in 'spell_list' to 'self.spells' if their 'selected' attribute is set
        to 'True'.
        ARGS:
            spell_list: tuple with instances of interactive text fields for spell selection.
        """
        self.spells.clear()

        for spell in spell_list:
            if spell.selected:
                self.spells.append(spell.text)
                spell.selected = False

        sd.selected_spell = None

    def set_languages(self, language_list: tuple[InteractiveText, ...]) -> None:
        """Append 'text' attributes from instances in 'language_list' to 'self.languages' if their 'selected' attribute
        is set to 'True'.
        ARGS:
            language_list: tuple with instances of interactive text fields for language selection.
        """
        self.languages.clear()

        for language in language_list:
            if language.selected:
                self.languages.append(language.text)

        sd.clear_language_selection()

    def set_random_selections(self, spell_list: tuple[InteractiveText], language_flag: bool,
                              language_list: tuple[InteractiveText, ...]) -> None:
        """Select and set various additional character attributes like spells and languages for random character creation
        process.
        ARGS:
             spell_list: tuple with instances of interactive text fields for spell selection.
             language_flag: bool to check if character meets minimum requirements for additional languages. Value
                is set in function 'set_language_flag()' from module 'core.rules.py' (See docstring for details).
             language_list: tuple with instances of interactive text fields for language selection.
        """
        magic_classes = CLASS_CATEGORIES["magic_classes"]
        default_spells = CLASS_DATA[self.class_name.lower()]["spells"]
        default_languages = RACE_DATA[self.race_name.lower()]["languages"]

        if self.class_name in magic_classes:
            random.choice(spell_list).selected = True

            for spell in spell_list:
                if spell.text in default_spells:
                    spell.selected = True

            self.set_starting_spell(spell_list)

        for language in default_languages:
            for lang in language_list:
                if language == lang.text:
                    lang.selected = True

        if language_flag:
            random.choice(language_list).selected = True

        self.set_languages(language_list)


    """Inventory and trade related methods."""
    def buy_item(self, item: object, amount: int) -> bool:
        """Buy 'amount' number of instance 'item' of a class from 'item_model' module.
        ARGS:
            item: instance of a class from 'item_model' module, instances are listed in module 'item_instances'.
            amount: number of items to buy.
        RETURN:
            False: not enough money to buy given number of items.
            True: trade successful. Items added to list 'self.items', item weight added to 'self.weight_carried' and
            money subtracted from 'self.money'.
        """
        money: int | float = self.money - (item.cost * amount)
        insufficient_money_message: str = f"\n\tYou do not have enough money to buy {amount} '{item.name}(s)'"

        if money < 0:
            print(insufficient_money_message)
            return False
        else:
            self.modify_weight_carried(item, amount, "add")
            self.set_movement_rate()
            self.money = money

            for i in range(amount):
                self.inventory.append(item)
            return True

    def sell_item(self, item: object, amount: int) -> None:
        """Sell instance 'item' of a class from 'item_model' module.
        ARGS:
            item: instance of a class from 'item_model' module, instances are listed in module 'item_instances'.
            amount: number of items to sell.
        """
        self.modify_weight_carried(item, amount, "remove")
        self.set_movement_rate()
        self.money += item.cost * amount
        for i in range(amount):
            self.inventory.remove(item)


    """Equip/unequip methods.""" # TODO works only for armor right now.
    def equip_item(self, item: object) -> None:
        """Equip instance 'item' from inventory and move previously equipped item to inventory.
        ARGS:
            item: instance of a class from 'item_model' module, instances are listed in module 'item_instances'.
        """
        item_index: int = self.inventory.index(item)
        equip = self.inventory.pop(item_index)

        if not equip.shield:
            if self.armor != item_inst.NO_ARMOR:
                self.unequip_item(self.armor)
                self.armor = equip
            else:
                self.armor = equip

        else:
            if self.shield != item_inst.NO_SHIELD:
                self.unequip_item(self.shield)
                self.shield = equip
            else:
                self.shield = equip

        self.set_armor_class()
        self.set_movement_rate()

    def unequip_item(self, item: object) -> None:
        """Unequip instance 'item' and move it to inventory. Set 'self.armor' and 'self.shield' to instances 'no_armor'
        and 'no_shield' if no other item is equipped.
        ARGS:
            item: instance of a class from 'item_model' module, instances are listed in module 'item_instances'.
        """
        self.inventory.append(item)
        if not item.shield:
            self.armor = item_inst.NO_ARMOR
        else:
            self.shield = item_inst.NO_SHIELD
        self.set_armor_class()
        self.set_movement_rate()

    def modify_weight_carried(self, item: object, amount: int, add_remove: str) -> None:
        """Change 'self.weight_carried' by adding/subtracting 'item.weight', taking following race-specific modifiers
        into account:
        HALFLINGS: instances of class 'Armor' are calculated with 1/4 of the weight.

        NOTE: Method has to be called whenever any item transaction from/to the character occurs.

        ARGS:
            item: instance of a class from 'item_model' module, instances are listed in module 'item_instances'.
            amount: amount: number of items to add/remove.
            add_remove: keyword string to switch between addition and subtraction of item weight from 'self.weight_carried'.
                "add": addition of items to character.
                "remove": subtraction of item from character.
        """
        # Halfling armor weight modifier.
        modified_halfling_armor_weight: float = item.weight * 0.25

        if add_remove == "add":
            if isinstance(item, Armor) and self.race_name == "Halfling":
                self.weight_carried += modified_halfling_armor_weight * amount
            else:
                self.weight_carried += item.weight * amount

        elif add_remove == "remove":
            if isinstance(item, Armor) and self.race_name == "Halfling":
                self.weight_carried -= modified_halfling_armor_weight * amount
            else:
                self.weight_carried -= item.weight * amount


    """Save/load character related methods."""
    def serialize(self) -> dict[str, Any]:
        """Convert the character object into a serializable dictionary.
        RETURNS:
            dict: dictionary representation of the character, with item instances (armor, shield, weapon, etc.) replaced
                by their name attributes.
        """
        data: dict[str, Any] = self.__dict__.copy()

        data["armor"] = self.armor.name
        data["shield"] = self.shield.name
        data["weapon"] = self.weapon.name

        if self.inventory:
            data["inventory"] = [item.name for item in self.inventory]

        return data

    def deserialize(self, data: dict[str, Any]) -> None:
        """Reconstruct the character object from a dictionary.
        ARGS:
            data (dict): dictionary with character attributes, including item name attributes as strings.
        """
        self.__dict__.update(data)

        self.armor = self.get_item_by_name(data["armor"])
        self.shield = self.get_item_by_name(data["shield"])
        self.weapon = self.get_item_by_name(data["weapon"])

        # Retrieve inventory list with instances via 'name' attribute.
        if data["inventory"]:
            self.inventory = [self.get_item_by_name(item) for item in data["inventory"]]

    @staticmethod
    def get_item_by_name(item: str) -> object:
        """Retrieve an item instance by its name.
        ARGS:
            item: The name of the item to retrieve as string.
        RETURNS:
            object: The matching item instance, or a string error message if not found.
        """
        if item in item_inst.ALL_ITEMS_BY_NAME:
            return item_inst.ALL_ITEMS_BY_NAME[item]
        else:
            return f"{item} not found!"
