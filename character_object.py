from functions import dice_roll, get_ability_score
"""Class for character."""


class Character:
    """Set and store race, class and character specific attributes as well as final character values."""

    def __init__(self):
        """Set race and class specific attributes and set character values based on race and class."""
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
        self.armor_class = 11  # Default for no armor.
        self.attack_bonus = 1  # Default for level 1 characters.
        self.specials = []
        self.hit_die = 0
        self.next_level_xp = 0
        self.specials = []
        self.saving_throws = {}
        self.hp = 0
        self.carrying_capacity = {}
        self.money = 0


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

        elif class_selection == "Thief":
            self.class_name = "Thief"
            self.class_description = "descr/thief.txt"
            self.class_hit_die = 4
            self.next_level_xp = 1250
            self.class_specials = ["Sneak Attack", "Thief Abilities"]
            self.class_saving_throws = [13, 14, 13, 16, 15]


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

        # Adding constitution bonus/penalty to HP:
        self.hp += self.abilities["con"][1]


    def set_carrying_capacity(self):
        """Set dict 'self.carrying_capacity' based on ability score for "str" and race."""
        check_str = self.abilities["str"][0]
        # Keys for 'self.carrying_capacity'
        cap_light_key = "Light Load"
        cap_heavy_key = "Heavy Load"

        # Basic carrying capacities for Halflings.
        if self.race_name == "Halfling":
            if check_str <= 3:
                self.carrying_capacity = {
                    cap_light_key: 20,
                    cap_heavy_key: 40,
                }
            elif check_str <= 5:
                self.carrying_capacity = {
                    cap_light_key: 30,
                    cap_heavy_key: 60,
                }
            elif check_str <= 8:
                self.carrying_capacity = {
                    cap_light_key: 40,
                    cap_heavy_key: 80,
                }
            elif check_str <= 12:
                self.carrying_capacity = {
                    cap_light_key: 50,
                    cap_heavy_key: 100,
                }
            elif check_str <= 15:
                self.carrying_capacity = {
                    cap_light_key: 55,
                    cap_heavy_key: 110,
                }
            elif check_str <= 17:
                self.carrying_capacity = {
                    cap_light_key: 60,
                    cap_heavy_key: 120,
                }
            else:
                self.carrying_capacity = {
                    cap_light_key: 65,
                    cap_heavy_key: 130,
                }

        # Basic carrying capacity for all other races:
        else:
            if check_str <= 3:
                self.carrying_capacity = {
                    cap_light_key: 25,
                    cap_heavy_key: 60,
                }
            elif check_str <= 5:
                self.carrying_capacity = {
                    cap_light_key: 35,
                    cap_heavy_key: 90,
                }
            elif check_str <= 8:
                self.carrying_capacity = {
                    cap_light_key: 50,
                    cap_heavy_key: 120,
                }
            elif check_str <= 12:
                self.carrying_capacity = {
                    cap_light_key: 60,
                    cap_heavy_key: 150,
                }
            elif check_str <= 15:
                self.carrying_capacity = {
                    cap_light_key: 65,
                    cap_heavy_key: 165,
                }
            elif check_str <= 17:
                self.carrying_capacity = {
                    cap_light_key: 70,
                    cap_heavy_key: 180,
                }
            else:
                self.carrying_capacity = {
                    cap_light_key: 80,
                    cap_heavy_key: 195,
                }


    def set_starting_money(self):
        """Set starting value for attribute 'self.money'"""
        self.money = dice_roll(3, 6) * 10
