import gui.screen_objects as so
from gui.ui_helpers import draw_screen_title
from core.settings import settings
"""
Class for credits screen.
"""


class Credits:
    """Class to store, manage and show credits screen for pygame."""

    def __init__(self, screen, gui_elements):
        """Initialize credits screen elements."""
        # Assign text sizes from 'gui_elements' to attributes.
        title_size, text_large, text_medium = gui_elements["title_size"], gui_elements["text_large"], gui_elements["text_medium"]
        # Positioning variables.
        self.credits_pos_y_start = screen.get_rect().bottom + 5
        self.title_pos_x = screen.get_rect().centerx + screen.get_rect().width / 12
        self.name_pos_x = screen.get_rect().centerx
        self.category_spacing = screen.get_rect().height / 10
        # Y-position variable which dynamically changes for each element on screen.
        self.dynamic_pos_y = self.credits_pos_y_start

        # Credits screen title.
        self.credits_title = so.TextField(screen, "- CREDITS -", title_size)
        # Credits.
        dev_title = so.TextField(screen, "Lead Developer", text_large)
        dev_name = so.TextField(screen, "René Grewe Romero", text_medium)
        concept_creator_title = so.TextField(screen, "Based on 'Basic Tabletop RPG'", text_large)
        concept_creator_name = so.TextField(screen, "by Chris Gonnerman", text_medium)
        art_ui_title = so.TextField(screen, "Artwork & UI Design", text_large)
        art_ui_name = so.TextField(screen, "René Grewe Romero", text_medium)
        font_creator_title = so.TextField(screen, "Font 'Eagle Lake'", text_large)
        font_creator_name = so.TextField(screen, "by Brian J. Bonislawsky", text_medium)

        # Array of objects to be shown on screen as instantiated above. Each inner tuple representing a credit category,
        # with the element at index [0] being the category title and the following elements being the credited names.
        self.credits_elements = ((dev_title, dev_name),
                                 (concept_creator_title, concept_creator_name),
                                 (art_ui_title, art_ui_name),
                                 (font_creator_title, font_creator_name))

        # Calculate fade-out speed. Represent intervals for alpha value changes per frame when credits fade out at the
        # top of the screen.
        self.fading_speed = int(7 * (30 / settings.frame_rate))

    def show_credits(self, screen, gui_elements):
        """Position and draw credits on screen."""

        draw_screen_title(screen, self.credits_title, gui_elements)

        # Iterate through 'credits_elements' array, set positioning and spacing, and draw objects on screen.
        for category in self.credits_elements:
            for item in category:
                # Position category title.
                if item == category[0]:
                    item.text_rect.top, item.text_rect.right = self.dynamic_pos_y, self.title_pos_x
                    self.dynamic_pos_y += item.text_rect.height
                # Position last credited name and add spacing between it and next category.
                elif item == category[-1]:
                    item.text_rect.top, item.text_rect.left = self.dynamic_pos_y, self.name_pos_x
                    self.dynamic_pos_y += self.category_spacing
                # Position credited names.
                else:
                    item.text_rect.top, item.text_rect.left = self.dynamic_pos_y, self.name_pos_x
                    self.dynamic_pos_y += item.text_rect.height

                # Call class method for fade-out effect when credits reach top of the screen.
                self.fade_out_credits(screen, item)

                item.draw_text()

        # Call function to have credits scroll from bottom to top over the screen.
        self.dynamic_credits_position(screen)

    def dynamic_credits_position(self, screen):
        """Dynamically change position of credits elements for scrolling effect."""
        # Change starting y-position for each frame and set new starting value for dynamically changed y-position to
        # make text move across the screen.
        self.credits_pos_y_start -= screen.get_rect().height / 300
        self.dynamic_pos_y = self.credits_pos_y_start

        # Reset y-positions when last credit left top of the screen to start over again from the bottom.
        if self.credits_elements[-1][-1].text_rect.bottom <= screen.get_rect().top:
            self.credits_pos_y_start = screen.get_rect().bottom + 5
            self.dynamic_pos_y = self.credits_pos_y_start

    def fade_out_credits(self, screen, item):
        """Fade out credits item when it reaches top of the screen, then reset alpha transparency to opaque when it has
        fully left the screen."""
        # Set item transparency based on position on screen for fade-out effect.
        if item.text_rect.top <= screen.get_rect().height / 4 and not item.text_rect.bottom <= screen.get_rect().top:
            item.text_surface.set_alpha(item.background_alpha)
            item.background_alpha -= self.fading_speed
        # Reset transparency when the item has fully left the top of the screen, ensuring it is opaque when it
        # reappears at the bottom.
        elif item.background_alpha != 255:
            item.background_alpha = 255
            item.text_surface.set_alpha(item.background_alpha)
