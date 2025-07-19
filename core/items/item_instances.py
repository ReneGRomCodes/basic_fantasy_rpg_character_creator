"""
Initialize instances of classes from 'item_objects.py'.
Instances are sorted into dicts at the end of this file for use in other modules.
"""
from .item_objects import Item, Weapon, Projectile, RangedWeapon, Armor


# General Equipment (args = "name, cost, weight").
BACKPACK: Item = Item("Backpack", 4, 0.1)
BELT_POUCH: Item = Item("Belt Pouch", 1, 0.1)
BIT_AND_BRIDLE: Item = Item("Bit and Bridle", 1.5, 3)
CANDLES_12: Item = Item("Candles, 12", 1, 0.1)
CHALK: Item = Item("Chalk, small bag of pieces", 2, 0.1)
CLOAK: Item = Item("Cloak", 2, 1)
CLOTHING_COMMON: Item = Item("Clothing, common outfit", 4, 1)
GLASS_BOTTLE_VIAL: Item = Item("Glass bottle or vial", 1, 0.1)
GRAPPLING_HOOK: Item = Item("Grappling Hook", 2, 4)
HOLY_SYMBOL: Item = Item("Holy Symbol", 25, 0.1)
HORSESHOES: Item = Item("Horseshoes & shoeing", 1, 10)
INK_JAR: Item = Item("Ink, per jar", 8, 0.5)
IRON_SPIKES_12: Item = Item("Iron Spikes, 12", 1, 1)
LADDER_10FT: Item = Item("Ladder, 10 ft.", 1, 20)
LANTERN: Item = Item("Lantern", 5, 2)
LANTERN_BULLSEYE: Item = Item("Lantern, Bullseye", 14, 3)
LANTERN_HOODED: Item = Item("Lantern, Hooded", 8, 2)
MANACLES: Item = Item("Manacles, without padlock", 6, 4)
MAP_SCROLL_CASE: Item = Item("Map or scroll case", 1, 0.5)
MIRROR_SMALL: Item = Item("Mirror, small metal", 7, 0.1)
PADLOCK: Item = Item("Padlock, with 2 keys", 12, 1)
PAPER_SHEET: Item = Item("Paper, per sheet", 1, 0)
POLE_WOOD: Item = Item("Pole, 10 ft. wooden", 1, 10)
QUILL: Item = Item("Quill", 0.1, 0)
QUILL_KNIFE: Item = Item("Quill Knife", 1, 0.1)
QUIVER_BOLT_CASE: Item = Item("Quiver or Bolt case", 1, 1)
DRY_RATIONS_WEEK: Item = Item("Rations, dry, one week", 10, 14)
ROPE_HEMP: Item = Item("Rope, Hemp, per 50 ft.", 1, 5)
ROPE_SILK: Item = Item("Rope, Silk, per 50 ft.", 10, 2)
SACK_LARGE: Item = Item("Sack, Large", 1, 0.1)
SACK_SMALL: Item = Item("Sack, Small", 0.5, 0.1)
SADDLE_PACK: Item = Item("Saddle, Pack", 5, 15)
SADDLE_RIDING: Item = Item("Saddle, Riding", 10, 35)
SADDLEBAGS_PAIR: Item = Item("Saddlebags, pair", 4, 7)
SPELLBOOK: Item = Item("Spellbook, 128 pages", 25, 1)
TENT_LARGE: Item = Item("Tent, Large (10 men)", 25, 20)
TENT_SMALL: Item = Item("TENT, SMALL (1 MAN)", 5, 10)
THIEVES_TOOLS: Item = Item("Thieves' picks and tools", 25, 1)
TINDERBOX: Item = Item("Tinderbox, flint and steel", 3, 1)
TORCHES_6: Item = Item("Torches, 6", 1, 1)
WHETSTONE: Item = Item("Whetstone", 1, 1)
WHISTLE: Item = Item("Whistle", 1, 0)
SKIN_WINE_WATER: Item = Item("Wineskin/Waterskin", 1, 2)
WINTER_BLANKET: Item = Item("Winter blanket", 1, 3)


# Weapons (args = "name, cost, weight, size, damage").
# Default instance for no weapon.
NO_WEAPON: Weapon = Weapon("No Weapon", 0, 0, None, 0)

# Axes.
BATTLE_AXE: Weapon = Weapon("Battle Axe", 7, 7, "M", 8)
GREAT_AXE: Weapon = Weapon("Great Axe", 14, 15, "L", 10)

# Swords.
SHORTSWORD: Weapon = Weapon("Shortsword", 6, 3, "S", 6)
LONGSWORD: Weapon = Weapon("Longsword", 10, 4, "M", 8)
SCIMITAR: Weapon = Weapon("Scimitar", 10, 4, "M", 8)
TWO_HANDED_SWORD: Weapon = Weapon("Two-Handed Sword", 18, 10, "L", 10)

# Hammers and Maces.
MACE: Weapon = Weapon("Mace", 6, 10, "M", 8)
MAUL: Weapon = Weapon("Maul", 10, 16, "L", 10)

# Other weapons.
CLUB: Weapon = Weapon("Club", 0.5, 1, "M", 4)
CUDGEL: Weapon = Weapon("Cudgel", 0.5, 1, "M", 4)
WALKING_STAFF: Weapon = Weapon("Walking Staff", 0.5, 1, "M", 4)
QUARTERSTAFF: Weapon = Weapon("Quarterstaff", 2, 4, "L", 6)
POLE_ARM: Weapon = Weapon("Pole Arm", 9, 15, "L", 10)
# SPEAR: Weapon = Weapon("Spear", 5, 5, "M", None)  # TODO figure out how to implement different attacks with spear.


# Projectiles for ranged weapons and grenade-like items.
# (args = "name, cost, weight, damage, splash_damage=False, range_list=False, throw=False")
ARROW_SHORTBOW: Projectile = Projectile("Shortbow Arrow", 0.1, 0.1, 6)
ARROW_SHORTBOW_SILVER: Projectile = Projectile("Shortbow Arrow (Silver)", 2, 0.1, 6)
ARROW_LONGBOW: Projectile = Projectile("Longbow Arrow", 0.2, 0.1, 8)
ARROW_LONGBOW_SILVER: Projectile = Projectile("Longbow Arrow (Silver)", 4, 0.1, 8)
QUARREL_LIGHT: Projectile = Projectile("Light Quarrel", 0.2, 0.1, 6)
QUARREL_LIGHT_SILVER: Projectile = Projectile("Light Quarrel (Silver)", 5, 0.1, 6)
QUARREL_HEAVY: Projectile = Projectile("Heavy Quarrel", 0.4, 0.1, 8)
QUARREL_HEAVY_SILVER: Projectile = Projectile("Heavy Quarrel (Silver)", 10, 0.1, 8)
BULLET_SLING: Projectile = Projectile("Bullet", 0.1, 0.1, 4)
STONE_SLING: Projectile = Projectile("Stone", 0, 0.1, 3)
# Grenade-like items. 'holy_water' and 'oil_flask' are listed in 'general_items'.
HOLY_WATER: Projectile = Projectile("Holy Water, per vial", 10, 0.1, 8, 6, (10, 30, 50), throw=True)
OIL_FLASK: Projectile = Projectile("Oil, per flask", 1, 1, 8, 6, (10, 30, 50), throw=True)


# Ranged weapons (args = "name, cost, weight, size, damage, range_list, ammo=False, throw=False").
# Note that bows and crossbows need projectiles to do damage, therefor damage for them is '0'.
SHORTBOW: RangedWeapon = RangedWeapon("Shortbow", 25, 2, "M", 0, (50, 100, 150),
                                      ammo=(ARROW_SHORTBOW, ARROW_SHORTBOW_SILVER))
LONGBOW: RangedWeapon = RangedWeapon("Longbow", 60, 3, "L", 0, (70, 140, 210),
                                     ammo=(ARROW_LONGBOW, ARROW_LONGBOW_SILVER))
CROSSBOW_LIGHT: RangedWeapon = RangedWeapon("Light Crossbow", 30, 7, "M", 0, (60, 120, 180),
                                            ammo=(QUARREL_LIGHT, QUARREL_LIGHT_SILVER))
CROSSBOW_HEAVY: RangedWeapon = RangedWeapon("Heavy Crossbow", 50, 14, "L", 0, (80, 160, 240),
                                            ammo=(QUARREL_HEAVY, QUARREL_HEAVY_SILVER))
SLING: RangedWeapon = RangedWeapon("Sling", 1, 0.1, "S", 0, (30, 60, 90),
                                   ammo=(BULLET_SLING, STONE_SLING))
# Throwable weapons. Listed under their respective key in dict 'weapons'.
DAGGER: RangedWeapon = RangedWeapon("Dagger", 2, 1, "S", 4, (10, 20, 30), throw=True)
DAGGER_SILVER: RangedWeapon = RangedWeapon("Dagger (Silver)", 25, 1, "S", 4, (10, 20, 30), throw=True)
WARHAMMER: RangedWeapon = RangedWeapon("Warhammer", 4, 6, "S", 6, (10, 20, 30), throw=True)
HAND_AXE: RangedWeapon = RangedWeapon("Hand Axe", 4, 5, "S", 6, (10, 20, 30), throw=True)


# Armor (args = "name, cost, weight, armor_class, shield=False"). 'NO_ARMOR' and 'NO_SHIELD' cannot be bought but are
# default settings.
NO_ARMOR: Armor = Armor("No Armor", 0, 0, 11)
LEATHER_ARMOR: Armor = Armor("Leather Armor", 20, 15, 13)
CHAIN_MAIL: Armor = Armor("Chain Mail", 60, 40, 15)
PLATE_MAIL: Armor = Armor("Plate Mail", 300, 50, 17)
NO_SHIELD: Armor = Armor("No Shield", 0, 0, 0, shield = True)
SHIELD: Armor = Armor("Shield", 7, 5, 1, shield = True)


# Dicts of instances.
GENERAL_ITEMS: dict[str, tuple[object, ...]] = {
    "general_items": (BACKPACK, BELT_POUCH, BIT_AND_BRIDLE, CANDLES_12, CHALK, CLOAK, CLOTHING_COMMON, GLASS_BOTTLE_VIAL,
                      GRAPPLING_HOOK, HOLY_SYMBOL, HOLY_WATER, HORSESHOES, INK_JAR, IRON_SPIKES_12, LADDER_10FT, LANTERN,
                      LANTERN_BULLSEYE, LANTERN_HOODED, MANACLES, MAP_SCROLL_CASE, MIRROR_SMALL, OIL_FLASK, PADLOCK,
                      PAPER_SHEET, POLE_WOOD, QUILL, QUILL_KNIFE, QUIVER_BOLT_CASE, DRY_RATIONS_WEEK, ROPE_HEMP, ROPE_SILK,
                      SACK_LARGE, SACK_SMALL, SADDLE_PACK, SADDLE_RIDING, SADDLEBAGS_PAIR, SPELLBOOK, TENT_LARGE,
                      TENT_SMALL, THIEVES_TOOLS, TINDERBOX, TORCHES_6, WHETSTONE, WHISTLE, SKIN_WINE_WATER, WINTER_BLANKET),
}

WEAPONS: dict[str, tuple[object, ...] | object] = {
    "no_weapon": NO_WEAPON,
    "axes": (HAND_AXE, BATTLE_AXE, GREAT_AXE),
    "swords": (SHORTSWORD, LONGSWORD, SCIMITAR, TWO_HANDED_SWORD),
    "daggers": (DAGGER, DAGGER_SILVER),
    "hammers_maces": (WARHAMMER, MACE, MAUL),
    "ranged_weapons": (SHORTBOW, LONGBOW, CROSSBOW_LIGHT, CROSSBOW_HEAVY, SLING),
    "other_weapons": (CLUB, CUDGEL, WALKING_STAFF, QUARTERSTAFF, POLE_ARM),
}

PROJECTILES: dict[str, tuple[object, ...] | object] = {
    "shortbow": (ARROW_SHORTBOW, ARROW_SHORTBOW_SILVER),
    "longbow": (ARROW_LONGBOW, ARROW_LONGBOW_SILVER),
    "crossbow": (QUARREL_LIGHT, QUARREL_LIGHT_SILVER, QUARREL_HEAVY, QUARREL_HEAVY_SILVER),
    "sling": (BULLET_SLING, STONE_SLING),
}

ARMORS: dict[str, tuple[object, ...] | object] = {
    "no_armor": NO_ARMOR,
    "no_shield": NO_SHIELD,
    "armors": (LEATHER_ARMOR, CHAIN_MAIL, PLATE_MAIL, SHIELD),
}

# Flat dict of all items (key = item name, value = item instance) for quick lookups.
ALL_ITEMS_BY_NAME: dict[str, object] = {
    item.name: item
    for category in (GENERAL_ITEMS, WEAPONS, PROJECTILES, ARMORS)
    for group in category.values()
    for item in (group if isinstance(group, (list, tuple)) else [group])
}
