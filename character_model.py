from functions import dice_roll, get_ability_score
import item_instances as item_inst
"""Class for character."""


class Character:
    """Represent a character."""

    def __init__(self):
        """Initialize race and class specific attributes and character values."""
        # Race specific attributes.
        self.race_name = None
        self.race_description = None
        self.max_hit_die = False
        self.race_specials = []
        self.bonuses = []
        # Class specific attributes.
        self.class_name = None
        self.class_description = None
        self.class_hit_die = 0
        self.class_specials = []
        self.class_saving_throws = []

        # Character attributes. Values set based on race and class.
        self.name = None
        self.abilities = {}
        self.armor_class = None
        self.attack_bonus = 1  # Default attack bonus of +1 for Lvl characters.
        self.specials = []
        self.hit_die = 0
        self.next_level_xp = 0
        self.specials = []
        self.saving_throws = {}
        self.spells = False
        self.hp = 0
        # Attributes related to inventory.
        self.carrying_capacity = {}
        self.weight_carried = 0
        self.money = 0
        self.items = []
        self.armor = item_inst.no_armor
        self.shield = item_inst.no_shield
        self.weapon = item_inst.no_weapon

    def set_race(self, race_selection):
        """Set race-specific values based on chosen race."""
        if race_selection == "Dwarf":
            self.race_name = "Dwarf"
            self.race_description = "descr/dwarves.txt"
            self.max_hit_die = False
            self.race_specials = ["Darkvision 60'",
                                  "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6"]
            self.bonuses = [4, 4, 4, 3, 4]
        elif race_selection == "Elf":
            self.race_name = "Elf"
            self.race_description = "descr/elves.txt"
            self.max_hit_die = 6
            self.race_specials = ["Darkvision 60'",
                                  "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                                  "Range reduction by 1 for surprise checks"]
            self.bonuses = [0, 2, 1, 0, 2]
        elif race_selection == "Halfling":
            self.race_name = "Halfling"
            self.race_description = "descr/halflings.txt"
            self.max_hit_die = 6
            self.race_specials = ["+1 attack bonus on ranged weapons",
                                  "+1 to initiative die rolls",
                                  "Hide (10% chance to be detected outdoors, 30% chance to be detected indoors"]
            self.bonuses = [4, 4, 4, 3, 4]
        elif race_selection == "Human":
            self.race_name = "Human"
            self.race_description = "descr/humans.txt"
            self.max_hit_die = False
            self.race_specials = ["+10% to all earned XP"]
            self.bonuses = [0, 0, 0, 0, 0]

    def set_class(self, class_selection):
        """Set class-specific values based on chosen class."""
        if class_selection == "Cleric":
            self.class_name = "Cleric"
            self.class_description = "descr/cleric.txt"
            self.class_hit_die = 6
            self.next_level_xp = 1500
            self.class_specials = ["Turn the Undead"]
            self.class_saving_throws = [11, 12, 14, 16, 15]
            self.spells = "None"
        elif class_selection == "Fighter":
            self.class_name = "Fighter"
            self.class_description = "descr/fighter.txt"
            self.class_hit_die = 8
            self.next_level_xp = 2000
            self.class_specials = [False]
            self.class_saving_throws = [12, 13, 14, 15, 17]
        elif class_selection == "Magic-User":
            self.class_name = "Magic-User"
            self.class_description = "descr/magic-user.txt"
            self.class_hit_die = 4
            self.next_level_xp = 2500
            self.class_specials = [False]
            self.class_saving_throws = [13, 14, 13, 16, 15]
            self.spells = "Read Magic"
            self.items.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight
        elif class_selection == "Thief":
            self.class_name = "Thief"
            self.class_description = "descr/thief.txt"
            self.class_hit_die = 4
            self.next_level_xp = 1250
            self.class_specials = ["Sneak Attack", "Thief Abilities"]
            self.class_saving_throws = [13, 14, 13, 16, 15]
        # Elf specific combination classes.
        elif class_selection == "Fighter/Magic-User":
            self.class_name = "Fighter/Magic-User"
            self.class_description = "descr/fighter_magic-user.txt"
            self.class_hit_die = 6
            self.next_level_xp = 4500
            self.class_specials = [False]
            self.class_saving_throws = [13, 14, 14, 16, 17]
            self.spells = "Read Magic"
            self.items.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight
        elif class_selection == "Magic-User/Thief":
            self.class_name = "Magic-User/Thief"
            self.class_description = "descr/magic-user_thief.txt"
            self.class_hit_die = 4
            self.next_level_xp = 3750
            self.class_specials = ["Sneak Attack", "Thief Abilities"]
            self.class_saving_throws = [13, 14, 13, 16, 15]
            self.spells = "Read Magic"
            self.items.append(item_inst.spellbook)
            self.weight_carried += item_inst.spellbook.weight

    def reset_character(self):
        """Reset values that may not be overwritten when creating a new character."""
        self.spells = False
        self.items = []
        self.weight_carried = 0

    def set_name(self, char_name):
        """Set name for character."""
        self.name = char_name

    def build_ability_dict(self):
        """Build attribute dictionary 'self.abilities' for character abilities."""
        ability_names = ["str", "dex", "con", "int", "wis", "cha"]

        for item in ability_names:
            # Adding default INT bonus of +1.
            if item == "int":
                self.abilities[item] = get_ability_score()
                self.abilities[item][1] += 1
            else:
                self.abilities[item] = get_ability_score()

    def set_specials(self):
        """Get special abilities and add them to attribute list 'self.specials'."""

        # Set list to empty to not contain any values if previous characters have been created.
        self.specials = []

        for v in self.race_specials:
            if not v:
                pass
            else:
                self.specials.append(v)

        for v in self.class_specials:
            if not v:
                pass
            else:
                self.specials.append(v)

    def set_saving_throws(self):
        """Get saving throw values and add them to attribute dict 'self.saving_throws'."""
        # List of saving throws.
        throws_list = ["Death Ray or Poison", "Magic Wands", "Paralysis or Petrify", "Dragon Breath", "Spells"]

        for item in throws_list:
            index = throws_list.index(item)
            self.saving_throws[item] = self.bonuses[index] + self.class_saving_throws[index]

    def set_hp(self):
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

    def set_armor_class(self):
        """Set armor class based on equipped armor and shield."""
        self.armor_class = self.armor.armor_class + self.shield.armor_class

    def set_carrying_capacity(self):
        """Set dict 'self.carrying_capacity' based on race and ability score and bonus for "strength"."""
        strength = self.abilities["str"][0]

        # Keys for 'self.carrying_capacity'
        cap_light_key = "Light Load"
        cap_heavy_key = "Heavy Load"

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
    def buy_item(self, item):
        """Buy instance 'item' of a class from 'item_model' module and return 'True' if trade was successful, 'False'
        otherwise."""
        money = self.money - item.cost
        insufficient_money = f"\n\tYou do not have enough money to buy '{item.name}'"
        if money < 0:
            print(insufficient_money)
            return False
        else:
            self.items.append(item)
            self.weight_carried += item.weight
            self.money = money
            return True

    def sell_item(self, item):
        """Sell instance 'item' of a class from 'item_model' module."""
        self.items.remove(item)
        self.weight_carried -= item.weight
        self.money += item.cost

    # Equip/unequip methods. TODO works only for armor right now.
    def equip_item(self, item):
        """Equip instance 'item' from inventory."""
        item_index = self.items.index(item)
        equip = self.items.pop(item_index)
        if not equip.shield:
            self.armor = equip
        else:
            self.shield = equip
        self.set_armor_class()

    def unequip_item(self, item):
        """Unequip instance 'item' and move it to inventory."""
        self.items.append(item)
        if not item.shield:
            self.armor = item_inst.no_armor
        else:
            self.shield = item_inst.no_shield
        self.set_armor_class()
