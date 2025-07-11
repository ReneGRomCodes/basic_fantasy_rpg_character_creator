"""
Classes for equipment. Parent class 'Items' for items with basic attributes (name, cost, weight) and collection of
child classes items with specialized attributes (weapons, armor, etc.). Items are instantiated in 'item_instances.py'.
"""


class Item:
    """Represent basic items."""

    def __init__(self, name, cost, weight):
        """Initialize attributes string 'name', int 'cost' in gp (gold pieces) and int 'weight' in pounds."""
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


class RangedWeapon(Weapon):
    """Child class of 'Weapon' to represent ranged and throwable weapons."""

    def __init__(self, name, cost, weight, size, damage, range_list, ammo=False, throw=False):
        """Initialize attributes from parent class 'Weapons'.

        ARGS:
            cost: int
            size: string "S", "M" or "L"
            damage: int for number of sides on the die for the dice roll. NOTE: 0 for weapons that need ammo.
            range_list: tuple of ints for short, medium and long range.
            ammo: tuple of projectile instances for the weapon if needed. Default = False
            throw: bool if weapon is throwable. Default = False
        """
        super().__init__(name, cost, weight, size, damage)
        self.range_list = range_list
        self.ammo = ammo
        self.throw = throw


class Projectile(Item):
    """Child class to represent projectiles for ranged weapons and grenade-like items."""
    
    def __init__(self, name, cost, weight, damage, splash_damage=False, range_list=False, throw=False):
        """Initialize attributes from parent class 'Items'.

        ARGS:
            damage: int for number of sides on the die for the dice roll.

        ARGS that apply to grenade-like items and are 'default=False' for other projectiles:
            splash_damage: int for number of sides on the die for the dice roll for damage within 5 feet of the point of
                           impact.
            range_list: tuple of ints for short, medium and long range.
            throw: bool if weapon is throwable.
        """
        super().__init__(name, cost, weight)
        self.damage = damage
        # Attributes specific for grenade-like items.
        self.splash_damage = splash_damage
        self.range_list = range_list
        self.throw = throw


class Armor(Item):
    """Child class to represent armor."""

    def __init__(self, name, cost, weight, armor_class, shield = False):
        """Initialize attributes from parent class 'Items'.

        ARGS:
            armor_class: int for AC.
            shield: bool to indicate if item is shield (True) or not (False). Default = False.
        """
        super().__init__(name, cost, weight)
        self.armor_class = armor_class
        self.shield = shield
