import pandas as pd
import numpy as np

# read in mi2 tracker
workstream_products = pd.read_csv(
    'data/processed/workstream-products.csv', index_col=0
    )
cross_mission_products = pd.read_csv(
    'data/processed/cross-mission-products.csv', index_col=0
    )
field_support_units = pd.read_csv(
    'data/processed/field-support-units.csv', index_col=0
    )
buy_in_products = pd.read_csv(
    'data/processed/buy-in-products.csv', index_col=0
    )
buy_in_tasks = pd.read_csv(
    'data/processed/buy-in-tasks.csv', index_col=0
    )

# read in bva
bva_approved = pd.read_csv('data/processed/bva-staff-approved.csv', 
                           index_col=0)
bva_revenue = pd.read_csv('data/processed/bva-staff-revenue.csv', 
                          index_col=0)
tdy_approved = pd.read_csv('data/processed/bva-tdy-approved.csv', 
                           index_col=0)
tdy_revenue = pd.read_csv('data/processed/bva-tdy-revenue.csv', 
                          index_col=0)

# read in xtracker
xtracker = pd.read_csv('data/processed/xtracker.csv')

# update mi2 tracker - workstream products
workstream_products['Source'] = 'workstream_products'
workstream_products['unique_id'] = 'Product #'
workstream_products['xbva'] = workstream_products['Workstream']
workstream_products.rename({'Product #': 'MI2_Tracker_ID'}, 
                           axis=1, inplace=True)

# update mi2 tracker - cross mission products
cross_mission_products['Focal Area'] = '2. CROSS MISSION LEARNING GROUPS'
cross_mission_products['Source'] = 'cross_mission_products'
cross_mission_products['unique_id'] = 'Product #'
cross_mission_products['xbva'] = cross_mission_products['Workstream']

# update mi2 tracker - field support units
field_support_units['Focal Area'] = '1. DIRECT FIELD SUPPORT'
field_support_units['Source'] = 'field_support_units'
field_support_units['unique_id'] = 'Operating Unit'
field_support_units['xbva'] = field_support_units['Operating Unit']
field_support_units.rename({'Operating Unit': 'MI2_Tracker_ID',
                            'POC: FAB': 'FAB Lead', 
                            'POC: MI': 'MI Lead', 
                            'POC: Mission': 'Mission Lead',
                            'Product Status Per Mission': 'Product Status',
                            'Production Timeline (No. of Months) Per Mission': 'Production Timeline (No. of Months)',
                            '% Annual Completion': '% Completion'}, 
                           axis=1, inplace=True)


# update mi2 tracker - buy ins
buy_ins = pd.merge(buy_in_tasks, buy_in_products, 
                   on=['Buy-In', 'Product Name'], how='left')
buy_ins['Source'] = 'buy_in_products'
buy_ins['unique_id'] = 'Product Name'
buy_ins['xbva'] = buy_ins['Buy-In'] + ' ' + buy_ins['Task']
buy_ins.rename({'Buy-In': 'Focal Area',
                'Product Name': 'MI2_Tracker_ID'}, 
               inplace=True, axis=1)

flat_file_products = pd.concat([workstream_products, 
                               cross_mission_products, 
                               field_support_units, 
                               buy_ins],
                              axis=0, sort=False)

# convert completeness to numeric
complete_dict = {
    '0-24%': 12,
    '25-34%': 29.5,
    '35-79%': 57,
    '80-95%': 87.5,
    '96-99%': 97,
    '100%': 100
}

flat_file_products['complete'] = flat_file_products['% Completion'].map(complete_dict)

# item-specific remapping
product_remap = ['5.3.1.A', '5.3.1.B', '5.3.1.C', '5.3.1.D', '5.3.2.A', '5.3.3.A']
filt = flat_file_products['MI2_Tracker_ID'].isin(product_remap)
flat_file_products.loc[filt, 'xbva'] = flat_file_products.loc[filt, 'MI2_Tracker_ID']

# calculate approved and expended
approved = bva_approved.groupby('Project').sum()[['Approved']]
expended = bva_revenue.groupby('Project').sum()[['Billed']]
budget = pd.merge(approved, expended, left_index=True, right_index=True)
budget.reset_index(inplace=True)

# join xtracker to flat file
products_x = pd.merge(xtracker, flat_file_products,
                      left_on='MI2-Wide Tracker', right_on='xbva', 
                      how='outer')

products_v_budget=pd.merge(products_x, budget, right_on='Project', left_on='MI2 BVA', 
                           how='outer')

comparison = products_v_budget.groupby(['Focal Area', 'MI2 BVA']).mean()
comparison.reset_index(inplace=True)
comparison.drop('Production Timeline (No. of Months)', axis=1, inplace=True)

comparison.to_csv('data/processed/comparison.csv')
