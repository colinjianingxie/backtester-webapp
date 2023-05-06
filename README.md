
# Backtester Webapp

## Directory layout for project

    .
    ├── financial_instruments                 # Source files for computing Options
    |   └── OptionConstants.hpp               # Holds all of the Option Constants
    |   └── Option.(hpp/cpp)                  # Abstract Base class of all Options
    |   └── EuropeanOption.(hpp/cpp)          # European Option
    |   └── AmericanPerpetualOption.(hpp/cpp) # American Option
    |   └── OptionManager.(hpp/cpp)           # Manager for Option functionalities
    |   └── OptionFormulas.(hpp/cpp)          # Formulas for calculating theoretical values
    ├── utils                                 # Utility files for general helpers
    |   └── Print.(hpp/cpp)                   # Print helper
    ├── main.cpp                              # Main driver program for each project
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

### Author
Jianing (Colin) Xie, developed 2023
