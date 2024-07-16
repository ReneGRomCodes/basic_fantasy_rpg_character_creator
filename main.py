import functions as func


# Name the character.
while True:
    char_name = input("Enter character name: ")

    name_prompt = f"Do you want your character to be named '{char_name}'? (Y/N) "
    name_proceed = input(name_prompt)

    if func.check_yes_no(name_proceed, name_prompt):
        break
    else:
        continue


# Get ability scores.
while True:
    print(f"Let's roll the dice for {char_name}!")

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

    ability_prompt = "Keep these scores and proceed to choose your race and class? (Y/N) "
    ability_proceed = input("\n" + ability_prompt)

    if func.check_yes_no(ability_proceed, ability_prompt):
        break
    else:
        continue


# Race and class selection.
while True:
    possible_characters = func.build_race_class_list(race_list, class_list)
    character = func.select_character(possible_characters)

    char_prompt = f"Are you sure you want {char_name} to be a {character}? (Y/N) "
    char_proceed = input("\n" + char_prompt)

    if func.check_yes_no(char_proceed, char_prompt):
        break
    else:
        continue


# Character variables.
char_race = character.split(" ")[0]
char_class = character.split(" ")[1]
char_level = 1
char_xp = 0
xp_next_level = None
armor_class = None
char_hp = None
attack_bonus = 1
starting_money = func.dice_roll(3, 6) * 10


# Character Sheet:
print(f"{char_name.upper()}                   XP: {char_xp}")
print()
print(f"Race: {char_race}    Class: {char_class}\nLevel: {char_level}       XP for next level: {xp_next_level}\n")
print(f"Strength:       {ability_scores["str"]}")
print(f"Dexterity:      {ability_scores["dex"]}")
print(f"Constitution:   {ability_scores["con"]}")
print(f"Intelligence:   {ability_scores["int"]}")
print(f"Wisdom:         {ability_scores["wis"]}")
print(f"Charisma:       {ability_scores["cha"]}")
print(f"\nMoney:          {starting_money}")


input("\nPress Enter to continue")
