from dash.dependencies import Input, Output, State
from components import functions
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import app

import pandas as pd
import json

comparison = pd.read_csv('data/processed/comparison.csv', index_col=0)
filt = (comparison['complete']>0) | (comparison['Approved']>0) | (comparison['Billed']>0)
comparison_clean = comparison.loc[filt, :].copy()

products = pd.read_csv('data/processed/products.csv', index_col=0)
# filt = products['Product Status'].isnull()
products_clean = products

focal_areas = {
    'Direct Field Support - Mission Support Through TA & Buy-Ins': '1A. DFS - Mission Support',
    'Direct Field Support - Regional Technical Coordination and Forecasting': '1B. DF - Regional Coordination & Forecasting',
    'Cross-Mission Learning Groups (XMLGs)': '2. Cross-Mission Learning',
    'Evidence Use and Generation': '3. Evidence Use & Generation',
    'Business Processes (WG2) and Integration (WG3)': '4. Business Processes & Integration',
    'Capacity Development and Adult Learning': '5. Capacity Development & Adult Learning',
    'MI2 Learning and Adapting and KM': '6. MI2 Learning, Adapting & KM',
    'Project-Wide Management': '7. Project Management'
    }

comparison_clean['Focal Area'] = comparison_clean['Focal Area'].replace(focal_areas)
products_clean['Focal Area'] = products_clean['Focal Area'].replace(focal_areas)

buy_ins = [
    'BI-LAC',
    'BI-MAD',
    'BI-COL',
    'BI-SAR',
    'BI-PERU',
    'BI-MEX',
    'BI-NEPAL',
    'BI-CDP'
    ]



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
    if clickData is None:
        fig = functions.update_chart(
                comparison_clean, 
                'Project'
                )
    
    else:
        click = clickData['points'][0]['y']
        if click == 'Project':
            fig = functions.update_chart(
                comparison_clean, 
                'Funding Source'
                )
            fig.update_layout(
                title=dict(text=click)
            )
        elif click == 'FAB':
            fig = functions.update_chart(
                comparison_clean,
                'Focal Area'
                )
            fig.update_layout(
                title=dict(text=click)
            )
        elif click == 'Buy-In':
            fig = functions.update_chart(
                comparison_clean,
                'Buy-In'
            )
            fig.update_layout(
                title=dict(text=click)
            )
        elif click in list(focal_areas.values()) + buy_ins:
            fig = functions.update_chart(
                comparison_clean, 
                'Product', 
                [click]                
            )
            fig.update_layout(
                title=dict(text=click)
            )
        else:
            fig = functions.update_chart(
                comparison_clean,
                'Funding Source'
            )            
            fig.update_layout(
                title=dict(text='Funding Source')
            )
            
    return fig
            
# reset chart
@app.callback(
    Output('complete-fa', 'clickData'),
    [Input('clear-clickData', 'n_clicks')]
)
def clear_clickData(n_clicks):
    if n_clicks:
        return None
    
# pie chart
@app.callback(
    Output('budget-pie', 'figure'),
    [Input('complete-fa', 'clickData'),
     Input('approved-v-billed', 'value'),
     Input('org-v-source', 'value')]
)
def populate_pie(clickData, approved_billed,
                 org_source):
    if 'Billed' in approved_billed:
        value_col = 'Billed'
    else:
        value_col = 'Approved'
        
    if 'Funding Source' in org_source:
        group = 'Funding Source'
    else:
        group = 'Organization'
        
    if clickData is None:
        fig = functions.update_pie(
            comparison_clean,
            group,
            value_col
        )
    else:
        click = clickData['points'][0]['y']
        if click == 'Project':
            fig = functions.update_pie(
                comparison_clean,
                group,
                value_col
            )
        if click in ['FAB', 'Buy-In']:
            fig = functions.update_pie(
                comparison_clean,
                group,
                value_col,
                'Funding Source',
                [click]
            )
            fig.update_layout(
                title=dict(text=value_col + ' Funding by ' + group +
                           f'<br><i>{click}</i>')
            )
        elif click in list(focal_areas.values()) + buy_ins:
            fig = functions.update_pie(
                comparison_clean,
                group,
                value_col,
                'Focal Area',
                [click]
            )
            fig.update_layout(
                title=dict(text=value_col + 
                           ' Funding by ' + 
                           group +
                           f'<br><i>{click}</i>')
            )
        else:
            fig = functions.update_pie(
                comparison_clean,
                group,
                value_col
            )       
            
    return fig

# product status bar chart
@app.callback(
    Output('product-status', 'figure'),
    [Input('complete-fa', 'clickData')]
)
def populate_product_status(clickData):
    if clickData is None:
        fig = functions.product_status_chart(
            products_clean
            )
    else:
        click = clickData['points'][0]['y']
        if click == 'Project':
            fig = functions.product_status_chart(
                products_clean
            )
        elif click in ['FAB', 'Buy-In']:
            fig = functions.product_status_chart(
                products_clean,
                'Funding Source',
                [click]
            )
            fig.update_layout(
                title=dict(text="Number of Products by Status"+
                           f'<br><i>{click}</i>')
            )
        elif click in list(focal_areas.values()) + buy_ins:
            fig = functions.product_status_chart(
                products_clean,
                'Focal Area',
                [click]
            )
            fig.update_layout(
                title=dict(text="Number of Products by Status"+
                           f'<br><i>{click}</i>')
            )
        else:
            fig = functions.product_status_chart(
            products_clean
            )
        
    return fig

@app.callback(
    Output("instructions", "is_open"),
    [Input("instructions-toggle", "n_clicks")],
    [State("instructions", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('product-table', 'children'),
    [Input('complete-fa', 'clickData')]
)
def add_product_table(clickData):
    if clickData is None:
        return None
    else:
        click = clickData['points'][0]['y']
        if click == 'Project':
            raise PreventUpdate
            # table = functions.generate_product_table(
            #     products_clean
            # )
        elif click in ['FAB', 'Buy-In']:
            raise PreventUpdate
            # table = functions.generate_product_table(
            #     products_clean,
            #     'Funding Source',
            #     [click]
            # )
        elif click in list(focal_areas.values()) + buy_ins:
            table = functions.generate_product_table(
                products_clean,
                'Focal Area',
                [click]
            )
        else:
            table = functions.generate_product_table(
            products_clean
            )
        
    product_table = dbc.Table.from_dataframe(table,
                                             striped=True,
                                             bordered=False,
                                             hover=True,
                                             responsive=True)
    
    return product_table


# # Open Instructions
# @app.callback(
#     Output("instructions", "is_open"),
#     [Input("instructions-toggle", "n_clicks")],
# )
# def open_toast(n):
#     if n:
#         return True
#     return False