import numpy as np
import pandas as pd
from textblob import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from joblib import delayed, Parallel
import multiprocessing
from file_handling import *
from selection import *


def main():
    print("Program: Sentiment")
    print("Release: 1.2")
    print("Date: 2020-03-09")
    print("Author: Brian Neely")
    print()
    print()
    print("This program reads a csv file and will preform a sentiment analysis on a specified column.")
    print()
    print()

    # Hide Tkinter GUI
    Tk().withdraw()

    # Find input file
    file_in = askopenfilename(initialdir="../", title="Select file",
                              filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_in:
        input("Program Terminated. Press Enter to continue...")
        exit()

    # Set ouput file
    file_out = asksaveasfilename(initialdir=file_in, title="Select file",
                                 filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_out:
        input("Program Terminated. Press Enter to continue...")
        exit()

    # Ask for Delimination
    delimiter = input("Please input Delimiter: ")

    # Read data
    data = open_unknown_csv(file_in, delimiter)

    # Create Column Header List
    headers = list(data.columns.values)

    # Select Column for Sentiment Analysis
    column_list = column_selection_multi(headers, "sentiment analysis")

    # Create an empty output file
    open(file_out, 'a').close()

    # Loop through selected columns
    for column in column_list:
        # Remove Nan for clean subset of data
        data_no_na = data.dropna(subset=[column], inplace=False)

        # Split data for Parallel Processing
        data_split = split_data(data_no_na)

        # Create sentiment score for Data using parallel processing
        print("Sentiment score creation...")
        data_split = Parallel(n_jobs=-1)(delayed(sentiment_calculation)(i, column, par_index, len(data_split))
                                         for par_index, i in enumerate(data_split))
        print("Score Calculation Complete!")
        print()

        # Union split data frames
        data_no_na_out = pd.concat(data_split)

        # Join back to original dataset
        data = data.join(data_no_na_out[str(column) + ' - Sentiment'], how='left')

    # Write CSV
    print("Writing CSV File...")
    data.to_csv(file_out, index=False)
    print("Wrote CSV File!")
    print()

    print("Sentiment Analysis Completed on column: [" + column + "]")
    print("File written to: " + file_out)
    input("Press Enter to close...")


def sentiment_calculation(data, column, par_index, par_len):
    sentmnt = list()
    for index, i in enumerate(data[column]):
        sentmnt.append(TextBlob(i).sentiment.polarity)
    data[str(column) + ' - Sentiment'] = sentmnt
    print("Sentiment Calculation Complete on: " + str(par_index) + " out of " + str(par_len) + "!")
    return data


def split_data(data):
    # *****Split data for parallel processing*****
    print("Calculating Splits...")
    # Find number of CPUs and multiply by 16 for number of parallel threads
    num_splits = multiprocessing.cpu_count() * 16
    # Calculate the split locations
    split_locations = np.linspace(0, len(data), num_splits)
    # Rounds up the  split_locations
    split_locations = np.ceil(split_locations)
    # Convert split_locations to int for splitting data
    split_locations = split_locations.astype(int)
    # Split data for parallel processing
    data_split = np.split(data, split_locations)
    print("Splits Calculated!")
    print()
    return data_split
    # *****End Split*****


if __name__ == '__main__':
    main()