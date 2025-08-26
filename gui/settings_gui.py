"""
Class for settings screen.
"""
import pygame

from core.settings import settings

from .screen_objects import TextField, InteractiveText, Button
from .ui_helpers import draw_screen_title, draw_button_background_image
from .ui_registry import initialize_ui_registry
from .shared_data import ui_shared_data as uisd


class SettingsGUI:
    """Class to store, manage and show settings screen for pygame."""

    def __init__(self, screen) -> None:
        """Initialize settings screen elements.
        ARGS:
            screen: PyGame window.
        """
        self.title_size: int = uisd.ui_registry["title_size"]
        self.text_large: int = uisd.ui_registry["text_large"]
        self.text_medium: int = uisd.ui_registry["text_medium"]

        # Screen title.
        self.title: TextField = TextField(screen, "- SETTINGS -", self.title_size)

        # Window size settings elements.
        self.window_size_field: TextField = TextField(screen, "Window Size", self.text_large)
        window_size_button_small: InteractiveText = InteractiveText(screen, "1280x720", self.text_medium, select=True)
        window_size_button_medium: InteractiveText = InteractiveText(screen, "1600x900", self.text_medium, select=True)
        window_size_button_large: InteractiveText = InteractiveText(screen, "1920x1080", self.text_medium, select=True)
        window_size_button_full: InteractiveText = InteractiveText(screen, "Full Screen", self.text_medium, select=True)

        # Window size UI objects and corresponding 'settings' attributes.
        self.size_settings: tuple[tuple[InteractiveText, tuple[int, int] | bool], ...] = (
            (window_size_button_small, settings.small_screen),
            (window_size_button_medium, settings.medium_screen),
            (window_size_button_large, settings.large_screen),
            (window_size_button_full, False)
        )
        self.size_buttons_list: list[InteractiveText] = [item[0] for item in self.size_settings]

        # Selected window attribute initialized with starting value 'None'. Default value is then assigned when
        # 'self.get_default_settings()' is called.
        self.selected_window_size: InteractiveText | None = None

        # Collection of ALL instances from module 'gui.screen_objects' used in settings screen as created above.
        self.settings_gui_objects: tuple[TextField | InteractiveText, ...] = (self.title, self.window_size_field,
                                                                              window_size_button_small, window_size_button_medium,
                                                                              window_size_button_large, window_size_button_full)

        self.get_default_settings()

    def get_default_settings(self) -> None:
        """Set default settings as defined in 'core.settings.py'."""
        size_setting_index: int = 1
        size_button_index: int = 0

        for setting in self.size_settings:
            if setting[size_setting_index] in settings.default_settings:
                self.selected_window_size: InteractiveText = setting[size_button_index]
                self.selected_window_size.selected = True

    def show_settings(self, screen, mouse_pos) -> None:
        """Display settings screen.
            ARGS:
                screen: PyGame window.
                mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
            """
        back_button: Button = uisd.ui_registry["back_button"]

        self.format_settings_screen_elements(screen)
        self.format_position_element_background(screen)

        draw_screen_title(screen, self.title)
        draw_button_background_image(screen, back_button)
        back_button.draw_button(mouse_pos)

        self.window_size_field.draw_text()

        for button in self.size_buttons_list:
            # Reset the surface if it exists and its size doesn't match the rect. Prevents unnecessary reassignments
            # while ensuring it updates when window size is changed.
            if button.interactive_text_surface and (button.interactive_text_surface.get_size() != button.interactive_rect.size):  # type: ignore
                button.interactive_text_surface = None

            button.draw_interactive_text(mouse_pos)

    def format_settings_screen_elements(self, screen) -> None:
        """Format and position objects from 'ui_registry' for settings screen."""
        spacing: int = uisd.ui_registry["default_edge_spacing"]
        screen_x: int = screen.get_rect().centerx
        screen_y: int = screen.get_rect().centery

        window_size_anchor: pygame.Rect = self.size_buttons_list[0].interactive_rect
        window_size_medium: pygame.Rect = self.size_buttons_list[1].interactive_rect
        window_size_large: pygame.Rect = self.size_buttons_list[2].interactive_rect
        window_size_full: pygame.Rect = self.size_buttons_list[3].interactive_rect

        for button in self.size_buttons_list:
            button.interactive_rect.width, button.interactive_rect.height = screen.get_rect().width / 8, screen.get_rect().height  / 12

        self.window_size_field.text_rect.centery = screen_y
        self.window_size_field.text_rect.right = screen_x - spacing
        # Position selection fields for window sizes. 'window_size_anchor' is placed first as anchor for positioning
        # of further buttons. To move the entire block only the anchor has to be moved.
        window_size_anchor.left, window_size_anchor.bottom = screen_x + spacing, int(screen_y - spacing / 2)
        window_size_medium.left, window_size_medium.bottom = window_size_anchor.right + spacing, window_size_anchor.bottom
        window_size_large.left, window_size_large.top = window_size_anchor.left, window_size_anchor.bottom + spacing
        window_size_full.left, window_size_full.top = window_size_anchor.right + spacing, window_size_anchor.bottom + spacing

    @staticmethod
    def format_position_element_background(screen) -> None:
        """Format, position and draw element background on screen.
        ARGS:
            screen: PyGame Window.
        """
        bg_image_width = screen.get_rect().width / 1.2
        bg_image_height = screen.get_rect().height / 2
        bg_image = pygame.transform.scale(uisd.ui_registry["parchment_images"][0], (bg_image_width, bg_image_height))
        bg_rect = bg_image.get_rect(center=screen.get_rect().center)

        screen.blit(bg_image, bg_rect)

    def select_window_size(self, screen, mouse_pos) -> None:
        """Selection logic for program's window size. Change attribute 'self.selected_window_size', re-initialize  and
        return dict 'ui_registry'.
        ARGS:
            screen: PyGame window.
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        """
        size_setting_index: int = 1
        size_button_index: int = 0

        for size in self.size_buttons_list:
            if size.interactive_rect.collidepoint(mouse_pos):
                if self.selected_window_size != size:
                    self.selected_window_size.selected = False
                    self.selected_window_size = size
                    self.selected_window_size.selected = True
                break

        for button in self.size_buttons_list:
            button.selected = (button == self.selected_window_size)

        for setting in self.size_settings:

            if setting[size_button_index].selected == True and setting[size_setting_index] != settings.screen_size:
                settings.screen_size = setting[size_setting_index]
                if setting[size_setting_index]:
                    pygame.display.set_mode(settings.screen_size)
                else:
                    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                # Wait 200ms to avoid immediate click registration directly after new window size is set.
                pygame.time.wait(200)

                uisd.ui_registry = initialize_ui_registry(screen)
                # Update text size of screen elements in settings screen. See method docstring for details.
                self.update_text_size()

            # Re-assign window size to 'selected_window_size' by comparing 'text' attributes with
            # 'setting[size_button_index]', replacing 'selected_window_size' with equivalent object and set its attribute
            # to 'True'. Re-initialization of dict 'ui_registry' above leads to 'selected_window_size' pointing to
            # obsolete object otherwise.
            if self.selected_window_size.text == setting[size_button_index].text:
                self.selected_window_size = setting[size_button_index]
                self.selected_window_size.selected = True

    def update_text_size(self) -> None:
        """Assign new values to text size attributes in '__init__()', then resize and render text for screen elements in
        settings screen.
        To be called after new window size is selected and 'ui_registry' is re-initialized. Screen element instances
        would otherwise keep their original sizes."""
        title_size_old: int = self.title_size
        text_large_old: int = self.text_large
        text_medium_old: int = self.text_medium

        self.title_size: int = uisd.ui_registry["title_size"]
        self.text_large: int = uisd.ui_registry["text_large"]
        self.text_medium: int = uisd.ui_registry["text_medium"]

        for item in self.settings_gui_objects:
            if item.size == title_size_old:
                item.size = self.title_size
            elif item.size == text_large_old:
                item.size = self.text_large
            elif item.size == text_medium_old:
                item.size = self.text_medium

            item.render_new_text_surface(settings_gui=True)
