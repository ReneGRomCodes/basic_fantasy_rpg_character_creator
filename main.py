import functions as func


# Get ability scores.
while True:
    print("Let's roll the dice!\n")

    # Generate dictionary for character abilities.
    ability_scores = func.build_ability_dict()

    # Check if abilities allow for valid race-class combinations.
    race_list = func.check_race(ability_scores)
    class_list = func.check_class(ability_scores)
    if not func.check_valid_race_class(race_list, class_list):
        continue

    # Print ability scores.
    func.show_ability_scores(ability_scores)

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
    # Show description of selected race and class.
    func.show_char_race_descr(character)
    func.show_char_class_descr(character)

    # if-else block to assure grammatically correct prompt... because it would bother me to no end.
    if character.split(" ")[0] == "Elf":
        char_prompt = f"\n\n\n\n\tDO YOU WANT TO BE AN '{character}'? (Y/N) "
        char_proceed = input("\n" + char_prompt)
    else:
        char_prompt = f"\n\n\n\n\tDO YOU WANT TO BE A '{character}'? (Y/N) "
        char_proceed = input("\n" + char_prompt)

    if func.check_yes_no(char_proceed, char_prompt):
        break
    else:
        continue


# Name the character.
while True:
    char_name = input("Enter character name: ")

    name_prompt = f"Do you want your character to be named '{char_name}'? (Y/N) "
    name_proceed = input(name_prompt)

    if func.check_yes_no(name_proceed, name_prompt):
        break
    else:
        continue


# Character variables.
char_race = character.split(" ")[0]
char_class = character.split(" ")[1]
xp_next_level = None
armor_class = None
char_hp = None
attack_bonus = 1
starting_money = func.dice_roll(3, 6) * 10


# Character Sheet:
print(f"{char_name.upper()}                Level: 1")
print(f"Race: {char_race}    Class: {char_class}\nXP: 0       XP for next level: {xp_next_level}")
func.show_ability_scores(ability_scores)
print(f"\nMoney:          {starting_money}")


input("\nPress Enter to continue")
