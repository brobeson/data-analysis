"""Meta-data for various tracking data sets."""

TB50 = [
    "Basketball",
    "Biker",
    "Bird1",
    "BlurBody",
    "BlurCar2",
    "BlurFace",
    "BlurOwl",
    "Bolt",
    "Box",
    "Car1",
    "Car4",
    "CarDark",
    "CarScale",
    "ClifBar",
    "Couple",
    "Crowds",
    "David",
    "Deer",
    "Diving",
    "DragonBaby",
    "Dudek",
    "Football",
    "Freeman4",
    "Girl",
    "Human3",
    "Human4",
    "Human6",
    "Human9",
    "Ironman",
    "Jump",
    "Jumping",
    "Liquor",
    "Matrix",
    "MotorRolling",
    "Panda",
    "RedTeam",
    "Shaking",
    "Singer2",
    "Skating1",
    "Skating2-1",
    "Skating2-2",
    "Skiing",
    "Soccer",
    "Surfer",
    "Sylvester",
    "Tiger2",
    "Trellis",
    "Walking",
    "Walking2",
    "Woman",
]

TB100 = TB50 + [
    "Bird2",
    "BlurCar1",
    "BlurCar2",
    "BlurCar4",
    "Board",
    "Bolt2",
    "Boy",
    "Car2",
    "Car24",
    "Coke",
    "Coupon",
    "Crossing",
    "Dancer",
    "Dancer2",
    "David2",
    "David3",
    "Dog",
    "Dog1",
    "Doll",
    "FaceOcc1",
    "FaceOcc2",
    "Fish",
    "FleetFace",
    "Football1",
    "Freeman1",
    "Freeman3",
    "Girl2",
    "Gym",
    "Human2",
    "Human5",
    "Human7",
    "Human8",
    "Jogging-1",
    "Jogging-2",
    "KiteSurf",
    "Lemming",
    "Man",
    "Mhyang",
    "MountainBike",
    "Rubik",
    "Singer1",
    "Skater",
    "Skater2",
    "Subway",
    "Suv",
    "Tiger1",
    "Toy",
    "Trans",
    "Twinnings",
    "Vase",
]
TB100.sort()


def determine_data_set(sequences):
    """
    Try to determine which data set a list of sequences is.

    Parameters:
    sequences (list): A list of strings. Each string is a sequence.

    Returns:
    None is returned if the sequences do not exactly match a particular data
    set.
    string: The name of the data set as a string.
    """
    if TB50 == sequences:
        return "tb50"
    if TB100 == sequences:
        return "tb100"
    return None
