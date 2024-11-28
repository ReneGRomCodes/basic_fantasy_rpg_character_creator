import functions as func
import random
from item_instances import no_shield
import gui.screen_objects as so
import pygame
"""Functions used to set race/class and build the character sheet."""


def draw_screen_title(screen, screen_title, gui_elements):
    """Draw 'screen_title' object on screen at default position."""
    screen_title.text_rect.top = screen.get_rect().top + gui_elements["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx
    screen_title.draw_text()


"""Background functions for abilty score screen."""

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


def build_possible_characters_list(race_list, class_list):
    """Take lists of possible races and classes and return list 'possible_characters' with valid race-class
    combinations."""
    possible_characters = []

    for char_race in race_list:
        for char_class in class_list:
            # Exclude Dwarves and Halflings from class 'Magic-User'.
            if char_race in ["Dwarf", "Halfling"] and char_class == "Magic-User":
                pass
            # Assure that combination classes are only shown for Elves.
            elif char_race != "Elf" and char_class in ["Fighter/Magic-User", "Magic-User/Thief"]:
                pass
            else:
                race_class = char_race + " " + char_class
                possible_characters.append(race_class)

    return possible_characters


"""Background functions for race/class selection screen."""

def race_class_check(available_choices, possible_races, possible_classes, race_name, class_name):
    """Check 'possible_races' and 'possible_classes' and populate and return dict 'available_choices' with allowed
    race/class combinations for use in function 'get_available_choices()'."""
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

    return available_choices


def get_available_choices(possible_characters, possible_races, possible_classes, selected_race, selected_class):
    """Create dict and populate it with instances from 'possible_races' and 'possible_classes' using function
        'race_class_check()' if their 'text' attributes match entries in 'possible_characters' (first word for race,
        second for class) and return it in 'available_choices'.
    ARGS:
        possible_characters: list of possible race-class combinations as strings.
        possible_races: entry from gui element dict 'gui_elements["possible_races"]'.
        possible_classes: entry from gui element dict 'gui_elements["possible_classes"]'.
        selected_race: instance of 'InteractiveText' class representing chosen race.
        selected_class: instance of 'InteractiveText' class representing chosen class.
    """
    # Dictionary for available race and class choices to be returned.
    available_choices = {
        "races": [],
        "classes": [],
    }

    for character in possible_characters:
        # Split each possible character to get race and class.
        race_name, class_name = character.split()

        # Add all available races and classes to dict if none are selected.
        if not selected_race and not selected_class:
            available_choices = race_class_check(available_choices, possible_races, possible_classes, race_name, class_name)

        # Add only classes that are compatible with selected race to dict.
        elif selected_race and selected_race.text == race_name:
            available_choices = race_class_check(available_choices, possible_races, possible_classes, race_name, class_name)

        # Add only races that are compatible with selected class to dict.
        elif selected_class and selected_class.text == class_name:
            available_choices = race_class_check(available_choices, possible_races, possible_classes, race_name, class_name)

    return available_choices


def position_race_class_elements(screen, race_class, inactive_races):
    """Get and return x and y values for GUI elements in function 'draw_available_choices()'.
    ARGS:
        screen: pygame window.
        race_class: string variable for race or class check.
        inactive_races: list of text field instances for non-choose able races. Only used here to calculate value for
        variable 'text_field_height'.
    """
    # General variables for element positioning.
    screen_center_y = screen.get_rect().centery
    text_field_height = inactive_races[0].text_rect.height  # Value taken from list item for consistent field height.
    text_field_y_offset = text_field_height * 2
    race_field_block_height = 4 * text_field_height
    race_field_centerx = int(screen.get_rect().width / 4)
    race_field_centery_start = screen_center_y - race_field_block_height
    class_field_block_height = 6 * text_field_height
    class_field_centerx = race_field_centerx * 3
    class_field_centery_start = screen_center_y - class_field_block_height

    # Text field positions.
    # Races.
    human_pos_x, human_pos_y = race_field_centerx, race_field_centery_start
    elf_pos_x, elf_pos_y = race_field_centerx, human_pos_y + text_field_y_offset
    dwarf_pos_x, dwarf_pos_y = race_field_centerx, elf_pos_y + text_field_y_offset
    halfling_pos_x, halfling_pos_y = race_field_centerx, dwarf_pos_y + text_field_y_offset
    # Classes.
    fighter_pos_x, fighter_pos_y = class_field_centerx, class_field_centery_start
    cleric_pos_x, cleric_pos_y = class_field_centerx, fighter_pos_y + text_field_y_offset
    magic_user_pos_x, magic_user_pos_y = class_field_centerx, cleric_pos_y + text_field_y_offset
    thief_pos_x, thief_pos_y = class_field_centerx, magic_user_pos_y + text_field_y_offset
    fighter_magic_user_pos_x, fighter_magic_user_pos_y = class_field_centerx, thief_pos_y + text_field_y_offset
    magic_user_thief_pos_x, magic_user_thief_pos_y = class_field_centerx, fighter_magic_user_pos_y + text_field_y_offset

    # Check 'race_class' and assign correct x and y value for each specific race/class.
    if race_class.text == "Human":
        x, y = human_pos_x, human_pos_y
    elif race_class.text == "Elf":
        x, y = elf_pos_x, elf_pos_y
    elif race_class.text == "Dwarf":
        x, y = dwarf_pos_x, dwarf_pos_y
    elif race_class.text == "Halfling":
        x, y = halfling_pos_x, halfling_pos_y
    elif race_class.text == "Fighter":
        x, y = fighter_pos_x, fighter_pos_y
    elif race_class.text == "Cleric":
        x, y = cleric_pos_x, cleric_pos_y
    elif race_class.text == "Magic-User":
        x, y = magic_user_pos_x, magic_user_pos_y
    elif race_class.text == "Thief":
        x, y = thief_pos_x, thief_pos_y
    elif race_class.text == "Fighter/Magic-User":
        x, y = fighter_magic_user_pos_x, fighter_magic_user_pos_y
    elif race_class.text == "Magic-User/Thief":
        x, y = magic_user_thief_pos_x, magic_user_thief_pos_y

    return x, y


def draw_available_choices(screen, available_choices, inactive_races, inactive_classes, mouse_pos):
    """Get position of text field items in dict 'available_choices' and draw them on screen.
    ARGS:
        screen: pygame window.
        available_choices: dict with instances of interactive text fields for race and class selection.
        inactive_races: list of text field instances for non-choose able races.
        inactive_classes: list of text field instances for non-choose able classes.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """

    # Create list to check if inactive or selectable text field should be displayed.
    check_list = []
    for r in available_choices["races"]:
        check_list.append(r.text)
    for c in available_choices["classes"]:
        check_list.append(c.text)

    # Draw race selection.
    for race in inactive_races:
        if race.text in check_list:
            for r in available_choices["races"]:
                r.text_rect.centerx, r.text_rect.centery = position_race_class_elements(screen, r, inactive_races)
                r.draw_interactive_text(mouse_pos)
        else:
            race.text_rect.centerx, race.text_rect.centery = position_race_class_elements(screen, race, inactive_races)
            race.draw_text()

    # Draw class selection.
    for cls in inactive_classes:
        if cls.text in check_list:
            for c in available_choices["classes"]:
                c.text_rect.centerx, c.text_rect.centery = position_race_class_elements(screen, c, inactive_races)
                c.draw_interactive_text(mouse_pos)
        else:
            cls.text_rect.centerx, cls.text_rect.centery = position_race_class_elements(screen, cls, inactive_races)
            cls.draw_text()


def select_race_class(available_choices, selected_race, selected_class, reset_button, mouse_pos):
    """Selection logic for characters race and class and return selected text field instances in 'selected_race' and
    selected class.
    ARGS:
        available_choices: dict with instances of interactive text fields for race and class selection.
        selected_race: instance of 'InteractiveText' class representing chosen race.
        selected_class: instance of 'InteractiveText' class representing chosen class.
        reset_button: entry from gui element dict 'gui_elements["reset_button"]'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Check if the left mouse button is pressed before proceeding with selection logic.
    if pygame.mouse.get_pressed()[0]:
        # Reset selected race/class if 'reset button' is clicked.
        if reset_button.button_rect.collidepoint(mouse_pos):
            if selected_race:
                selected_race.selected = False
                selected_race = None
            if selected_class:
                selected_class.selected = False
                selected_class = None

        # Loop through each available race and class option to see if any were clicked.
        for race in available_choices["races"]:
            if race.text_rect.collidepoint(mouse_pos):
                selected_race = race
                break
        for cls in available_choices["classes"]:
            if cls.text_rect.collidepoint(mouse_pos):
                selected_class = cls
                break

        if selected_race:
            # Unselect the previous selected race, if any.
            for race in available_choices["races"]:
                if race.selected:
                    race.selected = False  # Set the selected attribute of the previously selected race to False.
            # Select the new race.
            selected_race.selected = True
        if selected_class:
            # Unselect the previous selected class, if any.
            for cls in available_choices["classes"]:
                if cls.selected:
                    cls.selected = False  # Set the selected attribute of the previously selected class to False.
            # Select the new class.
            selected_class.selected = True

    return selected_race, selected_class


def set_character_values(character):
    """Set values for instance 'character' of class 'Character'."""
    character.set_saving_throws()
    character.set_specials()
    character.set_hp()
    character.set_armor_class()
    character.set_carrying_capacity()


"""Pygame screen functions."""

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

    # Draw screen title.
    draw_screen_title(screen, screen_title, gui_elements)

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

    # Draw buttons on screen.
    reroll_button.draw_button(mouse_pos)
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


def show_race_class_selection_screen(screen, possible_characters, selected_race, selected_class, gui_elements, mouse_pos):
    """Display race/class selection on screen."""
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["race_class_title"]
    reset_button = gui_elements["reset_button"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]
    inactive_continue_button = gui_elements["inactive_continue_button"]
    possible_races = gui_elements["possible_races"]
    possible_classes = gui_elements["possible_classes"]
    inactive_races = gui_elements["inactive_races"]
    inactive_classes = gui_elements["inactive_classes"]

    # Draw screen title.
    draw_screen_title(screen, screen_title, gui_elements)

    # Get dict of race and class interactive text field instances 'available_choices', which are then ready to be drawn
    # on screen.
    available_choices = get_available_choices(possible_characters, possible_races, possible_classes, selected_race,
                                                selected_class)

    # Position and draw instances from dict 'available_choices' on screen.
    draw_available_choices(screen, available_choices, inactive_races, inactive_classes, mouse_pos)

    # Select race and class.
    selected_race, selected_class = select_race_class(available_choices, selected_race, selected_class, reset_button, mouse_pos)

    # Draw buttons.
    reset_button.draw_button(mouse_pos)
    back_button.draw_button(mouse_pos)
    # Show continue button only if race AND class have been selected otherwise show inactive continue button.
    if selected_race and selected_class:
        continue_button.draw_button(mouse_pos)
    else:
        inactive_continue_button.draw_button(mouse_pos)

    return selected_race, selected_class


def show_naming_screen(screen, gui_elements, mouse_pos):
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["naming_title"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]
    inactive_continue_button = gui_elements["inactive_continue_button"]

    # Draw screen title.
    draw_screen_title(screen, screen_title, gui_elements)

    # Draw buttons on screen.
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


"""Console functions."""

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
        race_class_list = build_possible_characters_list(race_list, class_list)

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
