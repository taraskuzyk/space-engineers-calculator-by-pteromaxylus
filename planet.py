class Planet:
    def __init__(self, name, gravity, atmosphere, oxygen):
        self.name = name
        self.gravity = gravity
        self.atmosphere = atmosphere
        self.has_oxygen = oxygen

    def description(self):
        return f"{self.name} has a gravity of {self.gravity / 9.81} Gs. Its effective atmospheric zone averages {self.atmosphere} meters from the surface. Oxygen: {self.has_oxygen}."


def Planet_Name_Output():
    print("Planets")
    for x in planet_dict:
        print(f"\t{planet_dict[x].name}")


planet_dict = {
    "Earth": Planet("Earth", 9.81, 8900, True),
    "Alien": Planet("Alien", 10.791, 8900, True),
    "Mars": Planet("Mars", 8.829, 6900, False),
    "Moon": Planet("Moon", 2.4525, 0, False),
    "Titan": Planet("Titan", 2.4525, 670, False),
    "Europa": Planet("Europa", 2.4525, 860, False),
}
