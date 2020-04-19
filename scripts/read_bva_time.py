"""
bva_loe_raw is transformed to bva_loe by filling all merged rows
and renaming columns, and updating 6/1/YYYY - 6/22/YYYY to datetime objects. 
bva_loe is split into bva_staff, bva_tdy, and focal_area_to_project
bva_staff, bva_tdy are each split to revenues by period (*_revenue) and 
budget approved (*_approved)

NOTE changes to column order or number of columns in BVA will break script,
column names can be changed but dates must remain parsable to datetimes.
"""

import pandas as pd
import numpy as np
from datetime import datetime as dt
import os

# Planning year is used to indicate which year budgets are approved
PLANNING_YEAR = 2020
WORKBOOK_NAME = '1.2020 - MI2 BVA.xlsx'

# Read in bva from latest Excel sheet
file_name = os.path.join('data', 'external', WORKBOOK_NAME)
bva_loe_raw = pd.read_excel(file_name, 
                                'Time - Actuals', 
                                header=None, 
                                skiprows=6,
                                usecols='B:BH')

# Save original column names
original_cols = bva_loe_raw.iloc[0,:].copy()

# Save the first column to a list for future processing
column_a = bva_loe_raw.iloc[:,0].tolist()

# Update column names for succinctness
original_cols[0:7] = ['Staff', 
                      'Functional_Labor', 
                      'GSA_Labor', 
                      'Approved', 
                      'Remaining',
                      'This Period', 
                      'Spent to Date']

# Update column names of dataframe
bva_loe_raw.columns = original_cols

# Update 6/1/YYYY in each column to 6/1/YYYY and parse to datetime
mapper = {'6/1/2020 - 6/22/2020': dt.strptime('6/1/2020', '%m/%d/%Y'),
         '6/1/2021 - 6/22/2021': dt.strptime('6/1/2021', '%m/%d/%Y'),
         '6/1/2022 - 6/22/2022': dt.strptime('6/1/2022', '%m/%d/%Y'),
         '6/1/2023 - 6/22/2023': dt.strptime('6/1/2023', '%m/%d/%Y')}
bva_loe_raw.rename(mapper=mapper, axis=1, inplace=True)

# Extract focal area names from column a
focal_areas = [i for i in column_a if (str(i).startswith('Focal Area') 
                                       or str(i).startswith('BI'))]

# Extract project names from column a
projects = [i for i in column_a if str(i).startswith('MI2')]

# Identify indices where focal area names are located
focal_area_starts = (bva_loe_raw.index[bva_loe_raw.iloc[:,0]
                     .isin(focal_areas)]
                     .tolist())

# Identify indices where project names are located
project_starts = (bva_loe_raw.index[bva_loe_raw.iloc[:,0]
                  .isin(projects)]
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


# Fill down focal area names
fill_column(bva_loe_raw, focal_areas, focal_area_starts, 'Focal Area')

# Fill down project names
fill_column(bva_loe_raw, projects, project_starts, 'Project')

# Delete header rows
bva_loe_raw.drop([0,1,2], axis=0, inplace=True)

# Reorder columns
cols_ordered = (bva_loe_raw.columns[-2:]
                .append(bva_loe_raw.columns[:-2]))

bva_loe = bva_loe_raw[cols_ordered].copy()

### bva_staff
# Get list of staff from first project
staff = column_a[3:77]

# Filter bva_loe for staff only
filt = bva_loe.loc[:, 'Staff'].isin(staff)
bva_staff = bva_loe[filt].copy()
bva_staff.reset_index(inplace=True, drop=True)

# Convert data to numeric
numeric_cols = bva_staff.columns[6:]
for col in numeric_cols:
    bva_staff.loc[:, col] = bva_staff.loc[:, col].apply(
        pd.to_numeric, errors='raise')

# Split staff approved and add year
bva_staff_approved = bva_staff.drop(bva_staff.columns[6:], axis=1, inplace=False)
filt = bva_staff_approved.loc[:, 'Approved']>0
bva_staff_approved = bva_staff_approved[filt].copy()
bva_staff_approved.reset_index(inplace=True, drop=True)
bva_staff_approved['Year'] = pd.Series([PLANNING_YEAR]*len(bva_staff_approved.index))

# Save bva_staff_approved
bva_staff_approved.to_csv('data/processed/bva-staff-approved-loe.csv')

# Split staff revenues
bva_staff_loe_long = bva_staff.drop(['Functional_Labor', 
                                     'GSA_Labor', 'Approved', 'Remaining', 
                                     'This Period', 'Spent to Date'], 
                                     axis=1, inplace=False)

bva_staff_loe = pd.melt(bva_staff_loe_long, 
                            id_vars=['Focal Area', 'Project', 'Staff'],
                            var_name='Period Start', value_name='Billed')

filt = bva_staff_loe['Billed']>0
bva_staff_loe = bva_staff_loe[filt].copy()
bva_staff_loe.reset_index(inplace=True, drop=True)

# Save bva_staff_loe
bva_staff_loe.to_csv('data/processed/bva-staff-loe.csv')
