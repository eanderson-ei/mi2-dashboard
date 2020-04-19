import pandas as pd
import numpy as np
import os

CSV_PATH = os.path.join('data', 'raw', 'cross-mission-tracker.csv')

# Read in data (copy/paste from MI2 Wide Tracker FAB Workstream
# tab into a csv)
cml_raw = pd.read_csv(CSV_PATH, header=None, skiprows=0)

# Merge multi-level column names to one list
columns = []
for row1, row2 in zip(cml_raw.iloc[0,:].tolist(), cml_raw.iloc[1,:].tolist()):
    if row2 is np.nan:
        columns.append(row1)
    else:
        columns.append(row2)

# Merge sub-subheaders into columns
subheaders = cml_raw.iloc[2].to_list()
for idx, item in enumerate(subheaders):
    if not item is np.nan:
        columns[idx] = item

# Update column names
cml_raw.columns = columns

# Drop header rows up to 2.1 Conservation Enterprises...
cml_raw.drop([0,1,2], axis=0, inplace=True)

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
columns_to_fill = cml_raw.columns[:3].tolist()
cml_filled = fill_down(cml_raw, columns_to_fill)
cml_filled.reset_index(inplace=True, drop=True)

# Drop rows where product id is null (blue rows in tracker)
filt = cml_filled['Product #'].notnull()
cml_filled = cml_filled.loc[filt, :].copy()

cml_filled.to_csv('data/processed/cross-mission-products.csv')

