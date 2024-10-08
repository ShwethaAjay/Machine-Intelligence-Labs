from die import Die


def rollDice(dice_list):
    totalSum = 0
    for die in dice_list:
        totalSum += die.roll()
    return totalSum


def printDice(dice_list):
    for die in dice_list:
        print(f"#{dice_list.index(die)+1} : {die}")


def main():
    sides = int(input("How many sides does your dice have?: "))
    num_dice = int(input("How many dice do you have?: "))

    dice_list = []
    for num in range(num_dice):
        dice_list.append(Die(sides))

    while True:
        roll_choice = input("\nDo you want to roll the dice? (y/n): ").lower()
        if roll_choice == 'y':
            totalSum = rollDice(dice_list)
            # print(f"Sum of dice rolls: {total}")
            printDice(dice_list)

        elif roll_choice == 'n':
            print("Exiting the dice game.")
            break

        else:
            print("Invalid input. Please enter 'y' or 'n'.")


main()
