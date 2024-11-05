"""Contains function for the race descriptions."""

def get_race_descr():
    """Initialize variables containing race descriptions and return them in dict 'race_descr'.
        NOTE: String variables created have to be then added manually to dict 'race_descr'."""

    humans_descr = ("Description: Humans come in a broad variety of shapes and sizes; the Game Master must decide what "
                   "sorts of Humans live in the game world. An average Human male in good health stands around six feet "
                   "tall and weighs about 175 pounds, while females average five feet nine inches and weigh around 145 "
                   "pounds. Most Humans live around 75 years.\n"
                   "\n"
                   "Restrictions: Humans may be any single class. They have no minimum or maximum ability score "
                   "requirements.\n"
                   "\n"
                   "Special Abilities: Humans learn unusually quickly, gaining a bonus of 10% to all experience points "
                   "earned.\n"
                   "\n"
                   "Saving Throws: Humans are the 'standard', and thus have no saving throw bonuses.")

    elves_descr = ("Description: Elves are a slender race, with both males and females standing around five feet tall and "
                   "weighing around 130 pounds. Most have dark hair, with little or no body or facial hair. Their skin "
                   "is pale, and they have pointed ears and delicate features. Elves are lithe and graceful. They have "
                   "keen eyesight and hearing. Elves are typically inquisitive, passionate, self-assured, and sometimes "
                   "haughty. Their typical lifespan is a dozen centuries or more.\n"
                   "\n"
                   "Restrictions: Elves may become Clerics, Fighters, Magic-Users or Thieves; they are also allowed to "
                   "combine the classes of Fighter and Magic-User, and of Magic-User and Thief. They are required to "
                   "have a minimum Intelligence of 9. Due to their generally delicate nature, they may not have a "
                   "Constitution higher than 17. Elves never roll larger than six-sided dice (d6) for hit points.\n"
                   "\n"
                   "Special Abilities: All Elves have Darkvision with a 60' range. They are able to find secret doors "
                   "more often than normal (1-2 on 1d6 rather than the usual 1 on 1d6). An Elf is so observant that one "
                   "has a 1 on 1d6 chance to find a secret door with a cursory look. Elves are immune to the paralyzing "
                   "attack of ghouls. Also, they are less likely to be surprised in combat, reducing the chance of "
                   "surprise by 1 in 1d6.\n"
                   "\n"
                   "Saving Throws: Elves save at +1 vs. Paralysis or Petrify, and +2 vs. Magic Wands and Spells.")

    dwarfes_descr = ("Description: Dwarves are a short, stocky race; both male and female Dwarves stand around four feet "
                     "tall and typically weigh around 120 pounds. Their long hair and thick beards are dark brown, gray "
                     "or black. They take great pride in their beards, sometimes braiding or forking them. They have a "
                     "fair to ruddy complexion. Dwarves have stout frames and a strong, muscular build. They are rugged "
                     "and resilient, with the capacity to endure great hardships. Dwarves are typically practical, "
                     "stubborn and courageous. They can also be introspective, suspicious and possessive. They have a "
                     "lifespan of three to four centuries.\n"
                     "\n"
                     "Restrictions: Dwarves may become Clerics, Fighters, or Thieves. They are required to have a minimum "
                     "Constitution of 9. Due to their generally dour dispositions, they may not have a Charisma higher "
                     "than 17. They may not employ Large weapons more than four feet in length (specifically, two-handed "
                     "swords, polearms, and longbows).\n"
                     "\n"
                     "Special Abilities: All Dwarves have Darkvision with a 60' range, and are able to detect slanting "
                     "passages, stonework traps, shifting walls and new construction on a roll of 1-2 on 1d6; a search "
                     "must be performed before this roll may be made.\n"
                     "\n"
                     "Saving Throws: Dwarves save at +4 vs. Death Ray or Poison, Magic Wands, Paralysis or Petrify, and "
                     "Spells, and at +3 vs. Dragon Breath.")

    halflings_desc = ("Description: Halflings are small, slightly stocky folk who stand around three feet tall and weigh "
                      "about 60 pounds. They have curly brown hair on their heads and feet, but rarely have facial hair. "
                      "They are usually fair skinned, often with ruddy cheeks. Halflings are remarkably rugged for their "
                      "small size. They are dexterous and nimble, capable of moving quietly and remaining very still. "
                      "They usually go barefoot. Halflings are typically outgoing, unassuming and good natured. They live "
                      "about a hundred years.\n"
                      "\n"
                      "Restrictions: Halflings may become Clerics, Fighters or Thieves. They are required to have a "
                      "minimum Dexterity of 9. Due to their small stature, they may not have a Strength higher than 17. "
                      "Halflings never roll larger than six-sided dice (d6) for hit points regardless of class. Halflings "
                      "may not use Large weapons, and must wield Medium weapons with both hands.\n"
                      "\n"
                      "Special Abilities: Halflings are unusually accurate with all sorts of ranged weapons, gaining a +1 "
                      "attack bonus when employing them. When attacked in melee by creatures larger than man-sized, "
                      "Halflings gain a +2 bonus to their Armor Class. Halflings are quick-witted, adding +1 to Initiative "
                      "die rolls. In their preferred forest terrain, they are able to hide very effectively; so long as "
                      "they remain still there is only a 10% chance they will be detected. Even indoors, in dungeons or "
                      "in non-preferred terrain they are able to hide such that there is only a 30% chance of detection. "
                      "Note that a Halfling Thief will roll only once, using either the Thief ability or the Halfling "
                      "ability, whichever is better.\n"
                      "\n"
                      "Saving Throws: Halflings save at +4 vs. Death Ray or Poison, Magic Wands, Paralysis or Petrify, "
                      "and Spells, and at +3 vs. Dragon Breath.")

    race_descr = {
        "humans": humans_descr,
        "elves": elves_descr,
        "dwarves": dwarfes_descr,
        "halflings": halflings_desc,
    }

    return race_descr
