import functions as func
import main_functions as mf


# Get ability scores and lists with available races and classes.
ability_scores, race_list, class_list = mf.ability_score()

# Race and class selection.
char_race, char_class = mf.race_class_selection(race_list, class_list)

# Name the character.
char_name = mf.name_character()


# Remaining character variables.
xp_next_level = mf.get_next_level_xp(char_class)
armor_class = 0  # Value changes with ARMOR after implementation of the shop.
char_hp = mf.get_hp(char_race, char_class)
attack_bonus = 1  # Default for level 1 characters. Value changes with WEAPON after implementation of the shop.
starting_money = func.dice_roll(3, 6) * 10


# Character Sheet:
print(f"{char_name.upper()}                XP: 0")
print(f"Race: {char_race}    Class: {char_class}")
print(f"\nLevel: 1       XP for next level: {xp_next_level}")
print(f"\nArmor Class: {armor_class}      HP: {char_hp}       Attack Bonus: {attack_bonus}")
func.show_ability_scores(ability_scores)
print(f"\nMoney:          {starting_money}")


input("\nPress Enter to continue")
