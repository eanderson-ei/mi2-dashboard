import pandas as pd
import numpy as np
import os

CSV_PATH = os.path.join('data', 'raw', 'field-support-tracker.csv')

# Read in data (copy/paste from MI2 Wide Tracker Field Support
# tab into a csv)
field_raw = pd.read_csv('data/raw/field-support-tracker.csv',
                        header=None, skiprows=0)

#eliminate white space and move worskstream 1.1 to column a
field_raw.iloc[3,0] = field_raw.iloc[3,1].strip()

# Merge multi-level column names to one list
columns = []
for row1, row2 in zip(field_raw.iloc[0,:].tolist(), field_raw.iloc[1,:].tolist()):
    if row2 is np.nan:
        columns.append(row1)
    else:
        columns.append(row2)

columns[6] = 'POC: FAB'
columns[7] = 'POC: Mission'
columns[8] = 'POC: MI'

# Update column names
field_raw.columns = columns

# Drop header rows 
field_raw.drop([0,1,2], axis=0, inplace=True)
field_raw.reset_index(inplace=True, drop=True)

# Save workstream as column
workstreams = [w for w in field_raw.iloc[:,0] 
               if str(w).startswith('WORKSTREAM')]

workstream_starts = (field_raw.index[field_raw.iloc[:,0]
                     .isin(workstreams)]
                     .tolist())

# Function for filling down using list of values and indices in specified column
def fill_column(df, values, indices, column):
    """fills the provided values from the first index to the next index in 
    the provided column in the provided dataframe"""
    
    for i in range(len(values)):
        value = values[i]
        start = indices[i]
        
        # don't index past end of list
        if i == len(indices) - 1:
            end = None
        else:
            end = indices[i+1]
        
        # start from the beginning
        if i == 0:
            start = 0
            
        df.loc[start:end, column] = value
        
# Fill down workstream names
fill_column(field_raw, workstreams, workstream_starts, 'Workstream')
field_raw.drop(workstream_starts, inplace=True)
field_raw.reset_index(inplace=True, drop=True)

# Save as csv
field_raw.to_csv('data/processed/field-support-units.csv')