"""
Shwetha Ajay
IDSN 542, Fall 2024
shwethaa@usc.edu
Lab 7
"""


class Hero:
    def __init__(self, input_str):
        # Split the input string based on the pipe symbol (|).
        herodata = input_str.strip().split('|')

        # Initialize the name, powers, and health based on parsed data.
        self.__name = herodata[0]
        self.__powers = herodata[1].split(',')
        self.__max_health = int(herodata[2])
        self.__current_health = self.__max_health

    # Getter for hero name
    def getName(self):
        return self.__name

    # Getter for current health
    def getHealth(self):
        return self.__current_health

    # String representation of the hero's powers
    def __str__(self):
        powers_str = f"{self.__name} has the following powers:\n"
        powers_str += "\n".join([f"\t{power}" for power in self.__powers])
        return powers_str
