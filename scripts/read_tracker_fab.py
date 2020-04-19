import pandas as pd
import numpy as np
import os

CSV_PATH = os.path.join('data', 'raw', 'workstream-tracker.csv')

# Read in data (copy/paste from MI2 Wide Tracker FAB Workstream
# tab into a csv)
workstream_raw = pd.read_csv(CSV_PATH, header=None, skiprows=0)

# Merge multi-level column names to one list
columns = []
for row1, row2 in zip(workstream_raw.iloc[0,:].tolist(), workstream_raw.iloc[1,:].tolist()):
    if row2 is np.nan:
        columns.append(row1)
    else:
        columns.append(row2)

# Merge subheaders into columns
subheaders = workstream_raw.iloc[2].to_list()
for idx, item in enumerate(subheaders):
    if not item is np.nan:
        columns[idx] = item

# Update column names
workstream_raw.columns = columns

# Drop header columns up to 3. Evidence-Based Practice
workstream_raw.drop([0,1,2,3,4], axis=0, inplace=True)

# Define function to fill down merged cells
def fill_down(df, columns_to_fill):
    value_dict = dict(zip(columns_to_fill, [None]*len(columns_to_fill)))
    filled_df = pd.DataFrame(columns=df.columns)
    for _, row in df.iterrows():
        for column in columns_to_fill:        
            if row[column] is np.nan:
                row[column] = value_dict[column]
            else:
                value_dict[column] = row[column]
        filled_df = filled_df.append(row, sort=False)
    return filled_df

# Fill down Focal Area, Workstream, and What's Going on This Month?
columns_to_fill = workstream_raw.columns[:3].tolist()
workstream_filled = fill_down(workstream_raw, columns_to_fill)
workstream_filled.reset_index(inplace=True, drop=True)

# Drop rows where product id is null (in case they exist)
filt = workstream_filled['Product #'].notnull()
workstream_filled = workstream_filled.loc[filt, :].copy()

workstream_filled.to_csv('data/processed/workstream-products.csv')