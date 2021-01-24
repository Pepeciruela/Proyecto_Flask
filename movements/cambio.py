from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from movements.validacion import Validacion

API_KEY = '8c547a52-a34e-4549-9dd2-90fe0266d0af'
criptomonedas = ('BTC')

url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '8c547a52-a34e-4549-9dd2-90fe0266d0af',}
parameters = {
  'symbol': validacion.from_currency.data,
  'amount': validacion.from_quantity.data, 
  'convert': validacion.to_currency.data,}
  
session = Session()
session.headers.update(headers)
try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)