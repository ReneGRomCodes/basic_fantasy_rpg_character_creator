"""
Class for character.
"""
import random
from typing import Any

from gui.screen_objects import InteractiveText
from gui.shared_data import ui_shared_data as uisd

import core.items.item_instances as item_inst
from .rules import dice_roll, get_ability_score, get_class_categories, get_race_class_defaults
from .items.item_objects import Armor
from .shared_data import shared_data as sd


class Character:
    """Represent a character."""

    def __init__(self) -> None:
        """Initialize race and class-specific attributes and character values."""
        # Race specific attributes.
        self.race_name: str | None = None
        self.race_specials: tuple[str, ...] = ()
        self.bonuses: tuple[int, ...] = ()
        # Class specific attributes.
        self.class_name: str | None = None
        self.class_specials: tuple[str, ...] = ()
        self.class_saving_throws: tuple[int, ...] = ()

        # Race/class maximum hit die. Attributes only used to set characters maximum hit die.
        self.race_hit_die: int | False = False
        self.class_hit_die: int | False = False

        # Character attributes. Values set based on race and class.
        self.name: str | None = None
        self.abilities: dict[str, list[int]] = {}
        self.armor_class: int | None = None
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
        self.movement: int | None = None
        # Attributes related to inventory.
        self.carrying_capacity: dict[str, int] = {}
        self.weight_carried: int | float = 0
        self.money: int | float = 0
        self.inventory: list[object] = []
        self.armor: object = item_inst.armors["no_armor"]
        self.shield: object = item_inst.armors["no_shield"]
        self.weapon: object = item_inst.weapons["no_weapon"]

    def set_race(self, race_selection: str) -> None:
        """Set race-specific values based on chosen race.
        ARGS:
            race_selection: string representing the race chosen by the player.
        """
        self.race_name = race_selection

        if race_selection == "Dwarf":
            self.race_hit_die = False
            self.race_specials = ("Darkvision 60'",
                                  "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6")
            self.bonuses = (4, 4, 4, 3, 4)
        elif race_selection == "Elf":
            self.race_hit_die = 6
            self.race_specials = ("Darkvision 60'",
                                  "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                                  "Range reduction by 1 for surprise checks")
            self.bonuses = (0, 2, 1, 0, 2)
        elif race_selection == "Halfling":
            self.race_hit_die = 6
            self.race_specials = ("+1 attack bonus on ranged weapons",
                                  "+1 to initiative die rolls",
                                  "Hide (10% chance to be detected outdoors, 30% chance to be detected indoors")
            self.bonuses = (4, 4, 4, 3, 4)
        elif race_selection == "Human":
            self.race_hit_die = False
            self.race_specials = ("+10% to all earned XP", )
            self.bonuses = (0, 0, 0, 0, 0)

    def set_class(self, class_selection: str) -> None:
        """Set class-specific values based on chosen class.
        ARGS:
            class_selection: string representing the class chosen by the player.
        """
        self.class_name = class_selection

        if class_selection == "Cleric":
            self.class_hit_die = 6
            self.next_level_xp = 1500
            self.class_specials = ("Turn the Undead", )
            self.class_saving_throws = (11, 12, 14, 16, 15)
            self.spells = ["No Spells"]
            self.inventory = []
            self.weight_carried = 0
        elif class_selection == "Fighter":
            self.class_hit_die = 8
            self.next_level_xp = 2000
            self.class_specials = ()
            self.class_saving_throws = (12, 13, 14, 15, 17)
            self.inventory = []
            self.weight_carried = 0
        elif class_selection == "Magic-User":
            self.class_hit_die = 4
            self.next_level_xp = 2500
            self.class_specials = ()
            self.class_saving_throws = (13, 14, 13, 16, 15)
            self.inventory.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight
        elif class_selection == "Thief":
            self.class_hit_die = 4
            self.next_level_xp = 1250
            self.class_specials = ("Sneak Attack", "Thief Abilities")
            self.class_saving_throws = (13, 14, 13, 16, 15)
            self.inventory = []
            self.weight_carried = 0
        # Elf-specific combination classes.
        elif class_selection == "Fighter/Magic-User":
            self.class_hit_die = 6
            self.next_level_xp = 4500
            self.class_specials = ()
            self.class_saving_throws = (13, 14, 14, 16, 17)
            self.inventory = [item_inst.spellbook]
            self.weight_carried += item_inst.spellbook.weight
        elif class_selection == "Magic-User/Thief":
            self.class_hit_die = 4
            self.next_level_xp = 3750
            self.class_specials = ("Sneak Attack", "Thief Abilities")
            self.class_saving_throws = (13, 14, 13, 16, 15)
            self.inventory = [item_inst.spellbook]
            self.weight_carried += item_inst.spellbook.weight

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
        """Collected method calls to set multiple attributes.
        Used in 'state_manager.py' and 'event_handlers.py'."""
        self.set_max_hit_die()
        self.set_saving_throws()
        self.set_specials()
        self.set_hp()
        self.set_armor_class()
        self.set_carrying_capacity()
        self.set_movement_rate()

    def set_max_hit_die(self) -> None:
        """Set 'self.max_hit_die' based on chosen race and class."""
        if self.race_hit_die and self.class_hit_die > self.race_hit_die:
            self.max_hit_die = self.race_hit_die
        else:
            self.max_hit_die = self.class_hit_die

    def set_specials(self) -> None:
        """Get special abilities and add them to attribute list 'self.specials'."""
        self.specials = self.race_specials + self.class_specials

    def set_saving_throws(self) -> None:
        """Get saving throw values and add them to attribute dict 'self.saving_throws'."""
        # List of saving throws.
        throws: tuple[str, ...] = ("Death Ray or Poison", "Magic Wands", "Paralysis or Petrify", "Dragon Breath", "Spells")

        for index, item in enumerate(throws):
            index = throws.index(item)
            self.saving_throws[item] = self.bonuses[index] + self.class_saving_throws[index]

    def set_hp(self) -> None:
        """Set HP and adds constitution bonus/penalty."""
        # Roll for base hp with max hit die.
        self.hp = dice_roll(1, self.max_hit_die)

        # Adding constitution bonus/penalty to HP or set to minimum value of 1:
        if self.hp + self.abilities["con"][1] < 1:
            self.hp = 1
        else:
            self.hp += self.abilities["con"][1]

    def set_armor_class(self) -> None:
        """Set armor class based on equipped armor and shield."""
        # Add AC of worn armor, shield and dexterity bonus/penalty.
        self.armor_class = self.armor.armor_class + self.shield.armor_class + self.abilities["dex"][1]

    def set_carrying_capacity(self) -> None:
        """Set dict 'self.carrying_capacity' based on race and ability score and bonus for "strength"."""
        strength: int = self.abilities["str"][0]

        # Keys for 'self.carrying_capacity'
        cap_light_key: str = "Light Load"
        cap_heavy_key: str = "Heavy Load"

        # Basic carrying capacities for Halflings.
        if self.race_name == "Halfling":
            if strength <= 3:
                self.carrying_capacity = {cap_light_key: 20, cap_heavy_key: 40, }
            elif strength <= 5:
                self.carrying_capacity = {cap_light_key: 30, cap_heavy_key: 60, }
            elif strength <= 8:
                self.carrying_capacity = {cap_light_key: 40, cap_heavy_key: 80, }
            elif strength <= 12:
                self.carrying_capacity = {cap_light_key: 50, cap_heavy_key: 100, }
            elif strength <= 15:
                self.carrying_capacity = {cap_light_key: 55, cap_heavy_key: 110, }
            elif strength <= 17:
                self.carrying_capacity = {cap_light_key: 60, cap_heavy_key: 120, }
            else:
                self.carrying_capacity = {cap_light_key: 65, cap_heavy_key: 130, }

        # Basic carrying capacity for all other races:
        else:
            if strength <= 3:
                self.carrying_capacity = {cap_light_key: 25, cap_heavy_key: 60, }
            elif strength <= 5:
                self.carrying_capacity = {cap_light_key: 35, cap_heavy_key: 90, }
            elif strength <= 8:
                self.carrying_capacity = {cap_light_key: 50, cap_heavy_key: 120, }
            elif strength <= 12:
                self.carrying_capacity = {cap_light_key: 60, cap_heavy_key: 150, }
            elif strength <= 15:
                self.carrying_capacity = {cap_light_key: 65, cap_heavy_key: 165, }
            elif strength <= 17:
                self.carrying_capacity = {cap_light_key: 70, cap_heavy_key: 180, }
            else:
                self.carrying_capacity = {cap_light_key: 80, cap_heavy_key: 195, }

    def set_movement_rate(self) -> None:
        """Set movement rate in feet based on encumbrance ('self.carrying_capacity') and worn armor. Has to be called
        whenever changes to 'self.weight_carried' are made in other methods."""
        # Movement rates for lightly loaded characters.
        if self.weight_carried <= self.carrying_capacity["Light Load"]:
            if self.armor == item_inst.no_armor:
                self.movement: int = 40
            elif self.armor == item_inst.leather_armor:
                self.movement: int = 30
            # Movement rate for armor heavier than leather armor.
            else:
                self.movement: int = 20
        # Movement rates for heavily loaded characters.
        elif self.weight_carried <= self.carrying_capacity["Heavy Load"]:
            if self.armor == item_inst.no_armor:
                self.movement: int = 30
            elif self.armor == item_inst.leather_armor:
                self.movement: int = 20
            # Movement rate for armor heavier than leather armor.
            else:
                self.movement: int = 10

    def set_starting_spell(self, spell_list: tuple[InteractiveText, ...]) -> None:
        """Append 'text' attributes from instances in 'spell_list' to 'self.spells' if their 'selected' attribute is set
        to 'True'.
        ARGS:
            spell_list: tuple with instances of interactive text fields for spell selection.
        """
        # Ensure that 'self.spells' list is empty before appending selected languages to it.
        self.spells.clear()

        for spell in spell_list:
            if spell.selected:
                self.spells.append(spell.text)
                # Reset spell to default 'False'.
                spell.selected = False

        # Reset 'selected_spell' attribute in 'shared_data'.
        sd.selected_spell = None

    def set_languages(self, language_list: tuple[InteractiveText, ...]) -> None:
        """Append 'text' attributes from instances in 'language_list' to 'self.languages' if their 'selected' attribute
        is set to 'True'.
        ARGS:
            language_list: tuple with instances of interactive text fields for language selection.
        """
        # Ensure that 'self.languages' list is empty before appending selected languages to it.
        self.languages.clear()

        for language in language_list:
            if language.selected:
                self.languages.append(language.text)

        # Reset all language selection related data.
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
        # Dicts/sets for checks of default values for various races/classes.
        magic_classes = get_class_categories()[1]
        default_spells, default_languages = get_race_class_defaults()

        # Choose default and random spell for magic using classes.
        if self.class_name in magic_classes:
            # Random spell selection.
            random.choice(spell_list).selected = True
            # Check for and retrieve default spell.
            for spell in spell_list:
                if spell.text in default_spells[self.class_name.lower()]:
                    spell.selected = True
            # Set selected spells.
            self.set_starting_spell(spell_list)

        # Set default language for character's race.
        for language in default_languages[self.race_name.lower()]:
            for lang in language_list:
                if language == lang.text:
                    lang.selected = True
        # Choose additional language if requirements are met (See docstring for details).
        if language_flag:
            random.choice(language_list).selected = True
        # Set selected languages.
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
        weight_total: int | float = item.weight * amount
        insufficient_money_message: str = f"\n\tYou do not have enough money to buy {amount} '{item.name}(s)'"

        if money < 0:
            print(insufficient_money_message)
            return False
        else:
            self.modify_weight_carried(item, amount, "add")
            self.set_movement_rate()
            self.money = money
            # Add each item individually to list 'self.items'
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
            if self.armor != item_inst.no_armor:
                self.unequip_item(self.armor)
                self.armor = equip
            else:
                self.armor = equip

        else:
            if self.shield != item_inst.no_shield:
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
            self.armor = item_inst.no_armor
        else:
            self.shield = item_inst.no_shield
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
        # Copy '__dict__' as dict to 'data'.
        data: dict[str, Any] = self.__dict__.copy()

        # Add 'name' attributes of item instances as strings to 'data'.
        data["armor"] = self.armor.name
        data["shield"] = self.shield.name
        data["weapon"] = self.weapon.name

        # Add inventory items as strings to 'data'.
        if self.inventory:
            data["inventory"] = [item.name for item in self.inventory]

        return data

    def deserialize(self, data: dict[str, Any]) -> None:
        """Reconstruct the character object from a dictionary.
        ARGS:
            data (dict): dictionary with character attributes, including item name attributes as strings.
        """
        # Update '__dict__' by retrieving values from dict 'data'.
        self.__dict__.update(data)

        # Retrieve item instances via 'name' attribute.
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
        if item in item_inst.all_items_by_name:
            return item_inst.all_items_by_name[item]
        else:
            return f"{item} not found!"
