"""
Shared data class for character creation process.
Only instance of this class, 'shared_data', is created at the bottom of this module and imported/referenced in
'state_manager.py' and 'event_handlers.py'.
"""
from gui.screen_objects import InteractiveText
from gui.shared_data import ui_shared_data as uisd

from .rules import get_class_categories, get_race_class_defaults


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
        self.selected_languages: list[InteractiveText] = []

        # Characters starting money.
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
            # Check if option is already selected.
            if selected_attr:
                # Deselect option if the same option is clicked again.
                if selected_attr == option:
                    selected_attr = None
                # Switch selection if different option is chosen.
                else:
                    selected_attr.selected = False
                    selected_attr = option
            # Set selected option if none has been previously chosen.
            else:
                selected_attr = option

        else:
            if selected_attr:
                # Deselect option if the same option is clicked again.
                if option in selected_attr:
                    selected_attr.remove(option)
                # Add selection to list.
                else:
                    # Check if selection limit is reached and add option to 'selected_attr' if permitted.
                    if len(selected_attr) < limit:
                        selected_attr.append(option)
                    else:
                        # Set 'selected' attribute to 'False' to override 'handle_mouse_interaction()' method of class
                        # 'InteractiveText' setting it to 'True'. See class method docstring for details.
                        option.selected = False
            # Add selection if list is empty.
            else:
                selected_attr = [option]

        return selected_attr

    def select_race_class(self, option: InteractiveText) -> None:
        """Selection logic for race/class selection screen. Set class attributes 'selected_race' and 'selected_class'
        to interactive text field instances.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected race or class.
        """
        # Race selection logic.
        if option in uisd.ui_registry["active_races"]:
            self.selected_race = self.handle_selection_logic(option, self.selected_race)
        # Class selection logic.
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
        for spell in spells:
            if spell.text in self.default_spells[self.character.class_name.lower()]:
                spell.selected = True

    def select_spell(self, option: InteractiveText) -> None:
        """Selection logic for character's spell. Set class attribute 'selected_spell' to interactive text instance.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected spell.
        """
        # Ignore selection if clicked spell is the class-specific default. Prevents it from overriding other selections.
        if option.text not in self.default_spells.values():
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

    def select_languages(self, option: InteractiveText) -> None:
        """Selection logic for character's languages. Populate list 'self.selected_languages' storing interactive text
        instance.
        ARGS:
            option: selected instance of 'InteractiveText' representing selected language.
        """
        # Number of languages a character can learn in addition to race-specific languages. Value equals character's
        # intelligence bonus.
        max_additional_languages: int = self.character.abilities["int"][1]

        # Ignore selection if clicked language is a race-specific default. Prevents it from overriding other selections.
        if option.text not in self.default_languages[self.character.race_name.lower()]:
            # language selection logic.
            self.selected_languages = self.handle_selection_logic(option, self.selected_languages, multi_selection=True,
                                                                  limit=max_additional_languages)

        # Check if maximum number of additional languages have been selected and deactivate further selection by setting
        # corresponding flag in 'ui_shared_data'.
        if max_additional_languages == len(self.selected_languages):
            uisd.lang_selection_active = False
        else:
            uisd.lang_selection_active = True

    def clear_language_selection(self) -> None:
        """Reset entire language selection."""
        # Reset all languages to unselected state.
        for language in uisd.ui_registry["lang_fields"]:
            language.selected = False
        # Set 'self.selected_languages' to default value.
        self.selected_languages: list = []
        # Set flag 'uisd.lang_selection_active' to default value in case selection permission has been denied previously,
        # because maximum number of additional languages have been chosen before reset.
        uisd.lang_selection_active = True

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
            for language in self.selected_languages:
                language.selected = False

        # Reset attributes to 'None'.
        self.possible_characters: None = None
        self.selected_race: None = None
        self.selected_class: None = None
        self.selected_spell: None = None
        self.selected_languages: list[InteractiveText] = []
        self.cs_sheet: None = None


shared_data = SharedData()
