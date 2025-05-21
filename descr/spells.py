"""Contains function for the spells descriptions."""

def get_spell_descr() -> dict:
    """Initialize variables containing spell descriptions and return them in dict 'spell_descr'.
    NOTE: String variables created have to be then added manually to dict 'spell_descr'.
    RETURNS:
        spell_descr: dict containing lists for spell description texts as strings.
    """
    read_magic: str = ("Range: 0\t\t\t\t\t\t\t\tDuration: permanent\n"
                       "When cast upon any magical text, such as a spellbook or magic-user spell scroll, this spell "
                       "enables the caster to read that text. Casting this spell on a cursed text will generally trigger "
                       "the curse. All Magic-Users begin play knowing this spell, and it can be prepared even if the "
                       "Magic-User loses access to their spellbook.")

    charm_person: str = ("Range: 30'\t\t\t\t\t\t\t\tDuration: special\n"
                         "This spell causes a humanoid (including all character races as well as creatures such as orcs, "
                         "goblins, gnolls, and so on) of 4 hit dice or less to perceive the caster as a close friend, love "
                         "interest, or at the very least as its trusted ally. Normal characters (PC or NPC) may be "
                         "affected regardless of level of ability.\n"
                         "A save vs. Spells will negate the effect. If hostilities have already commenced or the target "
                         "otherwise feels threatened by the caster, it receives a bonus of +5 on its saving throw.\n"
                         "The caster does not directly control the target; rather, orders must be given verbally, in "
                         "writing, or by means of gestures. Obviously, verbal orders will only work if the target and "
                         "caster share a spoken language, and the same limitation applies to written orders. Also note "
                         "that the exact perception of the caster by the affected individual is not under the control of "
                         "the caster; the GM should decide how the subject of this spell perceives its relationship to the "
                         "caster.\n"
                         "Commands that go against the target's basic nature or ask it to attack its own allies or friends "
                         "grant it a fresh saving throw with a bonus of +5 on the roll. Even if the target fails this save "
                         "it may still choose to do something else when commanded to perform an unwanted action. Of course, "
                         "if the caster is attacked, the charmed creature will act to protect its 'friend# (though that "
                         "could mean attacking its own allies, which might cause the target to instead attempt to carry "
                         "off the caster to a 'safe' place).\n"
                         "The target receives a new saving throw each day if it has an Intelligence of 13 or greater, every "
                         "week if its Intelligence is 9-12, or every month if its Intelligence is 8 or less; the GM must "
                         "rule on the equivalent intelligence of humanoid monsters.")

    detect_magic: str = ("Range: 60'\t\t\t\t\t\t\t\tDuration: 2 turns\n"
                         "The caster of this spell is able to detect enchanted or enspelled objects or creatures within "
                         "the given range by sight, seeing them surrounded by a pale glowing light. Only the caster sees "
                         "the glow. Invisible creatures or objects are not detected by this spell, but the emanations of "
                         "the invisibility magic will be seen as an amorphous glowing fog, possibly allowing the caster "
                         "(only) to attack the invisible creature at an attack penalty of only -2.")

    floating_disc: str = ("Range: 0\t\t\t\t\t\t\t\tDuration: 5 turns +1 per level\n"
                          "The casting of this spell causes an invisible platform of magical force to appear. It is about "
                          "the size of a shield, about 3 feet in diameter and an inch deep at its center. It can support "
                          "a maximum of 500 pounds of weight. (Note that water weighs about 8 pounds per gallon.)\n"
                          "The disc floats level to the ground, at about the height of the caster's waist. It remains "
                          "still when within 10' of the caster, and follows at the caster's movement rate if they move "
                          "away from it. The floating disc can be pushed as needed to position it but will be dispelled "
                          "if somehow moved more than 10 feet from the caster. When the spell duration expires, the disc "
                          "disappears from existence and drops whatever was supported to the surface beneath.\n"
                          "The disc must be loaded so that the items placed upon it are properly supported, or they will "
                          "(of course) fall off. For example, the disc can support just over 62 gallons of water, but the "
                          "water must be in a barrel or other reasonable container that can be placed upon the disc. "
                          "Similarly, a pile of loose coins will tend to slip and slide about, and some will fall off with "
                          "every step the caster takes; but a large sack full of coins, properly tied, will remain stable.")

    hold_portal: str = ("Range: 100' + 1' per level\t\t\t\t\t\t\t\tDuration: 1 round per level\n"
                        "This spell secures a portal such as a door, gate, window, or shutter made of normal non-magical "
                        "building materials; the portal behaves as if securely locked for the duration of the spell. The "
                        "door may be opened early only by means of knock or a successful casting of dispel magic, or by "
                        "literally destroying the door (which may well require more time than the duration of this spell "
                        "allows).")

    light: str = ("Range: 120'\t\t\t\t\t\t\t\tDuration: 6 turns +1 per level\n"
                  "This spell creates a light equal to torchlight which illuminates a 30' radius area well (with dim light "
                  "extending for an additional 20') around the target location or object. This effect is stationary when "
                  "cast in an area, but it can be cast on a movable object or even onto a character or creature.\n"
                  "Reversed, light becomes darkness, creating an area of darkness just as described above. This darkness "
                  "blocks out Darkvision and negates mundane light sources. Wherever both spells overlap they cancel out, "
                  "leaving only normal illumination in the overlapping area.\n"
                  "A light spell may be cast to dispel the darkness spell of an equal or lower level caster (and vice versa), "
                  "leaving neither spell active; likewise, a darkness spell can cancel the light spell of an equal or lower "
                  "level caster.\n"
                  "Either version of this spell may be used to blind an opponent by means of casting it on the target's "
                  "ocular organs. The target is allowed a saving throw vs. Death Ray to avoid the effect, and if the save "
                  "is made the spell does not take effect at all. A light or darkness spell cast to blind does not have "
                  "the given area of effect (that is, no light or darkness is shed around the victim).")

    magic_missile: str = ("Range: 100' + 10' per level\t\t\t\t\t\t\t\tDuration: instantaneous\n"
                          "This spell causes a magical arrow of energy to fly from the caster's finger and unerringly hit "
                          "its target, inflicting 1d6+1 points of damage. The target must be at least partially visible "
                          "to the caster, and no saving throw is normally allowed. It's not possible to target a specific "
                          "part of the target. Inanimate objects are not affected by this spell.\n"
                          "For every three caster levels beyond 1st, an additional missile is fired: two at 4th level, "
                          "three at 7th, four at 10th, and the maximum of five missiles at 13th level or higher. When "
                          "multiple missiles are fired in this way, the caster can target one or several creatures as "
                          "desired, as long as all are visible to the caster at the same time. All such targets must be "
                          "designated before any damage is rolled.")

    magic_mouth: str = ("Range: 30'\t\t\t\t\t\t\t\tDuration: special\n"
                        "This spell places a simple form of programmed illusion on a non-living object within range. When "
                        "triggered, the spell causes the illusion of a mouth to appear on the object and a message to be "
                        "said aloud. The enchantment can remain in place indefinitely, but is expended when triggered "
                        "(i.e. the message is normally delivered only once).\n"
                        "The message recounted may be up to three words per caster level in length. The caster may insert "
                        "pauses in the message, but the entire message must be delivered in a time period of no more than "
                        "a turn. The voice of the spell can be made to speak at any volume attainable by a normal human. "
                        "It will sound enough like the caster's own voice to be recognized by a close associate of the "
                        "caster, but not identical.\n"
                        "The illusionary mouth moves as if actually speaking the message being delivered, and remains "
                        "visible during pauses. If placed on an artistic depiction of a creature with a mouth (such as a "
                        "painting or statue), the spell can be made to appear to animate the mouth of the object.\n"
                        "This spell cannot be used to activate magic items which have command words, nor to activate any "
                        "other magical effects.\n"
                        "The caster must choose the conditions under which this spell is triggered. The conditions may be "
                        "as complicated or simple as desired, but must depend only on sight and hearing; the spell has no "
                        "other sensory capabilities. The spell also has no particular intelligence, and can be fooled by "
                        "disguises or illusions. The spell does have the capability to effectively see in normal darkness, "
                        "but not in any sort of magical darkness, and it cannot detect invisible creatures nor see through "
                        "doors, walls, or even opaque curtains. Likewise, stealth or magical silence are effective in "
                        "preventing audible triggers. Finally, the spell cannot detect a character's class, level, ability "
                        "scores, or any other feature not obvious to a normal NPC.\n"
                        "Triggers have an effective sensory range of 10 feet per caster level; sounds, sights, or actions "
                        "outside that range will never trigger the spell.")

    protection_from_evil: str = ("Range: touch\t\t\t\t\t\t\t\tDuration: 1 turn per level\n"
                                 "This spell protects the caster or a creature touched by the caster (the 'subject') from "
                                 "evil; specifically, the spell wards against summoned creatures, creatures with "
                                 "significantly evil intentions, and extraplanar creatures of evil nature. A magical barrier "
                                 "with a radius of just 1 foot is created around the subject. The barrier moves with the "
                                 "subject, and provides three specific forms of magical protection against attacks or other "
                                 "effects attempted by the affected creatures against the subject.\n"
                                 "First, the subject receives a bonus of +2 to their Armor Class, and a similar bonus of "
                                 "+2 on all saving throws.\n"
                                 "Second, the barrier blocks all attempts to charm or otherwise control the subject, or to "
                                 "possess the subject (such as with magic jar). Such attempts simply fail during the "
                                 "duration of this spell. Note however that a creature who receives this protection after "
                                 "being possessed is not cured of the possession.\n"
                                 "to physically touch the subject. Attacks by such creatures using their natural weapons "
                                 "simply fail. This effect is canceled if the subject performs any form of physical attack "
                                 "(even with a ranged weapon) on any affected creature, but the other features of the "
                                 "spell continue in force.\n"
                                 "Reversed, this spell becomes protection from good. It functions in all ways as described "
                                 "above, save that 'good# creatures are kept away, rather than 'evil' ones.")

    read_languages: str = ("Range: 0\t\t\t\t\t\t\t\tDuration: special\n"
                           "This spell grants the caster the ability to read almost any written language. It may be cast "
                           "in one of three modes:\n"
                           "In the first mode, the spell allows the caster to read any number of written works in a variety "
                           "of languages. This mode lasts for 1 turn per caster level.\n"
                           "In the second mode, the spell allows the caster to read any one book or tome; this mode lasts "
                           "3 hours per caster level.\n"
                           "In the third mode, the spell allows the caster to read any one non-magical scroll or other "
                           "single-sheet document; this mode is permanent.\n"
                           "This spell does not work on any sort of magical text, such as spell scrolls or spellbooks; "
                           "see read magic, below, for the correct spell to use in such cases.\n"
                           "The spell grants the ability to read the texts, but does not in any way hasten the reading "
                           "nor grant understanding of concepts the caster doesn't otherwise have the ability to understand. "
                           "Also, for this spell to function, there must be at least one living creature that can read "
                           "the given language somewhere on the same plane. The knowledge is not copied from that creature's "
                           "mind; rather, it is the existence of the knowledge that enables the spell to function.")

    shield: str = ("Range: self\t\t\t\t\t\t\t\tDuration: 5 rounds +1 per level\n"
                   "This spell creates an invisible shield made of magical force which floats in front of the caster, "
                   "protecting them from various attacks. The spell totally blocks magic missile attacks directed at the "
                   "caster, and improves the caster's Armor Class by +3 vs. melee attacks and +6 vs. missile weapons. "
                   "The Armor Class benefits do not apply to attacks originating from behind the caster, but magic missiles "
                   "are warded off from all directions.")

    sleep: str = ("Range: 90'\t\t\t\t\t\t\t\tDuration: 5 rounds per level\n"
                  "This spell puts several creatures of 3 or fewer hit dice, or a single 4 hit die creature, into a magical "
                  "slumber. Creatures of 5 or more hit dice are not affected. The caster chooses a point of origin for "
                  "the spell (within the given range, of course), and those creatures within 30' of the chosen point may "
                  "be affected. Each creature in the area of effect is allowed a save vs. Spells to resist.\n"
                  "Victims of this spell can always be hit if attacked. Injuring such a creature will cause it to awaken, "
                  "and it may begin fighting back or defending itself on the very next round. Slapping or shaking such a "
                  "creature will awaken it in 1d4 rounds, but normal noises will not.\n"
                  "Sleep does not affect unconscious creatures, constructs, or undead creatures.\n"
                  "When the duration elapses, the sleeping creatures normally wake up immediately; however, if they are "
                  "made very comfortable and the surroundings are quiet, the affected creatures may continue sleeping "
                  "normally at the GM's option.")

    ventriloquism: str = ("Range: 60'\t\t\t\t\t\t\t\tDuration: 1 turn per level\n"
                          "This spell causes the caster's voice to appear to come from another location within range, "
                          "for example, from a dark alcove or statue. The caster may choose a new location each round if "
                          "desired, and can cause the spell to temporarily abate without ending it and then resume it "
                          "again at any time within the given duration.")

    spell_descr: dict[str, str] = {
        "read_magic": read_magic,
        "charm_person": charm_person,
        "detect_magic": detect_magic,
        "floating_disc": floating_disc,
        "hold_portal": hold_portal,
        "light": light,
        "magic_missile": magic_missile,
        "magic_mouth": magic_mouth,
        "protection_from_evil": protection_from_evil,
        "read_languages": read_languages,
        "shield": shield,
        "sleep": sleep,
        "ventriloquism": ventriloquism,
    }

    return spell_descr