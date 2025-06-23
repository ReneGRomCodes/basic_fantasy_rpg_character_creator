import pygame
import json
import gui.screen_objects as so
from gui.ui_helpers import draw_screen_title, set_elements_pos_y_values
from gui.screen_objects import TextField, Button, InteractiveText
from gui.shared_data import ui_shared_data as uisd
from core.shared_data import shared_data as sd
from core.settings import settings

"""Class to organize and access save/load screen objects as attributes."""

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

        # Size variables and elements from dict 'gui_elements'.
        gui_elements: dict = uisd.gui_elements
        self.edge_spacing: int = gui_elements["default_edge_spacing"]
        title_size: int = gui_elements["title_size"]
        text_medium: int = gui_elements["text_medium"]

        # Set strings for element text attributes based on screen mode flag.
        if self.load_only:
            self.title_text: str = "- LOAD CHARACTER -"
            self.exit_button_text: str = "Main Menu"
        else:
            self.title_text: str = "- SAVE/LOAD CHARACTER -"
            self.exit_button_text: str = "Return"

        # General screen objects.
        self.title: TextField = so.TextField(screen, self.title_text, title_size)
        self.exit_button: Button = so.Button(screen, self.exit_button_text, text_medium)
        self.save_button: Button = so.Button(screen, "Save", text_medium)
        self.load_button: Button = so.Button(screen, "Load", text_medium)
        self.delete_button: Button = so.Button(screen, "Delete Character", text_medium)
        # Tuple with 'Button' instances for use in for-loops when accessing instances.
        self.button_group: tuple[Button, ...] = (self.exit_button, self.save_button, self.load_button, self.delete_button)
        # Set default button width.
        for button in self.button_group:
            button.button_rect.width = gui_elements["default_button_width"]

        # Character slots representing entries in file 'save/characters.json'.
        slot_00: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_01: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_02: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_03: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_04: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_05: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_06: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_07: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
        slot_08: InteractiveText = so.InteractiveText(screen, "", text_medium, select=True)
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
        # Configure field width and text attributes for each slot element based on stored data in 'characters.json'.
        self.configure_character_slots()

        # Tuple storing string 'slot_id' and object 'slot' if one is selected.
        self.selected_slot: bool | tuple[str, InteractiveText] = False

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
        self.exit_button.button_rect.bottomright = (self.screen_rect.right - self.edge_spacing,
                                                    self.screen_rect.bottom - self.edge_spacing)
        # Position delete button.
        self.delete_button.button_rect.bottom = self.screen_rect.bottom - self.edge_spacing

        # Position save and load buttons based on screen mode flag 'self.load_only'.
        if self.load_only:
            self.load_button.button_rect.bottomleft = (self.screen_rect.left + self.edge_spacing,
                                                       self.screen_rect.bottom - self.edge_spacing)
            # Position save button outside the screen to avoid accidental collision detection.
            self.save_button.button_rect.bottomright = self.screen_rect.topleft
        else:
            self.save_button.button_rect.bottomleft = (self.screen_rect.left + self.edge_spacing,
                                                       self.screen_rect.bottom - self.edge_spacing)
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
                slot.text = f"{slot_text[0].capitalize()} {slot_text[1]}: EMPTY"

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

        return state

    def load_character(self) -> str:
        """Load stored character from JSON file if valid slot is selected.
        RETURNS:
            program state as string
        """
        # Default text used to identify empty slots. ": EMPTY" is unique to the default text attribute for empty slots.
        empty_slot_check_str: str = ": EMPTY"

        if self.selected_slot and empty_slot_check_str not in self.selected_slot[1].text:
            with open(settings.save_file) as f:
                data = json.load(f)
                sd.character.deserialize(data[self.selected_slot[0]])
                return "init_character_sheet"

        # If no valid slot is selected, return to the save/load screen.
        return "init_save_load_screen"

    def delete_character(self) -> str:
        """Delete selected character from JSON file and reset file entry to default 'None'.
        RETURN:
            program state as string
        """
        if self.selected_slot:
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

        return "init_save_load_screen"
