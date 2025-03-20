"""This file contains code in development and is meant to try out concepts or just play around with ideas... alright, at
this point it has become mostly a dumping ground for 'todos'."""

# Old TODOS from console times that could still be good to keep in mind when migrating that part over to PyGame:
# TODO figure out how to implement different attacks with spear in 'item_instance.py'
# TODO Equip/unequip methods work only for armor right now in 'character_model.py'
# TODO fully implement weapons shop within 'shop_functions.py'

# Shit to keep in mind:
# TODO keep an eye on functions in 'core\rules.py' and 'character_creation_functions.py' that will be obsolete after migration.
# TODO Remove function call 'build_character_sheet()' from event handler when final character sheet is done.
# TODO pop-up texts overlap with underlying text on some screens.

# PRIORITIES:
# TODO finish character sheet screen ffs!!!
# TODO Re-structure 'rules.py' and 'Character' class to get rid of overlap


"""
Fix:
Separate the info panel drawing from InteractiveText's draw_interactive_text() method and ensure it's drawn last in the
main loop:
    Store active info panels in a list.
    When an InteractiveText detects a hover, add its panel to that list.
    After all UI elements are drawn, loop through the list and draw the info panels last.
"""

"""
Modify InteractiveText.handle_mouse_interaction()
Instead of directly calling draw_info_panel(), store active panels somewhere:
"""
def handle_mouse_interaction(self, active_panels):
    """Handle interactive functions for the class object like info panel and selectability."""
    if self.interactive_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(self.screen, self.rect_hover_color, self.interactive_rect)

        if self.panel:
            active_panels.extend(self.panel)  # Store active panels to be drawn later

    # Selection handling stays the same

"""
Modify Main Loop
Before the loop:
"""
active_panels = []
"""
After the loop:
"""
for interactive_text in interactive_texts:
    interactive_text.draw_interactive_text(mouse_pos)
    interactive_text.handle_mouse_interaction(active_panels)

# Draw all active info panels LAST
for panel in active_panels:
    panel.draw_info_panel()

active_panels.clear()  # Reset for the next frame
