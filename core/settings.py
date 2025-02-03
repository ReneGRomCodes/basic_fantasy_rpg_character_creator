"""
Settings class for pygame.
"""


class Settings:
    """Class to store settings for pygame."""

    def __init__(self):
        """Initialize pygame's settings."""
        # Screen size options.
        self.small_screen = (1280,720)
        self.medium_screen = (1600,900)
        self.large_screen = (1920,1080)
        # Background color for screen.
        self.bg_color = (240, 220, 170)
        # Color settings for screen objects.
        self.text_color = (55, 40, 25)
        self.font = "gui/font/EagleLake-Regular.ttf"
        self.greyed_out_text_color = (140, 120, 100)
        self.info_panel_bg_color = (210, 180, 130)
        self.rect_hover_color = (180, 140, 80)
        self.rect_clicked_color = (255, 220, 140)
        self.rect_selected_color = (160, 90, 40)
        self.text_input_field_color = (245, 230, 190)
        self.inactive_continue_button_hover_color = (220, 150, 150)
        self.inactive_continue_button_click_color = (200, 50, 50)

        # Value collection for use in settings screen when resetting to default.
        self.default_settings = (self.small_screen, )

        # Empty starting attributes. Values are assigned first in 'run_character_creator()' in 'main.py' by calling the
        # 'set_default()' method.
        # This approach ensures easier maintainability if changes are made to 'self.default_settings' as everything else
        # is handled by 'set_default()' method.
        self.screen_size = None

    def set_default(self):
        """Set all settings variables to default values as defined in 'self.default_settings'."""
        self.screen_size = self.default_settings[0]
