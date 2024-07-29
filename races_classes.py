"""Classes for race and character class values."""


class CharacterRace:
    """Contains race-specific values."""

    def __init__(self):
        """Empty default values."""
        self.race_name = None
        self.description = None
        self.max_hit_die = 0
        self.specials = []
        self.bonuses = []

    def set_race(self, char_race):
        """Set race-specific values based on chosen race."""
        if char_race == "Dwarf":
            self.race_name = "Dwarf"
            self.description = "descr/dwarves.txt"
            self.max_hit_die = False
            self.specials = ["Darkvision 60'",
                             "Detect new construction, shifting walls, slanting passages, traps w/ 1-2 on d6"]
            self.bonuses = [4, 4, 4, 3, 4]
        elif char_race == "Elf":
            self.race_name = "Elf"
            self.description = "descr/elves.txt"
            self.max_hit_die = 6
            self.specials = ["Darkvision 60'"
                             "Detect secret doors 1-2 on d6, 1 on d6 with a cursory look",
                             "Range reduction by 1 for surprise checks"]
            self.bonuses = [0, 2, 1, 0, 2]
        elif char_race == "Halfling":
            self.race_name = "Halfling"
            self.description = "descr/halflings.txt"
            self.max_hit_die = 6
            self.specials = ["+1 attack bonus on ranged weapons",
                             "+1 to initiative die rolls",
                             "Hide (10% chance to be detected outdoors, 30% chance to be detected indoors"]
            self.bonuses = [4, 4, 4, 3, 4]
        elif char_race == "Human":
            self.race_name = "Human"
            self.description = "descr/humans.txt"
            self.max_hit_die = False
            self.specials = ["+10% to all earned XP"]
            self.bonuses = [0, 0, 0, 0, 0]
        else:
            raise ValueError("Invalid race")


class CharacterClass:
    """Contains class-specific values."""

    def __init__(self):
        """Empty default values."""
        self.class_name = None
        self.description = None
        self.hit_die = 0
        self.next_level_xp = 0
        self.specials = []
        self.saving_throws = []

    def set_class(self, char_class):
        """Set class-specific values based on chosen class."""
        if char_class == "Cleric":
            self.class_name = "Cleric"
            self.description = "descr/cleric.txt"
            self.hit_die = 6
            self.next_level_xp = 1500
            self.specials = ["Turn the Undead"]
            self.saving_throws = [11, 12, 14, 16, 15]

        elif char_class == "Fighter":
            self.class_name = "Fighter"
            self.description = "descr/fighter.txt"
            self.hit_die = 8
            self.next_level_xp = 2000
            self.specials = [False]
            self.saving_throws = [12, 13, 14, 15, 17]

        elif char_class == "Magic_User":
            self.class_name = "Magic-User"
            self.description = "descr/magic-user.txt"
            self.hit_die = 4
            self.next_level_xp = 2500
            self.specials = [False]
            self.saving_throws = [13, 14, 13, 16, 15]

        elif char_class == "Thief":
            self.class_name = "Thief"
            self.description = "descr/thief.txt"
            self.hit_die = 4
            self.next_level_xp = 1250
            self.specials = ["Sneak Attack", "Thief Abilities"]
            self.saving_throws = [13, 14, 13, 16, 15]
        else:
            raise ValueError("Invalid class")
