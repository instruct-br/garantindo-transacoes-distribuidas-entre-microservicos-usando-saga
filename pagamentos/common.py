import json
import random
import time
from http import HTTPStatus
from http.client import HTTPConnection
from io import BytesIO


class ManipuladorDeConteudoDeMentira:
    def __init__(self, handler):
        handler.send_response(HTTPStatus.OK)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        self.handler = handler

    def pega_conteudo(self) -> dict:
        ##################################################
        # Processamento pesado de mentira
        # para tratar o conteudo do request
        ##################################################
        print("Iniciando processamento da requisicao.")
        print()
        time.sleep(2)
        # cria um stream de bytes vazio
        response = BytesIO()

        # pega o conteudo da requisicao
        content_length = int(self.handler.headers["Content-Length"])

        # escreve o conteudo no stream de bytes
        response.write(self.handler.rfile.read(content_length))

        print("Processamento finalizado.")
        print()
        time.sleep(2)
        # converte para dicionario
        return json.loads(response.getvalue())

    def pega_referencia_da_passagem(self, pagamento):
        return {
            "id_da_passagem": pagamento["id_da_passagem"],
            "status_da_passagem": pagamento["status_da_passagem"],
        }


class VerificadorDePagamentoDeMentira:
    def verifica_pagamento(self, pagamento):
        return pagamento["pagamento"]["valor"] == "3.75"


class BancoDeDadosDeMentira:
    def __init__(self, handler):
        self.handler = handler

    def salva(self, pagamento):
        self.handler.pagamentos.append(pagamento)
        return {
            "id_do_pagamento": pagamento["id"],
            "status_do_pagamento": pagamento["status"],
        }


class SolicitadorDePassagemDeMentira:
    def __init__(self, handler):
        self.handler = handler

    def solicita_o_cancelamento_da_passagem_com(self, referencia_da_passagem):
        connection = HTTPConnection("localhost", 8001)
        headers = {"Content-Type": "application/json"}
        data = json.dumps(referencia_da_passagem)
        connection.request("POST", "/passagens/cancela", data, headers)
        response = connection.getresponse()
        return json.loads(response.read().decode())


class GeradorDePagamentoDeMentira:
    def gera_pagamento_valido(self, pagamento):
        print("Iniciando o fluxo de resposta Normal")
        print()
        time.sleep(2)

        ids = [str(random.randint(1, 99)) for _ in range(2)]
        id_do_pagamento = "".join(ids)

        numeros = [str(random.randint(1, 9)) for _ in range(5)]
        numero_do_pagamento = "".join(numeros)

        return {
            "id": id_do_pagamento,
            "numero": numero_do_pagamento,
            "valor": pagamento["pagamento"]["valor"],
            "status": "pago",
            "id_da_passagem": pagamento["id_da_passagem"],
        }

    def gera_pagamento_invalido(self, pagamento):
        print("Iniciando o fluxo de resposta Normal")
        print()
        time.sleep(2)

        return {
            "id": "0",
            "numero": "0",
            "valor": pagamento["pagamento"]["valor"],
            "status": "cancelado",
            "id_da_passagem": pagamento["id_da_passagem"],
        }
