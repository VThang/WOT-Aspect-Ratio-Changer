import os
import sys
import time
import xml.etree.ElementTree as ET

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
    This function is the main entry point of the program.
    It loads data using the `load_data` function,
    prompts the user to select a menu option using the `menu` function,
    gets the root element of the loaded data using the `getroot` method,
    changes the aspect ratio of the root element using the `change_aspect_ratio` function,
    saves the modified data using the `save_file` function.
    """
    element_tree = load_data()
    key = menu()
    root_element = element_tree.getroot()
    change_aspect_ratio(root_element, key)
    save_file(element_tree)
    print("VThang - 2023")
    time.sleep(4)


def load_data() -> ET.ElementTree:
    """
    Load data from the preferences.xml file located in the APPDATA directory.

    Returns:
        ET.ElementTree: The parsed XML tree object representing the preferences.xml file.

    Raises:
        FileNotFoundError: If the preferences.xml file is not found.
        ET.ParseError: If the preferences.xml file is malformed.
    """
    try:
        appdata = os.getenv("APPDATA")
        if appdata is None:
            print("APPDATA environment variable not found.\nProgram exited.")
        global file_location
        file_location = appdata + "\\Wargaming.net\\WorldOfTanks\\preferences.xml"
        print(f"Loading: {file_location}")
        # file = open(file_location)
        tree = ET.parse(file_location)
        root = tree.getroot()
        check = False
        for x in root:
            if x.tag == "devicePreferences":
                for y in x:
                    if y.tag == "aspectRatio":
                        check = True
                        print(f"Current settings is: {y.text}")
        if check is False:
            raise ET.ParseError
    except FileNotFoundError:
        print(
            "Preference.xml file not found. Trying to run game first to create preferences.xml file then run this program again.\nProgram exited."
        )
        time.sleep(4)
        sys.exit(0)
    except ET.ParseError:
        print(
            "Preference.xml file malformed. Trying to run game first to recreate preferences.xml file then run this program again.\nProgram exited."
        )
        time.sleep(4)
        sys.exit(0)
    return tree


def change_aspect_ratio(root_element: ET.Element, key: str) -> None:
    """
    Change the aspect ratio of the game window.

    Args:
        root_element (ET.Element): The root element of the XML tree.
        key (str): The key representing the desired aspect ratio.

    Returns:
        None: This function does not return anything.
    """
    print(f"Game aspect ratio will be changed to: {key} ={dict_aspect[key]}")
    for x in root_element:
        if x.tag == "devicePreferences":
            for y in x:
                if y.tag == "windowMode":
                    y.text = "1"
                if y.tag == "aspectRatio":
                    y.text = dict_aspect[key]
                if y.tag == "aspectRatio_override":
                    y.text = dict_aspect[key]


def save_file(element_tree: ET.ElementTree) -> None:
    """
    Save the given ElementTree to the specified file location.

    Args:
        element_tree (ET.ElementTree): The ElementTree object to be saved.

    Returns:
        None
    """
    element_tree.write(file_location)


def menu() -> str:
    """
    This function displays a menu for selecting a screen aspect ratio.
    It iterates through the `dict_aspect` dictionary and prints the options.
    The user is prompted to enter a number corresponding to their selection.
    If the user enters an invalid number, a `ValueError` is raised.
    If the user enters a valid number, the function returns the corresponding aspect ratio key.

    :return: A string representing the selected aspect ratio key.
    :rtype: str
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
                    return key
                i += 1
            break
        except ValueError:
            print("Please enter 1->5.")


if __name__ == "__main__":
    main()
