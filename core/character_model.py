from core.rules import dice_roll, get_ability_score
import item_instances as item_inst
"""Class for character."""


class Character:
    """Represent a character."""

    def __init__(self) -> None:
        """Initialize race and class specific attributes and character values."""
        # Race specific attributes.
        self.race_name: str | None = None
        self.max_hit_die: int | False = False
        self.race_specials: tuple[str, ...] = ()
        self.bonuses: tuple[int, ...] = ()
        # Class specific attributes.
        self.class_name: str | None = None
        self.class_hit_die: int = 0
        self.class_specials: tuple[str, ...] = ()
        self.class_saving_throws: tuple[int, ...] = ()

        # Character attributes. Values set based on race and class.
        self.name: str | None = None
        self.abilities: dict[str, list[int]] = {}
        self.armor_class: int | None = None
        self.attack_bonus: int = 1  # Default attack bonus of +1 for Lvl characters.
        self.specials = ()
        self.hit_die: int = 0
        self.xp: int = 0
        self.level: int = 1
        self.next_level_xp: int = 0
        self.saving_throws: dict[str, int] = {}
        self.spells: str | False = False
        self.hp: int = 0
        # Attributes related to inventory.
        self.carrying_capacity: dict[str, int] = {}
        self.weight_carried: int | float = 0
        self.money: int | float = 0
        self.inventory: list = []
        self.armor: object = item_inst.no_armor
        self.shield: object = item_inst.no_shield
        self.weapon: object = item_inst.no_weapon

    def set_race(self, race_selection: str) -> None:
        """Set race-specific values based on chosen race."""
        self.race_name = race_selection

        if race_selection == "Dwarf":
            self.max_hit_die = False
            self.race_specials = ("Darkvision 60'",
                                  "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6")
            self.bonuses = (4, 4, 4, 3, 4)
        elif race_selection == "Elf":
            self.max_hit_die = 6
            self.race_specials = ("Darkvision 60'",
                                  "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                                  "Range reduction by 1 for surprise checks")
            self.bonuses = (0, 2, 1, 0, 2)
        elif race_selection == "Halfling":
            self.max_hit_die = 6
            self.race_specials = ("+1 attack bonus on ranged weapons",
                                  "+1 to initiative die rolls",
                                  "Hide (10% chance to be detected outdoors, 30% chance to be detected indoors")
            self.bonuses = (4, 4, 4, 3, 4)
        elif race_selection == "Human":
            self.max_hit_die = False
            self.race_specials = ("+10% to all earned XP", )
            self.bonuses = (0, 0, 0, 0, 0)

    def set_class(self, class_selection: str) -> None:
        """Set class-specific values based on chosen class."""
        self.class_name = class_selection

        if class_selection == "Cleric":
            self.class_hit_die = 6
            self.next_level_xp = 1500
            self.class_specials = ("Turn the Undead", )
            self.class_saving_throws = (11, 12, 14, 16, 15)
            self.spells = "No Spells"
        elif class_selection == "Fighter":
            self.class_hit_die = 8
            self.next_level_xp = 2000
            self.class_specials = ()
            self.class_saving_throws = (12, 13, 14, 15, 17)
        elif class_selection == "Magic-User":
            self.class_hit_die = 4
            self.next_level_xp = 2500
            self.class_specials = ()
            self.class_saving_throws = (13, 14, 13, 16, 15)
            self.spells = "Read Magic"
            self.inventory.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight
        elif class_selection == "Thief":
            self.class_hit_die = 4
            self.next_level_xp = 1250
            self.class_specials = ("Sneak Attack", "Thief Abilities")
            self.class_saving_throws = (13, 14, 13, 16, 15)
        # Elf specific combination classes.
        elif class_selection == "Fighter/Magic-User":
            self.class_hit_die = 6
            self.next_level_xp = 4500
            self.class_specials = ()
            self.class_saving_throws = (13, 14, 14, 16, 17)
            self.spells = "Read Magic"
            self.inventory.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight
        elif class_selection == "Magic-User/Thief":
            self.class_hit_die = 4
            self.next_level_xp = 3750
            self.class_specials = ("Sneak Attack", "Thief Abilities")
            self.class_saving_throws = (13, 14, 13, 16, 15)
            self.spells = "Read Magic"
            self.inventory.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight

    def reset_character(self) -> None:
        """Reset values that may not be overwritten when creating a new character."""
        self.spells = False
        self.inventory = []
        self.weight_carried = 0
        self.specials = ()

    def set_name(self, char_name: str) -> None:
        """Set name for character."""
        self.name = char_name

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

        if not self.max_hit_die:
            self.hp = dice_roll(1, self.class_hit_die)
        else:
            if self.max_hit_die >= self.class_hit_die:
                self.hp = dice_roll(1, self.class_hit_die)
            else:
                self.hp = dice_roll(1, self.max_hit_die)

        # Adding constitution bonus/penalty to HP or set to minimum value of 1:
        if self.hp + self.abilities["con"][1] < 1:
            self.hp = 1
        else:
            self.hp += self.abilities["con"][1]

    def set_armor_class(self) -> None:
        """Set armor class based on equipped armor and shield."""
        self.armor_class = self.armor.armor_class + self.shield.armor_class

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

    # Inventory and trade related methods.
    def buy_item(self, item: object, amount: int) -> bool:
        """Buy 'amount' number of instance 'item' of a class from 'item_model' module.
        ARGS:
            item: instance of a class from 'item_model' module, instances are listed in module 'item_instances'.
            amount: number of items to buy.
        RETURN:
            False: not enough money to buy given amount of items.
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
            self.weight_carried += weight_total
            self.money = money
            # Add each item individually to list 'self.items'
            for i in range(amount):
                self.inventory.append(item)
            return True

    def sell_item(self, item: object, amount: int) -> None:
        """Sell instance 'item' of a class from 'item_model' module."""
        self.weight_carried -= item.weight * amount
        self.money += item.cost * amount
        for i in range(amount):
            self.inventory.remove(item)

    # Equip/unequip methods. TODO works only for armor right now.
    def equip_item(self, item: object) -> None:
        """Equip instance 'item' from inventory and move previously equipped item to inventory."""
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

    def unequip_item(self, item: object) -> None:
        """Unequip instance 'item' and move it to inventory. Set 'self.armor' and 'self.shield' to instances 'no_armor'
        and 'no_shield' if no other item is equipped."""
        self.inventory.append(item)
        if not item.shield:
            self.armor = item_inst.no_armor
        else:
            self.shield = item_inst.no_shield
        self.set_armor_class()
