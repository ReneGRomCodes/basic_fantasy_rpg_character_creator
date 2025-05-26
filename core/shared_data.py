from gui.screen_objects import TextField, InteractiveText
"""
Shared data class for character creation process.
Only instance of this class, 'shared_data', is created at the bottom of this module and imported/referenced in
'state_manager.py' and 'event_handlers.py'.
"""


class SharedData:
    """Class for initialization and storage of attributes relevant throughout the character creation process."""

    def __init__(self) -> None:
        """Initialize shared data attributes."""
        # Variable for later instances of class objects.
        self.character: object  # Instance 'Character()'.
        self.credits_screen: object  # Instance 'Credits()'.
        self.settings_gui: object = None  # Instance 'SettingsGUI()'
        self.cs_sheet: object  # Instance of 'CharacterSheet'.

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

        # Characters starting money.
        self.starting_money: int = 0
        self.random_money_flag: bool = False  # Flag to check money selection.
        self.custom_money_flag: bool = False  # Flag to check money selection.

    def shared_data_janitor(self, gui_elements: dict) -> None:
        """Reset shared data not automatically overwritten elsewhere with default values in case of a switch to a
        previous screen or the main menu.

        Method is imported into and called in event handler 'naming_character_events()' when returning to character menu
        from 'name_random_character' state, in addition to its function calls in states 'pre_main_menu' and 'show_abilities'.
        This resolves multiple issues that caused the program to freeze when switching between different screens or when
        creating a new character after one has already been created.

        ARGS:
            gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        """
        # Unselect race and class selection if user visited race/class selection screen previously. 'isinstance' check is
        # necessary as variables can hold either a screen object or a string during custom and random character creation
        # respectively.
        if isinstance(self.selected_race, InteractiveText):
            self.selected_race.selected = False
        if isinstance(self.selected_class, InteractiveText):
            self.selected_class.selected = False

        # Reset attributes to 'None'.
        self.possible_characters: None = None
        self.selected_race: None = None
        self.selected_class: None = None

        # Initialize/reset dict for use in 'gui/ui_helpers.py' in function 'position_race_class_elements()' to calculate
        # UI positioning, and automatically populate dict 'rc_dict' once with all races/classes available in the game
        # for later use in race/class selection.
        self.rc_dict = {
            "races": [race.text for race in gui_elements["active_races"]],
            "classes": [cls.text for cls in gui_elements["active_classes"]],
        }


shared_data = SharedData()
