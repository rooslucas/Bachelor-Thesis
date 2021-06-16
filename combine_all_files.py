# Written by Rosalie Lucas
# Last update 14/06/2021

# Script to combine all trials from all participants
import pandas as pd
import os
import glob

# Define the folder with all the files you want to combine
directory = '/Users/roos/Data/final_trials_CTET'

# Define the files and paths
all_files = glob.glob(os.path.join(directory, "*.csv"))

# Read all the files
df_all_files = (pd.read_csv(f, sep=',') for f in all_files)
# Concatenate all the files
combined_files = pd.concat(df_all_files, ignore_index=True)
# Safe them in a new file
combined_files.to_csv(r'/Users/roos/Data/all_trials_CTET2.csv', index=False, header=True)
# Safe file without NaN values
combined_files.dropna(inplace=True)
combined_files.to_csv(r'/Users/roos/Data/all_trials_noNaN_CTET2.csv', index=False, header=True)
