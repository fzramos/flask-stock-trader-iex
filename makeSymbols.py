from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock
from finance_app import app, db
import os
from dotenv import load_dotenv
from finance_app.models import Company


"""
    This program takes the list of IEX stocks symbols and put it in our app.db
"""
# print(os.environ)
# token = os.environ.get('IEX_TOKEN')
# print(token)

# Since not finance app we cant use os.environ.get('IEX_TOKEN')
APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
print(dotenv_path)
load_dotenv(dotenv_path)
# print(os.getenv('IEX_TOKEN'))
token = os.getenv('IEX_TOKEN')


def seedSymbols():
    symbols = get_symbols(token=token)
    # print(len(symbols))
    # print(symbols[1])
    for value in symbols:
        # print(value)
        symbol = value['symbol']
        name = value['name']
        # print(symbol, ' ', name)
        # if symbol and name:
            # print('worked')
        company = Company(symbol, name)
        db.session.add(company)
        db.session.commit()

    # print(f"Symbol: {temp[0]['symbol']}, Company Name: {temp[0]['name']} ")

if __name__ == '__main__':
    seedSymbols()
# make seedSymbols function which adds symbols and company names to company tables

# a = Stock("AAPL", token=token)
# print(a.get_quote())