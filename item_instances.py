import item_model as item
"""Initialize instances of classes from 'item_model.py'."""


# General Equipment (args = "name, cost, weight").
backpack = item.Item("Backpack", 4, 0.1)
belt_pouch = item.Item("Belt Pouch", 1, 0.1)
bit_and_bridle = item.Item("Bit and Bridle", 1.5, 3)
candles_12 = item.Item("Candles, 12", 1, 0.1)
chalk = item.Item("Chalk, small bag of pieces", 2, 0.1)
cloak = item.Item("Cloak", 2, 1)
clothing_common = item.Item("Clothing, common outfit", 4, 1)
glass_bottle_vial = item.Item("Glass bottle or vial", 1, 0.1)
grappling_hook = item.Item("Grappling Hook", 2, 4)
holy_symbol = item.Item("Holy Symbol", 25, 0.1)
holy_water = item.Item("Holy Water, per vial", 10, 0.1)
horseshoes = item.Item("Horseshoes & shoeing", 1, 10)
ink_jar = item.Item("Ink, per jar", 8, 0.5)
iron_spikes_12 = item.Item("Iron Spikes, 12", 1, 1)
ladder_10ft = item.Item("Ladder, 10 ft.", 1, 20)
lantern = item.Item("Lantern", 5, 2)
lantern_bullseye = item.Item("Lantern, Bullseye", 14, 3)
lantern_hooded = item.Item("Lantern, Hooded", 8, 2)
manacles = item.Item("Manacles, without padlock", 6, 4)
map_scroll_case = item.Item("Map or scroll case", 1, 0.5)
mirror_small = item.Item("Mirror, small metal", 7, 0.1)
oil_flask = item.Item("Oil, per flask", 1, 1)
padlock = item.Item("Padlock, with 2 keys", 12, 1)
paper_sheet = item.Item("Paper, per sheet", 1, 0)
pole_wood = item.Item("Pole, 10 ft. wooden", 1, 10)
quill = item.Item("Quill", 0.1, 0)
quill_knife = item.Item("Quill Knife", 1, 0.1)
quiver_bolt_case = item.Item("Quiver or Bolt case", 1, 1)
dry_rations_week = item.Item("Rations, dry, one week", 10, 14)
rope_hemp = item.Item("Rope, Hemp, per 50 ft.", 1, 5)
rope_silk = item.Item("Rope, Silk, per 50 ft.", 10, 2)
sack_large = item.Item("Sack, Large", 1, 0.1)
sack_small = item.Item("Sack, Small", 0.5, 0.1)
saddle_pack = item.Item("Saddle, Pack", 5, 15)
saddle_riding = item.Item("Saddle, Riding", 10, 35)
saddlebags_pair = item.Item("Saddlebags, pair", 4, 7)
spellbook = item.Item("Spellbook, 128 pages", 25, 1)
tent_large = item.Item("Tent, Large (10 men)", 25, 20)
tent_small = item.Item("Tent, Small (1 man)", 5, 10)
thieves_tools = item.Item("Thieves' picks and tools", 25, 1)
tinderbox = item.Item("Tinderbox, flint and steel", 3, 1)
torches_6 = item.Item("Torches, 6", 1, 1)
whetstone = item.Item("Whetstone", 1, 1)
whistle = item.Item("Whistle", 1, 0)
skin_wine_water = item.Item("Wineskin/Waterskin", 1, 2)
winter_blanket = item.Item("Winter blanket", 1, 3)


# Weapons (args = "name, cost, weight, size, damage").
# Axes.
hand_axe = item.Weapon("Hand Axe", 4, 5, "S", 6)
battle_axe = item.Weapon("Battle Axe", 7, 7, "M", 8)
great_axe = item.Weapon("Great Axe", 14, 15, "L", 10)

# Ranged weapons. Note: damage is calculated through the projectile, therefor damage for weapon itself is '0'.
shortbow = item.Weapon("Shortbow", 25, 2, "M", 0)
longbow = item.Weapon("Longbow", 60, 3, "L", 0)
crossbow_light = item.Weapon("Light Crossbow", 30, 7, "M", 0)
crossbow_heavy = item.Weapon("Heavy Crossbow", 50, 14, "L", 0)
sling = item.Weapon("Sling", 1, 0.1, "S", 0)

# Daggers.
dagger = item.Weapon("Dagger", 2, 1, "S", 4)
dagger_silver = item.Weapon("Silver Dagger", 25, 1, "S", 4)

# Swords. Note: Longsword and Scimitar have the same stats, but are split here for RP reasons.
shortsword = item.Weapon("Shortsword", 6, 3, "S", 6)
longsword = item.Weapon("Longsword", 10, 4, "M", 8)
scimitar = item.Weapon("Scimitar", 10, 4, "M", 8)
two_handed_sword = item.Weapon("Two-Handed Sword", 18, 10, "L", 10)

# Hammers and Maces.
warhammer = item.Weapon("Warhammer", 4, 6, "S", 6)
mace = item.Weapon("Mace", 6, 10, "M", 8)
maul = item.Weapon("Maul", 10, 16, "L", 10)

# Other weapons. Note: Club, Cudgel and Walking Staff have the same stats, but are split here for RP reasons.
club = item.Weapon("Club", 0.5, 1, "M", 4)
cudgel = item.Weapon("Cudgel", 0.5, 1, "M", 4)
walking_staff = item.Weapon("Walking Staff", 0.5, 1, "M", 4)
quarterstaff = item.Weapon("Quartestaff", 2, 4, "L", 6)
pole_arm = item.Weapon("Pole Arm", 9, 15, "L", 10)
#spear = item.Weapon("Spear", 5, 5, "M", None)  # TODO figure out how to implement different attacks with spear.


# Armor (args = "name, cost, weight, armor_class").
no_armor = item.Armor("No Armor", 0, 0, 11)
leather_armor = item.Armor("Leather Armor", 20, 15, 13)
chain_mail = item.Armor("Chain Mail", 60, 40, 15)
plate_mail = item.Armor("Plate Mail", 300, 50, 17)
shield = item.Armor("Shield", 7, 5, 1)  # Shield AC is added to overall AC when carried.


# Projectiles for ranged weapons (args = "name, cost, weight, damage, range_list")
arrow_shortbow = item.Projectile("Shortbow Arrow", 0.1, 0.1, 6, [50, 100, 150])
arrow_shortbow_silver = item.Projectile("Silver Shortbow Arrow", 2, 0.1, 6, [50, 100, 150])
arrow_longbow = item.Projectile("Longbow Arrow", 0.2, 0.1, 8, [70, 140, 210])
arrow_longbow_silver = item.Projectile("Silver Longbow Arrow", 4, 0.1, 8, [70, 140, 210])
quarrel_light = item.Projectile("Light Quarrel", 0.2, 0.1, 6, [60, 120, 180])
quarrel_light_silver = item.Projectile("Silver Light Quarrel", 5, 0.1, 6, [60, 120, 180])
quarrel_heavy = item.Projectile("Heavy Quarrel", 0.4, 0.1, 8, [80, 160, 240])
quarrel_heavy_silver = item.Projectile("Silver Heavy Quarrel", 10, 0.1, 8, [80, 160, 240])
bullet_sling = item.Projectile("Bullet", 0.1, 0.1, 4, [30, 60, 90])
stone_sling = item.Projectile("Stone", 0, 0.1, 3, [30, 60, 90])


# Lists of instances.
basic_items = [backpack, belt_pouch, bit_and_bridle]
weapons = [hand_axe, shortbow, dagger, shortsword, warhammer, club]
projectiles = [arrow_shortbow, arrow_shortbow_silver]
armors = [leather_armor, chain_mail, plate_mail, shield]

# TODO implement items and weapons that can be thrown, e.g. 'Warhammer' or 'Holy Water', but have already instances.
