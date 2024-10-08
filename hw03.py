"""
Part 1: Months dictionary
"""
months = {'January': 31, 'February': 28, 'March': 31, 'April': 30,
          'May': 31, 'June': 30, 'July': 31, 'August': 31,
          'September': 30, 'October': 31, 'November': 30, 'December': 31}

"""
Part 2: Calendar dictionary
"""

calendar = {}
for month in months:
    emptyDayList = []
    for day in range(months[month]):
        emptyDayList.append('')

    calendar[month] = emptyDayList

# Print out the calendar dictionary to check its content
# for month, days in calendar.items():
#     print(f"{month}: {len(days)} days -> {days}")

"""
Part 3: User input
"""


# Function to ch valid input for the date
def inputDate():
    while True:
        holiday = input('\nEnter a date for a holiday (for example "July 1"): ')

        # Exit if the user just hits enter
        if holiday == '':
            return None, None

        try:
            # Split the input into month and day
            month, day = holiday.split()

            # Capitalize the month to match the keys in the dictionary
            month = month.capitalize()

            # Check if the month is valid
            if month not in months:
                print(f'I don’t know about the month "{month}"')
                continue

            # Check if the day is valid for the given month
            day = int(day)
            if day < 1 or day > months[month]:
                print(f'{month.capitalize()} has {months[month]} days!')
                continue

            return month, day

        except ValueError:
            print("I don't see good input in there!")
            continue


def addEvent(month, day):
    event = input(f'What happens on {month}, {day}? :')

    # Add the event to the calendar (adjust for 0-based indexing)
    calendar[month][day - 1] = event


"""
Part 4: Display results
"""


# Display all the dates with events
def displayEvents():
    count = 0
    print("\nEvents in the calendar:\n")
    for month, days in calendar.items():
        for i, event in enumerate(days):
            # Only display dates with events
            if event:
                count += 1
                print(f"{month} {i + 1} : {event}")
    if count == 0:
        print("Looks like no event is added to the calendar!")


def main():
    while True:
        # Get valid date input
        month, day = inputDate()

        # If the user just hits enter, exit the loop
        if month is None and day is None:
            print("Exiting the program......")
            break

        # Add event to the calendar
        addEvent(month, day)

    # Display events in calendar
    displayEvents()


main()
