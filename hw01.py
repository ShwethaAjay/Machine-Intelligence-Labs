"""
Shwetha Ajay
IDSN 542, Fall 2024
shwethaa@usc.edu
Homework 1
"""

# Part 1: Prompt for input
# Ask for the person's name whose BMI is being calculated
name = input("Hello! Who's BMI is being calculated? ")

# Ask for the person's height in feet and inches component
print("\nGreat! Let's start with {}'s height. I need it in two parts: feet and inches".format(name.title()))
heightFeetComponent = float(input("First, how many feet tall is {}? ".format(name.title())))
heightInchesComponent = float(input("And how many additional inches? "))

# Ask for the person's weight
print("\nThank you! Now let's move on to {}'s weight".format(name.title()))
weightPounds = float(input("Enter weight in pounds : "))

# Part 2: Calculate total inches
# Convert the person's height into inches (1 foot = 12 inches)
totalHeightInches = float((heightFeetComponent * 12) + heightInchesComponent)
# print("Height in inches is ",totalHeightInches)

# Part 2: Calculate height in meters
# Convert the person's height into meter (1 meter = 39.37 inches)
totalHeightMeters = float(totalHeightInches/39.37)
# print("Height in meter is ",totalHeightMeters)

# Part 4: Calculate weight in kilograms
# Convert the weight from pounds to kilograms (1 kilogram = 2.2 pounds)
weightKilogram = float(weightPounds/2.2)
# print("Weight in kilograms is ",weightKilogram)

# Part 5: Calculate and output final BMI
bmi = float(weightKilogram/(totalHeightMeters**2))
print("\nBased on the information provided, {}'s BMI is ".format(name.title()),round(bmi,1))