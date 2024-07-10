import functions as func


strength = func.get_ability_score()
dexterity = func.get_ability_score()
constitution = func.get_ability_score()
intelligence = func.get_ability_score()
wisdom = func.get_ability_score()
charisma = func.get_ability_score()

player_name = "Adventurer"
player_race = "Human"
player_class = "Fighter"
player_level = 1
player_xp = 0
xp_next_level = 2000
armor_class = 11 + dexterity  # No armor
player_hp = func.dice_roll(8) + constitution
attack_bonus = 1
starting_money = func.dice_roll(18) * 10


# Character Sheet:
print(f"{player_name.upper()}                   XP: {player_xp}")
print()
print(f"Race: {player_race}    Class: {player_class}\nLevel: {player_level}       XP for next level: {xp_next_level}")
print()
print(f"Strength:       {strength}")
print(f"Dexterity:      {dexterity}")
print(f"Constitution:   {constitution}")
print(f"Intelligence:   {intelligence}")
print(f"Wisdom:         {wisdom}")
print(f"Charisma:       {charisma}")
print()
print(f"Money:          {starting_money}")
