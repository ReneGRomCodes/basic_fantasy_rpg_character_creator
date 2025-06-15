import pygame
import gui.screen_objects as so
from gui.ui_helpers import draw_screen_title
from gui.screen_objects import TextField, Button
from gui.shared_data import ui_shared_data as uisd

"""Helper class to organize and access save/load screen objects as attributes."""

class SaveLoadScreen:
    """A class to store and manage save/load screen elements."""

    def __init__(self, screen):
        """Initialize the SaveLoadScreen object with elements."""
        # Assign screen rect attributes.
        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.screen_height: int = self.screen_rect.height
        self.screen_width: int = self.screen_rect.width

        # Size variables and elements from dict 'gui_elements'.
        self.gui_elements: dict = uisd.gui_elements
        self.edge_spacing: int = uisd.gui_elements["default_edge_spacing"]
        title_size: int = uisd.gui_elements["title_size"]
        text_medium: int = uisd.gui_elements["text_medium"]

        # General screen objects.
        self.title: TextField = so.TextField(screen, "- SAVE/LOAD CHARACTER -", title_size)
        self.main_menu_button: Button = so.Button(screen, "Main Menu", text_medium)

    def show_sl_screen(self, screen, mouse_pos):
        draw_screen_title(screen, self.title)
        self.main_menu_button.draw_button(mouse_pos)

    def position_sl_elements(self):
        self.main_menu_button.button_rect.bottomright = (self.screen_rect.right - self.edge_spacing,
                                                         self.screen_rect.bottom - self.edge_spacing)
