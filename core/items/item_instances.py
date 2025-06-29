from core.items.item_objects import Item, Weapon, Projectile, RangedWeapon, Armor
"""Initialize instances of classes from 'item_objects.py'.
Instances are sorted into dicts at the end of this file for use in other modules."""


# General Equipment (args = "name, cost, weight").
backpack: Item = Item("Backpack", 4, 0.1)
belt_pouch: Item = Item("Belt Pouch", 1, 0.1)
bit_and_bridle: Item = Item("Bit and Bridle", 1.5, 3)
candles_12: Item = Item("Candles, 12", 1, 0.1)
chalk: Item = Item("Chalk, small bag of pieces", 2, 0.1)
cloak: Item = Item("Cloak", 2, 1)
clothing_common: Item = Item("Clothing, common outfit", 4, 1)
glass_bottle_vial: Item = Item("Glass bottle or vial", 1, 0.1)
grappling_hook: Item = Item("Grappling Hook", 2, 4)
holy_symbol: Item = Item("Holy Symbol", 25, 0.1)
horseshoes: Item = Item("Horseshoes & shoeing", 1, 10)
ink_jar: Item = Item("Ink, per jar", 8, 0.5)
iron_spikes_12: Item = Item("Iron Spikes, 12", 1, 1)
ladder_10ft: Item = Item("Ladder, 10 ft.", 1, 20)
lantern: Item = Item("Lantern", 5, 2)
lantern_bullseye: Item = Item("Lantern, Bullseye", 14, 3)
lantern_hooded: Item = Item("Lantern, Hooded", 8, 2)
manacles: Item = Item("Manacles, without padlock", 6, 4)
map_scroll_case: Item = Item("Map or scroll case", 1, 0.5)
mirror_small: Item = Item("Mirror, small metal", 7, 0.1)
padlock: Item = Item("Padlock, with 2 keys", 12, 1)
paper_sheet: Item = Item("Paper, per sheet", 1, 0)
pole_wood: Item = Item("Pole, 10 ft. wooden", 1, 10)
quill: Item = Item("Quill", 0.1, 0)
quill_knife: Item = Item("Quill Knife", 1, 0.1)
quiver_bolt_case: Item = Item("Quiver or Bolt case", 1, 1)
dry_rations_week: Item = Item("Rations, dry, one week", 10, 14)
rope_hemp: Item = Item("Rope, Hemp, per 50 ft.", 1, 5)
rope_silk: Item = Item("Rope, Silk, per 50 ft.", 10, 2)
sack_large: Item = Item("Sack, Large", 1, 0.1)
sack_small: Item = Item("Sack, Small", 0.5, 0.1)
saddle_pack: Item = Item("Saddle, Pack", 5, 15)
saddle_riding: Item = Item("Saddle, Riding", 10, 35)
saddlebags_pair: Item = Item("Saddlebags, pair", 4, 7)
spellbook: Item = Item("Spellbook, 128 pages", 25, 1)
tent_large: Item = Item("Tent, Large (10 men)", 25, 20)
tent_small: Item = Item("Tent, Small (1 man)", 5, 10)
thieves_tools: Item = Item("Thieves' picks and tools", 25, 1)
tinderbox: Item = Item("Tinderbox, flint and steel", 3, 1)
torches_6: Item = Item("Torches, 6", 1, 1)
whetstone: Item = Item("Whetstone", 1, 1)
whistle: Item = Item("Whistle", 1, 0)
skin_wine_water: Item = Item("Wineskin/Waterskin", 1, 2)
winter_blanket: Item = Item("Winter blanket", 1, 3)


# Weapons (args = "name, cost, weight, size, damage").
# Default instance for no weapon.
no_weapon: Weapon = Weapon("No Weapon", 0, 0, None, 0)

# Axes.
battle_axe: Weapon = Weapon("Battle Axe", 7, 7, "M", 8)
great_axe: Weapon = Weapon("Great Axe", 14, 15, "L", 10)

# Swords.
shortsword: Weapon = Weapon("Shortsword", 6, 3, "S", 6)
longsword: Weapon = Weapon("Longsword", 10, 4, "M", 8)
scimitar: Weapon = Weapon("Scimitar", 10, 4, "M", 8)
two_handed_sword: Weapon = Weapon("Two-Handed Sword", 18, 10, "L", 10)

# Hammers and Maces.
mace: Weapon = Weapon("Mace", 6, 10, "M", 8)
maul: Weapon = Weapon("Maul", 10, 16, "L", 10)

# Other weapons.
club: Weapon = Weapon("Club", 0.5, 1, "M", 4)
cudgel: Weapon = Weapon("Cudgel", 0.5, 1, "M", 4)
walking_staff: Weapon = Weapon("Walking Staff", 0.5, 1, "M", 4)
quarterstaff: Weapon = Weapon("Quartestaff", 2, 4, "L", 6)
pole_arm: Weapon = Weapon("Pole Arm", 9, 15, "L", 10)
# spear: Weapon = Weapon("Spear", 5, 5, "M", None)  # TODO figure out how to implement different attacks with spear.


# Projectiles for ranged weapons and grenade-like items.
# (args = "name, cost, weight, damage, splash_damage=False, range_list=False, throw=False")
arrow_shortbow: Projectile = Projectile("Shortbow Arrow", 0.1, 0.1, 6)
arrow_shortbow_silver: Projectile = Projectile("Shortbow Arrow (Silver)", 2, 0.1, 6)
arrow_longbow: Projectile = Projectile("Longbow Arrow", 0.2, 0.1, 8)
arrow_longbow_silver: Projectile = Projectile("Longbow Arrow (Silver)", 4, 0.1, 8)
quarrel_light: Projectile = Projectile("Light Quarrel", 0.2, 0.1, 6)
quarrel_light_silver: Projectile = Projectile("Light Quarrel (Silver)", 5, 0.1, 6)
quarrel_heavy: Projectile = Projectile("Heavy Quarrel", 0.4, 0.1, 8)
quarrel_heavy_silver: Projectile = Projectile("Heavy Quarrel (Silver)", 10, 0.1, 8)
bullet_sling: Projectile = Projectile("Bullet", 0.1, 0.1, 4)
stone_sling: Projectile = Projectile("Stone", 0, 0.1, 3)
# Grenade-like items. 'holy_water' and 'oil_flask' are listed in 'general_items'.
holy_water: Projectile = Projectile("Holy Water, per vial", 10, 0.1, 8, 6, (10, 30, 50), throw=True)
oil_flask: Projectile = Projectile("Oil, per flask", 1, 1, 8, 6, (10, 30, 50), throw=True)


# Ranged weapons (args = "name, cost, weight, size, damage, range_list, ammo=False, throw=False").
# Note that bows and crossbows need projectiles to do damage, therefor damage for them is '0'.
shortbow: RangedWeapon = RangedWeapon("Shortbow", 25, 2, "M", 0, (50, 100, 150),
                                      ammo=(arrow_shortbow, arrow_shortbow_silver))
longbow: RangedWeapon = RangedWeapon("Longbow", 60, 3, "L", 0, (70, 140, 210),
                                     ammo=(arrow_longbow, arrow_longbow_silver))
crossbow_light: RangedWeapon = RangedWeapon("Light Crossbow", 30, 7, "M", 0, (60, 120, 180),
                                            ammo=(quarrel_light, quarrel_light_silver))
crossbow_heavy: RangedWeapon = RangedWeapon("Heavy Crossbow", 50, 14, "L", 0, (80, 160, 240),
                                            ammo=(quarrel_heavy, quarrel_heavy_silver))
sling: RangedWeapon = RangedWeapon("Sling", 1, 0.1, "S", 0, (30, 60, 90),
                                   ammo=(bullet_sling, stone_sling))
# Throwable weapons. Listed under their respective key in dict 'weapons'.
dagger: RangedWeapon = RangedWeapon("Dagger", 2, 1, "S", 4, (10, 20, 30), throw=True)
dagger_silver: RangedWeapon = RangedWeapon("Dagger (Silver)", 25, 1, "S", 4, (10, 20, 30), throw=True)
warhammer: RangedWeapon = RangedWeapon("Warhammer", 4, 6, "S", 6, (10, 20, 30), throw=True)
hand_axe: RangedWeapon = RangedWeapon("Hand Axe", 4, 5, "S", 6, (10, 20, 30), throw=True)


# Armor (args = "name, cost, weight, armor_class, shield=False"). 'no_armor' and 'no_shield' cannot be bought but are
# default settings.
no_armor: Armor = Armor("No Armor", 0, 0, 11)
leather_armor: Armor = Armor("Leather Armor", 20, 15, 13)
chain_mail: Armor = Armor("Chain Mail", 60, 40, 15)
plate_mail: Armor = Armor("Plate Mail", 300, 50, 17)
no_shield: Armor = Armor("No Shield", 0, 0, 0, shield = True)
shield: Armor = Armor("Shield", 7, 5, 1, shield = True)


# Dicts of instances.
general_items: dict[str, tuple[object, ...]] = {
    "general_items": (backpack, belt_pouch, bit_and_bridle, candles_12, chalk, cloak, clothing_common, glass_bottle_vial,
                      grappling_hook, holy_symbol, holy_water, horseshoes, ink_jar, iron_spikes_12, ladder_10ft, lantern,
                      lantern_bullseye, lantern_hooded, manacles, map_scroll_case, mirror_small, oil_flask, padlock,
                      paper_sheet, pole_wood, quill, quill_knife, quiver_bolt_case, dry_rations_week, rope_hemp, rope_silk,
                      sack_large, sack_small, saddle_pack, saddle_riding, saddlebags_pair, spellbook, tent_large,
                      tent_small, thieves_tools, tinderbox, torches_6, whetstone, whistle, skin_wine_water, winter_blanket),
}

weapons: dict[str, tuple[object, ...] | object] = {
    "no_weapon": no_weapon,
    "axes": (hand_axe, battle_axe, great_axe),
    "swords": (shortsword, longsword, scimitar, two_handed_sword),
    "daggers": (dagger, dagger_silver),
    "hammers_maces": (warhammer, mace, maul),
    "ranged_weapons": (shortbow, longbow, crossbow_light, crossbow_heavy, sling),
    "other_weapons": (club, cudgel, walking_staff, quarterstaff, pole_arm),
}

projectiles: dict[str, tuple[object, ...] | object] = {
    "shortbow": (arrow_shortbow, arrow_shortbow_silver),
    "longbow": (arrow_longbow, arrow_longbow_silver),
    "crossbow": (quarrel_light, quarrel_light_silver, quarrel_heavy, quarrel_heavy_silver),
    "sling": (bullet_sling, stone_sling),
}

armors: dict[str, tuple[object, ...] | object] = {
    "no_armor": no_armor,
    "no_shield": no_shield,
    "armors": (leather_armor, chain_mail, plate_mail, shield),
}

# Flat dict of all items (key = item name, value = item instance) for quick lookups.
all_items_by_name: dict[str, object] = {
    item.name: item
    for category in (general_items, weapons, projectiles, armors)
    for group in category.values()
    for item in (group if isinstance(group, (list, tuple)) else [group])
}
