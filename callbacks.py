from dash.dependencies import Input, Output, State
from components import functions

from app import app

import pandas as pd
import json

comparison = pd.read_csv('data/processed/comparison.csv', index_col=0)
filt = (comparison['complete']>0) | (comparison['Approved']>0) | (comparison['Billed']>0)
comparison_clean = comparison.loc[filt, :].copy()

focal_areas = ['1. DIRECT FIELD SUPPORT', '2. CROSS MISSION LEARNING GROUPS', '3. EVIDENCE-BASED PRACTICE',
              '4. BUSINESS PROCESSES AND INTEGRATION', '5. CAPACITY DEVELOPMENT AND ADULT LEARNING', 
              '6. KNOWLEDGE MANAGEMENT, LEARNING, AND EVALUATION', '7. PROJECT MANAGEMENT']

buy_ins = [buy_in for buy_in in comparison_clean['Focal Area'].unique() if buy_in not in focal_areas]

# Nav bar 
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Completeness chart by product on click
@app.callback(
    Output('complete-fa', 'figure'),
    [Input('complete-fa', 'clickData')]
)
def click_through(clickData):
    if clickData is None or clickData['points'][0]['y'] not in focal_areas + buy_ins:
        fig = functions.update_chart(
                comparison_clean, 
                'Focal Area', 
                focal_areas
                )
    else:
        fig = functions.update_chart(
            comparison_clean, 
            'Product', 
            [clickData['points'][0]['y']])
        fig.update_layout(
            title=dict(text=clickData['points'][0]['y'])
        )
    return fig

# Completeness chart by 

@app.callback(
    Output('hover-data', 'children'),
    [Input('complete-fa', 'clickData')])
def display_hover_data(clickData):
    return json.dumps(clickData, indent=2)
