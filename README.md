
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
6.

### Author
Jianing (Colin) Xie, developed 2023
