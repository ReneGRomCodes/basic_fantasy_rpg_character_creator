import functions as func
import random
import os
from item_instances import no_shield
import gui.screen_objects as so
"""Functions used to set race/class and build the character sheet."""


def get_ability_score():
    """Generate random value for ability score, apply bonus/penalty and return both values in list
    'ability_score' with the base score at index 0 and the bonus/penalty at index 1."""
    ability_score = [func.dice_roll(3, 6)]

    if ability_score[0] <= 3:
        ability_score.append(-3)
        return ability_score
    elif ability_score[0] <= 5:
        ability_score.append(-2)
        return ability_score
    elif ability_score[0] <= 8:
        ability_score.append(-1)
        return ability_score
    elif ability_score[0] <= 12:
        ability_score.append(0)
        return ability_score
    elif ability_score[0] <= 15:
        ability_score.append(1)
        return ability_score
    elif ability_score[0] <= 17:
        ability_score.append(2)
        return ability_score
    else:
        ability_score.append(3)
        return ability_score


def get_race_class_lists(character):
    """Generate race and class based on abilities scores for instance 'character' and return lists 'race_list' and
    'class_list'."""
    race_list = func.check_race(character)
    class_list = func.check_class(character)

    return race_list, class_list


def show_ability_scores_screen(screen, character, gui_elements, mouse_pos):
    """Display character ability scores and bonus/penalty on screen."""
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["abilities_title"]
    reroll_button = gui_elements["reroll_button"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]

    # Assign further gui_elements to variables and add them to list 'abilities'.
    strength = gui_elements["strength"]
    dexterity = gui_elements["dexterity"]
    constitution = gui_elements["constitution"]
    intelligence = gui_elements["intelligence"]
    wisdom = gui_elements["wisdom"]
    charisma = gui_elements["charisma"]
    abilities = [strength, dexterity, constitution, intelligence, wisdom, charisma]
    # Assign dict 'character.abilities' to 'stats' to avoid confusion with list 'abilities' above.
    stats = character.abilities
    # Create instances of class 'TextField' to show ability scores on screen. Text size is taken from an instance in
    # 'gui_elements' to assure automatic scaling.
    ability_score_text = so.TextField(screen, "score", strength.size)
    bonus_penalty_text = so.TextField(screen, "bonus_penalty", strength.size)

    # Position and draw screen title.
    screen_title.text_rect.top = screen.get_rect().top + gui_elements["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx
    screen_title.draw_text()

    # Set initial position on y-axis for ability score fields.
    element_pos_y = screen.get_rect().height / 3

    for ability, key in zip(abilities, stats):
        # 'Pre-formatting' bonus/penalty to string for easier formatting and better code-readability further down.
        bonus_penalty = f"{stats[key][1]}"

        # Check bonus/penalty for positive or negative value to apply correct prefix in text field or give out an empty
        # string if bonus_penalty is 0.
        if stats[key][1] > 0:
            bonus_penalty = f"+{bonus_penalty}"
        elif stats[key][1] == 0:
            bonus_penalty = ""
        else:
            pass

        # Position and draw copied rect for item from list 'abilities'.
        ability_rect = ability.text_rect.copy()
        ability_rect.top = screen.get_rect().top + element_pos_y
        ability_rect.width = screen.get_rect().width / 6
        ability_rect.right = screen.get_rect().centerx
        # Position ability rect within copied rect for left-alignment.
        ability.text_rect.topleft = ability_rect.topleft
        ability.draw_interactive_text(mouse_pos)

        # Change contents and get rect of 'TextField' instances for each ability score stat.
        ability_score_text.text = str(stats[key][0])
        ability_score_text.text_image = ability_score_text.font.render(ability_score_text.text, True, ability_score_text.text_color)
        ability_score_text.text_rect = ability_score_text.text_image.get_rect()
        bonus_penalty_text.text = bonus_penalty
        bonus_penalty_text.text_image = bonus_penalty_text.font.render(bonus_penalty_text.text, True, bonus_penalty_text.text_color)
        bonus_penalty_text.text_rect = bonus_penalty_text.text_image.get_rect()

        # Position and draw copied rects for each stat and bonus/penalty field.
        ability_score_rect = ability_score_text.text_rect.copy()
        ability_score_rect.width = screen.get_rect().width / 12
        ability_score_rect.topleft = ability_rect.topright
        bonus_penalty_rect = bonus_penalty_text.text_rect.copy()
        bonus_penalty_rect.width = screen.get_rect().width / 12
        bonus_penalty_rect.topleft = ability_score_rect.topright
        # Position stat and bonus/penalty rects within copied rects for right-alignment.
        ability_score_text.text_rect.topright = ability_score_rect.topright
        bonus_penalty_text.text_rect.topright = bonus_penalty_rect.topright

        ability_score_text.draw_text()
        bonus_penalty_text.draw_text()

        element_pos_y += ability_score_text.text_rect.height * 2

    # Position and draw buttons on screen
    reroll_button.button_rect.width = gui_elements["default_button_width"]
    reroll_button.button_rect.centerx = screen.get_rect().centerx
    reroll_button.button_rect.bottom = screen.get_rect().bottom - gui_elements["default_edge_spacing"]

    reroll_button.draw_button(mouse_pos)
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


def show_ability_scores(character):
    """Print formatted table of abilities from instance 'character' in console."""
    abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    for ability, key in zip(abilities, character.abilities):
        # 'Pre-formatting' ability name and bonus/penalty for better code-readability further down in print-statement.
        abilities_name = f"{ability}:"
        bonus_penalty = f"{character.abilities[key][1]}"

        # Check bonus/penalty for positive or negative value to apply correct prefix in output or give out an empty
        # string if bonus_penalty is 0.
        if character.abilities[key][1] > 0:
            bonus_penalty = f"+{bonus_penalty}"
        elif character.abilities[key][1] == 0:
            bonus_penalty = ""
        else:
            pass

        print(f"{abilities_name:<23} {character.abilities[key][0]:>2} {bonus_penalty:>4}")


def build_race_class_list(race_list, class_list):
    """Take lists of possible races and classes and return list 'possible_characters' with valid race-class
    combinations."""
    possible_characters = []

    for char_race in race_list:
        for char_class in class_list:
            # Exclude Dwarves and Halflings from class 'Magic-User'.
            if char_race in ["Dwarf", "Halfling"] and char_class == "Magic-User":
                pass
            # Assure that combination classes are only shown for Elves.
            if char_race != "Elf" and char_class in ["Fighter/Magic-User", "Magic-User/Thief"]:
                pass
            else:
                race_class = char_race + " " + char_class
                possible_characters.append(race_class)

    return possible_characters


def show_race_class_selection_screen(screen, possible_characters, gui_elements, mouse_pos):
    """Display race/class selection on screen."""
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["race_class_title"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]
    possible_races = gui_elements["possible_races"]
    possible_classes = gui_elements["possible_classes"]
    # Variables for element positioning.
    race_field_centerx = int(screen.get_rect().width / 4)
    class_field_centerx = race_field_centerx * 3

    # Create dict and populate it with instances from 'possible_races' and 'possible_classes' if their 'text' attributes
    # match entries in 'possible_characters' (first word for race, second for class). Objects in 'available_choices' are
    # then ready to be drawn on screen.
    available_choices = {
        "races": [],
        "classes": [],
    }
    for character in possible_characters:
        # Split each item to get race and class.
        race_name, class_name = character.split()
        # Check if the race matches.
        for race in possible_races:
            if race.text == race_name:
                # Assuring only one instance of each object is added to dict.
                if race not in available_choices["races"]:
                    available_choices["races"].append(race)
        # Check if the class matches.
        for cls in possible_classes:
            if cls.text == class_name:
                # Assuring only one instance of each object is added to dict.
                if cls not in available_choices["classes"]:
                    available_choices["classes"].append(cls)

    # Get position of elements on y-axis based on number of values in dict 'available_choices'.
    if len(available_choices["races"]) == 1:
        race_field_centery_start = screen.get_rect().centery
    else:
        race_field_block_height = len(available_choices["races"]) * available_choices["races"][0].text_rect.height * 2
        race_field_centery_start = screen.get_rect().centery - race_field_block_height / 2
    if len(available_choices["classes"]) == 1:
        class_field_centery_start = screen.get_rect().centery
    else:
        class_field_block_height = len(available_choices["classes"]) * available_choices["classes"][0].text_rect.height * 2
        class_field_centery_start = screen.get_rect().centery - class_field_block_height / 2

    # Draw text fields for available races on screen.
    for race in available_choices["races"]:
        race.text_rect.centerx, race.text_rect.centery = race_field_centerx, race_field_centery_start
        race.draw_text()
        race_field_centery_start += race.text_rect.height * 2
    # Draw text fields for available classes on screen.
    for cls in available_choices["classes"]:
        cls.text_rect.centerx, cls.text_rect.centery = class_field_centerx, class_field_centery_start
        cls.draw_text()
        class_field_centery_start += cls.text_rect.height * 2

    # Position and draw screen title.
    screen_title.text_rect.top = screen.get_rect().top + gui_elements["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx
    screen_title.draw_text()
    # Draw buttons.
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


def race_class_selection(character, race_list, class_list):
    """Take lists of possible races and classes, 'race_list' and 'class_list', check for allowed combination, let user
    choose a race/class combination and set race and class in instance 'character'."""
    while True:
        print("Based on your scores you can choose from the following race-class combinations:\n")

        possible_characters = build_race_class_list(race_list, class_list)
        selected_character = func.select_from_list(possible_characters,
                                                   "\nSelect a character to show race and class description: ")

        # Split selected 'character' into variables for race and class and call class methods 'set_race()' and
        # 'set_class()'.
        character.set_race(selected_character.split(" ")[0])
        character.set_class(selected_character.split(" ")[1])
        # Show description of selected race and class.
        show_char_race_descr(character)
        show_char_class_descr(character)

        # if-else block to assure grammatically correct prompt... because it would bother me to no end.
        if character.race_name == "Elf":
            if func.check_yes_no(f"\n\n\n\n\n\tDO YOU WANT TO BE AN '{selected_character}'? (Y/N) "):
                break
            else:
                continue
        else:
            if func.check_yes_no(f"\n\n\n\n\n\tDO YOU WANT TO BE A '{selected_character}'? (Y/N) "):
                break
            else:
                continue


def show_char_race_descr(character):
    """Take instance 'character' and print detailed description of character race."""
    os.system('cls')

    with open(character.race_description) as f:
        for line in f:
            output_text = line.rstrip()
            print(output_text)

    input(f"\n\n\n\n\tPRESS ENTER TO SHOW '{character.class_name}' CLASS.")


def show_char_class_descr(character):
    """Take instance 'character' and print detailed description of character class."""
    os.system('cls')

    with open(character.class_description) as f:
        for line in f:
            output_text = line.rstrip()
            print(output_text)

    input("\n\n\n\n\tPRESS ENTER TO CONTINUE.")


def name_character(character):
    """Prompt user to name character and set 'character.name'."""
    while True:
        print("- CHARACTER NAME -\n")
        char_name = input(f"Name your {character.race_name} {character.class_name}: ")

        if func.check_yes_no(f"Do you want your character to be named '{char_name}'? (Y/N) "):
            character.set_name(char_name)
            break
        else:
            continue


def show_saving_throws(character):
    """Print formatted output of dict 'saving_throws' from instance 'character'."""
    for k, v in character.saving_throws.items():
        print(f" - {k:<22} +{v:>2}")


def show_special_abilities(character):
    """Print formatted output of list 'specials' from instance 'character'."""
    for special in character.specials:
        print(f" - {special}")


def set_character_values(character):
    """Set values for instance 'character' of class 'Character'."""
    character.set_saving_throws()
    character.set_specials()
    character.set_hp()
    character.set_armor_class()
    character.set_carrying_capacity()


def set_starting_money(character):
    """Prompt user to set starting money for instance of class 'character'."""
    money_options = ["Roll the dice for your starting money (3d6 x 10)", "Choose your own amount of gold pieces"]

    while True:
        print("- STARTING MONEY -\n")
        selection = func.select_from_list(money_options, "\nYour choice: ")

        if selection == money_options[0]:
            character.money = func.dice_roll(3, 6) * 10
            print(f"\n\n\tYou receive {character.money} pieces of gold!\n\n\nPress ENTER to continue.")
            input()
            break
        else:
            while True:
                try:
                    character.money = int(input("\nHow many gold pieces do you want to give yourself? "))
                except ValueError:
                    continue
                break

            if func.check_yes_no(f"\nDo you want to start your adventure with {character.money} gold pieces (Y/N): "):
                break

            continue


def show_carrying_capacity(character):
    """Print formatted output of dict 'carrying_capacity' from instance 'character'."""
    for k, v in character.carrying_capacity.items():
        print(f" - {k}: {v:>3} pounds")


def show_inventory(character):
    """Print formatted output of list 'inventory' from instance 'character'."""
    for item in character.inventory:
        print(f" - {item.name:<30}{f"{item.weight} lbs":>7}")


def random_character_generator(character):
    """Create random character, prompt user for 'char_name' and set values for Character instance."""
    while True:

        # Generate dictionary for character abilities.
        character.set_ability_dict()

        # Check if abilities allow for valid race-class combinations.
        race_list, class_list = get_race_class_lists(character)
        if not func.check_valid_race_class(race_list, class_list):
            continue
        race_class_list = build_race_class_list(race_list, class_list)

        # Generate random character and set values.
        character_race_class = race_class_list[random.randint(0, (len(race_list)-1))]
        character.set_race(character_race_class.split(" ")[0])
        character.set_class(character_race_class.split(" ")[1])
        character.money = func.dice_roll(3, 6) * 10
        set_character_values(character)

        # prompt user for name.
        name_character(character)
        break


def build_character_sheet(character):
    """Take instance 'character' and print character sheet."""

    print(f"{character.name.upper():<25}Level: 1")
    print(f"{character.race_name} {character.class_name:<15}XP: 0 ({character.next_level_xp})")
    print(f"\nArmor Class: {character.armor_class:<8}HP: {character.hp:<8}"
          f"Attack Bonus: +{character.attack_bonus}")
    print("\nAbilities:")
    show_ability_scores(character)
    print("\nSaving Throws:")
    show_saving_throws(character)
    print("\nSpecial Abilities:")
    show_special_abilities(character)

    # Add spells section if class is 'Magic-User', 'Cleric' or combination class.
    if character.spells:
        print("\nSpells:")
        print(f" - {character.spells}")

    print(f"\nMoney: {character.money} gold pieces")
    print("\nCarrying Capacity:")
    show_carrying_capacity(character)
    print("\nWeight Carried:")
    print(f"{character.weight_carried} Pounds")
    print("\nWeapons:")
    print(f"{character.weapon.name}")
    print(f"\n{f"Armor:":<15}{f"AC":>5}")
    print(f"{character.armor.name:<15}{character.armor.armor_class:>5}")
    if character.shield == no_shield:
        pass
    else:
        print(f"{character.shield.name:<15}{f"+{character.shield.armor_class}":>5}")

    if character.inventory:
        print("\nInventory:")
        show_inventory(character)
