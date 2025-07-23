"""
Shared data class for GUI.
Only instance of this class, 'ui_shared_data', is created at the bottom of this module and imported/referenced in
'ui_helpers.py' and 'core/event_handlers.py'.
"""


class UISharedData:
    """Class for initialization and storage of attributes relevant for GUI functions for pygame screens."""

    def __init__(self) -> None:
        """Initialize shared data attributes."""
        # Dict of all UI elements populated during init (see 'initialize_ui_registry()' in 'main.py').
        self.ui_registry: dict = {}

        # If 'True', save/load screen runs in "load-only" mode (see 'SaveLoadScreen' in 'sl_model.py').
        self.load_only_flag: bool = False
        # Holds 'slot_id' if character is loaded from JSON, otherwise 'False'.
        self.is_loaded: str | False = False

        # Prevents repositioning of screen elements if they've already been placed. Used in most screens—except ones
        # like the ability score screen (gui/gui.py), where elements reuse the same objects but with different values.
        self.position_flag: bool = False

        # Y-position maps for race/class text elements.
        self.race_pos_y_dict: dict[str, int] = {}
        self.class_pos_y_dict: dict[str, int] = {}
        # Available race/class options.
        self.rc_options: dict[str, list] = {}

        # 'True' if character can learn extra languages (see 'set_language_flag()' in 'rules.py').
        self.language_flag: bool = False
        # Y-position map for language elements.
        self.lang_pos_y_dict: dict[str, int] = {}
        # 'True' while user is still picking languages. Turned 'False' when max is reached.
        self.lang_selection_active: bool = True

        # Dice roll animation timer start and state.
        self.dice_roll_start_time: int = 0
        self.dice_roll_complete: bool = False

    def reset_position_flag(self) -> None:
        """Reset position flag to 'False'. Used in event handler."""
        self.position_flag = False

    def reset_input_fields(self) -> None:
        """Reset text input fields to ensure each character creation process starts with empty input fields. Called from
        event handler in state 'creation_complete' before initializing character sheet screen."""
        self.ui_registry["character_name_input"][0].manager.value = ""
        self.ui_registry["money_amount_input"][0].manager.value = ""


ui_shared_data = UISharedData()
