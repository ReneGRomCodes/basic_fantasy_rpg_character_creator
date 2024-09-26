import pygame
"""Classes for screen objects (buttons, text, etc.)."""


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size=20, x=0, y=0):
        """Initialize the text field with screen, text, font size, and position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.size = size

        # Set text color to black and get rect for text field.
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()

        # Set text_rect's top left position based on x and y
        self.text_rect.topleft = (x, y)

    def draw_text(self):
        """Draw the text on the screen."""
        self.screen.blit(self.text_image, self.text_rect)
