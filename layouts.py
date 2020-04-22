import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from components import functions
import pandas as pd

focal_areas = ['1. DIRECT FIELD SUPPORT', '2. CROSS MISSION LEARNING GROUPS', '3. EVIDENCE-BASED PRACTICE',
              '4. BUSINESS PROCESSES AND INTEGRATION', '5. CAPACITY DEVELOPMENT AND ADULT LEARNING', 
              '6. KNOWLEDGE MANAGEMENT, LEARNING, AND EVALUATION', '7. PROJECT MANAGEMENT']
comparison = pd.read_csv('data/processed/comparison.csv', index_col=0)
filt = (comparison['complete']>0) | (comparison['Approved']>0) | (comparison['Billed']>0)
comparison_clean = comparison.loc[filt, :].copy()

# Nav Bar
LOGO = "assets/ei-logo-white.png"

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
    className="mb-5",
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
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

layout1 = html.Div([
    navbar,
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(html.Div(), width=1),
                dbc.Col(html.Div(
                    [
                    html.H1('Annual Work Plan'),
                    dcc.Graph(id='complete-fa',
                              figure=functions.update_chart(
                                  comparison_clean, 
                                  'Focal Area', 
                                  focal_areas
                                  )
                              )
                    ])
                ),
                dbc.Col(html.Div(), width=1)
            ]
        )
    )
])

# Life of Project Layout
layout2 = html.Div([
    navbar,
    jumbotron
])