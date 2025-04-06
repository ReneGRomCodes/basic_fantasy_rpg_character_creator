import pygame
from core.settings import Settings
import random
"""Classes for screen objects (buttons, text, etc.)."""

# Instance of 'Settings' class.
settings = Settings()


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text, size, bg_color=False, text_color="default", multi_line=False, surface_width=0, text_pos=(0,0)):
        """Initialize a text field on screen
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
            text_color: string for text color presets. "default" for RGB(55, 40, 25), "inactive" for greyed-out text.
                        Use RGB tuple for others.
            multi_line: boolean to control if text is rendered in a one- or multi-line textfield. Default is 'False'.
        ARGS for use when 'multi_line=True':
            surface_width: set width for attribute 'text_surface'. Default is '0'.
            text_pos: set starting point for text in 'text_surface'. Default is '(0,0)'.
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

        # Get surface for mult-line text field.
        if multi_line:
            self.surface_width = surface_width
            self.surface_height = self.font.get_height()  # Starting value for use in 'render_multiline_surface()'
            self.text_pos = text_pos
            self.text_surface = self.render_multiline_surface()
        # Get surface for standard, one-line text field.
        else:
            self.text_surface = self.font.render(self.text, True, self.text_color)

        # Get text_rect and set default center position. Get background_rect and center text_rect on it if 'bg_color'
        # is specified.
        if self.bg_color:
            self.background_rect = self.text_surface.get_rect().inflate(self.padding, self.padding)
            self.background_rect.center = self.screen_rect.center

        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.screen_rect.center

        """Attributes specific for use of alpha transparency."""
        # Default alpha transparency values. Not used by 'TextField' class, but can be changed and then applied using
        # '.set_alpha(self.alpha)' elsewhere to be changed to, for example, create a fade-in/fade-out effect.
        # See 'Button' and 'InteractiveText' class or methods in 'gui/credits.py' as examples.
        # NOTE: check if surface supports alpha channel (use 'pygame.SRCALPHA' argument when creating a new surface if
        # not)!
        self.fade_alpha = 0
        self.background_alpha = 255
        # Calculate fading speed based on frame rate. Represent intervals for alpha value changes per frame.
        self.fade_speed = int(25 * (30 / settings.frame_rate))

    def draw_text(self):
        """Draw the text field on the screen."""
        # Draw background rect if 'bg_color' is specified.
        if self.bg_color:
            self.text_rect.center = self.background_rect.center
            pygame.draw.rect(self.screen, self.bg_color, self.background_rect)

        # Draw the text on top of the rect.
        self.screen.blit(self.text_surface, self.text_rect)

    def render_multiline_surface(self):
        """Render and return multi line text surface."""
        # Create empty surface.
        text_surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        # Positioning and spacing variables.
        x, y = self.text_pos
        space = self.font.size(" ")[0]
        # 2D array, each row is a list of words.
        words = [word.split(" ") for word in self.text.splitlines()]

        for line_index, line in enumerate(words, start=1):
            for word in line:
                word_surface = self.font.render(word, True, self.text_color)
                word_width = word_surface.get_width()

                if x + word_width >= text_surface.get_width():
                    text_surface, x, y = self.expand_multiline_surface(text_surface, y)

                text_surface.blit(word_surface, (x, y))
                x += word_width + space

            # Check if we are at the last line to avoid addition of empty line at the end.
            if line_index < len(words):
                text_surface, x, y = self.expand_multiline_surface(text_surface, y)

        return text_surface

    def expand_multiline_surface(self, text_surface, y):
        """Helper function for use in 'render_multiline_surface()' to expand 'text_surface' for accommodation of new lines
        of text automatically through use of a temporary surface."""
        x = self.text_pos[0]  # Reset 'x' for next line.
        y += self.font.get_height()  # Set 'y' for next line.

        # Create a temporary surface to accommodate the new line of text.
        # The new height is calculated by adding the current surface height to the font height.
        # Blit the existing text surface onto the temporary surface, then update text_surface to reference the
        # expanded surface.
        new_height = self.surface_height + self.font.get_height()
        temporary_surface = pygame.Surface((self.surface_width, new_height), pygame.SRCALPHA)
        temporary_surface.blit(text_surface, (0,0))
        text_surface = temporary_surface
        self.surface_height = new_height  # Update surface height

        return text_surface, x, y

    def render_new_text_surface(self, settings_gui=False):
        """Re-render 'text_surface' attribute and get new 'text_rect'. This method is for use after an already created
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

        # Check if element has 'multi_line' attribute set to 'True' and render 'text_surface' accordingly, using class method
        # '.render_multiline_surface()' if element is multi line normal render method otherwise.
        if self.multi_line:
            self.text_surface = self.render_multiline_surface()
        else:
            self.text_surface = self.font.render(self.text, True, self.text_color)

        self.text_rect = self.text_surface.get_rect()

    def blit_surface(self, surface, rect, color):
        """Fill 'surface' with 'color' attribute and blit it onto the screen at 'rect'."""
        surface.fill(color)
        self.screen.blit(surface, rect)

    """Following methods allow for fade-in/out effects for background surfaces on mouse collision in conjunction with
    alpha transparency attribute 'self.fade_alpha'.
    See application in 'Button' and 'InteractiveText' class methods as examples."""

    def alpha_fade_in(self, surface):
        """Check and set alpha transparency for 'surface', and limit 'self.fade_alpha' value to max of 255. Then apply to
        'surface' for fade-in effect.
        For use as effect on mouse hover, method should be called from within an 'if self.button_rect.collidepoint(mouse_pos)'
        statement."""
        # Check and set alpha transparency and limit 'self.fade_alpha' value to max of 255.
        if self.fade_alpha < 255:
            self.fade_alpha += self.fade_speed
            surface.set_alpha(self.fade_alpha)
        elif self.fade_alpha != 255:
            self.fade_alpha = 255
            surface.set_alpha(self.fade_alpha)

    def alpha_fade_out(self, surface, rect, color, mouse_pos):
        """Check and set alpha transparency for 'surface', and limit 'self.fade_alpha' value to min of 0. Then apply to
        'surface' for fade-out effect."""
        if not rect.collidepoint(mouse_pos) and self.fade_alpha != 0:
            if self.fade_alpha >= 0:
                self.fade_alpha -= self.fade_speed
                surface.set_alpha(self.fade_alpha)
                self.blit_surface(surface, rect, color)
            elif self.fade_alpha != 0:
                self.fade_alpha = 0
                surface.set_alpha(self.fade_alpha)


class Button(TextField):
    """Represent an interactive button."""

    def __init__(self, screen, text, size, bg_color=False, text_color="default"):
        """Initialize an interactive button on screen
        ARGS:
            screen: pygame window.
            text: string to be shown on the button.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
            text_color: string for text color presets. "default" for RGB(55, 40, 25), "inactive" for greyed-out text.
                        Use RGB tuple for others.
        Default position is centered on screen.
        """
        super().__init__(screen, text, size, bg_color, text_color)
        # Set button colors for events.
        self.rect_hover_color = settings.rect_hover_color
        self.rect_clicked_color = settings.rect_clicked_color
        # Set rect and size for button.
        self.button_rect = self.text_surface.get_rect()
        self.button_rect.height, self.button_rect.width = self.button_rect.height + size, self.button_rect.width + size
        # 'None' attribute to store the button surface, created in 'draw_button()', to represent the button background.
        # This ensures it is only initialized when drawn, and after any changes to 'button_rect' are made in other functions.
        self.button_surface = None

    def draw_button(self, mouse_pos):
        """Draw the button on the screen, changing color based on hover or click using 'mouse_pos' as initialized in
        main loop in 'main.py'."""
        if not self.button_surface:
            self.button_surface = pygame.Surface((self.button_rect.width, self.button_rect.height), pygame.SRCALPHA)

        # Determine button color based on mouse hover or click and apply alpha transparency for fade-in effect.
        if self.button_rect.collidepoint(mouse_pos):
            # Start surface color fade-in effect.
            self.alpha_fade_in(self.button_surface)
            if pygame.mouse.get_pressed()[0]:
                self.blit_surface(self.button_surface, self.button_rect, self.rect_clicked_color)
            else:
                self.blit_surface(self.button_surface, self.button_rect, self.rect_hover_color)
        # Draw opaque background surface if 'bg_color' is specified and no fade-out effect is in progress.
        elif self.bg_color and self.fade_alpha == 0:
            self.button_surface.set_alpha(self.background_alpha)
            self.blit_surface(self.button_surface, self.button_rect, self.bg_color)

        # Start fade-out effect (if mouse is not hovering over button anymore and 'self.alpha_fade_in()' has been
        # triggered previously).
        self.alpha_fade_out(self.button_surface, self.button_rect, self.rect_hover_color, mouse_pos)

        # Draw the text on top of the button.
        self.text_rect.center = self.button_rect.center
        self.screen.blit(self.text_surface, self.text_rect)


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
            panel: list or tuple of instances of 'InfoPanel' class for info panel. Default is 'False'.
                NOTE: if info panel/s is/are given, the relevant screen function has to call function 'show_info_panels()'
                from 'gui/ui_helpers.py' at the bottom to ensure that the info panel is always drawn on top of every
                other screen object.
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
        self.interactive_rect = self.text_surface.get_rect()
        # 'None' attribute to store the interactive text surface, created in 'draw_interactive_text()', to represent the
        # field background. This ensures it is only initialized when drawn, and after any changes to 'interactive_rect'
        # are made in other functions.
        self.interactive_text_surface = None

    def draw_interactive_text(self, mouse_pos):
        """Draw interactive text field on the screen."""
        # Create 'button_surface' surface.
        if not self.interactive_text_surface:
            self.interactive_text_surface = pygame.Surface((self.interactive_rect.width, self.interactive_rect.height), pygame.SRCALPHA)

        # Draw opaque background surface if 'selected' is True or 'bg_color' is specified.
        if self.selected or self.bg_color:
            self.interactive_text_surface.set_alpha(self.background_alpha)
            if self.selected:
                self.blit_surface(self.interactive_text_surface, self.interactive_rect, self.rect_selected_color)
            elif self.bg_color:
                self.blit_surface(self.interactive_text_surface, self.interactive_rect, self.bg_color)

        # Change field color based on mouse hover.
        if self.interactive_rect.collidepoint(mouse_pos):
            self.handle_mouse_interaction()

        # Start fade-out effect (if mouse is not hovering over button anymore and 'self.alpha_fade_in()' has been
        # triggered previously from within 'self.handle_mouse_interaction').
        self.alpha_fade_out(self.interactive_text_surface, self.interactive_rect, self.rect_hover_color, mouse_pos)

        # Draw the text on top of the interactive text field.
        self.text_rect.center = self.interactive_rect.center
        self.screen.blit(self.text_surface, self.text_rect)

    def handle_mouse_interaction(self):
        """Handle interactive functions for the class object.
        NOTE: info panel interactions are handled via method 'handle_mouse_interaction_info_panel()' further down."""
        # Start surface color fade-in effect.
        self.alpha_fade_in(self.interactive_text_surface)

        # Color change when mouse is pressed (only if 'self.select' is True).
        if self.select and pygame.mouse.get_pressed()[0]:
            self.blit_surface(self.interactive_text_surface, self.interactive_rect, self.rect_clicked_color)
        # Normal hover color when mouse is hovering but not pressed.
        else:
            self.blit_surface(self.interactive_text_surface, self.interactive_rect, self.rect_hover_color)

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

    def handle_mouse_interaction_info_panels(self, mouse_pos):
        """Handle mouse interactions and draw info panels when panels are assigned to the class instance.
        This method is called from the helper function 'show_info_panels()' in 'gui/ui_helpers.py' to ensure info panels
        are always drawn on top of every other object on screen."""
        if self.interactive_rect.collidepoint(mouse_pos):
            if self.panel:
                for i in self.panel:
                    i.draw_info_panel()


class InfoPanel(TextField):
    """Expanded child class of 'TextField' to represent an info panel for use in conjunction with an instance of class
    'InteractiveText' which allows for easier positioning.
    NOTE: see docstring section for 'panel' in class definition 'InteractiveText' for more details on how to properly
    implement info panels."""

    def __init__(self, screen, text, size, bg_color=settings.info_panel_bg_color, text_color="default",
                 multi_line=False, surface_width=0, text_pos=(0,0), surface_pos="topright"):
        """Initialize an info panel.
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is RGB(210, 180, 130).
            text_color: string for text color presets. "default" for RGB(55, 40, 25), "inactive" for greyed-out text.
                        Use RGB tuple for others.
            multi_line: boolean to control if text is rendered in a one- or multi-line textfield. Default is 'False'.
        ARGS for use when 'multi_line=True':
            surface_width: set width for attribute 'text_surface'. Default is '0'.
            text_pos: set starting point for text in 'text_surface'. Default is '(0,0)'.
        surface_pos: set position for info panel on screen using a string keyword. Possible keywords:
            "top",
            "bottom",
            "left",
            "right",
            "topleft",
            "topright",
            "bottomleft",
            "bottomright",
            "center".
            Default position is 'topright'.
        """
        super().__init__(screen, text, size, bg_color, text_color, multi_line, surface_width, text_pos)
        if surface_pos == "top":
            self.background_rect.top, self.background_rect.centerx = screen.get_rect().top, screen.get_rect().centerx
        elif surface_pos == "bottom":
            self.background_rect.bottom, self.background_rect.centerx = screen.get_rect().bottom, screen.get_rect().centerx
        elif surface_pos == "left":
            self.background_rect.left, self.background_rect.centery = screen.get_rect().left, screen.get_rect().centery
        elif surface_pos == "right":
            self.background_rect.right, self.background_rect.centery = screen.get_rect().right, screen.get_rect().centery

        elif surface_pos == "topleft":
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
        self.screen.blit(self.text_surface, self.text_rect)


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


class ProgressBar:
    """Represent a visual-only loading progress bar.
    NOTE: This class creates a progress bar that 'simulates' loading without reflecting actual data processing or task
    completion. It is purely for visual effect to enhance the user experience."""

    def __init__(self, screen, height=30, length=3, time=5):
        """Initialize loading progress bar.
        ARGS:
            screen: pygame window.
            height: height of the progress bar as a fraction of screen height. Default is '30'
            length: length of the progress bar as a fraction of screen width. Default is '3'
            time: approximate time in seconds for the progress bar to fill. Default is '5'
        """
        self.screen = screen
        # Assign height/length attributes based on screen size and passed arguments.
        self.height = self.screen.get_rect().height / height
        self.length = self.screen.get_rect().width / length
        # Calculate x and y position for rect to appear at the screen center.
        self.center_screen_pos = self.screen.get_rect().centerx - self.length / 2, self.screen.get_rect().centery

        # Border attributes.
        self.border_radius = int(self.screen.get_rect().height / 72)
        self.border_width = int(self.border_radius / 3)
        self.inner_border_radius = max(0, self.border_radius - self.border_width)
        self.border_color = settings.bar_border_color  # Retrieved from 'Settings' class instance.
        # Progress bar attributes.
        self.progress_bar_height = self.height - (2 * self.border_width)
        self.progress_bar_length = self.length - (2 * self.border_width)
        self.bar_color = settings.progress_bar_color  # Retrieved from 'Settings' class instance.

        # Set starting value for loading 'progress' to 1.
        self.progress = 1
        # Set speed attribute to be consistent across different frame rates.
        self.speed = int(self.progress_bar_length / (time * settings.frame_rate))

        # Values to calculate random speed-up/slow-down events.
        stop_duration_min_max = random.uniform(0.5, 2)  # seconds
        jump_value_min_max = random.uniform(5, 15)  # percent
        slow_value = 0.5  # multiplier
        slow_duration_min_max = random.uniform(1, 3)  # seconds
        speed_up_value_min_max = random.uniform(2, 3)  # multiplier
        speed_up_duration_min_max = random.uniform(1, 2)  # seconds
        #
        self.stop_duration = settings.frame_rate * slow_duration_min_max
        self.jump = int(self.progress_bar_length / (100 * jump_value_min_max))
        self.slow = int(self.speed * slow_value)
        self.speed_up = int(self.speed * speed_up_value_min_max)

        # Container rect.
        """NOTE: Change coordinates for this rect to position the progress bar as a whole!"""
        self.container_rect = pygame.Rect(self.center_screen_pos, (self.length, self.height))

        # 'None' attribute and method call to create rect for animated progress bar.
        self.progress_bar_rect = None
        self.build_progress_bar()

        # Flag attribute which is set to 'True' when progress bar is full. Not used within the class itself, but can be
        # used to, for example, trigger a 'continue' message after progress bar is finished. See 'show_title_screen()'
        # in 'gui/gui.py' and corresponding event handler for possible applications.
        self.finished = False

    def draw_progress_bar(self):
        """Draw progress bar on screen until 'self.progress' value equals the specific value for 'self.length'."""
        # Assign rect x and y attributes to variables for better code readability.
        container_left = self.container_rect.left
        container_centery = self.container_rect.centery
        progress_left = self.progress_bar_rect.left
        progress_centery = self.progress_bar_rect.centery

        # Check if container rect and progress bar rect positions align and correct positioning if necessary.
        if (container_left != progress_left) or (container_centery != progress_centery):
            self.build_progress_bar()

        # Check/adjust length of progress bar and draw it on screen until maximum length 'progress_bar_length' is reached.
        if self.progress <= self.progress_bar_length:
            pygame.draw.rect(self.screen, self.border_color, self.container_rect,
                             border_radius=self.border_radius, width=self.border_width)
            pygame.draw.rect(self.screen, self.bar_color, self.progress_bar_rect, border_radius=self.inner_border_radius)
            self.progress += self.speed
            self.progress_bar_rect.width = self.progress
        else:
            self.finished = True

    def build_progress_bar(self):
        """Create progress bar rect and position it at the center of the container rect."""
        self.progress_bar_rect = pygame.Rect(self.center_screen_pos, (self.progress, self.progress_bar_height))
        self.progress_bar_rect.left, self.progress_bar_rect.centery = (self.container_rect.left + self.border_width,
                                                                           self.container_rect.centery)
