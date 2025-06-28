"""
Shared data class for GUI.
Only instance of this class, 'ui_shared_data', is created at the bottom of this module and imported/referenced in
'ui_helpers.py' and 'core/event_handlers.py'.
"""


class UISharedData:
    """Class for initialization and storage of attributes relevant for GUI functions for pygame screens."""

    def __init__(self) -> None:
        """Initialize shared data attributes."""
        # Dict of UI elements as created in 'gui/gui_elements.py'. Relevant function call to populate the dict is called
        # from 'run_character_creator()' in 'main.py' when program is initialized.
        self.gui_elements: dict = {}

        # Flag to set mode in which save/load screen is displayed. 'False' allows for save and load, 'True' for load only.
        # See class 'SaveLoadScreen' in 'sl_model.py' for details.
        self.load_only_flag: bool = False

        # Flag to ensure screen-specific elements are positioned only once per appearance.
        # Used in non-adaptable screens to minimize unnecessary repositioning, but not applied to some adaptable screens
        # to keep functions more maintainable.
        self.position_flag: bool = False

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
