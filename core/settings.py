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
        # Frame rate.
        self.frame_rate = 30
        # Default font.
        self.font = "gui/font/EagleLake-Regular.ttf"
        # Background color for screen.
        self.bg_color = (235, 210, 160)
        # Color settings for screen objects.
        self.text_color = (50, 35, 25)
        self.button_border_color = (150, 110, 80)
        self.greyed_out_text_color = (130, 110, 90)
        self.info_panel_bg_color = (205, 175, 115)
        self.rect_hover_color = (185, 145, 85)
        self.rect_clicked_color = (255, 215, 105)
        self.rect_selected_color = (135, 90, 35)
        self.text_input_field_color = (245, 230, 190)
        self.text_input_border_color = (150, 110, 80)
        self.inactive_continue_button_hover_color = (215, 140, 130)
        self.inactive_continue_button_click_color = (190, 65, 50)
        # Progress bar:
        self.progress_bar_color = (120, 180, 70)
        self.bar_border_color = (220, 130, 75)

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
