"""
Class for credits screen.
"""
from core.settings import settings

from .screen_objects import TextField
from .ui_helpers import draw_screen_title
from .shared_data import ui_shared_data as uisd


class Credits:
    """Class to store, manage and show credits screen for pygame."""

    def __init__(self, screen) -> None:
        """Initialize credits screen elements.
        ARGS:
            screen: PyGame window.
        """
        self.screen_rect = screen.get_rect()
        title_size: int = uisd.ui_registry["title_size"]
        text_large: int = uisd.ui_registry["text_large"]
        text_medium: int = uisd.ui_registry["text_medium"]

        self.credits_pos_y_start: int = self.screen_rect.bottom + 5
        self.title_pos_x: int = self.screen_rect.centerx + self.screen_rect.width / 12
        self.name_pos_x: int = self.screen_rect.centerx
        self.category_spacing: int = self.screen_rect.height / 10
        # Y-position attribute which dynamically changes for each element on screen.
        self.dynamic_pos_y: int = self.credits_pos_y_start

        self.credits_title: TextField = TextField(screen, "- CREDITS -", title_size)
        dev_title: TextField = TextField(screen, "Lead Developer", text_large, text_color=settings.credits_text_color)
        dev_name: TextField = TextField(screen, "René Grewe Romero", text_medium, text_color=settings.credits_text_color)
        concept_creator_title: TextField = TextField(screen, "Based on 'Basic Tabletop RPG'", text_large, text_color=settings.credits_text_color)
        concept_creator_name: TextField = TextField(screen, "by Chris Gonnerman", text_medium, text_color=settings.credits_text_color)
        art_ui_title: TextField = TextField(screen, "Artwork & UI Design", text_large, text_color=settings.credits_text_color)
        art_ui_name: TextField = TextField(screen, "René Grewe Romero", text_medium, text_color=settings.credits_text_color)
        font_creator_title: TextField = TextField(screen, "Font 'Eagle Lake'", text_large, text_color=settings.credits_text_color)
        font_creator_name: TextField = TextField(screen, "by Brian J. Bonislawsky", text_medium, text_color=settings.credits_text_color)

        self.credits_elements: tuple[tuple[TextField, TextField], ...] = ((dev_title, dev_name),
                                                                          (concept_creator_title, concept_creator_name),
                                                                          (art_ui_title, art_ui_name),
                                                                          (font_creator_title, font_creator_name))

        self.fading_speed: int = int(7 * (30 / settings.frame_rate))

    def show_credits(self, screen) -> None:
        """Position and draw credits on screen.
        ARGS:
            screen: PyGame window.
        """

        draw_screen_title(screen, self.credits_title)

        for category in self.credits_elements:
            for item in category:
                if item == category[0]:  # Category title.
                    item.text_rect.top, item.text_rect.right = self.dynamic_pos_y, self.title_pos_x
                    self.dynamic_pos_y += item.text_rect.height
                elif item == category[-1]:  # Last credited name. Add spacing between it and next category.
                    item.text_rect.top, item.text_rect.left = self.dynamic_pos_y, self.name_pos_x
                    self.dynamic_pos_y += self.category_spacing
                else:  # Credited names.
                    item.text_rect.top, item.text_rect.left = self.dynamic_pos_y, self.name_pos_x
                    self.dynamic_pos_y += item.text_rect.height

                self.fade_out_credits(item)

                item.draw_text()

        self.dynamic_credits_position()

    def dynamic_credits_position(self) -> None:
        """Dynamically change position of credits elements for scrolling effect.
        """
        # Change starting y-position for each frame and set new starting value for dynamically changed y-position to
        # make text move across the screen.
        self.credits_pos_y_start -= self.screen_rect.height / 300
        self.dynamic_pos_y = self.credits_pos_y_start

        # Reset y-positions when last credit left top of the screen to start over again from the bottom.
        if self.credits_elements[-1][-1].text_rect.bottom <= self.screen_rect.top:
            self.credits_pos_y_start = self.screen_rect.bottom + 5
            self.dynamic_pos_y = self.credits_pos_y_start

    def fade_out_credits(self, item: TextField) -> None:
        """Fade out credits item when it reaches top of the screen, then reset alpha transparency to opaque when it has
        fully left the screen.
        ARGS:
            item: 'TextField' instance.
        """
        # Set item transparency based on position on screen for fade-out effect.
        if item.text_rect.top <= self.screen_rect.height / 4 and not item.text_rect.bottom <= self.screen_rect.top:
            item.text_surface.set_alpha(item.background_alpha)
            item.background_alpha -= self.fading_speed
        # Reset transparency when the item has fully left the top of the screen, ensuring it is opaque when it
        # reappears at the bottom.
        elif item.background_alpha != 255:
            item.background_alpha = 255
            item.text_surface.set_alpha(item.background_alpha)
