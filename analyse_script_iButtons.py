# Python version of analyse Script of Chris Janssen
# By Rosalie Lucas on 21-04-2021

# Import necessary libraries
import os
import pandas as pd

directory = '/Users/roos/Data/iButton'  # set Path
data = os.listdir(directory)
data.remove('.DS_Store')

data_frame = {'pp': 0, 'relativeTimeInSeconds': 0, 'B_4B0000004516B141': 0,
              'B_9A00000045146841': 0, 'B_76000000452C9741': 0,
              'B_7200000045201D41': 0, 'B_CB000000452D7441': 0,
              'B_F9000000452CCF41': 0, 'B_FF00000045298741': 0}
data_table = pd.DataFrame(columns=['pp', 'relativeTimeInSeconds', 'B_4B0000004516B141',
                                   'B_9A00000045146841', 'B_76000000452C9741',
                                   'B_7200000045201D41', 'B_CB000000452D7441',
                                   'B_F9000000452CCF41', 'B_FF00000045298741'])

for folder in range(len(data)):
    location = directory + '/' + data[folder]
    participant = data[folder]
    print(f"now processing directory {location}")

    all_files = os.listdir(location)
    print(all_files)

    location_meta_data_rows = pd.DataFrame()

    But_4B0000004516B141 = pd.DataFrame()
    But_9A00000045146841 = pd.DataFrame()
    But_76000000452C9741 = pd.DataFrame()
    But_7200000045201D41 = pd.DataFrame()
    But_CB000000452D7441 = pd.DataFrame()
    But_F9000000452CCF41 = pd.DataFrame()
    But_FF00000045298741 = pd.DataFrame()

    for file in all_files:
        specific_location = f'{location}/{file}'
        location_file = pd.read_csv(specific_location, sep=",", header=0, skiprows=18)
        firstlines = pd.read_csv(specific_location, sep=",", header=None, error_bad_lines=False,
                                 warn_bad_lines=False)[0:20]
       # print(firstlines)
        nr_sample_lines = firstlines.iloc[10]  # Start counting from 0
        nr_samples_1 = nr_sample_lines.tail().str.split("\t")[0][0]
        nr_samples = nr_samples_1.split(" ")[4]

        start_moment_lines = firstlines.iloc[9]
        start_moment_1 = start_moment_lines.str.split("\t")[0][0]
        start_moment = ''.join(start_moment_1.split(" ")[4:10])

        sample_rate_line = firstlines.iloc[5]
        sample_rate_1 = sample_rate_line.str.split("\t")[0][0]
        sample_rate = sample_rate_1.split(" ")[4]

        button_name_line = firstlines.iloc[1]
        button_number_1 = button_name_line.tail().str.split("\t")[0][0]
        button_number = button_number_1.split(" ")[3]

        times = pd.DataFrame(OriginalTime = location_file$Date.Time)
