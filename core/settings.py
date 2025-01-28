"""
Settings class for pygame.
"""


class Settings:
    """Class to store settings for pygame."""

    def __init__(self):
        """Initialize pygame's settings."""
        self.screen_width = 1200
        self.screen_height = 800
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
