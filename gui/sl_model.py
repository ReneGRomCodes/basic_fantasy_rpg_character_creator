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
        self.buttons: tuple[Button, ...] = (self.exit_button, self.save_button, self.load_button)
        # Set default button width.
        for button in self.buttons:
            button.button_rect.width = gui_elements["default_button_width"]

    def show_sl_screen(self, mouse_pos):
        """Draw save/load screen elements.
        ARGS:
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        # Draw general screen objects.
        draw_screen_title(self.screen, self.title)
        # Draw buttons.
        for button in self.buttons:
            button.draw_button(mouse_pos)

    def position_sl_elements(self):
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
