import json
import time
from http.client import HTTPConnection


def abertura():
    print(
        """
    Servico ingenuo e extremamente limitado de reserva de passagem
        """
    )


def escolhe_um_destino():
    destino = input("Para onde voce quer ir? ").strip()
    return destino


def solicita_reserva_de_passagem_para(destino):
    connection = HTTPConnection("localhost", 8001)
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"destino": destino})
    connection.request("POST", "/passagens", data, headers)
    response = connection.getresponse()
    result = json.loads(response.read().decode())
    print()
    print(result)
    print()
    time.sleep(2)
    return result


def pega_referencia_da_passagem(passagem_reservada):
    return {
        "id_da_passagem": passagem_reservada["id_da_passagem"],
        "status_da_passagem": passagem_reservada["status_da_passagem"],
    }


def solicita_pagamento(referencia_da_passagem):
    status_da_passagem = referencia_da_passagem["status_da_passagem"]

    if status_da_passagem == "reservada":
        pagamento = input("Digite o valor do pagamento: ").strip()

        connection = HTTPConnection("localhost", 8003)
        headers = {"Content-Type": "application/json"}
        referencia_da_passagem.update(
            {
                "pagamento": {
                    "valor": pagamento,
                }
            }
        )
        data = json.dumps(referencia_da_passagem)
        connection.request("POST", "/pagamentos", data, headers)
        response = connection.getresponse()
        result = json.loads(response.read().decode())
        print()
        print(result)
        print()
        time.sleep(2)
        return result
