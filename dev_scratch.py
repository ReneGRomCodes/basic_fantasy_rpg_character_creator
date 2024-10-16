"""This file contains code in development and is meant to try out concepts or just play around with ideas."""

# TODO figure out how to implement different attacks with spear in 'item_instance.py'
# TODO Equip/unequip methods work only for armor right now in 'character_model.py'
# TODO fully implement weapons shop within 'shop_functions.py'
# TODO keep an eye on correct position of 'pygame.quit()' statements in character creation functions in 'main_functions.py'


def draw_multiline_text(surface, text, pos, font, color):
    words = [word.split(" ") for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
