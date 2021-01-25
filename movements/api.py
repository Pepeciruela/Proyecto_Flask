from requests import Request, Session
import json

API_KEY = '8c547a52-a34e-4549-9dd2-90fe0266d0af'

url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount,symbol,convert,API_KEY)
  
respuesta = requests.get(url.format(C1,C2))

if respuesta.status_code == 200:
  datos = respuesta.json()
else: 
  print ('Error', respuesta.status)
  
Q2 = Q1 * (datos['data']['quote'][C2]['price'])

return Q2
  
