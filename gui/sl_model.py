import pygame
import os
import json
import gui.screen_objects as so
from gui.ui_helpers import draw_screen_title, set_elements_pos_y_values
from gui.screen_objects import TextField, Button, InteractiveText
from gui.shared_data import ui_shared_data as uisd
from core.shared_data import shared_data as sd
from core.settings import settings

"""Helper class to organize and access save/load screen objects as attributes."""

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
        # Tuple with 'Button' instances for use in for-loops when accessing instances.
        self.button_group: tuple[Button, ...] = (self.exit_button, self.save_button, self.load_button)
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
        for k, v in self.slots.items():
            with open(settings.save_file) as f:
                data = json.load(f)
                if data[k]:
                    v.text = f"{data[k]["name"] if data[k]["name"] else "UNNAMED"}: {data[k]["race_name"]} {data[k]["class_name"]}"
                else:
                    slot_text: list[str] = k.split("_")
                    v.text = f"{slot_text[0].capitalize()} {slot_text[1]}: EMPTY"
            v.interactive_rect.width = int(self.screen_width / 2)
            v.render_new_text_surface()

    def save_character(self, state: str) -> str:
        save_slot_selected: bool = False
        with open(settings.save_file) as f:
            data = json.load(f)
            for key, slot in self.slots.items():
                if slot.selected:
                    save_slot_selected = True
                    data[key] = sd.character.serialize()
                    slot.text = f"{sd.character.name} {sd.character.race_name} {sd.character.class_name}"
                    break

        if save_slot_selected:
            with open(settings.save_file, "w") as f:
                json.dump(data, f)
                state = "init_character_sheet"

        return state

    def load_character(self, state) -> str:
        with open(settings.save_file) as f:
            data = json.load(f)
            for key, slot in self.slots.items():
                if slot.selected and data[key]:
                    sd.character.deserialize(data[key])
                    state = "init_character_sheet"
                    break
                else:
                    state = "init_save_load_screen"

        return state
