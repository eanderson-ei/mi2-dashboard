import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

focal_areas = ['1. DIRECT FIELD SUPPORT', '2. CROSS MISSION LEARNING GROUPS', '3. EVIDENCE-BASED PRACTICE',
              '4. BUSINESS PROCESSES AND INTEGRATION', '5. CAPACITY DEVELOPMENT AND ADULT LEARNING', 
              '6. KNOWLEDGE MANAGEMENT, LEARNING, AND EVALUATION', '7. PROJECT MANAGEMENT']

def update_chart(comparison_clean, mode, selector_list):
        
    color_scale = [(0.00, "red"),   (0.25, "red"),
                   (0.25, "yellow"), (0.5, "yellow"),
                   (0.5, "green"),  (1.00, "green")]
    
    bar_width = .7          

    def get_data(group_cols):
        billed = comparison_clean.groupby(group_cols).sum()[['Approved', 'Billed']]
        billed['Expended'] = (billed['Billed'] / billed['Approved']) * 100
        complete = comparison_clean.groupby(group_cols).mean()[['complete']]

        df = pd.merge(billed, complete, left_index=True, right_index=True)
        df.reset_index(inplace=True)
        diff = (df['complete'] - df['Expended'])
        df['normal_diff'] = (diff - (-100))/((100) - (-100))

        return df


    def create_fig(rows=1, cols=1):
        if rows == 2:
            row_heights = [7/15, 8/15]  # Adjust for difference in fa vs buy ins
        else: 
            row_heights = [1]
        fig = make_subplots(rows=rows, cols=cols,
                            shared_xaxes=True,
                            vertical_spacing = .05,
                            row_heights=row_heights)

        return fig
    

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
        for bar in np.arange(sum(filt)):
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

        # Update chart elements
        fig.update_layout(
            title=dict(text='Expended vs. Complete'),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='y',
            barmode='stack',
            showlegend=False,
            height=800,
            margin_l=400
        )

        fig.update_layout(
            font=dict(
                family='Gill Sans MT, Arial',
                color="#5f5f5f"
            ))
    
    # Focal Areas & Buy Ins
    if mode == 'Focal Area':
        group_cols = ['Focal Area']
        df = get_data(group_cols)  
        fig = create_fig(rows=2, cols=1)
        filt = df['Focal Area'].isin(focal_areas)
        # Focal Areas
        add_traces(fig, filt, row=1, col=1)
        # Buy ins
        add_traces(fig, ~filt, row=2, col=1)
    elif mode == 'Product':
        group_cols = ['MI2 BVA', 'Focal Area']
        df = get_data(group_cols)  
        fig = create_fig(rows=1, cols=1)
        filt = df['Focal Area'].isin(selector_list)
        # Products
        add_traces(fig, filt, row=1, col=1)
        fig.update_layout(
            height=(sum(filt)-1)*40 + 225  #bar width of 40 plus 225 whitespace
        )
        
    return fig