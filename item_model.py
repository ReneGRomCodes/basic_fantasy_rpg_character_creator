"""Classes for equipment. Parent class 'Items' for items with basic attributes (name, cost, weight) and collection of
child classes items with specialized attributes (weapons, armor, etc.)."""


class Item:
    """Represent basic items."""

    def __init__(self, name, cost, weight):
        """Initialize attributes 'name', 'cost' in gp (gold pieces) and 'weight' in pounds."""
        self.name = name
        self.cost = cost
        self.weight = weight


class Weapon(Item):
    """Child class to represent weapons"""

    def __init__(self, name, cost, weight, size, damage):
        """Initialize attributes from parent class 'Items', size (string "S", "M" or "L") and 'damage' (int for number
        of sides on the die for the dice roll)"""
        super().__init__(name, cost, weight)
        self.size = size
        self.damage = damage


class Projectile(Item):
    """Child class to represent projectiles for ranged weapons."""
    
    def __init__(self, name, cost, weight, damage, range_list):
        """Initialize attributes from parent class 'Items', size (string "S", "M" or "L"), 'damage' (int for number of
        sides on the die for the dice roll) and list of ranges (int for short, medium and long range)."""
        super().__init__(name, cost, weight)
        self.damage = damage
        self.range_list = range_list  # List for short, medium and long ranges.


class Armor(Item):
    """Child class to represent armor."""

    def __init__(self, name, cost, weight, armor_class):
        """Initialize attributes from parent class 'Items' and 'armor_class'."""
        super().__init__(name, cost, weight)
        self.armor_class = armor_class
