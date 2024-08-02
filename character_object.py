from functions import dice_roll
"""Class for character."""


class Character:
    """Set and store race and class specific values as well as final character values."""

    def __init__(self):
        """Set race and class specific values and set character values based on race and class."""
        # Race specific values.
        self.race_name = None
        self.race_description = None
        self.max_hit_die = False
        self.race_specials = []
        self.bonuses = []
        # Class specific values.
        self.class_name = None
        self.class_description = None
        self.class_hit_die = 0
        self.class_specials = []
        self.class_saving_throws = []

        # Final Character values based on race and class.
        self.specials = []
        self.hit_die = 0
        self.next_level_xp = 0
        self.specials = []
        self.saving_throws = {}
        self.hp = 0


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


    def set_specials(self):
        """Get special abilities and add them to list 'self.specials'."""

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
        """Get saving throw values and add them to dict 'self.saving_throws'."""
        # List of saving throws.
        throws_list = ["Death Ray or Poison", "Magic Wands", "Paralysis or Petrify", "Dragon Breath", "Spells"]

        for item in throws_list:
            index = throws_list.index(item)
            self.saving_throws[item] = self.bonuses[index] + self.class_saving_throws[index]


    def set_hp(self, ability_scores):
        """Set HP and adds constitution bonus/penalty from dict 'ability_scores'."""

        if not self.max_hit_die:
            self.hp = dice_roll(1, self.class_hit_die)
        else:
            if self.max_hit_die >= self.class_hit_die:
                self.hp = dice_roll(1, self.class_hit_die)
            else:
                self.hp = dice_roll(1, self.max_hit_die)

        # Adding constitution bonus/penalty to HP:
        self.hp += ability_scores["con"][1]
