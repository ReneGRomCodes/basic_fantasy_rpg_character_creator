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
        self.bg_color = (230,230,230)

        # Color settings for screen objects.
        self.text_color = (0,0,0)
        self.info_panel_bg_color = (240,240,240)
        self.rect_hover_color = (200,200,200)
        self.rect_clicked_color = (255,255,255)
        self.rect_selected_color = (173,192,202)
