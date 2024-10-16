import pygame
"""Classes for screen objects (buttons, text, etc.)."""


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size, bg_color=(0, 0, 0, 0)):
        """Initialize a text field on screen
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is transparent.
        Default position is centered on screen.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.size = size
        self.bg_color = bg_color

        # Set text color to black and get rect for text field.
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()

        # Set text_rect's center position based on x and y.
        self.text_rect.center = self.screen_rect.center

    def draw_text(self):
        """Draw the text field on the screen."""
        # Draw background rect if 'bg_color' is not transparent.
        if self.bg_color != (0, 0, 0, 0):
            pygame.draw.rect(self.screen, self.bg_color, self.text_rect)

        # Draw the text on top of the rect.
        self.screen.blit(self.text_image, self.text_rect)


class Button(TextField):
    """Represent an interactive button."""

    def __init__(self, screen, text, size, bg_color=(0, 0, 0, 0)):
        """Initialize an interactive button on screen
        ARGS:
            screen: pygame window.
            text: string to be shown on the button.
            size: font size for text.
            bg_color: background color for rect. Default is transparent.
        Default position is centered on screen.
        """
        super().__init__(screen, text, size, bg_color)
        # Set button colors for events.
        self.rect_hover_color = (200, 200, 200)
        self.rect_clicked_color = (240, 240, 240)

        # Set rect and size for button.
        self.button_rect = self.text_image.get_rect()
        self.button_rect.height, self.button_rect.width = self.button_rect.height + size, self.button_rect.width + size

    def draw_button(self, mouse_pos):
        """Draw the button on the screen, changing color based on hover or click using 'mouse_pos' as initialized in
        main loop in 'main.py'."""
        # Draw background rect if 'bg_color' is not transparent.
        if self.bg_color != (0, 0, 0, 0):
            pygame.draw.rect(self.screen, self.bg_color, self.button_rect)

        # Determine button color based on mouse hover or click.
        if self.button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, self.rect_clicked_color, self.button_rect)
            else:
                pygame.draw.rect(self.screen, self.rect_hover_color, self.button_rect)

        # Draw the text on top of the button.
        self.text_rect.center = self.button_rect.center
        self.screen.blit(self.text_image, self.text_rect)


class InteractiveText(TextField):
    """Represent an interactive text field with popup and/or option to toggle between selected/unselected states based
    on user input like mouse collision or mouse button event."""

    def __init__(self, screen, text, size, bg_color=(0, 0, 0, 0), label=False, select=False):
        """Initialize an interactive text field.
        ARGS:
            screen: pygame window.
            text: string to be shown for the text field.
            size: font size for text.
            bg_color: background color for rect. Default is transparent.
            label: instance of 'TextField' class for popup. Default is 'False'.
            select: activate option to toggle between selected/unselected state. Default is 'False'.
        Default position is centered on screen.
        """
        super().__init__(screen, text, size, bg_color)
        self.label = label
        self.select = select
        # State attribute if 'select=True'.
        self.selected = False
        # Set field colors for events.
        self.rect_hover_color = (200, 200, 200)

    def draw_interactive_text(self, mouse_pos):
        """Draw interactive text field on the screen."""
        # Draw background rect if 'bg_color' is not transparent.
        if self.bg_color != (0, 0, 0, 0):
            pygame.draw.rect(self.screen, self.bg_color, self.text_rect)

        # Change field color based on mouse hover.
        if self.text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.rect_hover_color, self.text_rect)

        self.screen.blit(self.text_image, self.text_rect)
