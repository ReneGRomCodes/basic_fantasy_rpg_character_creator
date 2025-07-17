"""
Class to organize and access save/load screen objects as attributes.
"""
import json

import pygame

from core.shared_data import shared_data as sd
from core.settings import settings

from .ui_helpers import draw_screen_title, set_elements_pos_y_values
from .screen_objects import TextField, Button, InteractiveText
from .shared_data import ui_shared_data as uisd

"""
# Data structure for empty JSON file 'save/characters.json'.

data = {
    "slot_00": None,
    "slot_01": None,
    "slot_02": None,
    "slot_03": None,
    "slot_04": None,
    "slot_05": None,
    "slot_06": None,
    "slot_07": None,
    "slot_08": None,
}

'Settings' instance attribute 'settings.save_file' is used to reference save file.
"""

class SaveLoadScreen:
    """A class to store and manage save/load screen elements."""

    def __init__(self, screen) -> None:
        """Initialize the SaveLoadScreen object with elements."""
        # Assign screen rect attributes.
        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.screen_height: int = self.screen_rect.height
        self.screen_width: int = self.screen_rect.width

        # Check 'load_only_flag' in 'ui_shared_data' instance and set attribute for context-sensitive UI.
        # 'True' = load-only mode when accessing screen from main menu, 'False' = save/load mode when accessing from
        # character sheet screen.
        self.load_only: bool = uisd.load_only_flag

        # Size variables and elements from dict 'ui_registry'.
        ui_registry: dict = uisd.ui_registry
        self.edge_spacing: int = ui_registry["default_edge_spacing"]
        title_size: int = ui_registry["title_size"]
        text_standard: int = int(self.screen_height / 50)
        text_medium: int = ui_registry["text_medium"]

        # Set strings for element text attributes based on screen mode flag.
        if self.load_only:
            self.title_text: str = "- LOAD CHARACTER -"
            self.exit_button_text: str = "Main Menu"
        else:
            self.title_text: str = "- SAVE/LOAD CHARACTER -"
            self.exit_button_text: str = "Return"

        # General screen objects.
        self.title: TextField = TextField(screen, self.title_text, title_size)
        self.exit_button: Button = Button(screen, self.exit_button_text, text_medium)
        self.save_button: Button = Button(screen, "Save", text_medium)
        self.load_button: Button = Button(screen, "Load", text_medium)
        self.delete_button: Button = Button(screen, "Delete Character", text_medium)
        # Tuple with 'Button' instances for use in for-loops when accessing instances.
        self.button_group: tuple[Button, ...] = (self.exit_button, self.save_button, self.load_button, self.delete_button)
        # Set default button width.
        for button in self.button_group:
            button.button_rect.width = ui_registry["default_button_width"]

        # Character slots representing entries in file 'save/characters.json'.
        slot_00: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_01: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_02: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_03: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_04: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_05: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_06: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_07: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        slot_08: InteractiveText = InteractiveText(screen, "", text_medium, select=True)
        # Dict with slot elements assigned as values to keys which correspond to keys in 'save/characters.json'.
        self.slots: dict[str, InteractiveText] = {
            "slot_00": slot_00,
            "slot_01": slot_01,
            "slot_02": slot_02,
            "slot_03": slot_03,
            "slot_04": slot_04,
            "slot_05": slot_05,
            "slot_06": slot_06,
            "slot_07": slot_07,
            "slot_08": slot_08,
        }
        # Default text used to format and identify empty slots. ": EMPTY" is unique to the default text attribute for
        # empty slots.
        self.empty_slot: str = ": EMPTY"
        # Configure field width and text attributes for each slot element based on stored data in 'characters.json'.
        self.configure_character_slots()

        # Tuple storing string 'slot_id' and object 'slot' if one is selected.
        self.selected_slot: bool | tuple[str, InteractiveText] = False

        # Confirmation message objects.
        self.not_saved_message: str = "Current character is not saved. Proceed anyway?"
        self.delete_message: str = "Delete selected character?"
        self.overwrite_message: str = "Overwrite selected character?"
        self.confirmation_message: TextField = TextField(screen, "", uisd.ui_registry["text_large"])
        self.confirm_proceed_button: Button = Button(screen, "PROCEED", text_standard)
        self.confirm_delete_button: Button = Button(screen, "DELETE", text_standard)
        self.confirm_overwrite_button: Button = Button(screen, "OVERWRITE", text_standard)
        self.cancel_button: Button = Button(screen, "CANCEL", text_standard)
        # Tuple with 'Button' instances for use in for-loops when accessing instances.
        self.confirm_buttons_group: tuple[Button, ...] = (self.confirm_proceed_button, self.confirm_delete_button,
                                                          self.confirm_overwrite_button, self.cancel_button)
        # Set confirmation buttons width.
        for button in self.confirm_buttons_group:
            button.button_rect.width = int(screen.get_rect().width / 5)

    def show_sl_screen(self, mouse_pos) -> None:
        """Draw save/load screen elements.
        ARGS:
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        # Draw general screen objects.
        draw_screen_title(self.screen, self.title)
        # Draw buttons.
        for button in self.button_group:
            button.draw_button(mouse_pos)

        # Draw character slots.
        for slot in self.slots.values():
            slot.draw_interactive_text(mouse_pos)

    def position_sl_elements(self) -> None:
        """Position save/load screen elements."""
        # Position exit button at the bottom right of the screen.
        self.exit_button.button_rect.bottomright = uisd.ui_registry["bottom_right_pos"]
        # Position delete button.
        self.delete_button.button_rect.bottom = self.screen_rect.bottom - self.edge_spacing

        # Position save and load buttons based on screen mode flag 'self.load_only'.
        if self.load_only:
            self.load_button.button_rect.bottomleft = uisd.ui_registry["bottom_left_pos"]
            # Position save button outside the screen to avoid accidental collision detection.
            self.save_button.button_rect.bottomright = uisd.ui_registry["off_screen_pos"]
        else:
            self.save_button.button_rect.bottomleft = uisd.ui_registry["bottom_left_pos"]
            self.load_button.button_rect.bottomleft = self.save_button.button_rect.bottomright

        # Position character slots.
        # Get dynamic y-positions for items in 'spells'.
        pos_y_start, pos_y_offset = set_elements_pos_y_values(self.screen, [slot for slot in self.slots.values()])

        for index, slot in enumerate([slot for slot in self.slots.values()]):
            # Align element x-position at screen center.
            slot.interactive_rect.centerx = self.screen_rect.centerx
            # Assign dynamic y-positions to elements.
            if index == 0:
                slot.interactive_rect.top = pos_y_start
            else:
                slot.interactive_rect.top = pos_y_start + pos_y_offset * index

    def configure_character_slots(self) -> None:
        """Set rect size and assign text attribute to character slots."""
        # Iterate through each entry in the 'self.slots' dict to check if a slot is used or empty.
        for slot_id, slot in self.slots.items():
            # Read the save file to compare each slot against the corresponding entry.
            with open(settings.save_file) as f:
                data = json.load(f)

            if data[slot_id]:
                # Set slot's text attribute if a character is saved at 'slot_id'.
                slot.text = (f"{data[slot_id]["name"] if data[slot_id]["name"] else "UNNAMED"}: "
                             f"{data[slot_id]["race_name"]} {data[slot_id]["class_name"]}")
            else:
                # Set default string ('Slot XX: EMPTY') if no character is saved at 'slot_id'.
                slot_text: list[str] = slot_id.split("_")
                slot.text = f"{slot_text[0].capitalize()} {slot_text[1]}{self.empty_slot}"

            # Adjust the slot's interactive rect width and render updated text surface.
            slot.interactive_rect.width = int(self.screen_width / 2)
            slot.render_new_text_surface()

    def select_character_slot(self, slot_id: str, slot: InteractiveText) -> None:
        """Selection logic for character slots. Updates 'self.selected_slot' to store the selected slot ID and instance.
        ARGS:
            slot_id: string corresponding to selected slot as stored in 'self.slots'.
            slot: selected 'InteractiveText' instance.
        """
        # If a slot is already selected, determine whether to deselect it or switch selection.
        if self.selected_slot:
            # If the selected slot is clicked again, deselect it and clear 'self.selected_slot'.
            if self.selected_slot[0] == slot_id:
                slot.selected = False
                self.selected_slot = False
            # Otherwise, switch selection to the newly clicked slot.
            else:
                self.selected_slot[1].selected = False
                slot.selected = True
                self.selected_slot = (slot_id, slot)
        else:
            # If no slot was selected, activate the clicked slot.
            slot.selected = True
            self.selected_slot = (slot_id, slot)

    def save_character(self, state: str) -> str:
        """Check if slot is selected and save created character in JSON file, assign descriptive text to slot's text
        attribute, and re-initialize screen to display updated slot.
        ARGS:
            state: program state.
        RETURNS:
            state
        """
        if self.selected_slot:
            if self.empty_slot in self.selected_slot[1].text or state == "char_overwrite":
                # Load existing save data.
                with open(settings.save_file) as f:
                    data = json.load(f)

                    # Save character data to the selected slot and update the slot's label.
                    data[self.selected_slot[0]] = sd.character.serialize()
                    self.selected_slot[1].text = f"{sd.character.name} {sd.character.race_name} {sd.character.class_name}"

                # Write updated data back to file and return to the save/load screen.
                with open(settings.save_file, "w") as f:
                    json.dump(data, f)
                    state = "init_save_load_screen"

                sd.cs_sheet.is_saved = self.selected_slot[0]
            else:
                state = "char_overwrite"

        return state

    def load_character(self) -> str:
        """Load stored character from JSON file if valid slot is selected.
        RETURNS:
            program state as string
        """
        if self.selected_slot and self.empty_slot not in self.selected_slot[1].text:
            if uisd.load_only_flag or sd.cs_sheet.is_saved:
                with open(settings.save_file) as f:
                    data = json.load(f)
                    sd.character.deserialize(data[self.selected_slot[0]])
                    uisd.is_loaded = self.selected_slot[0]
                    return "init_character_sheet"
            else:
                return "char_not_saved"

        # If no valid slot is selected, return to the save/load screen.
        return "init_save_load_screen"

    def delete_character(self, state: str) -> str:
        """Delete selected character from JSON file and reset file entry to default 'None'.
        ARGS:
            state: program state.
        RETURN:
            state
        """
        if state == "char_delete":
            # Check if deleted character is the currently active character and set its 'is_saved' attribute to 'False' if so.
            if sd.cs_sheet:
                if self.selected_slot[0] == sd.cs_sheet.is_saved:
                    sd.cs_sheet.is_saved = False

            # Load existing save data.
            with open(settings.save_file) as f:
                data = json.load(f)
                # Reset selected entry to default 'None'.
                data[self.selected_slot[0]] = None

            # Write updated data back to file and return to the save/load screen.
            with open(settings.save_file, "w") as f:
                json.dump(data, f)

            # Set 'self.selected_slot' back to 'False'.
            self.selected_slot: bool = False

            state = "init_save_load_screen"

        elif self.selected_slot:
            if self.empty_slot in self.selected_slot[1].text:  #type: ignore  # calm down pycharm, I checked it!
                state = "init_save_load_screen"
            else:
                state = "char_delete"

        return state

    def show_confirm_message(self, state, mouse_pos) -> None:
        """Draw confirmation message for save/load operations.
        ARGS:
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        # Draw confirmation message.
        self.confirmation_message.draw_text()

        # Draw cancel button.
        self.cancel_button.draw_button(mouse_pos)
        # Draw remaining buttons.
        for button in self.confirm_buttons_group:
            button.draw_button(mouse_pos)

    def position_confirm_message_elements(self, state) -> None:
        """Position confirmation message objects."""
        # Spacing and instance variables.
        edge_spacing = uisd.ui_registry["default_edge_spacing"]
        button_spacing = uisd.ui_registry["button_spacing"]
        confirm: TextField = self.confirmation_message
        # Position variables for buttons.
        button_top, button_right = self.screen_rect.centery + edge_spacing, self.screen_rect.centerx - button_spacing
        cancel_button_left = self.screen_rect.centerx + button_spacing

        # Position confirmation message.
        confirm.text_rect.bottom, confirm.text_rect.centerx = self.screen_rect.centery - edge_spacing, self.screen_rect.centerx

        # Position button instances outside of screen before positioning relevant buttons on screen based on program
        # state.
        for button in self.confirm_buttons_group:
            button.button_rect.bottomright = uisd.ui_registry["off_screen_pos"]

        if state == "char_not_saved":
            self.confirm_proceed_button.button_rect.top = button_top
            self.confirm_proceed_button.button_rect.right = button_right
        elif state == "char_delete":
            self.confirm_delete_button.button_rect.top = button_top
            self.confirm_delete_button.button_rect.right = button_right
        elif state == "char_overwrite":
            self.confirm_overwrite_button.button_rect.top = button_top
            self.confirm_overwrite_button.button_rect.right = button_right

        # Position cancel button again to mirror other buttons position along screens centerx axis.
        self.cancel_button.button_rect.top = button_top
        self.cancel_button.button_rect.left = cancel_button_left

    def format_confirm_message(self, state: str) -> None:
        """Format confirmation message based on program state.
        ARGS:
            state: program state.
        """
        confirm: TextField = self.confirmation_message

        if state == "char_not_saved":
            confirm.text = self.not_saved_message
        elif state == "char_delete":
            confirm.text = self.delete_message
        elif state == "char_overwrite":
            confirm.text = self.overwrite_message

        confirm.render_new_text_surface()
        self.position_confirm_message_elements(state)
