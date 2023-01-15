class Cargo:
    def __init__(self, ID, name, space, weight):
        self.ID = ID
        self.grid_size, self.type = self.ID.split("_")
        self.name = name
        self.space = space
        self.weight = weight

    def description(self):
        return "\n".join(
            [
                f"Cargo: {self.name}",
                f"Capacity: {self.space}L",
                f"Weight: {self.weight}kg.",
            ]
        )


def Cargo_Name_Output():
    print("Cargo Containers")
    for x in cargo_dict:
        print(f"\t{cargo_dict[x].ID}")


cargo_dict = {
    "Sm_La": Cargo("Sm_La", "small ship large cargo container", 15625, 626),
    "Sm_Me": Cargo("Sm_Me", "small ship medium cargo container", 3375, 274),
    "Sm_Sm": Cargo("Sm_Sm", "small ship small cargo container", 125, 49),
    "Sm_Co": Cargo("Sm_Co", "small cockpit", 1000, 1200),
    "Sm_Dr": Cargo("Sm_Dr", "small drill", 3375, 1004),
    "La_La": Cargo("La_La", "large ship large cargo container", 421875, 2593),
    "La_Sm": Cargo("La_Sm", "large ship small cargo container", 15625, 648),
    "La_Me": None,
    "La_Co": Cargo("La_Co", "large cockpit", 1000, 2000),
    "La_Dr": Cargo("La_Dr", "large drill", 23437.5, 6741),
}
