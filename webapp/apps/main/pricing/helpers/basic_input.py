import datetime


def call_basic_security_input(number_stocks=1):

    ticker_names = []

    for i in range(number_stocks):
        ticker_name = input(f"Enter ticker {i+1} name: ")
        ticker_names.append(ticker_name.upper())
        print('-----')

    start_date = input("Enter start date in this format yyyy-mm-dd: ")
    end_date = input("Enter end date in this format yyyy-mm-dd: ")

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")


    return ticker_names, start_date, end_date
