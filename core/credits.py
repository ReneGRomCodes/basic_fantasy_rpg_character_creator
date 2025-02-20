import gui.screen_objects as so
from gui.ui_helpers import draw_screen_title
"""
Class for credits screen.
"""


class Credits:
    """Class to store, manage and show credits screen for pygame."""

    def __init__(self, screen, gui_elements):
        """Initialize credits screen elements."""
        # Assign text sizes from 'gui_elements' to attributes.
        self.title_size, self.text_large, self.text_medium = (gui_elements["title_size"], gui_elements["text_large"],
                                                              gui_elements["text_medium"])
        # Positioning variables.
        self.credits_pos_y_start = screen.get_rect().bottom + 5
        #self.credits_pos_y_start = screen.get_rect().height / 3
        self.title_pos_x = screen.get_rect().centerx + screen.get_rect().width / 12
        self.name_pos_x = screen.get_rect().centerx
        self.category_spacing = screen.get_rect().height / 10
        # Y-position variable which dynamically changes for each element on screen.
        self.dynamic_pos_y = self.credits_pos_y_start

        # Credits screen title.
        self.credits_title_text = "- CREDITS -"
        self.credits_title = so.TextField(screen, self.credits_title_text, self.title_size)
        # Credits.
        self.programmer_title = so.TextField(screen, "Programming & UI Design", self.text_large)
        self.programmer_name = so.TextField(screen, "René Grewe Romero", self.text_medium)
        self.concept_creator_title = so.TextField(screen, "Based on 'Basic Tabletop RPG'", self.text_large)
        self.concept_creator_name = so.TextField(screen, "by Chris Gonnerman", self.text_medium)
        self.font_creator_title = so.TextField(screen, "Font 'Eagle Lake'", self.text_large)
        self.font_creator_name = so.TextField(screen, "by Brian J. Bonislawsky", self.text_medium)

        # Array of objects to be shown on screen as instantiated above. Each inner tuple representing a credit category,
        # with the element at index [0] being the category title and the following elements being the credited names
        self.credits_elements = ((self.programmer_title, self.programmer_name),
                                 (self.concept_creator_title, self.concept_creator_name),
                                 (self.font_creator_title, self.font_creator_name))

    def show_credits(self, screen, gui_elements):
        """Position and draw credits on screen"""

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
