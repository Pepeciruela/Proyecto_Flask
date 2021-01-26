import requests
import json

def consulta_api(url):
  respuesta = requests.get(url)
  if respuesta.status_code == 200:
    datos = respuesta.json()
    return datos
  else: 
    print ('Error', respuesta.status)
    
    