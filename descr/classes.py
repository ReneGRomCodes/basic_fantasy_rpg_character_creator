"""Contains function for the class descriptions."""

def get_class_descr():
    """Initialize variables containing class descriptions and return them in dict 'class_descr'.
        NOTE: String variables created have to be then added manually to dict 'class_descr'."""

    fighter_descr = ("Fighters include soldiers, guardsmen, barbarian warriors, and anyone else for whom fighting is a "
                     "way of life. They train in combat, and they generally approach problems head-on, weapon in hand.\n"
                     "\n"
                     "Not surprisingly, Fighters are the best at fighting of all the classes. They are also the hardiest, "
                     "able to take more punishment than any other class. Although they are not skilled in the ways of "
                     "magic, Fighters can nonetheless use many magic items, including but not limited to magical weapons "
                     "and armor.\n"
                     "\n"
                     "The Prime Requisite for Fighters is Strength; a character must have a Strength score of 9 or higher "
                     "to become a Fighter. Members of this class may wear any armor and use any weapon.")
    cleric_descr = ("Clerics are those who have devoted themselves to the service of a deity, pantheon or other belief "
                    "system. Most Clerics spend their time in mundane forms of service such as preaching and ministering "
                    "in a temple; but there are those who are called to go abroad from the temple and serve their deity "
                    "in a more direct way, smiting undead monsters and aiding in the battle against evil and chaos. Player "
                    "character Clerics are assumed to be among the latter group.\n"
                    "\n"
                    "Clerics fight about as well as Thieves, but not as well as Fighters. They are hardier than Thieves, "
                    "at least at lower levels, as they are accustomed to physical labor that the Thief would deftly avoid. "
                    "Clerics can cast spells of divine nature starting at 2nd level, and they have the power to Turn the "
                    "Undead, that is, to drive away undead monsters by means of faith alone.\n"
                    "\n"
                    "The Prime Requisite for Clerics is Wisdom; a character must have a Wisdom score of 9 or higher to "
                    "become a Cleric. They may wear any armor, but may only use blunt weapons (specifically including "
                    "warhammer, mace, maul, club, quarterstaff, and sling).")
    magic_user_descr = ("Magic-Users are those who seek and use knowledge of the arcane. They do magic not as the Cleric "
                        "does, by faith in a greater power, but rather through insight and understanding.\n"
                        "\n"
                        "Magic-Users are the worst of all the classes at fighting; hours spent studying massive tomes of "
                        "magic do not lead a character to become strong or adept with weapons. They are the least hardy, "
                        "equal to Thieves at lower levels but quickly falling behind.\n"
                        "\n"
                        "The Prime Requisite for Magic-Users is Intelligence; a character must have an Intelligence score "
                        "of 9 or higher to become a Magic-User. The only weapons they become proficient with are the "
                        "dagger and the walking staff (or cudgel). Magic-Users may not wear armor of any sort nor use a "
                        "shield as such things interfere with spellcasting.\n"
                        "\n"
                        "A first level Magic-User begins play knowing read magic and one other spell of first level. These "
                        "pells are written in a spellbook provided by their master. The GM may roll for the spell, assign "
                        "it as they see fit, or allow the player to choose it, at their option.")
    thief_descr = ("Thieves are those who take what they want or need by stealth, disarming traps and picking locks to get "
                   "to the gold they crave; or 'borrowing' money from pockets, beltpouches, etc. right under the nose of "
                   "the 'mark' without the victim ever knowing.\n"
                   "\n"
                   "Thieves fight better than Magic-Users but not as well as Fighters. Avoidance of honest work leads "
                   "Thieves to be less hardy than the other classes, though they do pull ahead of the Magic-Users at "
                   "higher levels.\n"
                   "\n"
                   "The Prime Requisite for Thieves is Dexterity; a character must have a Dexterity score of 9 or higher "
                   "to become a Thief. They may use any weapon, but may not wear metal armor as it interferes with "
                   "stealthy activities, nor may they use shields of any sort. Leather armor is acceptable, however.\n"
                   "\n"
                   "Thieves have a number of special abilities, described below. One turn (ten minutes) must usually be "
                   "spent to use any of these abilities, as determined by the GM. The GM may choose to make any of these "
                   "rolls on behalf of the player to help maintain the proper state of uncertainty. Also note that the "
                   "GM may apply situational adjustments (plus or minus percentage points) as they see fit; for instance, "
                   "it's obviously harder to climb a wall slick with slime than one that is dry, so the GM might apply a "
                   "penalty of 20% for the slimy wall.")
    fighter_magic_user_descr = ("The Fighter/Magic-User is a rare blend of martial prowess and arcane mastery, combining "
                                "the battlefield prowess of a Fighter with the spellcasting abilities of a Magic-User. "
                                "These versatile combatants can face enemies with both sword and spell, making them "
                                "formidable opponents in any situation.\n"
                                "\n"
                                "Fighter/Magic-Users are capable of donning armor and wielding weapons while still being "
                                "able to cast their spells, an ability unique to this combination class. This grants them "
                                "a significant advantage over pure Magic-Users, who must forgo such protection to weave "
                                "their magic. While they are not as hardy as pure Fighters nor as proficient in magic as "
                                "dedicated Magic-Users, their ability to mix both disciplines allows them to adapt to a "
                                "variety of challenges.\n"
                                "\n"
                                "The Prime Requisites for Fighter/Magic-Users are both Strength and Intelligence; a "
                                "character must have a Strength score of 9 or higher and an Intelligence score of 9 or "
                                "higher to pursue this path. They may wear any armor and use any weapon, and they start "
                                "their journey with a spellbook containing read magic and one additional spell of first "
                                "level, similar to the Magic-User.")
    magic_user_thief_descr = ("The Magic-User/Thief is a cunning and elusive character, merging the arcane arts with the "
                              "skills of subterfuge and stealth. These individuals use their magical knowledge to enhance "
                              "their thieving capabilities, making them unpredictable and dangerous in a world that "
                              "underestimates them.\n"
                              "\n"
                              "Magic-User/Thieves are proficient in casting spells while wearing leather armor, enabling "
                              "them to maintain some protection without sacrificing their magical abilities. This makes "
                              "them more resilient than pure Magic-Users, though they remain less hardy than Fighters. "
                              "Their magical skills can be used to supplement their thievery, whether by disarming traps "
                              "with a mystical touch, charming their marks, or becoming invisible to evade capture.\n"
                              "\n"
                              "The Prime Requisites for Magic-User/Thieves are Intelligence and Dexterity; a character "
                              "must have an Intelligence score of 9 or higher and a Dexterity score of 9 or higher to "
                              "pursue this class. They may use any weapon and wear leather armor, but like pure "
                              "Magic-Users, they may not don metal armor or use shields. A first-level Magic-User/Thief "
                              "begins with a spellbook containing read magic and one additional first-level spell, "
                              "allowing them to embark on their adventures with both magical and practical tools at their "
                              "disposal.")

    class_descr = {
        "fighter": fighter_descr,
        "cleric": cleric_descr,
        "magic-user": magic_user_descr,
        "thief": thief_descr,
        "fighter_magic-user": fighter_magic_user_descr,
        "magic-user_thief": magic_user_thief_descr,
    }

    return class_descr
