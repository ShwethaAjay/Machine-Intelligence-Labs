import random


def frequencyChart(n):
    # generating 'n' many random numbers between 0 and 50,000
    randomNumbers = [random.randrange(50001) for i in range(n)]
    # print(randomNumbers)

    # creating a dictionary of factors (2-53)
    factors = {factor: 0 for factor in range(2, 54)}

    # finding what numbers between 2 and 53 evenly divide each of the random numbers
    for num in randomNumbers:
        for factor in range(2, 54):
            if num % factor == 0:
                factors[factor] += 1

    print(f"\nFactor Frequency Chart for {n} random numbers :\n")
    for factor in range(2, 54):
        if factors[factor] > 0:
            print(f"{factor}: {'*' * factors[factor]}")


n = int(input("Give a number: "))
frequencyChart(n)
