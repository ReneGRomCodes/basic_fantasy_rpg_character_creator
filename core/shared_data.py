from gui.screen_objects import InteractiveText
from core.rules import get_class_categories, get_race_class_defaults
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
        self.save_load_screen: object | None # Instance 'SaveLoadScreen()'.
        self.credits_screen: object | None = None  # Instance 'Credits()'.
        self.settings_gui: object = None  # Instance 'SettingsGUI()'
        self.cs_sheet: object | None = None  # Instance of 'CharacterSheet'.

        # Class sets for category checks (example: spell selection screen shown only for magic using classes).
        self.spell_using_classes, self.magic_classes, self.no_armor_classes = get_class_categories()
        # Dicts of default values for races and classes (spells, languages, etc.).
        self.default_spells, self.default_languages = get_race_class_defaults()

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

    @staticmethod
    def handle_selection_logic(option: InteractiveText, selected_attr: InteractiveText | None) -> InteractiveText | None:
        """General method to handle detailed selection logic for race/class, spell and language selection screens.
        ARGS:
            option: selected instance of 'InteractiveText'.
            selected_attr: instance attribute relevant to selection screen (i.e. 'self.selected_race' for race selection).
                Value is 'None' if no selection has been made.
        RETURNS:
            selected_attr
        """
        # Check if option is already selected.
        if selected_attr:
            # Deselect option if the same option is clicked again.
            if selected_attr == option:
                option.selected = False
                selected_attr = None
            # Switch selection if different option is chosen.
            else:
                selected_attr.selected = False
                option.selected = True
                selected_attr = option
        # Set selected option if none has been previously chosen.
        else:
            option.selected = True
            selected_attr = option

        return selected_attr

    def select_race_class(self, option: InteractiveText) -> None:
        """Selection logic for race/class selection screen. Set class attributes 'selected_race' and 'selected_class'
        to interactive text field instances.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected race or class.
        """
        # Race selection logic.
        if option in uisd.gui_elements["active_races"]:
            self.selected_race = self.handle_selection_logic(option, self.selected_race)
        # Class selection logic.
        elif option in uisd.gui_elements["active_classes"]:
            self.selected_class = self.handle_selection_logic(option, self.selected_class)

    def clear_race_class_selection(self):
        """Reset entire race/class selection."""
        if self.selected_race:
            self.selected_race.selected = False
            self.selected_race = None
        if self.selected_class:
            self.selected_class.selected = False
            self.selected_class = None

    def set_default_spell(self, spells: tuple[InteractiveText, ...]) -> None:
        """Check the selected class for default spells and set 'selected' attribute of corresponding spell InteractiveText
        instances on screen to 'True'.
        Method is called in every frame from state 'spell_selection' in state manager to ensure default spells are
        always displayed as selected.
        ARGS:
            spells: tuple with instances of interactive text fields for spell selection.
        """
        for spell in spells:
            if spell.text in self.default_spells[self.character.class_name.lower()]:
                spell.selected = True

    def select_spell(self, option: InteractiveText) -> None:
        """Selection logic for character's spell. Set class attribute 'selected_spell' to interactive text instance.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected spell.
        """
        # Spell selection logic.
        self.selected_spell = self.handle_selection_logic(option, self.selected_spell)

    def set_default_languages(self, languages: tuple[InteractiveText, ...]) -> None:
        """Check the selected race for default languages and set 'selected' attribute of corresponding language
        InteractiveText instances on screen to 'True'.
        Method is called in every frame from state 'language_selection' in state manager to ensure default languages are
        always displayed as selected.
        ARGS:
            languages: tuple with instances of interactive text fields for language selection.
        """
        for language in languages:
            if language.text in self.default_languages[self.character.race_name.lower()]:
                language.selected = True

    def select_languages(self, option) -> None:
        """Selection logic for character's languages. Set class attribute 'selected_languages' to interactive text
        instance.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected language.
        """
        # language selection logic.
        self.selected_languages = self.handle_selection_logic(option, self.selected_languages)

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
        # Unselect language selection if user visited language selection screen previously.
        if self.selected_languages:
            self.selected_languages.selected = False

        # Reset attributes to 'None'.
        self.possible_characters: None = None
        self.selected_race: None = None
        self.selected_class: None = None
        self.selected_spell: None = None
        self.selected_languages: None = None

        # Initialize/reset dict for use in 'gui/ui_helpers.py' in function 'position_race_class_elements()' to calculate
        # UI positioning, and automatically populate dict 'rc_dict' once with all races/classes available in the game
        # for later use in race/class selection.
        self.rc_dict = {
            "races": [race.text for race in uisd.gui_elements["active_races"]],
            "classes": [cls.text for cls in uisd.gui_elements["active_classes"]],
        }


shared_data = SharedData()
