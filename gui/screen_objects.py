import pygame
"""Classes for screen objects (buttons, text, etc.)."""


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size):
        """Initialize a text field on the screen with text and font size. Default position is centered on screen."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.size = size

        # Set text color to black and get rect for text field.
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()

        # Set text_rect's center position based on x and y.
        self.text_rect.center = self.screen_rect.center

    def draw_text(self):
        """Draw the text on the screen."""
        self.screen.blit(self.text_image, self.text_rect)


class Button(TextField):
    """Represent a selectable button."""

    def __init__(self, screen, text, size):
        """Initialize a button on screen with text and font size. Default position is centered on screen."""
        super().__init__(screen, text, size)
        # Set button colors for events.
        self.rect_hover_color = (200, 200, 200)
        self.rect_clicked_color = (240, 240, 240)

        # Set rect and size for button.
        self.button_rect = pygame.Rect(0, 0, self.text_rect.width, self.text_rect.height)
        self.button_rect.height, self.button_rect.width = self.button_rect.height + size, self.button_rect.width + size

    def draw_button(self, mouse_pos):
        """Draw the button on the screen, changing color based on hover or click."""
        # Determine button color based on mouse hover or click.
        if self.button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, self.rect_clicked_color, self.button_rect)
            else:
                pygame.draw.rect(self.screen, self.rect_hover_color, self.button_rect)

        # Draw the text on top of the button.
        self.text_rect.center = self.button_rect.center
        self.screen.blit(self.text_image, self.text_rect)
