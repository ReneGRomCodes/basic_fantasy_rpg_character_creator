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

        # Flag to ensure screen-specific elements are positioned only once per appearance.
        # Used in non-adaptable screens to minimize unnecessary repositioning, but not applied to adaptable screens to
        # keep functions more maintainable.
        self.position_flag: bool = False

        # Create int variable 'dice_roll_start_time' to be used as timer for dice roll effect on screen (e.g. starting
        # money screen).
        self.dice_roll_start_time: int = 0

    def reset_position_flag(self) -> None:
        """Reset position flag to 'False'. Used in event handler."""
        self.position_flag = False


ui_shared_data = UISharedData()
