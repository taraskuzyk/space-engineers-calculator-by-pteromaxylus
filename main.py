from dataclasses import dataclass
from typing import Callable, List, Dict

import planet
import thruster
import cargo
import curses, sys
import math

CARGO_TYPES = ["La", "Sm", "Me", "Co", "Dr"]

"Cock pit"
"Drill"

curses.setupterm()
# clear = str(curses.tigetstr('clear'), 'ascii')
clear = "cls\n"
sys.stdout.write(clear)


def info():
    infoloop = True

    while infoloop:
        # start of info function
        selection = prompt_user_with_options(
            prompt_string="Select info section:",
            description_vs_value=get_description_vs_values(
                ["planets", "thrusters", "cargo", "go back"]
            ),
        )
        if selection == "go back":
            main()
        elif selection == "planets":
            planet_selection = prompt_planet_selection(
                "To see planet descriptions, enter the name of the planet you wish to see:\n"
            )
            print(planet.planet_dict[planet_selection].description())

        elif selection == "thrusters":
            thruster_ids = list(thruster.thruster_dict.keys())
            thruster_selection = prompt_user_with_options(
                prompt_string="Type the ID of the thruster you wish to see data from:\n",
                description_vs_value=get_description_vs_values([*thruster_ids, "all"]),
            )
            if thruster_selection == "all":
                thruster.TWR_Output()
            else:
                print(f"{thruster.thruster_dict[thruster_selection].description()}")

        elif selection == "cargo":
            cargo_ids = list(cargo.cargo_dict.keys())
            cargo_selection = prompt_user_with_options(
                prompt_string="Select cargo (Grid_Size format):",
                description_vs_value=get_description_vs_values([*cargo.cargo_dict, "all"])
            )
            if cargo_selection == "all":
                for cargo_id in cargo_ids:
                    print(cargo.cargo_dict[cargo_id].description())
            else:
                cargo.cargo_dict[cargo_selection].description()


def main():
    # chooosing which program to run
    while True:
        global bc
        bc = (
            input(
                "Type 'Info' for planet and thruster data, type 'Tc' to get to my thrust calculator\n"
            )
            .lower()
            .capitalize()
        )
        if bc in ("Info", "Tc"):
            break
        else:
            sys.stdout.write(clear)
            print("Invalid Selection")

    # using the choice in program to run the specified function
    if bc == "Tc":
        sys.stdout.write(clear)
        thrust_calculations()
    elif bc == "Info":
        sys.stdout.write(clear)
        info()
    else:
        print("I don't know how you got here.")


def thrust_calculations():
    planet_string = prompt_planet_selection(
        "Keep in mind that this is the way the game lists information, "
        "I know moons aren't planets and I know that their gravity is not what is shown.\n"
        "Which planet is your ship going to fly on?"
    )
    global planet_choice
    planet_choice = planet.planet_dict[planet_string]

    engine_select()

    prompt_user_with_options(
        prompt_string=(
            "Your options were shortened to their first two letters in the ID. "
            f"Make sure this ID is correct: {Engine_ID}"
            "Is this correct?."
        ),
        options=get_description_vs_values(["yes", "no"]),
    )

    volume = prompt_user_for_cargo_volume()
    extra_weight = volume * 2.7027

    dry_weight = prompt_user(
        prompt_string=(
            "Make sure your ship is empty with no items in it, then check your info screen "
            "in the control panel for your crafts weight.\n "
            "It will be listed as the Grid Mass, it also can be seen on your hud in "
            "the lower right while in the cockpit."
        ),
        validate_output=lambda output: output.isdigit() and output != "0",
    )
    dry_weight = int(dry_weight)

    desired_acceleration = prompt_user(
        prompt_string=(
            "How fast do you want your ship to be able to accelerate "
            "upwards against gravity in m/s^2?\n"
            "If you want the default (0.5G upward, 4.905 m/s^2), hit enter."
        ),
        validate_output=lambda output: True,
    )

    if is_float(desired_acceleration):
        desired_acceleration = float(desired_acceleration)
    else:
        desired_acceleration = 4.905
        print("Using default value of 4.905 m/s^2")

    total_loaded_weight = extra_weight + dry_weight
    required_mp_s_a = planet_choice.gravity + desired_acceleration
    new_engine_thrust = EngineChoice.thrust - (EngineChoice.weight * required_mp_s_a)
    required_newtons = total_loaded_weight * required_mp_s_a
    total_engines_required = required_newtons / new_engine_thrust
    extra_thrust_percent = (
        ((math.ceil(total_engines_required) * new_engine_thrust) / required_newtons) - 1
    ) * 100

    engine_name = (
        f"{EngineChoice.name}s" if total_engines_required > 1 else EngineChoice.name
    )
    print(
        f"Your ship has a cargo capacity of {volume} liters.\n"
        f"A dry weight of {math.ceil(dry_weight)} kilograms.\n"
        f"A wet weight of {math.ceil(total_loaded_weight)} kilograms.\n"
        f"A total ore load of capacity of {math.ceil(extra_weight)} kilograms.\n"
        f"Requiring {math.ceil(total_engines_required)} {engine_name}.\n"
        f"Extra thrust caused by rounding: {round(extra_thrust_percent, 1)}%"
    )


def prompt_planet_selection(prompt_string):
    planets = list(planet.planet_dict.keys())
    description_vs_values = get_description_vs_values(planets)
    return prompt_user_with_options(
        prompt_string=prompt_string,
        description_vs_value=description_vs_values,
    )


def is_float(string: str) -> bool:
    if string.isdigit():
        return True

    if "." in string:
        split = string.split(".")
        return len(split) == 2


def get_description_vs_values(options: List[str]) -> Dict[str, str]:
    return dict(zip(options, options))


def prompt_user_with_options(
    prompt_string: str, description_vs_value: Dict[str, str]
) -> str:
    descriptions = list(description_vs_value.keys())
    output = prompt_user(
        prompt_string=f"{prompt_string} {stringify_options_list(descriptions)}",
        validate_output=lambda output: output.lower() in descriptions,
    )
    return description_vs_value[output]


def stringify_options_list(options: List[str]) -> str:
    if len(options) == 1:
        raise ValueError("More than one option required")
    quoted_options = [f"'{option}'" for option in options]

    if len(options) == 2:
        return " or ".join(quoted_options)
    else:
        last_option = quoted_options[-1]
        all_but_last = ", ".join(quoted_options[:-1])
        return f"{all_but_last}, or {last_option}"


def engine_select():
    global Engine_ID
    Engine_ID = ""
    # Grid Size Selection
    global grid_size

    grid_size = prompt_user_with_options(
        prompt_string="Which grid size are you using?",
        description_vs_value={"large": "La", "small": "Sm"},
    )

    engine_size = prompt_user_with_options(
        prompt_string="Which size of thruster are you using?",
        description_vs_value={"large": "La", "small": "Sm"},
    )

    if planet_choice.atmosphere == 0:
        engine_type = prompt_user_with_options(
            prompt_string=(
                "Hydrogen has high thrust but requies piping hydrogen fuel.\n"
                "Ion has low thrust but only reqires the ship to be powered.\n"
                "Which engine type do you want?"
            ),
            description_vs_value={"hydrogen": "Hy", "ion": "Io"},
        )
    else:
        engine_type = prompt_user_with_options(
            prompt_string=(
                "Hydrogen has high thrust but requies piping hydrogen fuel.\n"
                "Atmospheric engines only require power. Though they only work in "
                "atmosphere and their thrust diminishes with altitude.\n"
                "Which engine type do you want?"
            ),
            description_vs_value={"hydrogen": "Hy", "atmospheric": "At"},
        )
    Engine_ID = f"{grid_size}_{engine_size}_{engine_type}"
    global EngineChoice
    EngineChoice = thruster.thruster_dict[Engine_ID]


cargo_type_to_description = {
    "La": "Large Cargo Container",
    "Me": "Medium Cargo Container",
    "Sm": "Small Cargo Container",
    "Co": "Cockpit",
    "Dr": "Drill",
}


def prompt_user(prompt_string: str, validate_output: Callable[[str], bool]):
    while True:
        output = input(prompt_string + "\n")
        if validate_output(output):
            return output
        print("Give a valid input.")


def prompt_cargo_type_number(cargo_type: str) -> int:
    output = prompt_user(
        prompt_string=f"How many {cargo_type_to_description[cargo_type]}s do you have?\n",
        validate_output=lambda output: output.isdigit(),
    )
    return int(output)


def prompt_user_for_cargo_volume():
    volume = 0

    for cargo_type in CARGO_TYPES:
        cargo_id = f"{grid_size}_{cargo_type}"
        if cargo_id == "La_Me":
            continue
        cargo_type_number = prompt_cargo_type_number(cargo_type)
        some_cargo = cargo.cargo_dict[cargo_id]
        volume += some_cargo.space * int(cargo_type_number)

    return volume


# notes for later, I could right the thruster choice code to take multiple
# \inputs the append the input to a string then compare that string to the
# definition of the thrusters then use that data afterward of the selected thruster.
# Like going L for large ship then add H for hydrogen, then L for large thruster. Making
# the name of a Large ship Large hydrogen engine LHL. then use that to reference the
# dictionary with class definitions of the thrusters to then redifine the choice engine
# as the engine from thruster.py   But it is 1am and I need to sleep.
# Nah that was a bad idea, it is less user friendly but is far simpler coding wise
# just to make the use have to input an id.

# I don't know how this black magic right here makes the program run but it does.
if __name__ == "__main__":
    main()
