# Script to combine all trials from all participants
import pandas as pd
import os
import glob
import statistics

directory = '/Users/roos/Data/final_trials'

# Define the files and paths
all_files = glob.glob(os.path.join(directory, "*.csv"))
# stats = pd.DataFrame()
# stats['PPID'] = ''
# index = 0
# for file in all_files:
#     fil = pd.read_csv(file)
#     stats.at[index, 'PPID'] = file
#     print(file)
#     features = ['FLIR_forehead', 'FLIR_nose', 'CB000000452D7441', '4B0000004516B141', '7200000045201D41', '76000000452C9741', 'F9000000452CCF41', '9A00000045146841']
#     for col in features:
#         if col in fil.columns:
#             #print(col)
#             # append row to the dataframe
#             #print(statistics.stdev(fil[col]))
#             stdev = statistics.stdev(fil[col])
#             stats.at[index, col] = stdev
#     print(stats.iloc[index])
#     index += 1
#
# print(stats)
# stats.to_csv(r'/Users/roos/Data/stats.csv', index=False, header=True)

# Read all the files
df_all_files = (pd.read_csv(f, sep=',') for f in all_files)
# Concatenate all the files
combined_files = pd.concat(df_all_files, ignore_index=True)
# Safe them in a new file
combined_files.to_csv(r'/Users/roos/Data/all_trials2.csv', index=False, header=True)
# Safe file without NaN values
combined_files.dropna(inplace=True)
combined_files.to_csv(r'/Users/roos/Data/all_trials_noNaN2.csv', index=False, header=True)
