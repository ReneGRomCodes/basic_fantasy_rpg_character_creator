import functions as func


str = func.get_ability_score()
dex = func.get_ability_score()
con = func.get_ability_score()
int = func.get_ability_score()
wis = func.get_ability_score()
cha = func.get_ability_score()

player_name = "Adventurer"
player_race = "Human"
player_class = "Fighter"
player_level = 1
player_xp = 0
xp_next_level = 2000
armor_class = 11 + dex  # No armor
player_hp = func.dice_roll(8) + con
attack_bonus = 1
starting_money = func.dice_roll(18) * 10


# Character Sheet:
print(f"{player_name.upper()}                   XP: {player_xp}")
print()
print(f"Race: {player_race}    Class: {player_class}\nLevel: {player_level}       XP for next level: {xp_next_level}")
print()
print(f"Strength:       {str}")
print(f"Dexterity:      {dex}")
print(f"Constitution:   {con}")
print(f"Intelligence:   {int}")
print(f"Wisdom:         {wis}")
print(f"Charisma:       {cha}")
print()
print(f"Money:          {starting_money}")
