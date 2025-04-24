import gui.screen_objects as so
from gui.ui_helpers import draw_screen_title
import pygame
from gui.gui_elements import initialize_screen_elements
from core.settings import settings
"""
Class for settings screen.
"""


class SettingsGUI:
    """Class to store, manage and show settings screen for pygame."""

    def __init__(self, screen, gui_elements):
        """Initialize settings screen elements."""
        # Assign text sizes from 'gui_elements' to attributes.
        self.title_size, self.text_large, self.text_medium = (gui_elements["title_size"], gui_elements["text_large"],
                                                              gui_elements["text_medium"])

        # Screen title.
        self.title = so.TextField(screen, "- SETTINGS -", self.title_size)
        # Window size settings elements.
        self.window_size_field = so.TextField(screen, "Window Size", self.text_large)
        window_size_button_small = so.InteractiveText(screen, "1280x720", self.text_medium, select=True)
        window_size_button_medium = so.InteractiveText(screen, "1600x900", self.text_medium, select=True)
        window_size_button_large = so.InteractiveText(screen, "1920x1080", self.text_medium, select=True)
        window_size_button_full = so.InteractiveText(screen, "Full Screen", self.text_medium, select=True)
        # Tuple of window size option buttons.
        self.window_size_buttons = (window_size_button_small, window_size_button_medium,
                                    window_size_button_large, window_size_button_full)
        # Initialize attribute for selected window size with 'None' value. Value is assigned when first executing
        # method 'select_window_size()'.
        self.selected_window_size = None

        # Collection of ALL instances from module 'gui.screen_objects' used in settings screen and created above.
        self.settings_gui_objects = (self.title, self.window_size_field, window_size_button_small, window_size_button_medium,
                                     window_size_button_large, window_size_button_full)

    def show_settings(self, screen, gui_elements, mouse_pos):
        """Display settings screen.
            ARGS:
                screen: PyGame window.
                gui_elements: dict of gui elements as created in module 'gui_elements.py'.
                mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
            RETURNS:
                Re-initialized dict 'gui_elements'.
            """
        # Assign gui_elements to variables.
        back_button = gui_elements["back_button"]

        # Format elements on screen.
        self.format_settings_screen_elements(screen, gui_elements)

        # Select window size and re-initialize 'gui_elements'.
        gui_elements = self.select_window_size(screen, gui_elements, mouse_pos)

        # Draw basic elements on screen.
        draw_screen_title(screen, self.title, gui_elements)
        back_button.draw_button(mouse_pos)
        # Draw window size selection on screen.
        self.window_size_field.draw_text()
        for button in self.window_size_buttons:
            # Reset the surface if it exists and its size doesn't match the rect. Prevents unnecessary reassignments
            # while ensuring it updates when window size is changed.
            if button.interactive_text_surface and (button.interactive_text_surface.get_size() != button.interactive_rect.size):
                button.interactive_text_surface = None

            button.draw_interactive_text(mouse_pos)

        return gui_elements

    def format_settings_screen_elements(self, screen, gui_elements):
        """Format and position objects from 'gui_elements' for settings screen."""
        # Assign elements to variables.
        spacing = gui_elements["default_edge_spacing"]
        screen_x = screen.get_rect().centerx
        screen_y = screen.get_rect().centery
        # Assign anchor object 'window_size_buttons[0].interactive_rect' (small window) and further options to variables for
        # easier positioning and better readability.
        window_size_anchor = self.window_size_buttons[0].interactive_rect
        window_size_medium = self.window_size_buttons[1].interactive_rect
        window_size_large = self.window_size_buttons[2].interactive_rect
        window_size_full = self.window_size_buttons[3].interactive_rect

        # Set button size.
        for button in self.window_size_buttons:
            button.interactive_rect.width, button.interactive_rect.height = screen.get_rect().width / 8, screen.get_rect().height  / 12

        # Position window size section label.
        self.window_size_field.text_rect.centery = screen_y
        self.window_size_field.text_rect.right = screen_x - spacing
        # Position selection fields for window sizes. 'window_size_anchor' is placed first as anchor for positioning
        # of further buttons. To move the entire block only the anchor has to be moved.
        window_size_anchor.left, window_size_anchor.bottom = screen_x + spacing, screen_y - spacing / 2
        window_size_medium.left, window_size_medium.bottom = window_size_anchor.right + spacing, window_size_anchor.bottom
        window_size_large.left, window_size_large.top = window_size_anchor.left, window_size_anchor.bottom + spacing
        window_size_full.left, window_size_full.top = window_size_anchor.right + spacing, window_size_anchor.bottom + spacing

    def select_window_size(self, screen, gui_elements, mouse_pos):
        """Selection logic for programs window size. Change attribute 'self.selected_window_size', re-initialize  and
        return dict 'gui_elements'.
        ARGS:
            screen: PyGame window.
            gui_elements: dict of gui elements as created in module 'gui_elements.py'.
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        RETURNS:
            Re-initialized dict 'gui_elements'.
        """
        # Tuple to store window size UI objects and corresponding 'settings' attributes. Last item represents full screen,
        # and has no settings attribute assigned, instead using 'pygame.FULLSCREEN' when setting window size.
        object_attribute_pairs = ((self.window_size_buttons[0], settings.small_screen),
                                  (self.window_size_buttons[1], settings.medium_screen),
                                  (self.window_size_buttons[2], settings.large_screen),
                                  (self.window_size_buttons[3], False))

        # Set 'window_sizes[0].selected' to 'True' to show default selection in settings menu when screen is first shown.
        if settings.screen_size == settings.default_settings[0]:
            self.window_size_buttons[0].selected = True

        # Assign default object (small window) to 'selected_window_size' if it is 'None' in case of first access to the
        # settings screen.
        if not self.selected_window_size:
            self.selected_window_size = object_attribute_pairs[0][0]

        # Check if the left mouse button is pressed before proceeding with selection logic.
        if pygame.mouse.get_pressed()[0]:
            # Loop through each available window size option to see which one is selected.
            for size in self.window_size_buttons:
                if size.interactive_rect.collidepoint(mouse_pos):
                    if self.selected_window_size != size:
                        self.selected_window_size.selected = False  # Unselect previous window size.
                        self.selected_window_size = size
                        self.selected_window_size.selected = True  # Select new window size.
                    break

            # Ensure that only one button is selected at a time.
            for button in self.window_size_buttons:
                button.selected = (button == self.selected_window_size)

        # Iterate through 'object_attribute_pairs' and check if currently selected UI object corresponds with window size set
        # in 'Settings' object. Change 'settings.screen_size' and change 'pygame.display' to selected value if pairs don't
        # correspond.
        for pair in object_attribute_pairs:

            if pair[0].selected == True and pair[1] != settings.screen_size:
                settings.screen_size = pair[1]
                # Check if 'pair[1]' has a window size assigned, otherwise set window to full screen.
                if pair[1]:
                    pygame.display.set_mode(settings.screen_size)
                else:
                    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                # Wait 200ms to avoid immediate click registration directly after new window size is set. Window could be
                # accidentally changed again otherwise.
                pygame.time.wait(200)

                # Re-initialize dict 'gui_elements' for proper size and positions of gui objects based on screen size.
                gui_elements = initialize_screen_elements(screen, settings)
                # Update text size of screen elements in settings screen. See method docstring for details.
                self.update_text_size(gui_elements)

            # Re-assign window size to 'selected_window_size' by comparing 'text' attributes with 'pair[0]', replacing
            # 'selected_window_size' with equivalent object and set its attribute to 'True'. Re-initialization of dict
            # 'gui_elements' above leads to 'selected_window_size' pointing to obsolete object otherwise.
            if self.selected_window_size.text == pair[0].text:
                self.selected_window_size = pair[0]
                self.selected_window_size.selected = True

        return gui_elements

    def update_text_size(self, gui_elements):
        """Assign new values to text size attributes in '__init__()', then resize and render text for screen elements in
        settings screen.
        To be called after new window size is selected and 'gui_elements' is re-initialized. Screen element instances
        would otherwise keep their original sizes."""
        # Assign obsolete size attributes to variables for use in checks further down.
        title_size_old, text_large_old, text_medium_old = self.title_size, self.text_large, self.text_medium

        # Assign updated values to text size attributes.
        self.title_size, self.text_large, self.text_medium = (gui_elements["title_size"], gui_elements["text_large"],
                                                              gui_elements["text_medium"])

        # Check GUI objects size attribute and assign corresponding, updated size.
        for item in self.settings_gui_objects:
            if item.size == title_size_old:
                item.size = self.title_size
            elif item.size == text_large_old:
                item.size = self.text_large
            elif item.size == text_medium_old:
                item.size = self.text_medium

            # Re-render element to show new text size on screen.
            item.render_new_text_surface(settings_gui=True)
