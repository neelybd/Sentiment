import time


def y_n_question(question):
    while True:
        # Ask question
        answer = input(question)
        answer_cleaned = answer[0].lower()
        if answer_cleaned == 'y' or answer_cleaned == 'n':
            if answer_cleaned == 'y':
                return True
            else:
                return False
        else:
            print("Invalid input, please try again.")


def list_selection(list_in, note, type_in):
    while True:
        try:
            print(note)
            for j, i in enumerate(list_in):
                print(str(j) + ": to select " + type_in + " [" + str(i) + "]")
            column = list_in[int(input("Enter Selection: "))]
        except ValueError:
            print("Input must be integer between 0 and " + str(len(list_in)))
            continue
        else:
            break
    return column

def list_selection_multiple(list_in, note, type_in):
    # Dedupe list_in
    list_in = unique(list_in)

    # Sort list_in
    list_in.sort()

    while True:
        try:
            print(note)
            for j, i in enumerate(list_in):
                print(str(j) + ": to include " + type_in + " [" + str(i) + "]")

            # Ask for index list
            list_index_string = input("Enter selections separated by spaces: ")

            # Check if input was not empty
            while not list_index_string:
                list_index_string = input("Input was blank, please select " + type_in + " to include.")
                time.sleep(3)

            # Split string based on spaces
            index_list = list_index_string.split()

            # Get names of selections
            name_list = list()
            for i in index_list:
                name_list.append(list_in[int(i)])

            break

        except:
            print("An invalid input was detected, please try again.")
            time.sleep(3)
            continue

    return name_list


def unique(items):
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep


def column_selection(headers, task):
    while True:
        try:
            print("Select column.")
            for j, i in enumerate(headers):
                print(str(j) + ": to perform " + task + " on column [" + str(i) + "]")
            column = headers[int(input("Enter Selection: "))]
        except ValueError:
            print("Input must be integer between 0 and " + str(len(headers)))
            continue
        else:
            break
    return column

def column_selection_multi(headers, task):
    while True:
        try:
            print("Select column.")
            for j, i in enumerate(headers):
                print(str(j) + ": to perform " + task + " on column [" + str(i) + "]")
            column_index_list_string = input("Enter Selections separated by spaces: ")

            # Check if input was empty
            while not column_index_list_string:
                column_index_list_string = input("Input was blank, please select columns to include.")

            # Split string based on spaces
            column_index_list = column_index_list_string.split()

            # Get column names list
            column_name_list = list()
            for i in column_index_list:
                column_name_list.append(headers[int(i)])

        except ValueError:
            print("Input must be integer between 0 and " + str(len(headers) - 1))
            continue
        else:
            break
    return column_name_list
