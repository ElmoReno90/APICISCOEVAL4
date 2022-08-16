import json
import requests
import admpw

sandbox_url = "https://sandboxapicdc.cisco.com"


def obtener_token(user, passwd):
    url = sandbox_url + "/api/aaaLogin.json"
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


def Check_System_State():
    cabecera = {
        "Content-Type": "application/json"
    }
    galletita = {
        "APIC-Cookie": obtener_token(admpw.user, admpw.passwd)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(sandbox_url + "/api/class/topSystem.json", headers=cabecera, cookies=galletita, verify=False)

    total_nodos = int(respuesta.json()["totalCount"])
    print("La cantidad de dispositivos es", total_nodos)

    if total_nodos == 4: # !!! Este numero puede variar, al momento del desarrollo estaban operativos 4 nodos.

        print("La red tiene operativo todos los dispositivos, no se detectan elementos adicionales")
    else:
        print("!!!POSIBLE INTRUSO!!!! Hay un dispositivo adicional en la Red - Identifique los siguientes dispositivos")

    for i in range(0, total_nodos):
        name_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["name"]
        ip_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["address"]
        mac_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["fabricMAC"]

        print("nombre", name_local + "|" + "IP", ip_local + "|" + "MAC", mac_local)
Check_System_State()
