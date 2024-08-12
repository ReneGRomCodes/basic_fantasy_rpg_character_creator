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

# Ranged weapons. Note that damage is calculated through the projectile, therefor damage for weapon itself is '0'.
shortbow = item.Weapon("Shortbow", 25, 2, "M", 0)
longbow = item.Weapon("Longbow", 60, 3, "L", 0)
crossbow_light = item.Weapon("Light Crossbow", 30, 7, "M", 0)
crossbow_heavy = item.Weapon("Heavy Crossbow", 50, 14, "L", 0)

# Daggers.
dagger = item.Weapon("Dagger", 2, 1, "S", 4)
dagger_silver = item.Weapon("Silver Dagger", 25, 1, "S", 4)

# Swords. Note that Longsword and Scimitar have the same stats, but I decided to treat them as different for RP reasons.
shortsword = item.Weapon("Shortsword", 6, 3, "S", 6)
longsword = item.Weapon("Longsword", 10, 4, "M", 8)
scimitar = item.Weapon("Scimitar", 10, 4, "M", 8)
two_handed_sword = item.Weapon("Two-Handed Sword", 18, 10, "L", 10)
