"""
Settings class for pygame.
Only instance of this class, 'settings', is created at the bottom of this module and imported/referenced throughout the
program.
"""


class Settings:
    """Class to store settings for pygame."""

    def __init__(self) -> None:
        """Initialize pygame's settings."""
        # Screen size options.
        self.small_screen: tuple[int, int] = (1280,720)
        self.medium_screen: tuple[int, int] = (1600,900)
        self.large_screen: tuple[int, int] = (1920,1080)
        # Frame rate.
        self.frame_rate: int = 30

        # Art assets.
        self.font: str = "gui/art/font/EagleLake-Regular.ttf"
        # Assets are loaded and scaled in 'gui/gui_elements.py' to be then accessible via dict 'gui_elements'.
        self.bg_image: str = "gui/art/bg_image.jpg"

        # Background color for screen.
        self.bg_color: tuple[int, int, int] = (235, 210, 160)  # OBSOLETE. 'self.bg_image' IS USED NOW.

        # Color settings for screen objects.
        self.text_color: tuple[int, int, int] = (50, 35, 25)
        self.button_border_color: tuple[int, int, int] = (150, 110, 80)
        self.greyed_out_text_color: tuple[int, int, int] = (130, 110, 90)
        self.info_panel_bg_color: tuple[int, int, int] = (205, 175, 115)
        self.rect_hover_color: tuple[int, int, int] = (185, 145, 85)
        self.rect_clicked_color: tuple[int, int, int] = (255, 215, 105)
        self.rect_selected_color: tuple[int, int, int] = (135, 90, 35)
        self.text_input_field_color: tuple[int, int, int] = (245, 230, 190)
        self.text_input_border_color: tuple[int, int, int] = (150, 110, 80)
        self.inactive_continue_button_hover_color: tuple[int, int, int] = (215, 140, 130)
        self.inactive_continue_button_click_color: tuple[int, int, int] = (190, 65, 50)
        # Progress bar:
        self.progress_bar_color: tuple[int, int, int] = (120, 180, 70)
        self.bar_border_color: tuple[int, int, int] = (220, 130, 75)

        # Value collection for use in settings screen when resetting to default.
        self.default_settings: tuple[tuple] = (self.small_screen, )

        # Empty starting attributes. Values are assigned first in 'run_character_creator()' in 'main.py' by calling the
        # 'set_default()' method.
        # This approach ensures easier maintainability if changes are made to 'self.default_settings' as everything else
        # is handled by 'set_default()' method.
        self.screen_size: tuple[int, int] | None = None

        # JSON save file for characters.
        self.save_file = "save/characters.json"

    def set_default(self) -> None:
        """Set all settings variables to default values as defined in 'self.default_settings'."""
        self.screen_size: tuple[tuple] = self.default_settings[0]


# Create shared settings object.
settings: Settings = Settings()
