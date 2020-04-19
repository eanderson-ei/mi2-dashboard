"""
bva_revenue_raw is transformed to bva_revenue by filling all merged rows
and renaming columns, and updating 6/1/YYYY - 6/22/YYYY to datetime objects. 
bva_revenue is split into bva_staff, bva_tdy, and focal_area_to_project
bva_staff, bva_tdy are each split to revenues by period (*_revenue) and 
budget approved (*_approved)

NOTE changes to column order or number of columns in BVA will break script,
column names can be changed but dates must remain parsable to datetimes.
NOTE Time - Actuals is identical except it does not include the 'Organization'
column (remove reference to column and update column filters) and has no TDY
(delete second half of the script to parse TDY)
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
bva_revenue_raw = pd.read_excel(file_name, 
                                'Revenue - Actuals', 
                                header=None, 
                                skiprows=6,
                                usecols='B:BI')

# Save original column names
original_cols = bva_revenue_raw.iloc[0,:].copy()

# Save the first column to a list for future processing
column_a = bva_revenue_raw.iloc[:,0].tolist()

# Update column names for succinctness
original_cols[0:8] = ['Staff', 
                      'Organization', 
                      'Functional_Labor', 
                      'GSA_Labor', 
                      'Approved', 
                      'Remaining',
                      'This Period', 
                      'Spent to Date']

# Update column names of dataframe
bva_revenue_raw.columns = original_cols

# Update 6/1/YYYY in each column to 6/1/YYYY and parse to datetime
mapper = {'6/1/2020 - 6/22/2020': dt.strptime('6/1/2020', '%m/%d/%Y'),
         '6/1/2021 - 6/22/2021': dt.strptime('6/1/2021', '%m/%d/%Y'),
         '6/1/2022 - 6/22/2022': dt.strptime('6/1/2022', '%m/%d/%Y'),
         '6/1/2023 - 6/22/2023': dt.strptime('6/1/2023', '%m/%d/%Y')}
bva_revenue_raw.rename(mapper=mapper, axis=1, inplace=True)

# Extract focal area names from column a
focal_areas = [i for i in column_a if (str(i).startswith('Focal Area') 
                                       or str(i).startswith('BI'))]

# Extract project names from column a
projects = [i for i in column_a if str(i).startswith('MI2')]

# Identify indices where focal area names are located
focal_area_starts = (bva_revenue_raw.index[bva_revenue_raw.iloc[:,0]
                     .isin(focal_areas)]
                     .tolist())

# Identify indices where project names are located
project_starts = (bva_revenue_raw.index[bva_revenue_raw.iloc[:,0]
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
fill_column(bva_revenue_raw, focal_areas, focal_area_starts, 'Focal Area')

# Fill down project names
fill_column(bva_revenue_raw, projects, project_starts, 'Project')

# Delete header rows
bva_revenue_raw.drop([0,1,2], axis=0, inplace=True)

# Reorder columns
cols_ordered = (bva_revenue_raw.columns[-2:]
                .append(bva_revenue_raw.columns[:-2]))

bva_revenue = bva_revenue_raw[cols_ordered].copy()

### bva_staff
# Get list of staff from first project
staff = column_a[3:77]

# Filter bva_revenue for staff only
filt = bva_revenue.loc[:, 'Staff'].isin(staff)
bva_staff = bva_revenue[filt].copy()
bva_staff.reset_index(inplace=True, drop=True)

# Convert data to numeric
numeric_cols = bva_staff.columns[6:]
for col in numeric_cols:
    bva_staff.loc[:, col] = bva_staff.loc[:, col].apply(
        pd.to_numeric, errors='raise')

# Split staff approved and add year
bva_staff_approved = bva_staff.drop(bva_staff.columns[7:], axis=1, inplace=False)
filt = bva_staff_approved.loc[:, 'Approved']>0
bva_staff_approved = bva_staff_approved[filt].copy()
bva_staff_approved.reset_index(inplace=True, drop=True)
bva_staff_approved['Year'] = pd.Series([PLANNING_YEAR]*len(bva_staff_approved.index))

# Save bva_staff_approved
bva_staff_approved.to_csv('data/processed/bva-staff-approved.csv')

# Split staff revenues
bva_staff_revenue_long = bva_staff.drop(['Organization', 'Functional_Labor', 
                                         'GSA_Labor', 'Approved', 'Remaining', 
                                         'This Period', 'Spent to Date'], 
                                        axis=1, inplace=False)

bva_staff_revenue = pd.melt(bva_staff_revenue_long, 
                            id_vars=['Focal Area', 'Project', 'Staff'],
                            var_name='Period Start', value_name='Billed')

filt = bva_staff_revenue['Billed']>0
bva_staff_revenue = bva_staff_revenue[filt].copy()
bva_staff_revenue.reset_index(inplace=True, drop=True)

# Save bva_staff_revenue
bva_staff_revenue.to_csv('data/processed/bva-staff-revenue.csv')

### bva_tdy
# Filter bva by tdy columns (note tdy is in 'Staff' column)
travel_odc_rows = ['Total ODC', 
                   'Total Travel', 
                   'Buy-in Home Office Support (10%)', 
                   'LAC Share of Field Support (27%)', 
                   'LAC Deduction: MI2 Start Up']
filt = bva_revenue.loc[:, 'Staff'].isin(travel_odc_rows)
bva_tdy = bva_revenue[filt].copy()
bva_tdy.drop(['Project', 'Organization', 'Functional_Labor', 'GSA_Labor'], 
                  inplace=True, axis=1)

# Rename 'Staff' column
bva_tdy.rename(mapper={'Staff': 'TDY'}, axis=1, inplace=True)

# Convert data to numeric
numeric_cols = bva_tdy.columns[2:]
for col in numeric_cols:
    bva_tdy.loc[:, col] = bva_tdy.loc[:, col].apply(
        pd.to_numeric, errors='raise')

# Split TDY approved and add year
bva_tdy_approved = bva_tdy.drop(bva_tdy.columns[3:], axis=1, 
                                     inplace=False)
filt = bva_tdy_approved.loc[:, 'Approved']>0
bva_tdy_approved = bva_tdy_approved[filt].copy()
bva_tdy_approved.reset_index(inplace=True, drop=True)
bva_tdy_approved['Year'] = pd.Series([PLANNING_YEAR]*len(bva_tdy_approved.index))

# Save bva_tyd_approved
bva_tdy_approved.to_csv('data/processed/bva-tdy-approved.csv')

# Split TDY revenues
bva_tdy_revenue_long = bva_tdy.drop(['Approved', 'Remaining', 
                                    'This Period', 'Spent to Date'], 
                                     axis=1, inplace=False)

bva_tdy_revenue = pd.melt(bva_tdy_revenue_long, 
                          id_vars=['Focal Area', 'TDY'],
                          var_name='Period Start', value_name='Billed')

filt = bva_tdy_revenue['Billed']>0
bva_tdy_revenue = bva_tdy_revenue[filt].copy()
bva_tdy_revenue.reset_index(inplace=True, drop=True)

# Save bva_tdy_revenue
bva_tdy_revenue.to_csv('data/processed/bva-tdy-revenue.csv')






