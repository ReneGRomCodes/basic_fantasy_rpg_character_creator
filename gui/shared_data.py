"""
Shared data class for GUI.
Only instance of this class, 'ui_shared_data', is created at the bottom of this module and imported/referenced in
'ui_helpers.py' and 'core/event_handlers.py'.
"""


class UISharedData:
    """Class for initialization and storage of attributes relevant for GUI functions for pygame screens."""

    def __init__(self) -> None:
        """Initialize shared data attributes."""
        # Dict of UI elements as created in 'gui/ui_registry.py'. Relevant function call to populate the dict is called
        # from 'run_character_creator()' in 'main.py' when program is initialized.
        self.ui_registry: dict = {}

        # Flag to set mode in which save/load screen is displayed. 'False' allows for save and load, 'True' for load only.
        # See class 'SaveLoadScreen' in 'sl_model.py' for details.
        self.load_only_flag: bool = False
        # Attribute to check if character has been loaded in from 'characters.json'. Contains 'slot_id' string if so.
        self.is_loaded: str | False = False

        # Flag to ensure screen-specific elements are positioned only once per appearance.
        # Used to minimize unnecessary repositioning in most screens. Exceptions are screens which use single screen
        # objects with changing attributes to display different values (See ability score screen functions in 'gui/gui.py'
        # as an example).
        self.position_flag: bool = False

        # Dicts with y-positions for race and class elements.
        self.race_pos_y_dict: dict[str, int] = {}
        self.class_pos_y_dict: dict[str, int] = {}
        # Dict for lists of available race/class options.
        self.rc_options: dict[str, list] = {}

        # Flag to check if character can learn additional languages. Set in event handler in state "show_abilities"
        # by calling function 'set_language_flag()' from 'rules.py' module after ability scores are set. Used to decide
        # if language selection screen should be displayed.
        self.language_flag: bool = False
        # Dict with y-positions for language elements.
        self.lang_pos_y_dict: dict[str, int] = {}
        # Flag to check if language selection is still active (True). Set to 'False' in 'shared_data' (core) when
        # maximum number of additional languages have been selected.
        self.lang_selection_active: bool = True

        # Create int variable 'dice_roll_start_time' to be used as timer for dice roll effect on screen (e.g. starting
        # money screen).
        self.dice_roll_start_time: int = 0
        # Bool to check if dice roll is complete and active continue button should be displayed.
        self.dice_roll_complete: bool = False

    def reset_position_flag(self) -> None:
        """Reset position flag to 'False'. Used in event handler."""
        self.position_flag = False


ui_shared_data = UISharedData()
