"""
Shwetha Ajay
IDSN 542, Fall 2024
shwethaa@usc.edu
Lab 7
"""

# Import the Hero class from the hero.py file
from hero import Hero


# Function to load heroes from a given file
def loadHeroes(filename):
    heroes = []
    try:
        # Open the file with the given filename and read each line
        with open(filename, 'r') as file:
            for line in file:
                hero = Hero(line)  # Creating a Hero object from each line
                heroes.append(hero)  # Adding this object to heroes list
        print(f"{len(heroes)} heroes loaded\n")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    return heroes


def printRoster(heroes):
    print(f"The following {len(heroes)} heroes are loaded...")
    for hero in heroes:
        print("********************************************")
        # Print the hero's details using the Hero class' __str__ method
        print(hero)
    print("********************************************")


def main():
    print("Welcome to the hero fighter!")

    while True:
        filename = input("\nEnter the file to be loaded (or press enter to quit): ")
        if filename == '':
            print("Exiting.....")
            break
        # Call the loadHeroes function to load the heroes from the file
        heroes = loadHeroes(filename)

        # Only print the roster if heroes were loaded
        if len(heroes) > 0:
            printRoster(heroes)
            break
    print("Goodbye!")


main()
