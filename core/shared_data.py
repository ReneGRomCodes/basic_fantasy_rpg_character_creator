from gui.screen_objects import InteractiveText
from core.rules import get_class_categories
from gui.shared_data import ui_shared_data as uisd
"""
Shared data class for character creation process.
Only instance of this class, 'shared_data', is created at the bottom of this module and imported/referenced in
'state_manager.py' and 'event_handlers.py'.
"""


class SharedData:
    """Class for initialization and storage of attributes relevant throughout the character creation process and contains
    selection logic methods for various screens (race/class selection, spell selection, etc.)."""

    def __init__(self) -> None:
        """Initialize shared data attributes."""
        # Variable for later instances of class objects.
        self.character: object | None = None  # Instance 'Character()'.
        self.credits_screen: object | None = None  # Instance 'Credits()'.
        self.settings_gui: object = None  # Instance 'SettingsGUI()'
        self.cs_sheet: object | None = None  # Instance of 'CharacterSheet'.

        # Class sets for category checks (example: spell selection screen shown only for magic using classes).
        self.spell_using_classes, self.magic_classes, self.no_armor_classes = get_class_categories()

        # All available races/classes in the game.
        # 'None' as starting value, dict is created in 'shared_data_janitor()' when method is called in from module
        # 'state_manager.py' in state "pre_main_menu".
        self.rc_dict: dict[str, str] | None = None
        # Possible race-class combinations.
        # 'None' as starting value before actual value is assigned.
        self.possible_characters: list[str] | None = None
        # 'InteractiveText' instances representing selected race and class in custom creation, string in random creation.
        # 'None' as default values before actual values are assigned.
        self.selected_race: InteractiveText | str | None = None
        self.selected_class: InteractiveText | str | None = None

        # 'InteractiveText' instances representing selected spell for spell casters.
        # 'None' as default values before actual values are assigned.
        self.selected_spell: InteractiveText | None = None

        # 'InteractiveText' instances representing selected languages for character.
        # 'None' as default values before actual values are assigned.
        self.selected_languages: InteractiveText | None = None

        # Characters starting money.
        self.starting_money: int = 0
        self.random_money_flag: bool = False  # Flag to check money selection.
        self.custom_money_flag: bool = False  # Flag to check money selection.

    def select_race_class(self, mouse_pos, reset: bool = False) -> None:
        """Selection logic for race/class selection screen. Set class attributes 'selected_race' and 'selected_class'
        to interactive text field instances.
        ARGS:
            mouse_pos: position of mouse on screen.
            reset: bool to reset race/class selection. Default is 'False'.
        """
        # Assign entries from 'gui_elements' to variables.
        races: tuple[InteractiveText, ...] = uisd.gui_elements["active_races"]
        classes: tuple[InteractiveText, ...] = uisd.gui_elements["active_classes"]

        # Loop through each available race and class option to see if any were clicked.
        for race in races:
            if race.interactive_rect.collidepoint(mouse_pos):
                self.selected_race = race
                break
        for cls in classes:
            if cls.interactive_rect.collidepoint(mouse_pos):
                self.selected_class = cls
                break

        if self.selected_race:
            # Unselect the previous selected race, if any.
            for race in races:
                if race.selected:
                    race.selected = False  # Set the selected attribute of the previously selected race to False.
            # Select the new race.
            self.selected_race.selected = True
        if self.selected_class:
            # Unselect the previous selected class, if any.
            for cls in classes:
                if cls.selected:
                    cls.selected = False  # Set the selected attribute of the previously selected class to False.
            # Select the new class.
            self.selected_class.selected = True

        # Reset entire race/class selection if 'reset button' is clicked (when method is called from event handler with
        # 'reset=True').
        if reset:
            if self.selected_race:
                self.selected_race.selected = False
                self.selected_race = None
            if self.selected_class:
                self.selected_class.selected = False
                self.selected_class = None

    def select_spell(self, spells: tuple[InteractiveText, ...], mouse_pos) -> None:
        """Selection logic for character's spell. Set class attribute 'selected_spell' to interactive text instance.
        ARGS:
            spells: tuple with instances of interactive text fields for spell selection.
                NOTE: item at index '0' is not processed here as it represents the default spell for all magic-users.
            mouse_pos: position of mouse on screen.
        """
        # Create new tuple that excludes the first element. That element represents the default spell 'Read Magic', known
        # by all Magic-Users and cannot be selected/unselected.
        selectable_spells: tuple[InteractiveText, ...] = spells[1:]

        # Loop through each available spell option to see if any were clicked.
        for spell in selectable_spells:
            if spell.interactive_rect.collidepoint(mouse_pos):
                self.selected_spell = spell
                break

        if self.selected_spell:
            # Unselect the previous selected spell, if any.
            for spell in selectable_spells:
                if spell.selected:
                    spell.selected = False  # Set the selected attribute of the previously selected spell to False.
            # Select the new spell.
            self.selected_spell.selected = True

    def select_languages(self, languages: tuple[InteractiveText, ...], mouse_pos) -> None:
        """Selection logic for character's languages. Set class attribute 'selected_languages' to interactive text
        instance.
        ARGS:
            languages: tuple with instances of interactive text fields for language selection.
                NOTE: item at index '0' is not processed here as it represents the default language for all races.
            mouse_pos: position of mouse on screen.
        """
        # Create new tuple that excludes the first element. That element represents the default language 'Common', known
        # by all characters and cannot be selected/unselected.
        selectable_languages: tuple[InteractiveText, ...] = languages[1:]

        # Loop through each available language option to see if any were clicked.
        for language in selectable_languages:
            if language.interactive_rect.collidepoint(mouse_pos):
                self.selected_languages = language
                break

        if self.selected_languages:
            # Unselect the previous selected language, if any.
            for language in selectable_languages:
                if language.selected:
                    language.selected = False  # Set the selected attribute of the previously selected language to False.
            # Select the new language.
            self.selected_languages.selected = True

    def shared_data_janitor(self) -> None:
        """Reset shared data not automatically overwritten elsewhere with default values in case of a switch to a
        previous screen or the main menu.

        Method is called in event handler 'naming_character_events()' when returning to character menu from
        'name_random_character' state, in addition to its method calls in states 'pre_main_menu' and 'show_abilities'.
        This resolves multiple issues that caused the program to freeze when switching between different screens or when
        creating a new character after one has already been created.
        """
        # Unselect race and class selection if user visited race/class selection screen previously. 'isinstance' check is
        # necessary as variables can hold either a screen object or a string during custom and random character creation
        # respectively.
        if isinstance(self.selected_race, InteractiveText):
            self.selected_race.selected = False
        if isinstance(self.selected_class, InteractiveText):
            self.selected_class.selected = False
        # Unselect spell selection if user visited spell selection screen previously.
        if self.selected_spell:
            self.selected_spell.selected = False

        # Reset attributes to 'None'.
        self.possible_characters: None = None
        self.selected_race: None = None
        self.selected_class: None = None
        self.selected_spell: None = None

        # Initialize/reset dict for use in 'gui/ui_helpers.py' in function 'position_race_class_elements()' to calculate
        # UI positioning, and automatically populate dict 'rc_dict' once with all races/classes available in the game
        # for later use in race/class selection.
        self.rc_dict = {
            "races": [race.text for race in uisd.gui_elements["active_races"]],
            "classes": [cls.text for cls in uisd.gui_elements["active_classes"]],
        }


shared_data = SharedData()
