"""
Classes for screen objects (buttons, text, etc.).

Instances for GUI objects are created in module 'gui/ui_registry.py', scaled if necessary, and then added to dict
'ui_registry'.
Functions for the use of screen objects are located in 'gui/gui.py' with helper functions for positioning located in
'gui/ui_helpers.py'.

Exceptions are 'Credits Screen', 'Settings Screen', Save/Load Screen' and 'Character Sheet Screen' which separately
handle their own instances/logic in their respective class modules (credits.py, settings_gui.py, sl_model, cs_model.py).

See documentation in relevant modules for details.
"""
import pygame
import random

from pygame_textinput import TextInputVisualizer

from core.settings import settings


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text: str, size: int, bg_color: bool | str | tuple[int, int, int] = False,
                 text_color: str | tuple[int, int, int] = "default", multi_line: bool = False, surface_width: int = 0,
                 text_pos: tuple[int, int] = (0,0)) -> None:
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
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.text: str = text
        self.size: int = size
        self.bg_color: bool | str | tuple[int, int, int] = bg_color
        self.multi_line: bool = multi_line

        if text_color == "default":
            self.text_color: str | tuple[int, int, int] = settings.text_color
        elif text_color == "inactive":
            self.text_color: str | tuple[int, int, int] = settings.greyed_out_text_color
        else:
            self.text_color: str | tuple[int, int, int] = text_color
        self.font: pygame.font.Font = pygame.font.Font(settings.font, self.size)

        self.padding: int = int(self.screen_rect.width / 40)

        # Get surface for mult-line text field.
        if multi_line:
            self.surface_width: int = surface_width
            self.surface_height: int = self.font.get_height()  # Starting value for use in 'render_multiline_surface()'
            self.text_pos: tuple[int, int] = text_pos
            self.text_surface: pygame.Surface = self.render_multiline_surface()
        # Get surface for standard, one-line text field.
        else:
            self.text_surface: pygame.Surface = self.font.render(self.text, True, self.text_color)

        if self.bg_color:
            self.background_rect: pygame.Rect = self.text_surface.get_rect().inflate(self.padding, self.padding)
            self.background_rect.center = self.screen_rect.center

        self.text_rect: pygame.Rect = self.text_surface.get_rect()
        self.text_rect.center = self.screen_rect.center

        # Default alpha transparency values. Not used by 'TextField' class, but can be changed and then applied using
        # '.set_alpha(self.alpha)' elsewhere to be changed to, for example, create a fade-in/fade-out effect.
        # See 'Button' and 'InteractiveText' class or methods in 'gui/credits.py' as examples.
        # NOTE: check if surface supports alpha channel (use 'pygame.SRCALPHA' argument when creating a new surface if
        # not)!
        self.fade_alpha: int = 0
        self.background_alpha: int = 255
        self.fade_speed: int = int(25 * (30 / settings.frame_rate))

    def draw_text(self) -> None:
        """Draw the text field on the screen."""
        if self.bg_color:
            self.background_rect.center = self.text_rect.center
            pygame.draw.rect(self.screen, self.bg_color, self.background_rect)

        self.screen.blit(self.text_surface, self.text_rect)

    def render_multiline_surface(self) -> pygame.Surface:
        """Render and return multi line text surface.
        The method splits the text into lines and words, renders each word using the specified font, and dynamically
        expands the surface height if a word doesn't fit the current line.
        RETURNS:
            text_surface
        """
        text_surface: pygame.Surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)

        x, y = self.text_pos
        space = self.font.size(" ")[0]
        # 2D array, each row is a list of words.
        words = [word.split(" ") for word in self.text.splitlines()]

        for line_index, line in enumerate(words, start=1):
            for word in line:
                # Render each word and check if it fits the current line.
                word_surface = self.font.render(word, True, self.text_color)
                word_width = word_surface.get_width()

                if x + word_width >= text_surface.get_width():
                    # If the word doesn't fit, create more space and move to next line.
                    text_surface, x, y = self.expand_multiline_surface(text_surface, y)

                # Draw the word and advance horizontal position.
                text_surface.blit(word_surface, (x, y))
                x += word_width + space

            # Check if we are at the last line to avoid addition of empty line at the end.
            if line_index < len(words):
                text_surface, x, y = self.expand_multiline_surface(text_surface, y)

        return text_surface

    def expand_multiline_surface(self, text_surface: pygame.surface, y: int) -> tuple[pygame.surface, int, int]:
        """Helper function for use in 'render_multiline_surface()' to expand 'text_surface' to accommodate new lines of
        text automatically through use of a temporary surface.
        ARGS:
            text_surface: pygame surface to be expanded for multi-line texts.
            y: current Y-position of text line.
        RETURNS:
            text_surface, x, y: new text surface and coordinates for next line.
        """
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

    def render_new_text_surface(self, settings_gui: bool = False) -> None:
        """Re-render 'text_surface' attribute and get new 'text_rect'. This method is for use after an already created
        instance has its 'text' attribute changed to ensure that further changes to, for example, its position are applied
        to the modified instance.
        ARGS:
            settings_gui: argument for use when calling method 'update_text_size()' in class 'SettingsGUI' to ensure
                          screen elements in the settings screen change their text size if a new window size is selected.
                          Ignore in all other cases. Default is 'False'.
        """
        if settings_gui:
            self.font: pygame.font.Font = pygame.font.Font(settings.font, self.size)

        if self.multi_line:
            self.text_surface: pygame.Surface = self.render_multiline_surface()
        else:
            self.text_surface: pygame.Surface = self.font.render(self.text, True, self.text_color)

        self.text_rect: pygame.Rect = self.text_surface.get_rect()

    def blit_surface(self, surface: pygame.Surface, rect: pygame.Rect, color: str | tuple[int, int, int]) -> None:
        """Fill 'surface' with 'color' attribute and blit it onto the screen at 'rect'.
        ARGS:
            surface: pygame surface.
            rect: pygame rect.
            color: color attribute.
        """
        surface.fill(color)
        self.screen.blit(surface, rect)

    """Following methods allow for fade-in/out effects for background surfaces on mouse collision in conjunction with
    alpha transparency attribute 'self.fade_alpha'.
    See application in 'Button' and 'InteractiveText' class methods as examples."""

    def alpha_fade_in(self, surface: pygame.Surface) -> None:
        """Check and set alpha transparency for 'surface', and limit 'self.fade_alpha' value to max of 255. Then apply to
        'surface' for fade-in effect.
        For use as effect on mouse hover, method should be called from within an 'if self.rect.collidepoint(mouse_pos)'
        statement.
        ARGS:
            surface: pygame surface.
        """
        if self.fade_alpha < 255:
            self.fade_alpha += self.fade_speed
            surface.set_alpha(self.fade_alpha)
        elif self.fade_alpha != 255:
            self.fade_alpha = 255
            surface.set_alpha(self.fade_alpha)

    def alpha_fade_out(self, surface: pygame.Surface, rect: pygame.Rect, color: str | tuple[int, int, int], mouse_pos,
                       button: bool = False, interactive: bool = False) -> None:
        """Check and set alpha transparency for 'surface', and limit 'self.fade_alpha' value to min of 0. Then apply to
        'surface' for fade-out effect.
        ARGS:
            surface: pygame surface for color fade-out effect to be applied to.
            rect: rect to hold surface position to be blit onto.
            color: color for surface for fade-out effect to be applied to.
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
            button: Set to 'True' if called from a 'Button' instance to use its specialized blit method (handles borders
                    and rounded corners).
            interactive: Set to 'True' if called from an 'InteractiveText' instance to use its specialized blit method
                         (handles rounded corners).

        NOTE: Defaults values for 'button' and 'interactive' are 'False', representing other classes.
        """
        if not rect.collidepoint(mouse_pos) and self.fade_alpha != 0:
            if self.fade_alpha >= 0:
                self.fade_alpha -= self.fade_speed
                surface.set_alpha(self.fade_alpha)

                if button:
                    self.blit_button_surface(surface, rect, color)  # type: ignore
                elif interactive:
                    self.blit_interactive_surface(surface, rect, color)  # type: ignore
                else:
                    self.blit_surface(surface, rect, color)

            elif self.fade_alpha != 0:
                self.fade_alpha = 0
                surface.set_alpha(self.fade_alpha)


class Button(TextField):
    """Represent an interactive button."""

    def __init__(self, screen, text: str, size: int, bg_color: bool | str | tuple[int, int, int] = False,
                 text_color: str | tuple[int, int, int] = "default") -> None:
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
        self.rect_hover_color: str | tuple[int, int, int] = settings.rect_hover_color
        self.rect_clicked_color: str | tuple[int, int, int] = settings.rect_clicked_color

        self.button_rect_height, self.button_rect_width = (self.text_surface.get_rect().height + size,
                                                           self.text_surface.get_rect().width + size)
        self.button_rect: pygame.Rect = pygame.Rect((self.screen_rect.centerx, self.screen_rect.centery),
                                                    (self.button_rect_width,self.button_rect_height))

        self.border_radius: int = int(self.screen_rect.height / 100)
        self.border_width: int = int(self.border_radius / 3)
        self.border_color: str | tuple[int, int, int] = settings.button_border_color

        # 'None' attribute to store the button surface, created in 'draw_button()', to represent the button background.
        # This ensures it is only created once when drawn, and after any changes to 'button_rect' size are made in other
        # functions when 'Button' instance is used.
        self.button_surface: None | pygame.Surface = None

    def draw_button(self, mouse_pos) -> None:
        """Draw the button on the screen, changing color based on hover or click using 'mouse_pos' as initialized in
        main loop in 'main.py'.
        ARGS:
            mouse_pos: position of mouse on screen.
        """
        if not self.button_surface:
            self.button_surface = pygame.Surface((self.button_rect.width - self.border_width,
                                                  self.button_rect.height - self.border_width), pygame.SRCALPHA)

        if self.button_rect.collidepoint(mouse_pos):
            self.alpha_fade_in(self.button_surface)
            if pygame.mouse.get_pressed()[0]:
                self.blit_button_surface(self.button_surface, self.button_rect, self.rect_clicked_color)
            else:
                self.blit_button_surface(self.button_surface, self.button_rect, self.rect_hover_color)
        elif self.bg_color and self.fade_alpha == 0:
            self.button_surface.set_alpha(self.background_alpha)
            self.blit_button_surface(self.button_surface, self.button_rect, self.bg_color)

        self.alpha_fade_out(self.button_surface, self.button_rect, self.rect_hover_color, mouse_pos, button=True)

        self.text_rect.center = self.button_rect.center
        self.screen.blit(self.text_surface, self.text_rect)

        pygame.draw.rect(self.screen, self.border_color, self.button_rect,
                         border_radius=self.border_radius, width=self.border_width)

    def blit_button_surface(self, surface: pygame.Surface, rect: pygame.Rect, color: str | tuple[int, int, int]) -> None:
        """Fill 'surface' with 'color' and blit it onto the screen at 'rect', ensuring the button's background fits
        inside the button's borders with rounded corners.
        ARGS:
            surface: pygame surface.
            rect: pygame rect.
            color: color attribute.
        """
        surface.fill((0, 0, 0, 0))

        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=self.border_radius)
        surface_pos: tuple[int, int] = (int(rect.left + self.border_width / 2), int(rect.top + self.border_width / 2))
        self.screen.blit(surface, surface_pos)


class InteractiveText(TextField):
    """Represent an interactive text field with info panel and/or option to toggle between selected/unselected states
    based on user input like mouse collision or mouse button event."""

    def __init__(self, screen, text: str, size: int, bg_color: bool | str | tuple[int, int, int] =False,
                 panel: bool | object = False, select: bool = False) -> None:
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
        self.panel: bool = panel
        self.select: bool = select

        self.selected: bool = False
        self.was_pressed: bool = False # Track previous state of mouse button.

        self.rect_hover_color: str | tuple[int, int, int] = settings.rect_hover_color
        self.rect_clicked_color: str | tuple[int, int, int] = settings.rect_clicked_color
        self.rect_selected_color: str | tuple[int, int, int] = settings.rect_selected_color

        self.corner_radius: int = int(self.screen_rect.height / 100)
        # Create rect for field to allow for easier positioning of the 'text_rect' if field size is changed later.
        self.interactive_rect: pygame.Rect = self.text_surface.get_rect()
        # 'None' attribute to store the interactive text surface, created in 'draw_interactive_text()', to represent the
        # field background. This ensures it is only initialized when drawn, and after any changes to 'interactive_rect'
        # are made in other functions.
        self.interactive_text_surface: None | pygame.Surface = None

    def draw_interactive_text(self, mouse_pos) -> None:
        """Draw interactive text field on the screen.
        ARGS:
            mouse_pos: position of mouse on screen.
        """
        if not self.interactive_text_surface:
            self.interactive_text_surface = pygame.Surface((self.interactive_rect.width, self.interactive_rect.height), pygame.SRCALPHA)

        if self.selected or self.bg_color:
            self.interactive_text_surface.set_alpha(self.background_alpha)
            if self.selected:
                self.blit_interactive_surface(self.interactive_text_surface, self.interactive_rect, self.rect_selected_color)
            elif self.bg_color:
                self.blit_interactive_surface(self.interactive_text_surface, self.interactive_rect, self.bg_color)

        if self.interactive_rect.collidepoint(mouse_pos):
            self.handle_mouse_interaction()

        self.alpha_fade_out(self.interactive_text_surface, self.interactive_rect, self.rect_hover_color, mouse_pos,
                            interactive=True)

        self.text_rect.center = self.interactive_rect.center
        self.screen.blit(self.text_surface, self.text_rect)

    def blit_interactive_surface(self, surface, rect: pygame.Rect, color: str | tuple[int, int, int]) -> None:
        """Fill 'surface' with 'color' and blit it onto the screen at 'rect' with rounded corners.
        ARGS:
            surface: pygame surface.
            rect: pygame rect.
            color: color attribute.
        """
        surface.fill((0, 0, 0, 0))

        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=self.corner_radius)
        self.screen.blit(surface, rect)

    def handle_mouse_interaction(self) -> None:
        """Handle interactive functions for the class object.
        NOTE: info panel interactions are handled via method 'handle_mouse_interaction_info_panel()' further down."""
        self.alpha_fade_in(self.interactive_text_surface)

        if self.select and pygame.mouse.get_pressed()[0]:
            self.blit_interactive_surface(self.interactive_text_surface, self.interactive_rect, self.rect_clicked_color)
        else:
            self.blit_interactive_surface(self.interactive_text_surface, self.interactive_rect, self.rect_hover_color)

        if self.select:
            is_pressed = pygame.mouse.get_pressed()[0]
            if is_pressed and not self.was_pressed:
                self.selected = not self.selected

            self.was_pressed = is_pressed
        else:
            self.was_pressed = False

    def handle_mouse_interaction_info_panels(self, mouse_pos) -> None:
        """Handle mouse interactions and draw info panels when 'InfoPanel' instances are passed as 'panel' argument to
        the 'InteractiveText' instance.
        If info panel instance has 'slide' attribute set to 'True', reset panels back to starting position when no mouse
        collision event with 'InteractiveText' rect is detected.
        See class 'InfoPanel' for details on sliding functionality.

        ARGS:
            mouse_pos: position of mouse on screen.

        This method is called from the helper function 'show_info_panels()' in 'gui/ui_helpers.py' to ensure info panels
        are always drawn on top of every other object on screen."""
        if self.panel:
            if self.interactive_rect.collidepoint(mouse_pos):
                for i in self.panel:  # type: ignore
                    i.draw_info_panel(show_panel=True)
            else:
                for i in self.panel:  # type: ignore
                    i.draw_info_panel(show_panel=False)


class InfoPanel(TextField):
    """Expanded child class of 'TextField' to represent an info panel for use in conjunction with an instance of class
    'InteractiveText' which allows for easier positioning.
    NOTE: see docstring section for 'panel' in class definition 'InteractiveText' for more details on how to properly
    implement info panels."""

    def __init__(self, screen, text: str, size: int, bg_color: str | tuple[int, int, int] = settings.info_panel_bg_color,
                 text_color: str | tuple[int, int, int] = "default", multi_line: bool = False, surface_width: int = 0,
                 text_pos: tuple[int, int] = (0,0), pos: None | str = None, slide: bool = True) -> None:
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
        self.pos: None | str = pos
        # Set 'slide' attribute from default 'True' to 'False' if 'pos=None' argument is passed, equalling a centered
        # info panels which has no sliding animation implemented. Avoids having to pass 'slide=False' manually when
        # creating a centered info panel instance (little quality of life improvement).
        if not pos:
            slide = False

        self.slide: bool = slide
        self.bg_rect: pygame.Rect = self.background_rect

        # Dict with screen related reference coordinates (anchors) for info panel positions.
        # ["key"][0] = y-positions, ["key"][1] = x-positions.
        # Values that are given as 'None' are unused as they represent centerx and centery which are the default positions
        # for the class as handed down by the parent class 'TextField' and don't need to be re-assigned here.
        self.screen_anchors: dict[str, tuple[int | None, int | None]] = {
            "top":          (self.screen_rect.top, None),
            "bottom":       (self.screen_rect.bottom, None),
            "left":         (None, self.screen_rect.left),
            "right":        (None, self.screen_rect.right),
            "topleft":      (self.screen_rect.top, self.screen_rect.left),
            "topright":     (self.screen_rect.top, self.screen_rect.right),
            "bottomleft":   (self.screen_rect.bottom, self.screen_rect.left),
            "bottomright":  (self.screen_rect.bottom, self.screen_rect.right),
        }

        if self.pos:
            self.get_bg_rect_position()

        if self.slide:
            self.initial_speed: dict[str, int] = {"horizontal": int(self.bg_rect.width / 10),
                                                  "vertical": int(self.bg_rect.height / 10),}
            self.medium_speed: dict[str, int] = {"horizontal": int(self.bg_rect.width / 25),
                                                 "vertical": int(self.bg_rect.height / 25),}
            self.slow_speed: dict[str, int] = {"horizontal": int(self.bg_rect.width / 50),
                                               "vertical": int(self.bg_rect.height / 50),}
            # Slide-out speed.
            self.exit_speed: dict[str, int] = {"horizontal": int(self.bg_rect.width / 7),
                                               "vertical": int(self.bg_rect.height / 7),}

    def draw_info_panel(self, show_panel: bool) -> None:
        """Draw info panel on screen.
        ARGS:
            show_panel: Bool to trigger if object is to be drawn on or moved onto screen, or removed from it.
        """
        if show_panel:
            if self.slide and self.pos:
                self.slide_panel_in()

            self.text_rect.center = self.bg_rect.center
            pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
            self.screen.blit(self.text_surface, self.text_rect)

        else:
            if self.slide and self.pos:
                self.slide_panel_out()
                self.text_rect.center = self.bg_rect.center
                pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
                self.screen.blit(self.text_surface, self.text_rect)

    def slide_panel_in(self) -> None:
        """Animates the info panel sliding onto the screen from its starting edge or corner. The panel moves incrementally
        based on its 'pos' attribute and dynamically adjusts its speed depending on how far it is from its target. Once
        the final screen position is reached, it snaps into place to prevent 'overshooting'."""
        bg_rct: pygame.Rect = self.bg_rect
        sc_rct: pygame.Rect = self.screen_rect

        initial_speed_range = {"horizontal": int(bg_rct.width * 0.5),
                               "vertical": int(bg_rct.height * 0.5),}  # 50%
        medium_speed_range = {"horizontal": int(bg_rct.width * 0.75),
                               "vertical": int(bg_rct.height * 0.75),}  # 75%

        # Area of info panel that is visible on screen.
        visible_area_top: int = sc_rct.top + bg_rct.bottom
        visible_area_bottom: int = sc_rct.bottom - bg_rct.top
        visible_area_left: int = sc_rct.left + bg_rct.right
        visible_area_right: int = sc_rct.right - bg_rct.left

        if "top" in self.pos and bg_rct.bottom >= sc_rct.top > bg_rct.top:
            if visible_area_top > medium_speed_range["vertical"]:
                bg_rct.top += self.slow_speed["vertical"]
            if medium_speed_range["vertical"] >= visible_area_top > initial_speed_range["vertical"]:
                bg_rct.top += self.medium_speed["vertical"]
            if visible_area_top <= initial_speed_range["vertical"]:
                bg_rct.top += self.initial_speed["vertical"]

            bg_rct.top = min(bg_rct.top, sc_rct.top)

        elif "bottom" in self.pos and bg_rct.top <= sc_rct.bottom < bg_rct.bottom:
            if visible_area_bottom > medium_speed_range["vertical"]:
                bg_rct.bottom -= self.slow_speed["vertical"]
            if medium_speed_range["vertical"] >= visible_area_bottom > initial_speed_range["vertical"]:
                bg_rct.bottom -= self.medium_speed["vertical"]
            if visible_area_bottom <= initial_speed_range["vertical"]:
                bg_rct.bottom -= self.initial_speed["vertical"]

            bg_rct.bottom = max(bg_rct.bottom, sc_rct.bottom)

        if "left" in self.pos and bg_rct.right >= sc_rct.left > bg_rct.left:
            if visible_area_left > medium_speed_range["horizontal"]:
                bg_rct.left += self.slow_speed["horizontal"]
            if medium_speed_range["horizontal"] >= visible_area_left > initial_speed_range["horizontal"]:
                bg_rct.left += self.medium_speed["horizontal"]
            if visible_area_left <= initial_speed_range["horizontal"]:
                bg_rct.left += self.initial_speed["horizontal"]

            bg_rct.left = min(bg_rct.left, sc_rct.left)

        elif "right" in self.pos and bg_rct.left <= sc_rct.right < bg_rct.right:
            if visible_area_right > medium_speed_range["horizontal"]:
                bg_rct.right -= self.slow_speed["horizontal"]
            if medium_speed_range["horizontal"] >= visible_area_right > initial_speed_range["horizontal"]:
                bg_rct.right -= self.medium_speed["horizontal"]
            if visible_area_right <= initial_speed_range["horizontal"]:
                bg_rct.right -= self.initial_speed["horizontal"]

            bg_rct.right = max(bg_rct.right, sc_rct.right)

    def slide_panel_out(self) -> None:
        """Animate the info panel sliding off-screen from its on-screen position. The method adjusts the panel's position
        incrementally based on its 'pos' attribute until it reaches it's original off-screen position.
        Once the panel reaches its final position, it is snapped into place to prevent 'overshooting'."""
        bg_rct: pygame.Rect = self.bg_rect
        sc_rct: pygame.Rect = self.screen_rect

        if "top" in self.pos and bg_rct.bottom > sc_rct.top:
            bg_rct.bottom -= self.exit_speed["vertical"]
            bg_rct.bottom = max(bg_rct.bottom, sc_rct.top)
        elif "bottom" in self.pos and bg_rct.top < sc_rct.bottom:
            bg_rct.top += self.exit_speed["vertical"]
            bg_rct.top = min(bg_rct.top, sc_rct.bottom)

        if "left" in self.pos and bg_rct.right > sc_rct.left:
            bg_rct.right -= self.exit_speed["horizontal"]
            bg_rct.right = max(bg_rct.right, sc_rct.left)
        elif "right" in self.pos and bg_rct.left < sc_rct.right:
            bg_rct.left += self.exit_speed["horizontal"]
            bg_rct.left = min(bg_rct.left, sc_rct.right)

    def get_bg_rect_position(self) -> None:
        """Set starting info panel positions based on 'self.pos' argument."""
        anchor_y: int | None = self.screen_anchors[self.pos][0]
        anchor_x: int | None = self.screen_anchors[self.pos][1]

        if "top" in self.pos or "bottom" in self.pos:
            self.set_y_pos(anchor_y)
        if "left" in self.pos or "right" in self.pos:
            self.set_x_pos(anchor_x)

    def set_y_pos(self, anchor_y: int) -> None:
        """Set starting y-positions for all panels with occurrences of "top" or "bottom" in 'self.pos' based on
        'self.slide' attribute.
        Used in method 'get_bg_rect_positions()'.
        ARGS:
            anchor_y: Y-coordinate from the screen anchor used to position the panel vertically, depending on its 'pos'
            and 'slide' settings.
        """
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

    def set_x_pos(self, anchor_x: int) -> None:
        """Set starting x-positions for all panels with occurrences of "left" or "right" in 'self.pos' based on
        'self.slide' attribute.
        Used in method 'get_bg_rect_positions()'.
        ARGS:
            anchor_x: X-coordinate from the screen anchor used to position the panel horizontally, depending on its 'pos'
            and 'slide' settings.
        """

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

    def __init__(self, screen, input_field_instance: TextInputVisualizer, field_width: int) -> None:
        """Initialize text input field.
        ARGS:
            screen: pygame window.
            input_field_instance: instance of 'pygame_textinput'.
            field_width: width of background field.
        """
        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.input_field_instance: TextInputVisualizer = input_field_instance
        self.field_width: int = field_width

        self.field_height: int = input_field_instance.surface.get_height() * 2
        self.input_bg_field: pygame.Rect = pygame.Rect((0,0), (self.field_width, self.field_height))
        self.bg_rect_color: str | tuple[int, int, int] = settings.text_input_field_color
        self.input_bg_field.centerx, self.input_bg_field.centery = self.screen_rect.centerx, self.screen_rect.centery

        self.border_radius: int = int(self.screen_rect.height / 100)
        self.border_thickness: int = int(self.border_radius * 1.5)
        self.input_field_border: pygame.Rect = pygame.Rect((0,0), (int(self.input_bg_field.width + self.border_thickness),
                                                                   int(self.input_bg_field.height + self.border_thickness)))

    def draw_input_field(self) -> None:
        """Draw text input field with background on screen."""
        self.position_input_field_border()

        pygame.draw.rect(self.screen, settings.text_input_border_color, self.input_field_border, border_radius=self.border_radius)
        pygame.draw.rect(self.screen, self.bg_rect_color, self.input_bg_field)
        self.screen.blit(self.input_field_instance.surface,
                    (self.input_bg_field.centerx - self.input_field_instance.surface.get_width() / 2,
                     self.input_bg_field.centery - self.input_field_instance.surface.get_height() / 2))

    def position_input_field_border(self) -> None:
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

    def __init__(self, screen, height: int = 30, length: int = 3, time: int | float = 5) -> None:
        """Initialize loading progress bar.
        ARGS:
            screen: pygame window.
            height: height of the progress bar as a fraction of screen height. Default is '30'
            length: length of the progress bar as a fraction of screen width. Default is '3'
            time: approximate time in seconds for the progress bar to fill. Default is '5'
        """
        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()

        self.height: int = int(self.screen_rect.height / height)
        self.length: int = int(self.screen_rect.width / length)

        self.center_screen_pos: tuple[int, int] = int(self.screen_rect.centerx - self.length / 2), int(self.screen_rect.centery)

        self.border_radius: int = int(self.screen_rect.height / 72)
        self.border_width: int = int(self.border_radius / 3)
        self.inner_border_radius: int = max(0, self.border_radius - self.border_width)
        self.border_color: str | tuple[int, int, int] = settings.bar_border_color

        self.progress_bar_height: int = self.height - (2 * self.border_width)
        self.progress_bar_length: int = self.length - (2 * self.border_width)
        self.bar_color: str | tuple[int, int, int] = settings.progress_bar_color

        # Set starting value for loading 'progress' to 1.
        self.progress: int = 1

        self.speed: int = int(self.progress_bar_length / (time * settings.frame_rate))

        # Container rect.
        """NOTE: Change coordinates for this rect to position the progress bar as a whole!"""
        self.container_rect: pygame.Rect = pygame.Rect(self.center_screen_pos, (self.length, self.height))

        # 'None' attribute and method call to create rect for animated progress bar.
        self.progress_bar_rect: None | pygame.Rect = None
        self.build_progress_bar()

        # Flag attribute which is set to 'True' when progress bar is full. Not used within the class itself, but can be
        # used to, for example, trigger a 'continue' message after progress bar is finished. See 'show_title_screen()'
        # in 'gui/gui.py' and corresponding event handler for possible applications.
        self.finished: bool = False

        # Attributes ror random speed-up/slow-down events. Used in 'progress_manager()' and 'set_random_progress()'
        # methods further down.
        self.chance_per_second: float = 0.2  # 0.2% chance of event per frame.
        self.cooldown: bool = False
        self.cooldown_seconds: int | float = time / 2
        self.cooldown_timer: int = 0
        self.duration_timer: int = 0  # Timer for duration of event in frames.
        # Create 'backup' of set speed to be used for resetting of 'self.speed' if a random speed-up/slow-down event
        # modifies it.
        self.speed_backup: int = self.speed

    def draw_progress_bar(self) -> None:
        """Draw progress bar on screen until 'self.progress' value equals the specific value for 'self.length'."""
        container_left = self.container_rect.left
        container_centery = self.container_rect.centery
        progress_left = self.progress_bar_rect.left
        progress_centery = self.progress_bar_rect.centery

        if (container_left != progress_left) or (container_centery != progress_centery):
            self.build_progress_bar()

        if self.progress <= self.progress_bar_length:
            self.progress_manager(mode="trigger")
            pygame.draw.rect(self.screen, self.border_color, self.container_rect, border_radius=self.border_radius,
                             width=self.border_width)
            pygame.draw.rect(self.screen, self.bar_color, self.progress_bar_rect, border_radius=self.inner_border_radius)
            self.progress += self.speed
            self.progress_bar_rect.width = self.progress
        else:
            self.finished = True

        self.progress_manager(mode="reset")

    def build_progress_bar(self) -> None:
        """Create progress bar rect and position it at the center of the container rect."""
        self.progress_bar_rect = pygame.Rect(self.center_screen_pos, (self.progress, self.progress_bar_height))
        self.progress_bar_rect.left, self.progress_bar_rect.centery = (self.container_rect.left + self.border_width,
                                                                           self.container_rect.centery)

    def progress_manager(self, mode: str):
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
                    self.cooldown = True
                    self.cooldown_timer: int = int(settings.frame_rate * self.cooldown_seconds)

            if self.duration_timer > 0:
                self.duration_timer -= 1

            if self.duration_timer <= 0:
                self.speed: int = self.speed_backup

        elif mode == "reset":
            if self.cooldown:
                self.cooldown_timer -= 1
                if self.cooldown_timer <= 0:
                    self.cooldown: bool = False

    def set_random_progress(self) -> None:
        """Calculate and set random values for possible progress event types, then randomly choose an event to be
        triggered."""
        stop_duration_min_max: int | float = random.uniform(0.5, 2)  # seconds
        jump_value_min_max: int | float = random.uniform(15, 30)  # percent
        slow_value: int | float = 0.5  # multiplier
        slow_duration_min_max: int | float = random.uniform(1, 3)  # seconds
        speed_up_value_min_max: int | float = random.uniform(2, 3)  # multiplier
        speed_up_duration_min_max: int | float = random.uniform(1, 2)  # seconds

        stop_duration: int = int(settings.frame_rate * stop_duration_min_max)  # frames
        jump: int = int(self.progress_bar_length / (100 * jump_value_min_max))  # pixels
        slow: int = int(self.speed * slow_value)  # pixels
        speed_up: int = int(self.speed * speed_up_value_min_max)  # pixels

        events: tuple[tuple[str, int], ...] = (("stop", stop_duration),
                                               ("jump", jump),
                                               ("slow", slow),
                                               ("speed_up", speed_up))

        event_type, value = random.choice(events)

        if event_type == "stop":
            self.duration_timer: int = stop_duration
            self.speed: int = 0
        elif event_type == "jump":
            self.progress += jump
        elif event_type == "slow":
            self.speed: int = slow
            # Convert duration from seconds to frames and set timer.
            self.duration_timer: int = int(settings.frame_rate * slow_duration_min_max)
        elif event_type == "speed_up":
            self.speed: int = speed_up
            # Convert duration from seconds to frames and set timer.
            self.duration_timer: int = int(settings.frame_rate * speed_up_duration_min_max)
