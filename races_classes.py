# Race descriptions.
def show_race_descriptions():
    """Print detailed description of playable races from 'races_description.txt'."""
    file = "races_description.txt"
    with open(file) as f:
        for line in f:
            f.readline()
            print(line)


# Class descriptions.
def show_class_descriptions():
    """Print detailed description of playable classes from 'classes_description'.txt."""
    file = "classes_description.txt"
    with open(file) as f:
        for line in f:
            f.readline()
            print(line)
