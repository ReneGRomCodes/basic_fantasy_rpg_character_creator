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
        self.button_rect_height, self.button_rect_width = (self.text_surface.get_rect().height + size,
                                                           self.text_surface.get_rect().width + size)
        self.button_rect = pygame.Rect((self.screen_rect.centerx, self.screen_rect.centery),
                                       (self.button_rect_width,self.button_rect_height))
        # Button border/frame attributes.
        self.border_radius = int(self.screen_rect.height / 100)
        self.border_width = int(self.border_radius / 3)
        self.border_color = settings.button_border_color

        # 'None' attribute to store the button surface, created in 'draw_button()', to represent the button background.
        # This ensures it is only initialized when drawn, and after any changes to 'button_rect' are made in other functions.
        self.button_surface = None

    def draw_button(self, mouse_pos):
        """Draw the button on the screen, changing color based on hover or click using 'mouse_pos' as initialized in
        main loop in 'main.py'."""
        pygame.draw.rect(self.screen, self.border_color, self.button_rect,
                         border_radius=self.border_radius, width=self.border_width)

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
        """Handle mouse interactions and draw info panels when 'InfoPanel' instances are passed as 'panel' argument to
        the 'InteractiveText' instance.
        If info panel instance has 'slide' attribute set to 'True', reset panels back to starting position when no mouse
        collision event with 'InteractiveText' rect is detected.
        See class 'InfoPanel' for details on sliding functionality.

        This method is called from the helper function 'show_info_panels()' in 'gui/ui_helpers.py' to ensure info panels
        are always drawn on top of every other object on screen."""
        if self.panel:
            # Draw panel if mouse hovers over interactive text field.
            if self.interactive_rect.collidepoint(mouse_pos):
                for i in self.panel:
                    i.draw_info_panel(show_panel=True)
            else:
                for i in self.panel:
                    i.draw_info_panel(show_panel=False)


class InfoPanel(TextField):
    """Expanded child class of 'TextField' to represent an info panel for use in conjunction with an instance of class
    'InteractiveText' which allows for easier positioning.
    NOTE: see docstring section for 'panel' in class definition 'InteractiveText' for more details on how to properly
    implement info panels."""

    def __init__(self, screen, text, size, bg_color=settings.info_panel_bg_color, text_color="default",
                 multi_line=False, surface_width=0, text_pos=(0,0), pos=None, slide=True):
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

            pos: set position for info panel on screen using a string keyword. Possible keywords:
                "top",
                "bottom",
                "left",
                "right",
                "topleft",
                "topright",
                "bottomleft",
                "bottomright".
                Default position is 'None', centering the field on the screen. NOTE: 'pos=None' will set 'slide=False'
                as centered info panels have no sliding animation implemented.
            slide: add function for info panel to 'slide-in/off' the screen. Default is 'True'.
        """
        super().__init__(screen, text, size, bg_color, text_color, multi_line, surface_width, text_pos)
        self.pos = pos
        # Set 'slide' attribute from default 'True' to 'False' if 'pos=None' argument is passed, equalling a centered
        # info panels which has no sliding animation implemented. Avoids having to pass 'slide=False' manually when
        # creating a centered info panel instance (little quality of life improvement).
        if not pos:
            slide = False

        self.slide = slide
        # Assign background rect attribute to 'self.bg_rect' from parent class for more concise use here.
        self.bg_rect = self.background_rect

        # Dict with screen related reference coordinates (anchors) for info panel positions.
        # ["key"][0] = y-positions, ["key"][1] = x-positions.
        # Values that are given as 'None' are unused as they represent centerx and centery which are the default positions
        # for the class as handed down by the parent class 'TextField' and don't need to be re-assigned here.
        self.screen_anchors = {
            "top":          (self.screen_rect.top, None),
            "bottom":       (self.screen_rect.bottom, None),
            "left":         (None, self.screen_rect.left),
            "right":        (None, self.screen_rect.right),
            "topleft":      (self.screen_rect.top, self.screen_rect.left),
            "topright":     (self.screen_rect.top, self.screen_rect.right),
            "bottomleft":   (self.screen_rect.bottom, self.screen_rect.left),
            "bottomright":  (self.screen_rect.bottom, self.screen_rect.right),
        }

        # Assign info panel positions based on passed 'pos' and 'slide' argument. If no 'pos' argument is passed, panel
        # defaults to center position.
        if self.pos:
            self.get_bg_rect_position()

        # Dicts with slide speeds for info panels if 'slide=True'.
        if self.slide:
            self.initial_speed = {"horizontal": self.bg_rect.width / 10,
                                  "vertical": self.bg_rect.height / 10,}
            self.medium_speed = {"horizontal": self.bg_rect.width / 25,
                                 "vertical": self.bg_rect.height / 25,}
            self.slow_speed = {"horizontal": self.bg_rect.width / 50,
                               "vertical": self.bg_rect.height / 50,}
            # Slide-out speed.
            self.exit_speed = {"horizontal": self.bg_rect.width / 7,
                               "vertical": self.bg_rect.height / 7,}

    def draw_info_panel(self, show_panel):
        """Draw info panel on screen.
        ARGS:
            show_panel: Bool to trigger if object is to be drawn on or moved onto screen, or removed from it.
        """
        # Draw/move info panel on screen.
        if show_panel:
            # Progressively move 'sliding' panels into final position.
            if self.slide and self.pos:
                self.slide_panel_in()

            # Draw all panels (sliding and static) on screen.
            self.text_rect.center = self.bg_rect.center
            pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
            self.screen.blit(self.text_surface, self.text_rect)

        # Remove panels from screen. If 'self.slide=False', then panel is just removed from screen without animation.
        else:
            # Progressively move 'sliding' panels off screen.
            if self.slide and self.pos:
                self.slide_panel_out()
                self.text_rect.center = self.bg_rect.center
                pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
                self.screen.blit(self.text_surface, self.text_rect)

    def slide_panel_in(self):
        """Animates the info panel sliding onto the screen from its starting edge or corner. The panel moves incrementally
        based on its 'pos' attribute and dynamically adjusts its speed depending on how far it is from its target. Once
        the final screen position is reached, it snaps into place to prevent 'overshooting'."""
        # Dicts with panel height/width percentages on screen at which speed changes are triggerd.
        initial_speed_range = {"horizontal": self.bg_rect.width * 0.5,
                               "vertical": self.bg_rect.height * 0.5,}  # 50%
        medium_speed_range = {"horizontal": self.bg_rect.width * 0.75,
                               "vertical": self.bg_rect.height * 0.75,}  # 75%

        # Assign area of info panels that is visible on screen to variables.
        visible_area_top = self.screen_rect.top + self.bg_rect.bottom
        visible_area_bottom = self.screen_rect.bottom - self.bg_rect.top
        visible_area_left = self.screen_rect.left + self.bg_rect.right
        visible_area_right = self.screen_rect.right - self.bg_rect.left

        # Conditionals to apply correct speed based on visible area of info panel on screen.
        if "top" in self.pos and self.bg_rect.bottom >= self.screen_rect.top > self.bg_rect.top:
            if visible_area_top > medium_speed_range["vertical"]:
                self.bg_rect.top += self.slow_speed["vertical"]
            if medium_speed_range["vertical"] >= visible_area_top > initial_speed_range["vertical"]:
                self.bg_rect.top += self.medium_speed["vertical"]
            if visible_area_top <= initial_speed_range["vertical"]:
                self.bg_rect.top += self.initial_speed["vertical"]

            self.bg_rect.top = min(self.bg_rect.top, self.screen_rect.top)

        elif "bottom" in self.pos and self.bg_rect.top <= self.screen_rect.bottom < self.bg_rect.bottom:
            if visible_area_bottom > medium_speed_range["vertical"]:
                self.bg_rect.bottom -= self.slow_speed["vertical"]
            if medium_speed_range["vertical"] >= visible_area_bottom > initial_speed_range["vertical"]:
                self.bg_rect.bottom -= self.medium_speed["vertical"]
            if visible_area_bottom <= initial_speed_range["vertical"]:
                self.bg_rect.bottom -= self.initial_speed["vertical"]

            self.bg_rect.bottom = max(self.bg_rect.bottom, self.screen_rect.bottom)

        if "left" in self.pos and self.bg_rect.right >= self.screen_rect.left > self.bg_rect.left:
            if visible_area_left > medium_speed_range["horizontal"]:
                self.bg_rect.left += self.slow_speed["horizontal"]
            if medium_speed_range["horizontal"] >= visible_area_left > initial_speed_range["horizontal"]:
                self.bg_rect.left += self.medium_speed["horizontal"]
            if visible_area_left <= initial_speed_range["horizontal"]:
                self.bg_rect.left += self.initial_speed["horizontal"]

            self.bg_rect.left = min(self.bg_rect.left, self.screen_rect.left)

        elif "right" in self.pos and self.bg_rect.left <= self.screen_rect.right < self.bg_rect.right:
            if visible_area_right > medium_speed_range["horizontal"]:
                self.bg_rect.right -= self.slow_speed["horizontal"]
            if medium_speed_range["horizontal"] >= visible_area_right > initial_speed_range["horizontal"]:
                self.bg_rect.right -= self.medium_speed["horizontal"]
            if visible_area_right <= initial_speed_range["horizontal"]:
                self.bg_rect.right -= self.initial_speed["horizontal"]

            self.bg_rect.right = max(self.bg_rect.right, self.screen_rect.right)

    def slide_panel_out(self):
        """Animate the info panel sliding off-screen from its on-screen position. The method adjusts the panel's position
        incrementally based on its 'pos' attribute until it reaches it's original off-screen position.
        Once the panel reaches its final position, it is snapped into place to prevent 'overshooting'."""
        if "top" in self.pos and self.bg_rect.bottom > self.screen_rect.top:
            self.bg_rect.bottom -= self.exit_speed["vertical"]
            self.bg_rect.bottom = max(self.bg_rect.bottom, self.screen_rect.top)
        elif "bottom" in self.pos and self.bg_rect.top < self.screen_rect.bottom:
            self.bg_rect.top += self.exit_speed["vertical"]
            self.bg_rect.top = min(self.bg_rect.top, self.screen_rect.bottom)

        if "left" in self.pos and self.bg_rect.right > self.screen_rect.left:
            self.bg_rect.right -= self.exit_speed["horizontal"]
            self.bg_rect.right = max(self.bg_rect.right, self.screen_rect.left)
        elif "right" in self.pos and self.bg_rect.left < self.screen_rect.right:
            self.bg_rect.left += self.exit_speed["horizontal"]
            self.bg_rect.left = min(self.bg_rect.left, self.screen_rect.right)

    def get_bg_rect_position(self):
        """Set starting info panel positions based on 'self.pos' argument."""
        # Assign x- and y-anchor attributes to variables for shorter arguments in method calls.
        anchor_y = self.screen_anchors[self.pos][0]
        anchor_x = self.screen_anchors[self.pos][1]

        # Set positions for 'top' and 'bottom'.
        if "top" in self.pos or "bottom" in self.pos:
            self.set_y_pos(anchor_y)
        # Set position for 'left' and 'right'
        if "left" in self.pos or "right" in self.pos:
            self.set_x_pos(anchor_x)

    def set_y_pos(self, anchor_y):
        """Set starting y-positions for all panels with occurrences of "top" or "bottom" in 'self.pos' based on
        'self.slide' attribute.
        Used in method 'get_bg_rect_positions()'."""
        if "top" in self.pos:
            if self.slide:
                self.bg_rect.bottom = anchor_y
            else:
                self.bg_rect.top = anchor_y
        elif "bottom" in self.pos:
            if self.slide:
                self.bg_rect.top = anchor_y
            else:
                self.bg_rect.bottom = anchor_y

    def set_x_pos(self, anchor_x):
        """Set starting x-positions for all panels with occurrences of "left" or "right" in 'self.pos' based on
        'self.slide' attribute.
        Used in method 'get_bg_rect_positions()'."""
        if "left" in self.pos:
            if self.slide:
                self.bg_rect.right = anchor_x
            else:
                self.bg_rect.left = anchor_x
        elif "right" in self.pos:
            if self.slide:
                self.bg_rect.left = anchor_x
            else:
                self.bg_rect.right = anchor_x


class TextInputField:
    """Represent a text input field.
    NOTE: this class does not create the actual instance for a 'pygame_textinput' object, but instead streamlines the
    process of drawing it on screen with a colored background (color is set in 'Settings' class as attribute
    'self.text_input_field_color') and having the input centered in said field."""

    def __init__(self, screen, input_field_instance, field_width):
        """Initialize text input field.
        ARGS:
            screen: pygame window.
            input_field_instance: instance of 'pygame_textinput'.
            field_width: width of background field.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.input_field_instance = input_field_instance
        self.field_width = field_width

        # Create background field for text input 'input_bg_field' and set it to default position at screen center.
        self.field_height = input_field_instance.surface.get_height() * 2
        self.input_bg_field = pygame.Rect((0,0), (self.field_width, self.field_height))
        self.bg_rect_color = settings.text_input_field_color
        self.input_bg_field.centerx, self.input_bg_field.centery = self.screen_rect.centerx, self.screen_rect.centery
        # Create border around input field.
        self.border_radius = int(self.screen_rect.height / 100)
        self.border_thickness = self.border_radius * 1.5
        self.input_field_border = pygame.Rect((0,0), (int(self.input_bg_field.width + self.border_thickness),
                                                      int(self.input_bg_field.height + self.border_thickness)))

    def draw_input_field(self):
        """Draw text input field with background on screen."""
        # Ensure that input field and input field border align.
        self.position_input_field_border()

        pygame.draw.rect(self.screen, settings.text_input_border_color, self.input_field_border, border_radius=self.border_radius)
        pygame.draw.rect(self.screen, self.bg_rect_color, self.input_bg_field)
        self.screen.blit(self.input_field_instance.surface,
                    (self.input_bg_field.centerx - self.input_field_instance.surface.get_width() / 2,
                     self.input_bg_field.centery - self.input_field_instance.surface.get_height() / 2))

    def position_input_field_border(self):
        """Check if input field attributes divert from 'input_field_border' attributes (for example in cases where the
        input field size or position has been changed after initial creation) to ensure that size and position of both
        objects align."""
        if self.input_field_border.center != self.input_bg_field:
            self.input_field_border.center = self.input_bg_field.center
        if self.input_field_border.width != int(self.input_bg_field.width + self.border_thickness):
            self.input_field_border.width = int(self.input_bg_field.width + self.border_thickness)
        if self.input_field_border.height != int(self.input_bg_field.height + self.border_thickness):
            self.input_field_border.height = int(self.input_bg_field.height + self.border_thickness)


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
        self.screen_rect = screen.get_rect()
        # Assign height/length attributes based on screen size and passed arguments.
        self.height = self.screen_rect.height / height
        self.length = self.screen_rect.width / length
        # Calculate x and y position for rect to appear at the screen center.
        self.center_screen_pos = self.screen_rect.centerx - self.length / 2, self.screen_rect.centery

        # Border attributes.
        self.border_radius = int(self.screen_rect.height / 72)
        self.border_width = int(self.border_radius / 3)
        self.inner_border_radius = max(0, self.border_radius - self.border_width)
        self.border_color = settings.bar_border_color
        # Progress bar attributes.
        self.progress_bar_height = self.height - (2 * self.border_width)
        self.progress_bar_length = self.length - (2 * self.border_width)
        self.bar_color = settings.progress_bar_color

        # Set starting value for loading 'progress' to 1.
        self.progress = 1
        # Set speed attribute to be consistent across different frame rates.
        self.speed = int(self.progress_bar_length / (time * settings.frame_rate))

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

        # Attributes ror random speed-up/slow-down events. Used in 'progress_manager()' and 'set_random_progress()'
        # methods further down.
        self.chance_per_second = 0.2  # 0.2% chance of event per frame.
        self.cooldown = False
        self.cooldown_seconds = int(time / 2)
        self.cooldown_timer = 0
        self.duration_timer = 0  # Timer for duration of event.
        # Create 'backup' of set speed to be used for resetting of 'self.speed' if a random speed-up/slow-down event
        # modifies it.
        self.speed_backup = self.speed

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
            self.progress_manager(mode="trigger")  # Trigger and handle random speed-up/slow-down events for the progress bar.
            pygame.draw.rect(self.screen, self.border_color, self.container_rect,
                             border_radius=self.border_radius, width=self.border_width)
            pygame.draw.rect(self.screen, self.bar_color, self.progress_bar_rect, border_radius=self.inner_border_radius)
            self.progress += self.speed
            self.progress_bar_rect.width = self.progress
        else:
            self.finished = True

        # Reset cooldown for random speed-up/slow-down events.
        self.progress_manager(mode="reset")

    def build_progress_bar(self):
        """Create progress bar rect and position it at the center of the container rect."""
        self.progress_bar_rect = pygame.Rect(self.center_screen_pos, (self.progress, self.progress_bar_height))
        self.progress_bar_rect.left, self.progress_bar_rect.centery = (self.container_rect.left + self.border_width,
                                                                           self.container_rect.centery)

    def progress_manager(self, mode):
        """Trigger random loading bar progress event or reset event cooldown based on passed argument 'mode'.
        ARGS:
            mode: switches functionality between triggering a random event and reset cooldown for events.
                keywords: "trigger" for trigger, "reset" for reset functionality... what a shocker!
        """
        if mode == "trigger":
            # Only trigger random event if there's no cooldown, event count < 2, and event duration timer is done.
            if not self.cooldown and self.duration_timer <= 0:
                if random.random() < self.chance_per_second:
                    self.set_random_progress()  # Trigger random event.
                    self.cooldown = True  # Start cooldown.
                    self.cooldown_timer = settings.frame_rate * self.cooldown_seconds  # Set cooldown timer.

            # Decrease the duration timer.
            if self.duration_timer > 0:
                self.duration_timer -= 1

            # Reset speed after the event duration ends, based on event type.
            if self.duration_timer <= 0:
                self.speed = self.speed_backup  # Restore the original speed.

        elif mode == "reset":
            # Handle cooldown timer.
            if self.cooldown:
                self.cooldown_timer -= 1
                if self.cooldown_timer <= 0:
                    self.cooldown = False  # Reset cooldown state when the timer ends.

    def set_random_progress(self):
        """Calculate and set random values for possible progress event types, then randomly choose an event to be
        triggered."""
        # Set lower and upper limits for, and get random multiplier values.
        stop_duration_min_max = random.uniform(0.5, 2)  # seconds
        jump_value_min_max = random.uniform(15, 30)  # percent
        slow_value = 0.5  # multiplier
        slow_duration_min_max = random.uniform(1, 3)  # seconds
        speed_up_value_min_max = random.uniform(2, 3)  # multiplier
        speed_up_duration_min_max = random.uniform(1, 2)  # seconds
        # Calculate event values based on multiplier values above.
        stop_duration = int(settings.frame_rate * stop_duration_min_max)  # frames
        jump = int(self.progress_bar_length / (100 * jump_value_min_max))  # pixels
        slow = int(self.speed * slow_value)  # pixels
        speed_up = int(self.speed * speed_up_value_min_max)  # pixels

        # Array of possible event types and values.
        events = (("stop", stop_duration),
                  ("jump", jump),
                  ("slow", slow),
                  ("speed_up", speed_up))
        # Choose random event.
        event_type, value = random.choice(events)

        if event_type == "stop":
            self.duration_timer = stop_duration
            self.speed = 0
        elif event_type == "jump":
            self.progress += jump
        elif event_type == "slow":
            self.speed = slow
            # Convert duration from seconds to frames and set timer.
            self.duration_timer = int(settings.frame_rate * slow_duration_min_max)
        elif event_type == "speed_up":
            self.speed = speed_up
            # Convert duration from seconds to frames and set timer.
            self.duration_timer = int(settings.frame_rate * speed_up_duration_min_max)
