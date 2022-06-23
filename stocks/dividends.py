# Ryan Grayson
# 06/17/22
# find current dividends given a list of stocks
import pandas as pd
from bs4 import BeautifulSoup as bs # used for scraping data
import requests

def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')

def get_dividend(ticker):
    try:
        url1 = 'https://finance.yahoo.com/quote/'
        soup = get_soup(url1 + ticker + '?p=' + ticker)
        table = soup.find_all('table', {'class', 'W(100%) M(0) Bdcl(c)'})[0]
        tr = table.find_all('tr')[-3]
        td = tr.find_all('td')[1].text
        div_and_yield = str(td).replace('\n', '')
        return '$' + div_and_yield.split(' ')[0], div_and_yield.split(' ')[1][1:-1]
    except:
        try:
            #if data is not found on yahoo finance, check market watch
            url2 = 'https://www.marketwatch.com/investing/stock/'
            soup = get_soup(url2 + ticker + '?mod=search_symbol')
            lst = soup.find_all('ul', {'class', 'list list--kv list--col50'})[0]
            li = lst.find_all('li')
            _yield = str(li[10].text).replace('\n', '')
            _div = str(li[11].text).replace('\n', '')
            return _div[8:], _yield[5:]
        except:
            return 'not found', 'not found'

stock_data = pd.read_csv('dividend_stocks.csv')
stock_data.drop(stock_data.columns[[2, 3]], axis=1, inplace=True)
tickers = []
for ticker in stock_data.loc[:, 'Ticker']:
    tickers.append( ticker[ticker.find(':') + 1 : -1] )

divs, yields = [], []
for ticker in tickers:
    _div, _yield = get_dividend(ticker)
    print(_div + ' | ' + _yield)

    divs.append(_div)
    yields.append(_yield)

stock_data['Annual Dividend'] = divs
stock_data['Dividend Yield'] = yields

stock_data.to_csv('Dividend_stocks_A&B_rated.csv', index=False)