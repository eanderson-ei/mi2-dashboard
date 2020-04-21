# README

This library supports the MI2 Completion vs. Expended dashboard. Currently the library supports the Annual Work Plan view, but eventually will support the entire life of project.

To run, use `python index.py`. Also available at [mi2-dashboard.herokuapp.com](https://mi2-dashboard.herokuapp.com/).

## Contents

**app.py**: barebones Dash app with authentication

**index.py**: 'home' page of the app that handles page navigation

**layouts.py**: includes all layouts and bootstrap components

**callbacks.py**: includes all callbacks except for a few in index.py to handle the page navigation

**test.db**: an empty database with schema developed for the annual work plan data. Eventually may be populated with data for the dashboard and/or expanded to include LOP-wide schema. *During development, some foreign keys may have been removed, so before populating review the schema to make sure all foreign keys are present. Because product and task names are not unique, primary keys and foreign keys are necessary. Include cross-walk tables for MI2 tracker to BVA comparison*

**assets/**

* this folder is automatically detected by Dash (as named) and includes a favicon and logo image files

**data/**

* **external/**

  * **1.2020 - MI2 BVA.xlsx**: the January 2020 version of the BVA (BVA's are duplicated for each month). *Use caution if reading in a different month's version in case of unexpected changes.*
  * **related-products.md**: contains links to the BVA and the MI2 wide tracker

* **interim**/

  * disregard contents

* **processed**/

  * includes all normalized datasets from the BVA and MI2-wide tracker. Committed to GitHub so that raw versions can be used as input for web-based dashboard as interim solution (may not need to though). Eventually, up-to-date data will need to be piped in from ERP and MI2-wide tracker or MI2 Database.

* **raw/**

  *To avoid interacting with google sheets for now, data are copy/pasted as values into csv's. No other modification is done before reading in.*

  * **buy-in-tracker.csv**: all data from the *Buy In Task Level* tab of the MI2 wide tracker, pasted as values into a csv.
  * **cross-mission-tracker.csv**: all data from the *Cross-Mission Learning Groups* tab of the MI2 wide tracker, pasted as values into a csv.
  * **field-support-tracker.csv**: all data from the *Field Support* tab of the MI2-wide tracker, pasted as values into a csv.
  * **workstream-tracker.csv**: all data from the *FAB Workstream Level* tracker tab of the MI2 wide tracker, pasted as values into a csv.

**docs/**

* includes an ERD and a link to the Product Definition

**notebooks/**

* exploratory notebooks for data processing. All `read-*` notebooks are replicated as scripts in `scripts/`.
* exploratory notebooks for charts with plotly.

**scripts/**

* contains all scripts for reading in data. Data are saved to `data/processed/`.

**sql/**

* contains sql files for creating the database. The database was developed primarily for data modelling purposes, and is on hold. Data will be read in directly from csvs stored on GitHub (see *Design*).

## Design

### Inputs

**data/raw/**

* contents of this folder are derived from the MI2-wide tracker and read in by corresponding script in `scripts/` to `data/processed/`.

**data/external/**

* **1.20202 - MI2 BVA.xlsx** is read directly by scripts in `scripts/` to `data/processed/`.

### Flow

1. Process external and raw data and commit to GitHub
2. Read 'raw' version of the processed data into the Dash app
3. Populate Dashboard 

### Outputs

- A web-based interactive dashboard to aggregate and compare data at the annual work plan level

## Tips & Notes

The BVA and MI2 Wide Tracker use different terms to describe focal areas, workstreams, operating units, etc. A cross-walk table is required for comparing % complete and budget expended, available [here](https://docs.google.com/spreadsheets/d/1N4h3qbjXgVawH_ZGa2762aYnvT2NRSiIJFtgwUCuomI/edit?usp=sharing). Further, the BVA and MI2 wide tracker combine data at different scales (e.g., a product in the BVA represents two workstreams in the MI2 wide tracker).

---

Points of contact can reference either workstream_products or op_units. Because it's not possible to create a foreign key that references two tables, a new column is created for each foreign key needed. Alternatively, no foreign key can be established. Use a column 'reference text' to refer to the appropriate table, and 'reference id' to refer to the foreign key id of that table (either product id or op unit id).

---

Building the database in SQLite Studio was a good way of developing the SQL code and correcting errors as they happened.

---

Using [Bootstrap](https://dash-bootstrap-components.opensource.faculty.ai/) components for better look and feel. There are multiple [themes](https://www.bootstrapcdn.com/bootswatch/) available for free (and some paid). I picked [FLATLY](https://bootswatch.com/flatly/) for this project.

---

Concat **workstream products** (na for Mission lead), **cross mission products** (make LAC Lead : Mission Lead), **field support units** (name in mi2-wide tracker is operating unit, MI Lead is POC: MI, FAB Lead is POC: FAB, LAC lead is POC: Mission; note completeness is empty, add Focal Area = 1. DIRECT FIELD SUPPORT), **buy in products**. Join with BVA using xtracker as dict (1:M relationship, check uniqueness of product as key, confirm len of products is same before and after)

The key to bva is workstream products: Workstream or Product #, cross mission learning: Workstream (but all caps), field support: 'MI2_Tracker_ID', buy_in: Task for some (e.g., Columbia, but that columns has N/As).

---

Average all completeness along xbva attribute (xbva, % complete)

Join MI2 BVA column

Average again (bad) across al MI2 BVA columns

## Next Steps

- [x] develop database schema
- [x] create ERD and send to Elma w/ narrative
- [x] explore visuals as specified in the PD with plotly (using csv's)
- [ ] send Elma/Shelly a flat file with Annual work plan data needs
- [ ] schedule call with Elma/Shelly
- [ ] develop Annual Work Plan visuals and other dashboard components in notebooks 
- [ ] Lay out dashboard design in Dash and convert notebook plots with widgets.
- [ ] Deploy to Heroku

## TODO

- [ ] create virtual environment

## Future Directions

- [ ] Specify the report needed from the ERP to replace the BVA and connect the ERP to the Dashboard to auto update.

# Notes for EI-Dev

### Starting a Dash project

How to start a Dash project

```bash
conda create --new <project name>
conda activate <project name>
pip install dash==1.11.0  # use most recent version from Users Guide
pip install dash-auth==1.3.2  # for basic login protection
pip install requests  # this is not included in the docs, not sure why it isn't installed as a dependency, but it cleared things up
pip install dash-bootstrap-components  # if using Bootstrap
```

I use pip for installing packages rather than conda because Heroku uses pip and I find it leads to fewer errors.

### Structure

I'm building this [multi-page app](https://dash.plotly.com/urls) with insights provided by David Comfort in his [medium post](https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f). The structure used by David Comfort  is:

```
- __init__.py  # not sure this is needed, I left it out
- app.py
- assets
    |-- logo.jpeg
    |-- custom.css
    |-- favicon.ico
- callbacks.py
- components
    |-- __init__.py
    |-- functions.py
    |-- header.py
    |-- printButton.py
- data
    |-- datafile.csv
- index.py
- layouts.py
- Procfile
- requirements.txt
```

The **app.py** file simply initiates the app and handles authorization. Note that with a multipage app, **app.py** is not longer the primary file called to run the app, **index.py** is.

```python
import dash
import dash_bootstrap_components as dbc
import dash_auth
import json
import os

external_stylesheets = [dbc.themes.FLATLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.config.suppress_callback_exceptions = True

# Keep this out of source code repository - save in a file or a database
# Local dev
try:
    with open('secrets/passwords.json') as f:
        VALID_USERNAME_PASSWORD_PAIRS = json.load(f)
# Heroku dev
except:
    json_creds = os.environ.get("VALID_USERNAME_PASSWORD_PAIRS")
    VALID_USERNAME_PASSWORD_PAIRS = json.loads(json_creds)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
```

I'm using [dash bootstrap components](https://dash-bootstrap-components.opensource.faculty.ai/) for this project, so need to include a bootstrap css as the external stylesheets. I picked [FLATLY](https://bootswatch.com/flatly/) for this project.

For authentication, save a `.json` file in `secrets/` with the following code (INCLUDE THIS FILE IN YOUR GITIGNORE. Note I also include a .keep file in there so people who clone the repo know where that should be.) You can include as many username, password pairs as you want, separated by a comma.

```json
{
    'username':'password'
}
```

When deploying to Heroku, go to the Config Vars option under 'Settings' and paste the content of the json file there. The `KEY` will be `VALID_USERNAME_PASSWORD_PAIRS` and the `VALUE` will be the contents of the json file.

The try/except block allows the same code to work in both environments. Note you could save the passwords within a system environment variable locally, but I find that messy.

The **index.py** looks like this:

```python
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app
from layouts import layout1, layout2
import callbacks

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>MI2 Dashboard</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
         return layout1
    elif pathname == '/apps/app2':
         return layout2
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
```

The `app.index_string` variable allows us to change the name in the internet browser tab to 'MI2 Dashboard' by specifying the <title> tag.

Store a logo, favicon, and custom css or javascript in a folder `./assets/` and they will automatically be discovered by Dash. Save the external stylesheet as your css if you want to edit or amend it. See [docs](https://dash.plotly.com/external-resources) for more. Note that David Comfort found the css files unavailable on Heroku when using`dash_auth` and so saved them to codepen.io. Using, bootstrap, I had no issues.

I wasn't sure how the index.py file resolved the landing page, so I amended the callback to be:

```python
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout_main
    elif pathname == '/apps/app1':
         return layout1
    elif pathname == '/apps/app2':
         return layout2
    else:
        return '404'
```

Note I also imported layout_main from `layouts`.

### Handling data

David Comfort was able to keep data directly in his data directory when deploying to Heroku. I'll give that a shot also.

### Deploying to Heroku

I deployed as soon as the structure was built to make it easier to debug the deployment. Here are the steps:

* Make sure app.py includes (after defining variable app)

  ```python
  server = app.server
  ```

* Create Procfile with contents. We're running from index, rather than app.

  ```
  web: gunicorn index:server
  ```

  Note no space after `index:`

* Install gunicorn if not already installed

  ```bash
  pip install gunicorn
  ```

  Create requirements.txt

  * `pip freeze>requirements.txt`
  * You can also list the key dependencies in a text file called requirements.txt. Should set up a pip or conda environment though.

* Create a heroku project

* ```bash
  heroku create <app name>
  ```

* Use Heroku to deploy

  ```bash
  git add .
  git commit -m "<message>"
  git push origin master
  heroku create <app name>
  git push heroku master
  heroku ps:scale web=1
  ```



### Ideas

* Define a Header() function that returns front matter for each layout so you don't have to repeat it. Include logos, etc.