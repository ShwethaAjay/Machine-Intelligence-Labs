"""
Shwetha Ajay
IDSN 542, Fall 2024
shwethaa@usc.edu
Lab 3
"""

# List of science fiction curse words to censor
forbiddenWords = ["fren", "frak", "drel", "grob", "glud", "zarf", "nar"]

while True:
    # Ask user for a dialogue to be censored
    text = input("Enter the dialogue to be censored : ")

    # Quit the program IF user enters nothing
    if text == "":
        print("Quiting!")
        break

    # Split the input text into a list of words
    else:
        wordList = text.split(" ")
        # print(textList)

        censoredText = []
        for word in wordList:
            # print(word)
            if word.lower() in forbiddenWords:
                censoredText.append("BEEP")
            else:
                censoredText.append(word)

        print(" ".join(censoredText),'\n')
        