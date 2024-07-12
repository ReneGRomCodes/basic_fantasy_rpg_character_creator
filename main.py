import os
import functions as func


# Tuple to check for valid user input in loops.
yes_no = ("y", "n")


# Name the character.
while True:
    player_name = input("Enter character name: ")
    name_proceed = input(f"Do you want your character to be named '{player_name}'? (Y/N) ")

    while name_proceed.lower() not in yes_no:
        name_proceed = input(f"Do you want your character to be named '{player_name}'? (Y/N) ")
        continue

    if name_proceed.lower() == "y":
        break
    else:
        continue


os.system('cls')


# Get ability scores.
print(f"\nLet's roll the dice for {player_name}!")

while True:
    str = func.get_ability_score()
    dex = func.get_ability_score()
    con = func.get_ability_score()
    int = func.get_ability_score()
    wis = func.get_ability_score()
    cha = func.get_ability_score()

    print(f"\nABILITIES:\n")
    print(f"Strength:       {str}")
    print(f"Dexterity:      {dex}")
    print(f"Constitution:   {con}")
    print(f"Intelligence:   {int}")
    print(f"Wisdom:         {wis}")
    print(f"Charisma:       {cha}")
    ability_proceed = input("\nKeep these scores and proceed to choose your race? (Y/N) ")

    while ability_proceed.lower() not in yes_no:
        ability_proceed = input("Keep these scores and proceed to choose your race? (Y/N) ")
        continue

    if ability_proceed.lower() == "y":
        break
    else:
        continue


os.system('cls')


# Race and class selection.
race_list = func.check_race(con, cha, int, dex, str)
class_list = func.check_class(wis, str, int, dex)

print("\nBased on your scores you can choose from the following races and classes:")
print("\nRACE:")
for i in race_list:
    print("-", i)

print("\nCLASS:")
for i in class_list:
    print("-", i)

input()


os.system('cls')


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


stop = input()
