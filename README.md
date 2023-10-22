
# Backtester Webapp
This is an on-going project used to help me understand how a trading system works as well as experiment with various backtesting strategies. This code is inspired by: *Successful Algorithmic Trading* by Michael L. Halls-Moore.
## Directory layout for project

    .
    ├── webapp                      # Home folder
    |   └── apps                    # Folder for all apps
    |       └── api                 # App for all API
    |       └── dashboard           # App for user dashboard
    |       └── home                # App for landing page
    |       └── main                # App for core logic of system
    |       └── oauth               # App for user authentication
    |       └── securities_master   # App for holding all the security models
    |       └── securities_scraper  # App for running scrapy webcrawler  
    |       └── utils               # App for helper and misc functions
    |   └── core                    # Entry app
    |   └── settings                # Webapp settings folder
    |   └── static                  # Asset storage
    |   └── templates               # Template files for UI
    ├── manage.py                   # Django default driver file
    ├── requirements.txt        #    Holds all python libraries for this app
    └── README.md


## Setup
These are the setup instructions, assuming you've cloned the repo. We will create a virtual environment, install necessary packages, and link a PostgreSQL database via pgAdmin.
### Virtual Environment
Make sure you are running Python 3.10+ and have pip installed. At any point in time during the instructions, please make sure you are in this virtual environment when running the app. Otherwise, some commands will not work due to missing libraries.
1. Run the following: ```pip install virtualenv``` inside the terminal. This will enable creating virtual environments.
2. After cloning the repo, run: ```cd backtester-webapp/webapp/```
3. To create a virtual environment: ```virtualenv venv```
4. To start the virtual environment (Mac OS): ```source venv/bin/activate```. You should see something similar to: ```(venv) (base) username@sample-pc webapp``` with the (venv) at the beginning. **Note: to deactivate virtual environment, simply run: ```deactivate``` at any time.**
5. Now, install the designated libraries via: ```pip install -r requirements.txt```
### PostgreSQL
1. Install pgAdmin: https://www.pgadmin.org/download/
2. Create a master username/password
3. Under **Servers**->**PostgreSQL**, right click **Databases**->**Create**->**Database...**
4. Name the database: **securities_master**. This database will hold tables for all of the stock data, accounts, backtests, etc...
5. We will now connect the webapp to the newly created database. **Note: this next step is bad practice, but we will continue as a proof of concept.** Navigate to *webapp/settings/core.py* and under the ```DATABASES{...}``` dictionary, change the password to your master password.
### Setting up Default Data
1. Add your username/password to the superuser list inside: *webapp/apps/utils/management/commands/createaccs.py*
2. Run: ```python manage.py resetdb```. This will create migrations, migrate the schemas, create super users, and initialize the database by scraping the S&P 500 tickers off of Wikipedia and the ticker data off of Alphavantage or Yahoo Finance.

### Starting the Server
To start the server, within the virtual environment, run: ```python manage.py runserver``` and navigate to: **http://localhost:8000/home/index/**. Sign in with your admin account from the setup above.

### Basic Commands
All custom Django commands are stored in *webapp/apps/utils/management/commands/*.
* ```python manage.py create_symbol```: Allows user to create a custom Symbol in Database
* ```python manage.py createaccs```: Creates superusers
* ```python manage.py initdb```: Runs wiki scraper, vendor scraper, and default strategies.
* ```python manage.py resetdb```: Resets whole database by deleting all tables and data
* ```python manage.py scrape_vendors```: Scrapes all price data from scraped tickers
* ```python manage.py scrape_wiki```: Scrapes S&P 500 tickers from Wikipedia and stores the data

### Future Expansion
There are still many unfinished business for this project. Here's a list of high level items I plan to incorporate. The linked (private) Excel sheet: https://docs.google.com/spreadsheets/d/1lpBBQBJpJd2VFQI3NPjVIVGinpafc9Y-30MFSp9xaSk/edit?usp=sharing.
1. Forum for users
2. Polished landing page
3. Better User Authentication
4. Sophisticated Strategies
5. Parameter tuning for transactions

### Author
Jianing (Colin) Xie & Calvin Xie, developed 2023
