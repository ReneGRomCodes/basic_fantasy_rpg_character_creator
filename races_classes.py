# Race descriptions.

def show_race_descriptions():
    """Print detailed description of playable races from race_description.txt."""
    file = "races_description.txt"
    with open(file) as f:
        for line in f:
            f.readline()
            print(line)
