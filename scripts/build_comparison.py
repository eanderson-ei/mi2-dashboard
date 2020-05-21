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
xtracker = pd.read_csv('data/raw/xtracker.csv')

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
cross_mission_products.rename({'Workstream ': 'Workstream',
                               'Status': 'Product Status'}, axis=1, inplace=True)
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

# union all to flat file
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

# join xtracker to flat file on 'product' name
products_x = pd.merge(flat_file_products, xtracker, 
                      left_on='xbva', right_on='MI2-Wide Tracker', 
                      how='left')

# join xtracker to flat file on foca area
products_x = pd.merge(products_x, xtracker[['MI2-Wide Tracker', 'MI2 BVA']], 
                      left_on='Focal Area', right_on='MI2-Wide Tracker', 
                      how='left', suffixes=(None, '_x'))
products_x.drop('Focal Area', axis=1, inplace=True)
products_x.rename({'MI2 BVA_x': 'Focal Area'}, axis=1, inplace = True)

# Remove Focal Area prefix
products_x['Focal Area'] = products_x['Focal Area']\
    .str.replace('Focal Area: ', '')

products_x.to_csv('data/processed/products.csv')

# calculate average completeness by mi2 bva product
bva_completeness = products_x[['MI2 BVA', 'complete']]\
    .groupby(['MI2 BVA']).mean()
bva_completeness.reset_index(inplace=True)

# calculate approved and expended
approved = bva_approved.groupby(
    ['Focal Area', 'Project', 'Organization']
    ).sum()[['Approved']]

expended = bva_revenue.groupby(
    ['Focal Area', 'Project', 'Organization']
    ).sum()[['Billed']]

budget = pd.merge(approved, expended, left_index=True, right_index=True, how='outer')
budget.reset_index(inplace=True)

# add TDY
approved_tdy = tdy_approved.groupby(['Focal Area', 'TDY']).sum()[['Approved']]
expended_tdy = tdy_revenue.groupby(['Focal Area', 'TDY']).sum()[['Billed']]
tdy_merge = pd.merge(approved_tdy, expended_tdy, left_index=True, right_index=True)
tdy_merge.reset_index(inplace=True)
tdy_merge.rename({'TDY': 'Project'}, axis=1, inplace=True)

budget = pd.concat([budget, tdy_merge], axis=0, sort=False)
budget.sort_values('Focal Area', inplace=True)

# compare completeness
bva_completeness = bva_completeness.loc[bva_completeness['complete']>0, :]
comparison = pd.merge(budget, bva_completeness, left_on='Project', right_on='MI2 BVA', how='left')
comparison.drop('MI2 BVA', axis=1, inplace=True)
comparison.sort_values('Focal Area', inplace=True)

# assign funding source
filt = comparison['Focal Area'].str.startswith('Focal Area')
comparison.loc[filt, 'Funding Source'] = 'FAB'
comparison.loc[~filt, 'Funding Source'] = 'Buy-In'

# Remove Focal Area prefix
comparison.loc[filt, 'Focal Area'] = comparison.loc[filt, 'Focal Area']\
    .str.replace('Focal Area: ', '')

# save output
comparison.to_csv('data/processed/comparison.csv')
