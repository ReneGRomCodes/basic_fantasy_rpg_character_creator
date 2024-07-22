import main_functions as mf


# Get ability scores and lists with available races and classes.
ability_scores, race_list, class_list = mf.ability_score()

# Race and class selection.
char_race, char_class = mf.race_class_selection(race_list, class_list)

# Name the character.
char_name = mf.name_character()

# Build character sheet.
mf.build_character_sheet(char_class, char_race, char_name, ability_scores)


input("\nPress Enter to continue")
