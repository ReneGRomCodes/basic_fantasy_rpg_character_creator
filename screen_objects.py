import pygame
"""Classes for screen objects (buttons, text, etc.)."""


class ScreenObject:

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()


class TextField(ScreenObject):

    def __init__(self, screen, text):
        super().__init__(screen)
        self.text = text
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.text_image = self.font.render(self.text, True, self.text_color)

        # Create a rect for positioning.
        self.text_rect = self.text_image.get_rect()
        # Center text on the screen.
        self.text_rect.centerx = self.screen_rect.centerx
        self.text_rect.centery = self.screen_rect.centery

    def draw_text(self):
        self.screen.blit(self.text_image, self.text_rect)
