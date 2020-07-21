import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from components import functions
import pandas as pd

from app import app 

# Nav Bar
LOGO = app.get_asset_url('ei-logo-white.png')

# nav item links
nav_items = dbc.Container([
    dbc.NavItem(dbc.NavLink('Annual Work Plan', href='/apps/app1')),
    dbc.NavItem(dbc.NavLink('Life of Project', href='/apps/app2'))
]
)

# navbar with logo
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("MI2 Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_items], className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5"
)

# landing page jumbotron
jumbotron = dbc.Jumbotron(
    [
        html.H1("MI2 Dashboard", className="display-3"),
        html.P(
            """The MI2 Dashboard displays progress vs budget information
            for the Measuring Impact II project.""",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            """Content is under development."""
        ),
        html.P(dbc.Button("Learn more", color="primary", 
                          href='https://enviroincentives.com/projects/usaid-measuring-impact-ii/'),
                className="lead"),
    ]
)

# Main Layout
layout_main = html.Div([
    navbar,
    jumbotron
])

# Annual Work Plan Layout

# Card that holds the budget vs. actual chart and reset button
vs_chart_card = dbc.Card(
    dcc.Loading(
        dbc.CardBody(
            [
                dbc.Button("Reset", id='clear-clickData',
                            color='secondary', 
                            outline=True, size='sm'),
                dcc.Graph(id='complete-fa',
                            config={'displayModeBar': False}
                            ),
                html.Img(src=app.get_asset_url('progress-legend.png'), 
                         height="40px",
                         className='mx-auto d-block')
            ]
        )
    )
)

# Switches for funding source pie chart
inline_switches = dbc.Row(
    [
        dbc.Col(dbc.Row(
            [
                dbc.Label('Approved',
                        style={'font-family': 'Gill Sans MT, Arial',
                        'color': '#5f5f5f',
                        'margin-right': '.5em',
                        'margin-left': '.5em'}),
                dbc.Checklist(
                    options=[
                        {"label": "Billed", "value": 'Billed'},
                    ],
                    value=[],
                    id="approved-v-billed",
                    switch=True,
                    style={'font-family': 'Gill Sans MT, Arial',
                        'color': '#5f5f5f'}
                )
            ]),
        width=6),
        
        dbc.Col(dbc.Row(
            [
                dbc.Label('Org',
                        style={'font-family': 'Gill Sans MT, Arial',
                        'color': '#5f5f5f',
                        'margin-right': '.5em',
                        'margin-left': '2em'}),
                dbc.Checklist(
                    options=[
                        {"label": "Source", "value": 'Funding Source'},
                    ],
                    value=[],
                    id="org-v-source",
                    switch=True,
                    style={'font-family': 'Gill Sans MT, Arial',
                        'color': '#5f5f5f'}
                )
            ]),
        width=6)
    ]
)

# Card that illustrates funding source
card_1 = dbc.Card(
    [
    dbc.CardHeader(inline_switches),
    dcc.Loading(
        dbc.CardBody([
            dcc.Graph(id='budget-pie',
                    config={'displayModeBar': False}
            )]
        )
    )
    ]
)

# Card that illustrates proportion within each status
card_2 = dbc.Card(
    dcc.Loading(
        dbc.CardBody(
            dcc.Graph(id='product-status',
                      config={'displayModeBar': False})
            )
        )
    )

# Card that holds the choropleth map of status by geography
card_3 = dbc.Card(dbc.CardBody('C'))

# Card deck that contains the above three cards
card_deck = dbc.CardDeck(
    [
        card_1,
        card_2
    ]
)

# Instructions text
instructions = html.Div([
    html.P(
        'Click through the horizontal bar chart to "drill down" into '
        'each category. Categories include Project, Funding Source, '
        'FAB or Buy-In, and Workstream. All charts automatically update '
        'to match the selected category. "Reset" the chart to go back to '
        'Project level.'
    , style={
        'font-family': 'Gill Sans MT, Arial',
        'color': '#5f5f5f'
        }
    )
])

# Instructions toast
instructions_toast = html.Div(
    [
        dbc.Button(
            "Instructions",
            id='instructions-toggle',
            color='primary',
            size='sm'
        ),
        dbc.Toast(
            html.P(instructions),
            id='instructions',
            header='Instructions',
            dismissable=True,
            is_open=False,
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 850}
        )
    ]
)

# Instructions toast
instructions_pop = html.Div(
    [
        dbc.Button(
            "Instructions",
            id='instructions-toggle',
            color='primary',
            size='sm'
        ),
        dbc.Popover(
            [
                dbc.PopoverHeader('Instructions'),
                dbc.PopoverBody(instructions)
            ],
            id='instructions',
            is_open=False,
            # top: 66 positions the toast below the navbar
            target='instructions-toggle',
            placement='bottom'
        )
    ]
)


# LAYOUT 1
layout1 = html.Div([
    navbar,
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col(html.H5('FY20 Annual Work Plan Dashboard (Updated with May 2020 Actuals)', 
                                            style={'font-family': 'Gill Sans MT, Arial',
                                                   'color': '#5f5f5f'}), 
                                    width=10),
                            dbc.Col(instructions_pop, width=2)]),
                        html.Br(),
                        vs_chart_card,
                        html.Br(),
                        card_deck,
                        html.Br(),
                        dbc.Container(id='product-table')
                    ])
            ]
        )
    )
])





# Life of Project Layout
layout2 = layout_main