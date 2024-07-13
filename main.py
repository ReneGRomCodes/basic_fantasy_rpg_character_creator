import os
import functions as func


# Name the character.
while True:
    player_name = input("Enter character name: ")

    name_prompt = f"Do you want your character to be named '{player_name}'? (Y/N) "
    name_proceed = input(name_prompt)

    if func.check_yes_no(name_proceed, name_prompt):
        break
    else:
        continue


os.system('cls')


# Get ability scores.
print(f"Let's roll the dice for {player_name}!")

while True:
    # Generate dictionary for character abilities.
    ability_scores = func.build_ability_dict()

    # Check if abilities allow for valid race-class combinations.
    race_list = func.check_race(ability_scores)
    class_list = func.check_class(ability_scores)
    if not func.check_valid_race_class(race_list, class_list):
        continue

    print(f"\nABILITIES:\n")
    print(f"Strength: {ability_scores["str"]}")
    print(f"Dexterity: {ability_scores["dex"]}")
    print(f"Constitution: {ability_scores["con"]}")
    print(f"Intelligence: {ability_scores["int"]}")
    print(f"Wisdom: {ability_scores["wis"]}")
    print(f"Charisma: {ability_scores["cha"]}")

    ability_prompt = "Keep these scores and proceed to choose your race? (Y/N) "
    ability_proceed = input("\n" + ability_prompt)

    if func.check_yes_no(ability_proceed, ability_prompt):
        break
    else:
        continue


os.system('cls')


# Race and class selection.
possible_characters = func.build_race_class_list(race_list, class_list)

for character in possible_characters:
    print("-", character)

input()


os.system('cls')


"""
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
print(f"\nStrength:       {str}")
print(f"Dexterity:      {dex}")
print(f"Constitution:   {con}")
print(f"Intelligence:   {int}")
print(f"Wisdom:         {wis}")
print(f"Charisma:       {cha}")
print(f"\nMoney:          {starting_money}")
"""

stop = input()
