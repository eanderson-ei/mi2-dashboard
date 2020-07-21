# README

This library supports the MI2 Completion vs. Expended dashboard. Currently the library supports the Annual Work Plan view, but eventually will support the entire life of project.

To run, use `python index.py`. Also available at [mi2-dashboard.herokuapp.com](https://mi2-dashboard.herokuapp.com/).

## Update Procedure

DO NOT OVERWRITE XTRACKER.CSV!!!!!!!!!!!!!!!!!!!!! UPDATE LINE FOR LINE.

1. Initiate mi2-dashboard environment `conda activate mi2-dashboard`

2. Pull changes from github (`git pull`)

3. To preserve previous working versions of data, save the `data/processed` and `data/raw` folders as zip files.

4. Download most recent BVA (see `related-products.md` in `data/external` for link) and save a copy to `data/external`

5. Update `scripts/read_bva_revenue.py` and `scripts/read_bva_time.py` to point to new BVA (line 22 and 19, respectively)

6. Run (from root) the above two scripts. Note that data in `data/processed` will be overwritten. (Each new BVA includes data from all previous BVAs). Spot check any `data/processed/bva*.csv` files.

7. Navigate to MI2-Tracker and copy all data from each sheet, delete everything and then paste as text into the appropriate `CSV` in `data/raw`; run the corresponding python script and check the output in `data/processed`.

   - FAB Workstream Level : 
     - `workstream-tracker.csv` 
     - RUN `scripts/read_tracker_fab.py`; 
     - check `data/processed/workstream-products.csv`
   - Field Support by Region: 
     - `field-support-tracker.csv` 
     - RUN `scripts/read_field_support.py`; 
     - check `processed/field-support-units.csv`
   - Buy-In Task Level: 
     - `buy-in-tracker.csv` 
     - RUN `scripts/read_tracker_buy_in.py`; 
     - check `processed/buy-in*.csv`
   - Cross Mission Learning Groups:
     - `cross-mission-tracker.csv`
     - RUN `scripts/read_tracker_cml.py`
     - check `processed/cross-mission-products.csv`

8. Run `scripts/build_comparison.py` . A new `data/processed/products.csv` and `data/processed/comparison.csv` will be created.

9. Launch app and check for functionality (`python index.py`)

10. Commit changes, push to github and push to heroku

    ```bash
    git add -A
    git commit -m "<MESSAGE>"
    git push origin master
    git push heroku master
    ```

11. Done!

## Contents

**app.py**: barebones Dash app with authentication

**index.py**: 'home' page of the app that handles page navigation

**layouts.py**: includes all layouts and bootstrap components

**callbacks.py**: includes all callbacks except for a few in index.py to handle the page navigation

**test.db**: an empty database with schema developed for the annual work plan data. Eventually may be populated with data for the dashboard and/or expanded to include LOP-wide schema. *During development, some foreign keys may have been removed, so before populating review the schema to make sure all foreign keys are present. Because product and task names are not unique, primary keys and foreign keys are necessary. Include cross-walk tables for MI2 tracker to BVA comparison*

**assets/**

* this folder is automatically detected by Dash (as named) and includes a favicon and logo image files

**components/**

* **\_\_init\_\_.py**: allows importing from components
* **functions.py**: all functions, notably functions to create plots and manipulate data

**data/**

* **external/**

  * **1.2020 - MI2 BVA.xlsx**: the January 2020 version of the BVA (BVA's are duplicated for each month). *Use caution if reading in a different month's version in case of unexpected changes.*
  * **related-products.md**: contains links to the BVA and the MI2 wide tracker

* **interim**/

  * disregard contents

* **processed**/

  * includes all normalized datasets from the BVA and MI2-wide tracker. Committed to GitHub so that raw versions can be used as input for web-based dashboard as interim solution (may not need to though--heroku can access local data files). Eventually, up-to-date data will need to be piped in from ERP and MI2-wide tracker or MI2 Database.

* **raw/**

  *To avoid interacting with google sheets for now, data are copy/pasted as values into csv's. No other modification is done before reading in.* MODS REQUIRED IN CAPS, WORK WITH MARIA TO CORRECT.

  * **buy-in-tracker.csv**: all data from the *Buy In Task Level* tab of the MI2 wide tracker, pasted as values into a csv.
  * **cross-mission-tracker.csv**: all data from the *Cross-Mission Learning Groups* tab of the MI2 wide tracker, pasted as values into a csv.
  * **field-support-tracker.csv**: all data from the *Field Support* tab of the MI2-wide tracker, pasted as values into a csv. CORRECT LAST THREE ENTRIES THAT ARE INCONSISTENTLY MERGED.
  * **workstream-tracker.csv**: all data from the *FAB Workstream Level* tracker tab of the MI2 wide tracker, pasted as values into a csv. ADD 6.0.0 TO PROJECT NUMBER 6.0. DELETE \n ABOVE 5.3.3.

**docs/**

* includes an ERD and a link to the Product Definition

**notebooks/**

* exploratory notebooks for data processing. All `read-*` notebooks are replicated as scripts in `scripts/`.
* exploratory notebooks for charts with Plotly. Use Jupyter Notebook (not Lab) to view Plotly charts in browser.

**scripts/**

* contains all scripts for reading in data. Data are saved to `data/processed/`.

**sql/**

* contains sql files for creating the database. The database was developed primarily for data modelling purposes, and is on hold. Data will be read in directly from csv's stored on GitHub (see *Design*).

## Design

### Inputs

**data/raw/**

* contents of this folder are derived from the MI2-wide tracker and read in by corresponding script in `scripts/` to `data/processed/`.
* **xtracker.csv**: the cross walk between the ERP, MI2 Wide Tracker, and BVA, available [here](https://docs.google.com/spreadsheets/d/1N4h3qbjXgVawH_ZGa2762aYnvT2NRSiIJFtgwUCuomI/edit?usp=sharing).

**data/external/**

* **1.20202 - MI2 BVA.xlsx** is read directly by scripts in `scripts/` to `data/processed/`.

### Flow

The data processing will be conducted each month by me to speed dashboard load time and allow for QA checks with the MI2 Wide Tracker and BVA are still handled by Maria and Elma. A batch file will allow quick processing and testing once data are pulled down from the web. Each month, the updated data will be pushed to Heroku with any new app features.

1. Read in BVA and mi2-wide tracker data, save to disk (`read-*.py`)
2. Build comparison from saved csv files and xtracker.csv (`build_comparison.py`)
   1. For MI2 Tracker
      1. Identify and rename join column name in each mi2 tracker input
      2. Concatenate (union) all mi2 tracker inputs
      3. Convert % complete (a range rep as a string) to a numeric mid-point value
      4. Join to xtracker and calculate average completeness per BVA Product, select only positive values, and save as `bva-completeness`
      5. Group by Production Status (as count) and save as `product_status.csv`
   2. For BVA staff
      1. Group bva-staff-approved and -revenue by [Organization, Project] and sum approved, billed, respectively; merge
   3. For TDY
      1. Group bva-tdy-approved and -revenue by Project and sum approved, billed, respectively, merge
      2. Add TDY to bva staff output for each focal area, sort, save as `budget`
   4. To Join
      1. Join `bva completeness` to `budget`
   5. Returns df with [Focal Area/Buy In/TDY, Project, Organization, Completeness, Approved, Billed] as `comparison.csv`
3. Read `comparison.csv` into Dash app
4. Populate Dashboard 
   1. VS. Chart: uses `comparison.csv` to show % expended to % complete for Overall Project, by Funding Source (FAB vs. Buy In), by Focal Area or Buy In, and by Product using 'drill down' functionality (use dcc.Store as state variable to inform click?). Consider including filter for Organization to limit view to org level.
   2. Funding Pie Chart: uses `comparison.csv` to show funding by organization at corresponding level of the VS Chart (project, funding source, focal area/buy in). {Project: Overall, Funding Source: Overall, Focal Area/Buy In: corresponds to Focal_Area or Buy In, Product: corresponds to specific focal_area or buy in}
   3. Project Status: Uses `product_status.csv` to create bar chart showing proportion of products at each phase (scoping, production, etc). Filter by chart level. {}
   4. Status Map: For buy-ins and field TA, highlight countries where we work. Future: show progress status by country.

### Outputs

- A web-based interactive dashboard to aggregate and compare data at the annual work plan level

### Tests

* which mi2 tracker entries in xtracker are dupes?
* Each flat_file_products[xbva] has one  corresponding entry in the xtracker, same with budget
* Each budget['MI2']
* Confirm no N/A values in join fields from MI2 Wide Tracker
* Make sure there are no missing joins between the bva, xtracker, and mi2 wide tracker

## Tips & Notes

The BVA and MI2 Wide Tracker use different terms to describe focal areas, workstreams, operating units, etc. A cross-walk table is required for comparing % complete and budget expended, available [here](https://docs.google.com/spreadsheets/d/1N4h3qbjXgVawH_ZGa2762aYnvT2NRSiIJFtgwUCuomI/edit?usp=sharing). Further, the BVA and MI2 wide tracker combine data at different scales (e.g., a product in the BVA represents two workstreams in the MI2 wide tracker).

---

Points of contact can reference either workstream_products or op_units. Because it's not possible to create a foreign key that references two tables, a new column is created for each foreign key needed. Alternatively, no foreign key can be established. Use a column 'reference text' to refer to the appropriate table, and 'reference id' to refer to the foreign key id of that table (either product id or op unit id).

---

Building the database in SQLite Studio was a good way of developing the SQL code and correcting errors as they happened.

---

Using [Bootstrap](https://dash-bootstrap-components.opensource.faculty.ai/) components for better look and feel. There are multiple [themes](https://www.bootstrapcdn.com/bootswatch/) available for free (and some paid). I picked [FLATLY](https://bootswatch.com/flatly/) for this project.

---

Getting a flat file from workstream products, cm products, field support units, and buyins requires renaming one column in each as the 'key' and concatenating rows. I rename the columns that represent the same data but aren't named the same (e.g., Status and Product Status), but don't worry about columns in only a single table.

Here's the process:

Concat **workstream products** (na for Mission lead), **cross mission products** (make LAC Lead : Mission Lead), **field support units** (name in mi2-wide tracker is operating unit, MI Lead is POC: MI, FAB Lead is POC: FAB, LAC lead is POC: Mission; note completeness is empty, add Focal Area = 1. DIRECT FIELD SUPPORT), **buy in products**. Join with BVA using xtracker as dict (1:M relationship, check uniqueness of product as key, confirm len of products is same before and after)

The key to bva is workstream products: Workstream or Product #, cross mission learning: Workstream (but all caps), field support: 'MI2_Tracker_ID', buy_in: Task for some (e.g., Columbia, but that columns has N/As).

---

Use Cards (although any dbc component would work, even containers) to separate the content of the app layout from the layout declaration itself. This will make the code much easier to read, as you won't have as many nested statements. For example:

```python
card1 = dbc.Card(
    [
        dbc.CardHeader('Card Header'),
        dbc.CardBody(
        [
            html.H4('Card title', className='card-title'),
            dcc.Graph(id='graph'),
            dbc.CardLink(id='link-to-top', 'Go back', color='primary')
        ])
    ])

card2 = ...

cards = dbc.Row(
[dbc.Col(card1, width=4), dbc.Col(card2, width=8)]
)  # see also utility classes for responsive widths

layout1 = html.Div(
    [
        navbar,
        dbc.Container(cards)
    ]
)
```

This will allow pretty efficient moving around of components in the layout. The **Card Deck** component lays cards out in equal width and height (use for BAN boxes or similar content). **Card Columns** does the same but with unclear organization.

---

Heroku uses an ephemeral file system. This means that at least every 24 hours (or with a new deploy), all files are deleted and saved anew in a sometimes unpredictable location. So, I can't create a csv in an app, save it to data/processed, and expect it to be there when I log in again. This is why SQLite does not work in Heroku. SQLite stores data as files (much like a bunch of csvs), which will get swept away periodically. Alternatively, you can provision a PostgreSQL database that will be saved in AWS and maintained there. This is all done through Heroku, but the free tier limits to 10,000 rows. However, you can deploy with csvs in the data/processed folder and those (and their relative locations) will be known and available for the app. Of course, you can also serve through Raw Github or in Google Sheets.

---

A note on virtual environments. When [setting up a new conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#using-pip-in-an-environment), include the python argument or [it will not show up in the environment list](https://code.visualstudio.com/docs/python/environments#_conda-environments).

`conda create -n <ENV_NAME> python`

If you forget this step, install python using

`conda install -n <ENV_NAME> python`. Restart VS code and it will now be available.

Note that `-n` and `--name` [are equivalent](https://docs.conda.io/projects/conda/en/latest/commands/create.html#Named%20Arguments).

## Next Steps

- [ ] create a BAT file to read in new data before deploying

- [ ] add google analytics

  `heroku config:add GOOGLE_ANALYTICS_SITE_ID=UA-999999-99`

## TODO

- [x] left join xtracker [['Focal Area', 'MI2 BVA']] to products to rename Focal Area. Drop original focal area column and rename duplicate.
- [x] create dictionary for renaming focal areas from BVA to short name, include number for ordering.
- [x] add info badge with popup instructions in top right of dashboard
- [ ] add labels where expense is greater than 100
- [ ] add today line
- [ ] Add Last Updated text (Valid through: March 31, 2020)
- [x] source of funds pie chart
- [x] finish callbacks for proportion of projects by product status bar chart (where PreventUpdate now )
- [ ] status by country chart
- [ ] confirm MI2 FAB Training does not have any expenses. It does have completeness. Use QA to check for completeness where there is no invoice.
- [ ] review CARPE Buy In where it has completion status and it is not 

## Future Directions

- [ ] Specify the report needed from the ERP to replace the BVA and connect the ERP to the Dashboard to auto update.
- [ ] Progress over time (and projections): bva includes billed for products and tdy per period, which could be used to show billing intensity over time and even projections from historic trends
- [ ] TDY Forecasts: meet Kelsey's needs to have TDY forecasts

# Notes for EI-Dev

### Starting a Dash project

How to start a Dash project

```bash
conda create -n <ENV_NAME> python
conda activate <ENV_NAME>
conda install pandas
conda install xlrd
pip install dash==1.11.0  # use most recent version from Users Guide
pip install dash-auth==1.3.2  # for basic login protection
pip install requests  # this is not included in the docs, not sure why it isn't installed as a dependency, but it cleared things up
pip install dash-bootstrap-components  # if using Bootstrap
```

I use pip for installing packages rather than conda because Heroku uses pip and I find it leads to fewer errors when deploying. You'll probably need `pandas` and `numpy` among other libraries, but add as you need.

Note that conda [recommends](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#using-pip-in-an-environment) installing all packages with conda first (that are available through conda channels) and then switching to pip--and not switching back to conda. Once you go pip, don't go back.

VS Code may ask you to install pylint as a linter, I don't see any issue with doing this, but do it immediately so that you don't switch between pip and conda when VS Code does this for you.

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

Data are just stored and read from the 'processed' data folder, so you need to run the read_*.py files before deploying if updating data (for now). Try a data class that reads everything in, joins it, and stores it in a temp div for later access. There are also constants in the code (e.g., Focal Area names) that are just stored as code, which could be improved.

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

* Be sure to update the requirements file as you go if you add new libraries.

### Tracking with Google Analytics

To track with google analytics, set up a new web property on Google Analytics, get the code (e.g., `UA-999999-99) and simply use the command:

```bash
heroku config:add GOOGLE_ANALYTICS_SITE_ID=UA-999999-99
```

Push to heroku again.

### Ideas

* Define a Header() function that returns front matter for each layout so you don't have to repeat it. Include logos, etc.
* Use cards to contain charts for some additional styling.