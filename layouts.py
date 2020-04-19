import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
layout1 = html.Div([
    navbar,
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(html.Div(), width=1),
                dbc.Col(html.Div([
                    html.H3('App 2'),
                    dcc.Dropdown(
                        id='app-2-dropdown',
                        options=[
                            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                                'NYC', 'MTL', 'LA'
                            ]
                        ]
                    ),
                    html.Div(id='app-2-display-value')
                    ])),
                dbc.Col(html.Div(), width=1),
            ]
        )
    )
])

# Life of Project Layout
layout2 = html.Div([
    navbar,
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value')
])