import pygame
"""Classes for screen objects (buttons, text, etc.)."""


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size, bg_color=False, multi_line=False, image_width=0, pos=(0,0)):
        """Initialize a text field on screen
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
            multi_line: boolean to control if text is rendered in a one- or multi-line textfield. Default is 'False'.
        ARGS for use when 'multi_line=True':
            image_width: set width for attribute 'text_image'. Default is '0'.
            pos: set starting point for text in 'text_image'. Default is '(0,0)'.
        Default position is centered on screen.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.size = size
        self.bg_color = bg_color
        self.multi_line = multi_line

        # Set font, text color to black and get rect for text field.
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.size)

        # Get image for mult-line text field.
        if multi_line:
            self.image_width = image_width
            self.image_height = self.font.get_height()  # Starting value for use in 'render_multiline_image()'
            self.pos = pos
            self.text_image = self.render_multiline_image()
        # Get image for standard, one-line text field.
        else:
            self.text_image = self.font.render(self.text, True, self.text_color)

        # Get text_rect and set default center position.
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.screen_rect.center

    def draw_text(self):
        """Draw the text field on the screen."""
        # Draw background rect if 'bg_color' is specified.
        if self.bg_color:
            pygame.draw.rect(self.screen, self.bg_color, self.text_rect)

        # Draw the text on top of the rect.
        self.screen.blit(self.text_image, self.text_rect)

    def render_multiline_image(self):
        """Render and return multi line text image."""
        # Create empty surface.
        text_image = pygame.Surface((self.image_width, self.image_height), pygame.SRCALPHA)
        # Positioning and spacing variables.
        x, y = self.pos
        space = self.font.size(" ")[0]
        # 2D array, each row is a list of words.
        words = [word.split(" ") for word in self.text.splitlines()]

        for line_index, line in enumerate(words, start=1):
            for word in line:
                word_image = self.font.render(word, True, self.text_color)
                word_width = word_image.get_width()

                if x + word_width >= text_image.get_width():
                    text_image, x, y = self.expand_multiline_image(text_image, y)

                text_image.blit(word_image, (x, y))
                x += word_width + space

            # Check if we are at the last line to avoid addition of empty line at the end.
            if line_index < len(words):
                text_image, x, y = self.expand_multiline_image(text_image, y)

        return text_image

    def expand_multiline_image(self, text_image, y):
        """Helper function for use in 'render_multiline_image()' to expand 'text_image' for accommodation of new lines
        of text automatically through use of a temporary surface."""
        x = self.pos[0]  # Reset 'x' for next line.
        y += self.font.get_height()  # Set 'y' for next line.

        # Create a temporary surface to accommodate the new line of text.
        # The new height is calculated by adding the current image height to the font height.
        # Blit the existing text image onto the temporary surface, then update text_image to reference the
        # expanded surface.
        new_height = self.image_height + self.font.get_height()
        temporary_surface = pygame.Surface((self.image_width, new_height), pygame.SRCALPHA)
        temporary_surface.blit(text_image, (0, 0))
        text_image = temporary_surface
        self.image_height = new_height  # Update image height

        return text_image, x, y


class Button(TextField):
    """Represent an interactive button."""

    def __init__(self, screen, text, size, bg_color=False):
        """Initialize an interactive button on screen
        ARGS:
            screen: pygame window.
            text: string to be shown on the button.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
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
        # Draw background rect if 'bg_color' is specified.
        if self.bg_color:
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

    def __init__(self, screen, text, size, bg_color=False, label=False, select=False):
        """Initialize an interactive text field.
        ARGS:
            screen: pygame window.
            text: string to be shown for the text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
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
        # Draw background rect if 'bg_color' is specified.
        if self.bg_color:
            pygame.draw.rect(self.screen, self.bg_color, self.text_rect)

        # Change field color based on mouse hover.
        if self.text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.rect_hover_color, self.text_rect)
            if self.label:
                self.label.text_rect.topleft = mouse_pos
                self.label.draw_text()

        self.screen.blit(self.text_image, self.text_rect)
