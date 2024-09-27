import pygame
"""Classes for screen objects (buttons, text, etc.)."""


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size, x=0, y=0):
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

        # Set text_rect's top left position based on x and y.
        self.text_rect.topleft = (x, y)

    def draw_text(self):
        """Draw the text on the screen."""
        self.screen.blit(self.text_image, self.text_rect)


class Button(TextField):
    """Represent a selectable button."""

    def __init__(self, screen, text, size, x=0, y=0):
        super().__init__(screen, text, size, x, y)
        # Set button colors for events.
        self.hover_color = (200, 200, 200)
        self.clicked_color = (240, 240, 240)

        # Set rect and size for button
        self.button_rect = self.text_image.get_rect()
        self.button_rect.height, self.button_rect.width = self.button_rect.height + size, self.button_rect.width + size

        # Set button_rect's top left position based on x and y.
        self.button_rect.topleft = (x, y)

    def draw_button(self):
        self.screen.blit(self.text_image, self.button_rect)
