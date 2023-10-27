from io import TextIOWrapper
import os
import sys

from bs4 import BeautifulSoup

global list_aspect
dict_aspect = {
    "4:3  ": " 1.333333 ",
    "16:9 ": " 1.777778 ",
    "16:10": " 1.600000 ",
    "21:9 ": " 2.333333 ",
    "32:9 ": " 3.555556 ",
}


def main():
    """
    Execute the main logic of the program.
    This function loads data from a file using the `load_data` function.
    It then prompts the user to select a key using the `menu` function.
    Finally, it calls the `change_aspect_ratio` function with the loaded data and the selected key.

    Parameters:
        None

    Returns:
        None
    """
    file = load_data()
    key = menu()

    change_aspect_ratio(file, key)
    print("VThang - 2023")


def load_data() -> TextIOWrapper:
    """
    Loads data from the preferences.xml file located in the %APPDATA%/Wargaming.net/WorldOfTanks directory.

    Returns:
        TextIOWrapper: The file object representing the opened preferences.xml file.
    """
    try:
        appdata = os.getenv("APPDATA")
        if appdata is None:
            print("APPDATA environment variable not found.\nProgram exited.")
        file_location = appdata + "\\Wargaming.net\\WorldOfTanks\\preferences.xml"
        print(f"Loading: {file_location}")
        file = open(file_location)
    except FileNotFoundError:
        print(
            "Preference.xml file not found.\nTrying to run game first to create preferences.xml file then run this program again.\nProgram exited."
        )
        sys.exit(0)
    return file


def change_aspect_ratio(file, key: str):
    """
    Changes the aspect ratio of the game.

    Args:
        file (file-like object): The XML file containing the game preferences.
        key (str): The key representing the desired aspect ratio.

    Returns:
        None

    Prints the original and updated aspect ratios to the console.
    """
    print(f"Game aspect ratio will be changed to: {key} ={dict_aspect[key]}")
    pref_file = BeautifulSoup(file.read(), "xml")
    before = pref_file.root.devicePreferences.aspectRatio.text
    pref_file.root.devicePreferences.aspectRatio.string = dict_aspect[key]
    after = pref_file.root.devicePreferences.aspectRatio.text
    print(f"{before} -> {after}")


def menu() -> str:
    """
    Prints a menu of screen aspect ratios and prompts the user to select one.

    Returns:
        str: The selected screen aspect ratio.
    """
    print(
        "World of Tanks change aspect ratio mini tools."
        + "\nSelect your screen aspect ratio:"
    )
    i: int = 1
    for key, value in dict_aspect.items():
        print(f"{i}.{key} -> {value}")
        i += 1
    while True:
        try:
            select = int(input("Select: "))
            if select < 1 or select > 5:
                raise ValueError
            i = 0
            for key, value in dict_aspect.items():
                if i == select - 1:
                    print(f"{key} -> {value}")
                    return key
                i += 1
            break
        except ValueError:
            print("Please enter 1->5.")


if __name__ == "__main__":
    main()
