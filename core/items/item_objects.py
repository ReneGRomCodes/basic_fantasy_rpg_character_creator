"""
Classes for equipment. Parent class 'Items' for items with basic attributes (name, cost, weight) and collection of
child classes items with specialized attributes (weapons, armor, etc.). Items are instantiated in 'item_instances.py'.
"""


class Item:
    """Represent basic items."""

    def __init__(self, name: str, cost: int | float, weight: int | float) -> None:
        """Initialize attributes string 'name', int 'cost' in gp (gold pieces) and int 'weight' in pounds.
        ARGS:
            name: item name as string.
            cost: cost in gp (gold pieces) as int or float.
            weight: weight as int or float.
        """
        self.name: str = name
        self.cost: int | float = cost
        self.weight: int | float = weight


class Weapon(Item):
    """Child class to represent weapons"""

    def __init__(self, name: str, cost: int | float, weight: int | float, size: str | None, damage: int) -> None:
        """Initialize attributes from parent class 'Items', size (string "S", "M" or "L") and 'damage' (int for number
        of sides on the die for the dice roll).
        ARGS:
            name: item name as string.
            cost: cost in gp (gold pieces) as int or float.
            weight: weight as int or float.
            size: string representing item size ("S", "M", or "L"). 'None' is used for instances representing 'No Armor'.
            damage: int for number of sides for the damage dice roll.
        """
        super().__init__(name, cost, weight)
        self.size: str | None = size
        self.damage: int = damage


class RangedWeapon(Weapon):
    """Child class of 'Weapon' to represent ranged and throwable weapons."""

    def __init__(self, name: str, cost: int | float, weight: int | float, size: str, damage: int,
                 range_list: tuple[int, int, int], ammo=False, throw: bool=False) -> None:
        """Initialize attributes from parent class 'Weapons'.
        ARGS:
            name: string.
            cost: int or float
            weight: weight as int or float.
            size: string "S", "M" or "L"
            damage: int for number of sides on the die for the dice roll. NOTE: 0 for weapons that need ammo.
            range_list: tuple of ints for short, medium and long range.
            ammo: tuple of projectile instances for the weapon if needed. Default = False
            throw: bool if weapon is throwable. Default = False
        """
        super().__init__(name, cost, weight, size, damage)
        self.range_list: tuple[int, int, int] = range_list
        self.ammo: Projectile | False = ammo
        self.throw: bool = throw


class Projectile(Item):
    """Child class to represent projectiles for ranged weapons and grenade-like items."""
    
    def __init__(self, name: str, cost: int | float, weight: int | float, damage: int, splash_damage: int|bool=False,
                 range_list: tuple[int,int,int]|bool=False, throw: bool=False) -> None:
        """Initialize attributes from parent class 'Items'.
        ARGS:
            name: string.
            cost: int or float
            weight: weight as int or float.
            damage: int for number of sides on the die for the dice roll.
        ARGS that apply to grenade-like items and are 'default=False' for other projectiles:
            splash_damage: int for number of sides on the die for the dice roll for damage within 5 feet of the point of
                           impact.
            range_list: tuple of ints for short, medium and long range.
            throw: bool if weapon is throwable.
        """
        super().__init__(name, cost, weight)
        self.damage: int = damage
        # Attributes specific for grenade-like items.
        self.splash_damage: int | False = splash_damage
        self.range_list: tuple[int, int, int] = range_list
        self.throw: bool = throw


class Armor(Item):
    """Child class to represent armor."""

    def __init__(self, name: str, cost: int | float, weight: int | float, armor_class: int, shield: bool=False) -> None:
        """Initialize attributes from parent class 'Items'.
        ARGS:
            name: string.
            cost: int or float
            weight: weight as int or float.
            armor_class: int for AC.
            shield: bool to indicate if item is shield (True) or not (False). Default = False.
        """
        super().__init__(name, cost, weight)
        self.armor_class: int = armor_class
        self.shield: bool = shield
