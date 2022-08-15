import json
import requests
import admpw

sandbox = "https://sandboxapicdc.cisco.com"


def obtener_token(user, passwd):
    url = sandbox + "/api/aaaLogin.json"
    body = {
        "aaaUser": {
            "attributes": {
                "name": user,
                "pwd": passwd
            }
        }
    }
    cabecera = {
        "Content-Type": "application/json"
    }
    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']
    return token


token = obtener_token(admpw.user, admpw.passwd)

# GET https://apic-ip-address/api/mo/topology/pod-1/node-1/sys/ch/bslot/board/sensor-3.json

def top_system():
    cabecera = {
        "Content-Type": "application/json"
    }
    galletita = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(sandbox + "/api/class/topSystem.json", headers=cabecera, cookies=galletita, verify=False)

    total_nodos = int(respuesta.json()["totalCount"])
    print("la cantidad de nodos es", total_nodos)
    if total_nodos == 3:
        print("La Red No tiene Intrusos")
    else:
        print("Hay un dispositivo adicional en la Red, posible Intruso")

top_system()
