import pygame
from core.settings import Settings
"""Classes for screen objects (buttons, text, etc.)."""

# Instance of 'Settings' class.
settings = Settings()


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size, bg_color=False, text_color="default", multi_line=False, image_width=0, text_pos=(0,0)):
        """Initialize a text field on screen
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
            text_color: string for text color presets. "default" for black, "inactive" for greyed-out text.
                        Use RGB tuple for others.
            multi_line: boolean to control if text is rendered in a one- or multi-line textfield. Default is 'False'.
        ARGS for use when 'multi_line=True':
            image_width: set width for attribute 'text_image'. Default is '0'.
            text_pos: set starting point for text in 'text_image'. Default is '(0,0)'.
        Default position is centered on screen.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text = text
        self.size = size
        self.bg_color = bg_color
        self.multi_line = multi_line

        # Set font, text color and get rect for text field.
        if text_color == "default":
            self.text_color = settings.text_color
        elif text_color == "inactive":
            self.text_color = settings.greyed_out_text_color
        else:
            self.text_color = text_color
        self.font = pygame.font.Font(settings.font, self.size)
        # Set padding for text fields with background color.
        self.padding = int(self.screen_rect.width / 40)

        # Get image for mult-line text field.
        if multi_line:
            self.image_width = image_width
            self.image_height = self.font.get_height()  # Starting value for use in 'render_multiline_image()'
            self.text_pos = text_pos
            self.text_image = self.render_multiline_image()
        # Get image for standard, one-line text field.
        else:
            self.text_image = self.font.render(self.text, True, self.text_color)

        # Get text_rect and set default center position. Get background_rect and center text_rect on it if 'bg_color'
        # is specified.
        if self.bg_color:
            self.background_rect = self.text_image.get_rect().inflate(self.padding, self.padding)
            self.background_rect.center = self.screen_rect.center

        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.screen_rect.center

    def draw_text(self):
        """Draw the text field on the screen."""
        # Draw background rect if 'bg_color' is specified.
        if self.bg_color:
            self.text_rect.center = self.background_rect.center
            pygame.draw.rect(self.screen, self.bg_color, self.background_rect)

        # Draw the text on top of the rect.
        self.screen.blit(self.text_image, self.text_rect)

    def render_multiline_image(self):
        """Render and return multi line text image."""
        # Create empty surface.
        text_image = pygame.Surface((self.image_width, self.image_height), pygame.SRCALPHA)
        # Positioning and spacing variables.
        x, y = self.text_pos
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
        x = self.text_pos[0]  # Reset 'x' for next line.
        y += self.font.get_height()  # Set 'y' for next line.

        # Create a temporary surface to accommodate the new line of text.
        # The new height is calculated by adding the current image height to the font height.
        # Blit the existing text image onto the temporary surface, then update text_image to reference the
        # expanded surface.
        new_height = self.image_height + self.font.get_height()
        temporary_surface = pygame.Surface((self.image_width, new_height), pygame.SRCALPHA)
        temporary_surface.blit(text_image, (0,0))
        text_image = temporary_surface
        self.image_height = new_height  # Update image height

        return text_image, x, y

    def render_new_text_image(self, settings_gui=False):
        """Re-render 'text_image' attribute and get new 'text_rect'. This method is for use after an already created
        instance has its 'text' attribute changed to ensure that further changes to, for example, its position are applied
        to the modified instance.
        ARGS:
            settings_gui: argument for use when calling method 'update_text_size()' in class 'SettingsGUI' to ensure
                          screen elements in the settings screen change their text size if a new window size is selected.
                          Ignore in all other cases. Default is 'False'.
        """

        # See docstring for following statement.
        if settings_gui:
            self.font = pygame.font.Font(settings.font, self.size)

        # Check if element has 'multi_line' attribute set to 'True' and render 'text_image' accordingly, using class method
        # '.render_multiline_image()' if element is multi line normal render method otherwise.
        if self.multi_line:
            self.text_image = self.render_multiline_image()
        else:
            self.text_image = self.font.render(self.text, True, self.text_color)

        self.text_rect = self.text_image.get_rect()


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
        self.rect_hover_color = settings.rect_hover_color
        self.rect_clicked_color = settings.rect_clicked_color

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
    """Represent an interactive text field with info panel and/or option to toggle between selected/unselected states
    based on user input like mouse collision or mouse button event."""

    def __init__(self, screen, text, size, bg_color=False, panel=False, select=False):
        """Initialize an interactive text field.
        ARGS:
            screen: pygame window.
            text: string to be shown for the text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
            panel: list of instances of 'TextField' class for info panel. Default is 'False'.
            select: activate option to toggle between selected/unselected state. Default is 'False'.
        Default position is centered on screen.
        """
        super().__init__(screen, text, size, bg_color)
        self.panel = panel
        self.select = select
        # State attributes if 'select=True'.
        self.selected = False
        self.was_pressed = False # Track previous state of mouse button.
        # Set field colors for events.
        self.rect_hover_color = settings.rect_hover_color
        self.rect_clicked_color = settings.rect_clicked_color
        self.rect_selected_color = settings.rect_selected_color
        # Create rect for field to allow for easier positioning of the 'text_rect' if field size is changed later.
        self.interactive_rect = self.text_image.get_rect()

    def draw_interactive_text(self, mouse_pos):
        """Draw interactive text field on the screen."""
        # Draw background rect if 'bg_color' is specified or use 'rect_selected_color' if 'selected' is True.
        if self.selected:
            pygame.draw.rect(self.screen, self.rect_selected_color, self.interactive_rect)
        elif self.bg_color:
            pygame.draw.rect(self.screen, self.bg_color, self.interactive_rect)

        # Change field color based on mouse hover.
        if self.interactive_rect.collidepoint(mouse_pos):
            self.handle_mouse_interaction()

        # Draw the text on top of the interactive text field.
        self.text_rect.center = self.interactive_rect.center
        self.screen.blit(self.text_image, self.text_rect)

    def handle_mouse_interaction(self):
        """Handle interactive functions for the class object like info panel and selectablility."""
        # Color change when mouse is pressed (only if 'self.select' is True).
        if self.select and pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(self.screen, self.rect_clicked_color, self.interactive_rect)
        # Normal hover color when mouse is hovering but not pressed.
        else:
            pygame.draw.rect(self.screen, self.rect_hover_color, self.interactive_rect)

        # Check for and draw info panel.
        if self.panel:
            for i in self.panel:
                i.draw_info_panel()

        # Change selected state of field by mouse click if 'select' is True.
        if self.select:
            is_pressed = pygame.mouse.get_pressed()[0]
            # Toggle only if mouse is pressed and wasn't pressed in the previous frame.
            if is_pressed and not self.was_pressed:
                self.selected = not self.selected
            # Update previous mouse button state.
            self.was_pressed = is_pressed
        else:
            # Reset 'was_pressed' if mouse is not over the button to avoid accidental toggles.
            self.was_pressed = False


class InfoPanel(TextField):
    """Represent an info panel for use in conjunction with an instance of class 'InteractiveText()'."""

    def __init__(self, screen, text, size, bg_color=settings.info_panel_bg_color, text_color="default",
                 multi_line=False, image_width=0, text_pos=(0,0), surface_pos="topright"):
        """Initialize an info panel.
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'white'.
            text_color: string for text color presets. "default" for black, "inactive" for greyed-out text.
                        Use RGB tuple for others.
            multi_line: boolean to control if text is rendered in a one- or multi-line textfield. Default is 'False'.
        ARGS for use when 'multi_line=True':
            image_width: set width for attribute 'text_image'. Default is '0'.
            text_pos: set starting point for text in 'text_image'. Default is '(0,0)'.
        surface_pos: set position for info panel on screen using a string keyword. Possible keywords:
            "topleft",
            "topright",
            "bottomleft",
            "bottomright",
            "center".
            Default position is 'topright'.
        """
        super().__init__(screen, text, size, bg_color, text_color, multi_line, image_width, text_pos)
        if surface_pos == "topleft":
            self.background_rect.topleft = screen.get_rect().topleft
        elif surface_pos == "topright":
            self.background_rect.topright = screen.get_rect().topright
        elif surface_pos == "bottomleft":
            self.background_rect.bottomleft = screen.get_rect().bottomleft
        elif surface_pos == "bottomright":
            self.background_rect.bottomright = screen.get_rect().bottomright
        elif surface_pos == "center":
            self.background_rect.center = screen.get_rect().center

    def draw_info_panel(self):
        """Draw info panel on screen."""
        self.text_rect.center = self.background_rect.center
        pygame.draw.rect(self.screen, self.bg_color, self.background_rect)
        self.screen.blit(self.text_image, self.text_rect)


class TextInputField:
    """Represent a text input field.
    NOTE: this class does not create the actual instance for a 'pygame_textinput' object, but instead streamlines the
    process of drawing it on screen with a colored background field (color is set in 'Settings' class as attribute
    'self.text_input_field_color') and having the input centered in said field."""

    def __init__(self, screen, input_field_instance, field_width):
        """Initialize text input field.
        ARGS:
            screen: pygame window.
            input_field_instance: instance of 'pygame_textinput'.
            field_width: width of background field.
        """
        self.screen = screen
        self.input_field_instance = input_field_instance
        self.field_width = field_width

        # Create background field for text input 'input_bg_field' and set it to default position at screen center.
        self.field_height = input_field_instance.surface.get_height() * 2
        self.input_bg_field = pygame.Rect((0,0), (field_width, self.field_height))
        self.bg_rect_color = settings.text_input_field_color
        self.input_bg_field.centerx, self.input_bg_field.centery = screen.get_rect().centerx, screen.get_rect().centery

    def draw_input_field(self):
        """Draw text input field with background on screen."""
        pygame.draw.rect(self.screen, self.bg_rect_color, self.input_bg_field)
        self.screen.blit(self.input_field_instance.surface,
                    (self.input_bg_field.centerx - self.input_field_instance.surface.get_width() / 2,
                     self.input_bg_field.centery - self.input_field_instance.surface.get_height() / 2))
