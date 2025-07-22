"""
Shared data class for character creation process.
Only instance of this class, 'shared_data', is created at the bottom of this module and imported/referenced in
'state_manager.py' and 'event_handlers.py'.
"""
from gui.screen_objects import InteractiveText
from gui.shared_data import ui_shared_data as uisd

from .rules import RACE_DATA, CLASS_DATA


class SharedData:
    """Class for initialization and storage of attributes relevant throughout the character creation process and contains
    selection logic methods for various screens (race/class selection, spell selection, etc.)."""

    def __init__(self) -> None:
        """Initialize shared data attributes."""
        # Variable for later instances of class objects.
        self.character: object | None = None
        self.save_load_screen: object | None
        self.credits_screen: object | None = None
        self.settings_gui: object = None
        self.cs_sheet: object | None = None

        self.possible_characters: list[str] | None = None
        # 'InteractiveText' instances representing selected race and class in custom creation, string in random creation.
        self.selected_race: InteractiveText | str | None = None
        self.selected_class: InteractiveText | str | None = None

        self.selected_spell: InteractiveText | None = None

        self.selected_languages: list[InteractiveText] = []

        self.starting_money: int = 0
        self.random_money_flag: bool = False  # Flag to check money selection.
        self.custom_money_flag: bool = False  # Flag to check money selection.

    @staticmethod
    def handle_selection_logic(option: InteractiveText, selected_attr: InteractiveText | None | list[InteractiveText],
                               multi_selection: bool = False, limit: bool | int = False)\
            -> InteractiveText | None | list[InteractiveText]:
        """General method to handle detailed selection logic for race/class, spell and language selection screens.
        NOTE: Method handles selection logic where a single option can be selected by default. See ARGS 'mult_selection'
            and 'limit' for details on how to handle multiple selections.
            Race- or class-specific default selections do NOT count towards additional selections and don't use
            'multi_use' and 'limit' arguments.
        ARGS:
            option: selected instance of 'InteractiveText'.
            selected_attr: instance attribute relevant to selection screen (i.e. 'self.selected_race' for race selection).
                Value is 'None' or empty list if no selection has been made.
            multi_selection: triggers permission for selection of multiple element. Default is 'False'.
            limit: int value for number of elements that can be selected if 'multi_selection=True'. Default is 'False'.
        RETURNS:
            selected_attr
        """
        if not multi_selection:
            if selected_attr:
                if selected_attr == option:
                    selected_attr = None
                else:
                    selected_attr.selected = False
                    selected_attr = option
            else:
                selected_attr = option

        else:
            if selected_attr:
                if option in selected_attr:
                    selected_attr.remove(option)
                else:
                    if len(selected_attr) < limit:
                        selected_attr.append(option)
                    else:
                        # Set 'selected' attribute to 'False' to override 'handle_mouse_interaction()' method of class
                        # 'InteractiveText' setting it to 'True'. See class method docstring for details.
                        option.selected = False
            else:
                selected_attr = [option]

        return selected_attr

    def select_race_class(self, option: InteractiveText) -> None:
        """Selection logic for race/class selection screen. Set class attributes 'selected_race' and 'selected_class'
        to interactive text field instances.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected race or class.
        """
        if option in uisd.ui_registry["active_races"]:
            self.selected_race = self.handle_selection_logic(option, self.selected_race)
        elif option in uisd.ui_registry["active_classes"]:
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
        default_spells = CLASS_DATA[self.character.class_name]["spells"]

        for spell in spells:
            if spell.text in default_spells:
                spell.selected = True

    def select_spell(self, option: InteractiveText) -> None:
        """Selection logic for character's spell. Set class attribute 'selected_spell' to interactive text instance.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected spell.
        """
        default_spells = CLASS_DATA[self.character.class_name]["spells"]

        # Ignore selection if clicked spell is the class-specific default. Prevents it from overriding other selections.
        if option.text not in default_spells:
            self.selected_spell = self.handle_selection_logic(option, self.selected_spell)

    def set_default_languages(self, languages: tuple[InteractiveText, ...]) -> None:
        """Check the selected race for default languages and set 'selected' attribute of corresponding language
        InteractiveText instances on screen to 'True'.
        Method is called in every frame from state 'language_selection' in state manager to ensure default languages are
        always displayed as selected.
        ARGS:
            languages: tuple with instances of interactive text fields for language selection.
        """
        default_languages = RACE_DATA[self.character.race_name]["languages"]

        for language in languages:
            if language.text in default_languages:
                language.selected = True

    def select_languages(self, option: InteractiveText) -> None:
        """Selection logic for character's languages. Populate list 'self.selected_languages' storing interactive text
        instance.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected language.
        """
        default_languages = RACE_DATA[self.character.race_name]["languages"]

        # Number of languages a character can learn in addition to race-specific languages. Value equals character's
        # intelligence bonus.
        max_additional_languages: int = self.character.abilities["int"][1]

        # Ignore selection if clicked language is a race-specific default. Prevents it from overriding other selections.
        if option.text not in default_languages:
            self.selected_languages = self.handle_selection_logic(option, self.selected_languages, multi_selection=True,
                                                                  limit=max_additional_languages)

        if max_additional_languages == len(self.selected_languages):
            uisd.lang_selection_active = False
        else:
            uisd.lang_selection_active = True

    def clear_language_selection(self) -> None:
        """Reset entire language selection."""
        for language in uisd.ui_registry["lang_fields"]:
            language.selected = False
        self.selected_languages: list = []

        uisd.lang_selection_active = True

    def shared_data_janitor(self) -> None:
        """Reset shared data not automatically overwritten elsewhere with default values in case of a switch to a
        previous screen or the main menu.

        Method is called in event handler 'naming_character_events()' when returning to character menu from
        'name_random_character' state, in addition to its method calls in states 'pre_main_menu' and 'show_abilities'.
        This resolves multiple issues that caused the program to freeze when switching between different screens or when
        creating a new character after one has already been created.
        """
        if isinstance(self.selected_race, InteractiveText):
            self.selected_race.selected = False
        if isinstance(self.selected_class, InteractiveText):
            self.selected_class.selected = False

        if self.selected_spell:
            self.selected_spell.selected = False
        if self.selected_languages:
            for language in self.selected_languages:
                language.selected = False

        self.possible_characters: None = None
        self.selected_race: None = None
        self.selected_class: None = None
        self.selected_spell: None = None
        self.selected_languages: list[InteractiveText] = []
        self.cs_sheet: None = None


shared_data = SharedData()
