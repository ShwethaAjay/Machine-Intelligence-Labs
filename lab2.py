# Initialize counter to count vowels
counter = 0

# Define a string containing the vowels to check against
vowels = "aeiou"
while True:
    name = input("Enter your name (Click \"enter\" to quit): ")

    # If the user enters an empty string (no input), quit the program
    if len(name) == 0:
        print("Quiting...")
        break

    # Analyzing name one letter at a time
    for letter in name.lower():
        if letter in vowels:
            counter += 1  # Increment the counter if it's a vowel

    print("Your name has ", counter, " vowels.\n")

    # Reset the counter to 0 for the next iteration
    counter = 0
