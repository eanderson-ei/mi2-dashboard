import pandas as pd
import numpy as np
import os

CSV_PATH = os.path.join('data', 'raw', 'buy-in-tracker.csv')

# Read in data (copy/paste from MI2 Wide Tracker FAB Workstream
# tab into a csv)
buy_in_raw = pd.read_csv(CSV_PATH, header=1)


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


### buy-ins
# Split out buy in level
filt = buy_in_raw.loc[:, 'Buy-In'].notnull()
buy_ins = buy_in_raw.loc[filt].copy()
buy_ins.drop(buy_ins.iloc[:, 7:], inplace=True, axis=1)
buy_ins.reset_index(drop=True, inplace=True)

# Save buy-in level
buy_ins.to_csv('data/processed/buy-in.csv')

# fill buy in table
buy_in_filled = fill_down(buy_in_raw, buy_in_raw.columns[:7])

### buy-in tasks
buy_in_tasks = buy_in_filled.loc[:, ['Buy-In', 'Task', 'Product Name']].copy()

# Save buy-in tasks
buy_in_tasks.to_csv('data/processed/buy-in-tasks.csv')

### buy-in products
buy_in_products_long = buy_in_filled.loc[:, 'Product Name':].copy()
buy_in_names = buy_in_filled.loc[:, 'Buy-In']
buy_in_products_long = pd.concat([buy_in_names, buy_in_products_long], axis=1)

# Filter null products
filt = buy_in_products_long['Product Name'].notnull()
buy_in_products = buy_in_products_long[filt].copy()
buy_in_products.drop('Unnamed: 10', inplace=True, axis=1)
buy_in_products.reset_index(drop=True, inplace=True)

# Save buy-in products
buy_in_products.to_csv('data/processed/buy-in-products.csv')
