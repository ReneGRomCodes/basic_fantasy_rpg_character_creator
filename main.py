import main_functions as mf
import os


def run_character_creator():
    menu_prompt = mf.show_menu()

    while True:
        try:
            user_input = int(input(menu_prompt))
            if user_input == 1:
                os.system('cls')
                # Get ability scores and lists with available races and classes.
                ability_scores, race_list, class_list = mf.ability_score()

                # Race and class selection.
                char_race, char_class = mf.race_class_selection(race_list, class_list)

                # Name the character.
                char_name = mf.name_character()

                # Build character sheet.
                mf.build_character_sheet(char_class, char_race, char_name, ability_scores)
                break

            elif user_input == 2:
                os.system('cls')
                # Get random class, race, name and ability scores.
                char_class, char_race, char_name, ability_scores = mf.random_character_generator()

                # Build character sheet.
                mf.build_character_sheet(char_class, char_race, char_name, ability_scores)
                break

        except ValueError:
            continue

    input("\nPress Enter to exit")


run_character_creator()
