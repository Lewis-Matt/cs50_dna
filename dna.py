# dna.py
# A program that will take a sequence of DNA and a CSV file containing STR counts
# for a list of individuals and then output to whom the DNA (most likely) belongs

from csv import DictReader
from sys import argv, exit


def main():
    # Ask for command-line argument of the relevant files (2), print error
    if len(argv) < 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit()

    database = argv[1]
    sequence = argv[2]

    # Open CSV and conver to dict
    with open(database, "r") as csvfile:
        # DictReader will use header names (assumes first row is name) as keys (while reader uses index)
        reader = DictReader(csvfile)
        # Convert csv file into a dict
        dict_list = list(reader)

    # Open sequence file and convert to list
    with open(sequence, "r") as file:
        # Returns contents of file as string
        sequence = file.read()

    # Define empty array to sore max consecutive sequence of each STR
    max_counts = []

    # Loop through STRs and check them in sequence (start at 1, as column 0 is the names of the people in the db)
    # The fieldnames parameter is a sequence. If fieldnames is omitted, the values in the first row of file f will be used as the fieldnames.
    # Regardless of how the fieldnames are determined, the dictionary preserves their original ordering.
    # ex: DictReader(f, fieldnames = ( "foo","bar","foobar","barfoo" ))
    for i in range(1, len(reader.fieldnames)):
        # STR being checked is stored in a variable
        STR = reader.fieldnames[i]
        # New value is being added to the array, storing the length of the longest seq. for each STR
        max_counts.append(0)

        # Loop through the current sequence and for each character checks if STR follows
        for j in range(len(sequence)):
            STR_count = 0

            # If the STR is found, check if the STR repeats and increment count
            if sequence[j: (j + len(STR))] == STR:
                k = 0
                while sequence[(j + k): (j + k + len(STR))] == STR:
                    STR_count += 1
                    k += len(STR)

                # If the STR_count is larger than the current max_count, then the current max for that STR is overwritten
                if STR_count > max_counts[i - 1]:
                    max_counts[i - 1] = STR_count

    # There will be one dictionary for each person in the database. For each person in the database, the list of STRs is cycled
    # through and the max counts array is compared to the max STR sequences for that person.
    for i in range(len(dict_list)):
        matches = 0
        for j in range(1, len(reader.fieldnames)):
            # dict_list[i] represents a dictionary and [reader.dieldnames[j]] returns the key to be looked up in that dict
            if int(max_counts[j - 1]) == int(dict_list[i][reader.fieldnames[j]]):
                #  If there is a match, the number of matches is incremented.
                matches += 1
                # If the number of matches equals the number of STRs in the database then the sequence being checked macthes someone in the database
            if matches == (len(reader.fieldnames) - 1):
                print(dict_list[i]['name'])
                exit(0)
    print("No match")


main()

# Notes
# Python strings allow “slicing” (accessing a particular substring within a string).
# If s is a string, then s[i:j] will return a new string with just the characters of s starting from
# character i up through (but not including) character j.
