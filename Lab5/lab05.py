import csv


def loadCSVFile(filename, fileData):
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            # Load rows into the dictionary with subreddit as the key
            for row in reader:
                subreddit = row['Subreddit']
                if subreddit not in fileData:
                    fileData[subreddit] = []
                fileData[subreddit].append(row["TotalPosts"])
            # print(fileData)
        return True

    except FileNotFoundError:
        return False


def main():
    fileData = {}
    while True:
        fileName = input("Enter the CSV file name (or press enter to quit): ")
        if fileName == '':
            print("Exiting.....")
            break
        if loadCSVFile(fileName, fileData):
            print("\nLoading file data.....")
            break
        else:
            print(f"\nError: '{fileName}' not found. Please try again.")

    if fileData:
        while True:
            subredditName = input("\nEnter a subreddit to display (or press enter to quit): ")
            if subredditName == '':
                print("Exiting.....")
                break
            elif subredditName in fileData:
                # Display data for the entered subreddit
                print(f"\nDisplaying data for subreddit '{subredditName}':")
                print(subredditName, "-->",fileData[subredditName][0])
            else:
                print(f"'{subredditName}' is an unknown subreddit. Please try again.")


main()

