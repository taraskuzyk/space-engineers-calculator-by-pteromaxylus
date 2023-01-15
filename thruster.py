class Thruster:
    def __init__(self, ID, name, thrust, weight):
        self.ID = ID
        self.name = name
        self.thrust = thrust
        self.weight = weight

    def description(self):
        return "\n".join(
            f"Thruster {self.name} parameters",
            f"Thrust: {self.thrust} N",
            f"Weight: {self.weight} kg",
            f"Thrust to weight ratio: {(self.thrust / self.weight).__round__()}",
        )


def TWR_Output():
    print("Grid_Size_Engine, thrust to weight ratio")
    for x in thruster_dict:
        print(
            f"\t{thruster_dict[x].ID}  TWR of {(thruster_dict[x].thrust / thruster_dict[x].weight).__round__()}"
        )


def Thruster_Name_Output():
    print("Thruster identifications, written as Grid_Size_Engine")
    for x in thruster_dict:
        print(f"\t{thruster_dict[x].ID}")


thruster_dict = {
    "La_La_Hy": Thruster(
        "La_La_Hy", "large grid, large hydrogen engine", 7200000, 6940
    ),
    "La_Sm_Hy": Thruster(
        "La_Sm_Hy", "large grid, small hydrgoen engine", 1080000, 1420
    ),
    "Sm_La_Hy": Thruster("Sm_La_Hy", "small grid, large hydrogen engine", 480000, 1222),
    "Sm_Sm_Hy": Thruster("Sm_Sm_Hy", "small grid, small hydrogen engine", 98400, 334),
    "La_La_Io": Thruster("La_La_Io", "large grid, large ion engine", 4320000, 43200),
    "La_Sm_Io": Thruster("La_Sm_Io", "large grid, small ion engine", 345600, 4380),
    "Sm_La_Io": Thruster("Sm_La_Io", "small grid, large ion engine", 172800, 721),
    "Sm_Sm_Io": Thruster("Sm_Sm_Io", "small grid, small ion engine", 14400, 121),
    "La_La_At": Thruster(
        "La_La_At", "large grid, large atmospheric engine", 6480000, 32970
    ),
    "La_Sm_At": Thruster(
        "La_Sm_At", "large grid, small atmospheric engine", 648000, 3970
    ),
    "Sm_La_At": Thruster(
        "Sm_La_At", "small grid, large atmospheric engine", 576000, 2948
    ),
    "Sm_Sm_At": Thruster(
        "Sm_Sm_At", "small grid, small atmospheric engine", 96000, 699
    ),
}

# def engine_choice():
#   global engine
#   if planetchoice.atmosphere != 0:
#     engine = input(f"""What type of thruster do you wish to use?
# Enter one of the listed names or 9 if you wish to see information on the thrusters.
#   Atmospheric
#   Hydrogen""")

#   elif planetchoice.atmosphere == 0:
#     engine = input(f"""What type of thruster do you wish to use?
# Enter one of the listed names or 9 if you wish to see information on the thrusters.
#   Hydrogen
#   Ion""")
