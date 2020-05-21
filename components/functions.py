import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

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

colors = {
'blue':      '#2C3E50',
'indigo':    '#6610f2',
'purple':    '#6f42c1',
'pink':      '#e83e8c',
'red':       '#E74C3C',
'orange':    '#fd7e14',
'yellow':    '#F39C12',
'green':     '#18BC9C',
'teal':      '#20c997',
'cyan':      '#3498DB',
'lightgrey': '#ced4da'
}

product_order = {
    'Scoping': 1,
    'Production': 2,
    'Review': 3,
    'Completed': 4,
    'Clearance': 5    
}


def update_chart(comparison_clean, mode, selector_list=None):
        
    color_scale = [(0.00, colors['red']),   (0.25, colors['red']),
                   (0.25, colors['yellow']), (0.475, colors['yellow']),
                   (0.475, colors['green']),  (1.00, colors['green'])]
    
    bar_width = .7          

    def get_data(group_cols):
        if group_cols:
            df = comparison_clean.groupby(group_cols)\
                .agg({'complete': 'mean', 'Approved': 'sum', 'Billed': 'sum'})
            df.reset_index(inplace=True)
        else:
            df = comparison_clean\
                .agg({'complete': 'mean', 'Approved': 'sum', 'Billed': 'sum'})
            df = pd.DataFrame(df).T
        
        df['Expended'] = (df['Billed'] / df['Approved']) * 100
        diff = (df['complete'] - df['Expended'])
        df['normal_diff'] = (diff - (-100))/((100) - (-100))

        return df


    def create_fig(rows=1, cols=1):
        """SUBPLOTS A REMNANT AND NO LONGER USED"""
        # if rows == 2:
        #     row_heights = [7/15, 8/15]  # Adjust for difference in fa vs buy ins
        # else: 
        #     row_heights = [1]
        row_heights=[1]
        fig = make_subplots(rows=rows, cols=cols,
                            shared_xaxes=True,
                            vertical_spacing = .05,
                            row_heights=row_heights)

        return fig
    
    def show_main(fig, row=1, col=1):
        fig.add_trace(go.Bar(
            x=df['Expended'],
            y=['Project'],
            orientation='h',
            width=bar_width,
            marker=dict(color=df['normal_diff'],
                       colorscale=color_scale,
                       cmin=0,
                       cmax=1),
            hovertemplate='%{x:.0f}%<extra> Expended</extra>'),
            row=row, col=col)
        
        # Add complete dots
        fig.add_trace(go.Scatter(
            x=df['complete'],
            y=['Project'],
            mode='markers',
            marker=dict(color='black', symbol='diamond'),
            hovertemplate='%{x:.0f}%<extra> Complete</extra>'),
            row=row, col=col)

        # Add borders to each bar
        for bar in np.arange(1):
            fig.add_shape(
                    # unfilled Rectangle
                        type="rect",
                        x0=0,
                        y0=bar-(bar_width/2),
                        x1=100,
                        y1=bar+(bar_width/2),
                        line=dict(
                            width=.5,
                            color="lightgrey"
                        ),
                        fillcolor='white',
                        layer='below',
            row=row, col=col)

        # update y_axes
        fig.update_yaxes(autorange='reversed',
                         automargin=True,
                         tickfont=dict(size=14))
        
        # update x_axes
        fig.update_xaxes(range=[0, 100])

        # Update chart elements
        fig.update_layout(
            title=dict(text='Expended vs. Complete'),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='closest',
            barmode='stack',
            showlegend=False
        )

        fig.update_layout(
            font=dict(
                family='Gill Sans MT, Arial',
                color="#5f5f5f"
            ))
    
        fig.update_yaxes(automargin=True)
        

    def add_traces(fig, filt, row=1, col=1):
        # update color for over-spent regardless of completion
        filt_over = df['Expended'] > 100
        df.loc[filt_over, 'normal_diff'] = 0
        
        filter_col = group_cols[0]
        # Add expended bars
        fig.add_trace(go.Bar(
            x=df.loc[filt, 'Expended'],
            y=df.loc[filt, filter_col],
            orientation='h',
            width=bar_width,
            marker=dict(color=df.loc[filt, 'normal_diff'],
                       colorscale=color_scale,
                       cmin=0,
                       cmax=1),
            hovertemplate='%{x:.0f}%<extra> Expended</extra>'),
            row=row, col=col)

        # Add complete dots
        fig.add_trace(go.Scatter(
            x=df.loc[filt, 'complete'],
            y=df.loc[filt, filter_col],
            mode='markers',
            marker=dict(color='black', symbol='diamond'),
            hovertemplate='%{x:.0f}%<extra> Complete</extra>'),
            row=row, col=col)

        # Add borders to each bar
        for bar in np.arange(len(df.loc[filt])):
            fig.add_shape(
                    # unfilled Rectangle
                        type="rect",
                        x0=0,
                        y0=bar-(bar_width/2),
                        x1=100,
                        y1=bar+(bar_width/2),
                        line=dict(
                            width=.5,
                            color="lightgrey"
                        ),
                        fillcolor='white',
                        layer='below',
            row=row, col=col)

        # update y_axes
        fig.update_yaxes(autorange='reversed',
                         tickfont=dict(size=14)
                         )
        
        # update x_axes
        fig.update_xaxes(range=[0, 100])

        # Update chart elements
        fig.update_layout(
            title=dict(text='Expended vs. Complete'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='closest',
            barmode='stack',
            showlegend=False
        )

        fig.update_layout(
            font=dict(
                family='Gill Sans MT, Arial',
                color="#5f5f5f"
            ))
        
        fig.update_yaxes(automargin=True)
    
    # Plots by mode    
    if mode == 'Project':
        group_cols = None
        df = get_data(group_cols)
        fig = create_fig(rows=1, cols=1)
        show_main(fig, row=1, col=1)
        fig.update_layout(
            height=225  #bar width of 40 plus 225 whitespace
        )
    elif mode == 'Funding Source':
        group_cols = ['Funding Source']
        df = get_data(group_cols)
        df = df[::-1]  # put FAB first
        fig = create_fig(rows=1, cols=1)
        filt = slice(None)
        add_traces(fig, filt, row=1, col=1)
        fig.update_layout(
            height=40 + 225  #bar width of 40 plus 225 whitespace
        )
    elif mode == 'Focal Area':
        group_cols = ['Focal Area']
        df = get_data(group_cols)
        df.sort_values('Focal Area', ascending=True, inplace=True)
        fig = create_fig(rows=1, cols=1)
        filt = df['Focal Area'].isin(focal_areas.values())
        # Focal Areas
        add_traces(fig, filt, row=1, col=1)
        fig.update_layout(
            height=(sum(filt)-1)*40 + 225  #bar width of 40 plus 225 whitespace
        )
        # fig.update_layout(margin=dict(l=420))  # if Focal Area names are longer than 50% of chart, they are ignored in auto margin
    elif mode == 'Buy-In':
        group_cols = ['Focal Area']
        df = get_data(group_cols)  
        fig = create_fig(rows=1, cols=1)
        filt = df['Focal Area'].isin(focal_areas.values())
        # Buy ins
        add_traces(fig, ~filt, row=1, col=1)
        fig.update_layout(
            height=(sum(filt)-1)*40 + 225  #bar width of 40 plus 225 whitespace
        )
    elif mode == 'Product':
        group_cols = ['Project', 'Focal Area']
        df = get_data(group_cols)  
        fig = create_fig(rows=1, cols=1)
        filt = df['Focal Area'].isin(selector_list)
        # Products
        add_traces(fig, filt, row=1, col=1)
        fig.update_layout(
            height=(sum(filt)-1)*40 + 225  #bar width of 40 plus 225 whitespace
        )
    else:
        return None
        
    return fig


def update_pie(comparison_clean, group, value_col, 
               selector_col= None, selector_list=None):
    if selector_col:
        filt = comparison_clean[selector_col].isin(selector_list)
        df_filt = comparison_clean.loc[filt, :]
        df = df_filt.groupby(group).sum()
    else:
        df = comparison_clean.groupby(group).sum()
    values = df.loc[df[value_col]>0, value_col]
    labels = df.index
    
    colors_series = df.index.map({
        'FAB': colors['blue'],
        'Buy-In': colors['green'],
        'Environmental Incentives': colors['green'],
        'FOS': colors['blue'],
        'ICF': colors['cyan'],
        'Consultant': colors['lightgrey']
    })
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    fig.update_traces(hoverinfo='label+percent', textinfo='value',
                      texttemplate='$%{value:,.0f}', hole=.4,
                      marker=dict(colors=colors_series),
                      textfont=dict(size=14))
    
    # Update chart elements
    fig.update_layout(
        title=dict(text=value_col + ' Funding by ' + group),  # update with subtext for sub Focal Area/Buy In level
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(size=14),
                    orientation='h'),
        margin=dict(l=20, r=20, t=50, b=120)
    )

    fig.update_layout(
        font=dict(
            family='Gill Sans MT, Arial',
            color="#5f5f5f"
        ))
    
    return fig


def product_status_chart(products_clean, selector_col=None, 
                         selector_list=None):
    
    if selector_col:
        filt = products_clean[selector_col].isin(selector_list)
        df_filt = products_clean.loc[filt, :]
        df = df_filt.groupby('Product Status').count()
    else:
        df = products_clean.groupby('Product Status').count()
    
    df['order'] = df.index.map(product_order)
    df.sort_values('order', inplace=True)
    
    fig = go.Figure()
    
    fig.add_traces(go.Bar(
        y = df['Focal Area'],
        x = df.index,
        marker=dict(color=colors['cyan'])
    ))
    
    fig.update_layout(
            title=dict(text='Number of Products by Status'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=165, b=40)
    )
    
    fig.update_layout(
        font=dict(
            family='Gill Sans MT, Arial',
            color="#5f5f5f"
        ))
    
    return fig


def generate_product_table(products_clean, selector_col=None,
                           selector_list=None):
    if selector_col:
        filt = products_clean[selector_col].isin(selector_list)
        df = products_clean.loc[filt, :]
    else:
        df = products_clean
    
    # Filter to important columns    
    columns = ['MI2_Tracker_ID', 'Product Name', 'MI Lead', 'FAB Lead', 
             'Product Status', 'Production Timeline (No. of Months)', 
             '% Completion', 'Due Date', 'Output #', 'Status', 'LAC Lead']
    
    filt = df.columns.isin(columns)
    df = df.loc[:, filt].copy()
    
    # Drop column if no data
    df.dropna(axis=1, how='all', inplace=True)
    
    # Drop row if no data
    df.dropna(axis=0, how='all', inplace=True)
    
    print(df)
    
    return df

if __name__ == '__main__':
    comparison =  pd.read_csv('data/processed/comparison.csv', index_col=0)
    filt = (comparison['complete']>0) | (comparison['Approved']>0) | (comparison['Billed']>0)
    comparison_clean = comparison.loc[filt, :].copy()
    mode = 'Product'
    selector_list = ['Cross-Mission Learning Groups (XMLGs)']
    
    # fig = update_chart(comparison_clean, mode, selector_list)
    # fig.show()
    
    # fig = update_pie(comparison_clean, 'Organization', 'Approved')
    # fig.show()
    products = pd.read_csv('data/processed/products.csv', index_col=0)
    filt = products['Product Status'].isnull()
    products_clean = products.loc[~filt, :]

    fig = product_status_chart(products_clean, 'Funding Source', ['FAB'])
    fig.show()