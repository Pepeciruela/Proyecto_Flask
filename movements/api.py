from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_KEY = '8c547a52-a34e-4549-9dd2-90fe0266d0af'
criptomonedas = ('BTC','ETH','XRP','LTC','BCH','BNB','USTD','EOS','BSV','XLM','ADA','TRX')

for moneda in criptomonedas:
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '8c547a52-a34e-4549-9dd2-90fe0266d0af',}
  parameters = {
    'symbol': moneda,}
  
  session = Session()
  session.headers.update(headers)
  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
