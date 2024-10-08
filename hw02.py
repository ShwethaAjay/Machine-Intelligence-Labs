import random
import string

"""
Part 1 – Word Jumble Game
"""
print("Word Jumble Game\n")
wordList = ["apple", "cheese", "lemon", "carrot", "hummus"]
chosenWord = random.choice(wordList)

chosenWordList = list(chosenWord)
jumbledList = []
counter = 0

for i in range(len(chosenWordList)):
    letter = random.choice(chosenWordList)
    jumbledList.append(letter)
    chosenWordList.remove(letter)

jumbledWord = "".join(jumbledList)

print("The jumbled word is : ", jumbledWord, "\n")

while True:
    answer = input("Type your answer (Click on enter to quit) : ")
    if answer == "":
        print("Quiting")
        break

    if answer != chosenWord:
        print("Incorrect answer. Try again!\n")
        counter += 1

    if answer == chosenWord:
        if counter == 0:
            print("You guessed it right on the first try!\n")
            break
        else:
            print("You guessed it right! Took you", counter + 1, "tries.\n")
            break

"""
Part 2 – Encrypt / Decrypt
"""
print("Encrypt / Decrypt")

my_alphas = string.ascii_lowercase
alphabet = list(my_alphas)

plainText = input("Enter the text to be encrypted: ").lower()
shiftValue = int(input("Enter a number to shift by (0-25): "))
encryptText = ""

print("\nEncrypting message.....")

for letter in plainText:
    # print(letter)
    if letter in alphabet:
        pos = alphabet.index(letter) + shiftValue
        pos = pos % len(alphabet)
        encryptText += alphabet[pos]
    else:
        encryptText += letter

print("Encrypted message : ", encryptText)

decryptText = ""

print("\nDecrypting message.....")

for letter in encryptText:

    if letter in alphabet:
        pos = alphabet.index(letter) - shiftValue
        pos = pos % len(alphabet)
        decryptText += alphabet[pos]
    else:
        decryptText += letter

print("Decrypted message : ", decryptText)
