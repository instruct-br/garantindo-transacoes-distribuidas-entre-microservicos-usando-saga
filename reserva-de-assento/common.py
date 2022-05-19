import json
import random
import time
from http import HTTPStatus
from io import BytesIO


class ManipuladorDeConteudoDeMentira:
    def __init__(self, handler):
        handler.send_response(HTTPStatus.OK)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        self.handler = handler

    def pega_conteudo(self):
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


class BancoDeDadosDeMentira:
    def __init__(self, handler):
        self.handler = handler

    def marca_como_cancelado(self, conteudo):
        ##################################################
        # Processamento pesado de mentira
        # para cancelar um assento
        ##################################################
        print("Iniciando cancelamento do assento")
        print()
        time.sleep(2)

        assento_cancelado = {}
        for assento in self.handler.assentos:
            if assento["id_da_passagem"] == conteudo["id_da_passagem"]:
                assento["assento"]["numero"] = "0"
                assento["assento"]["status"] = "cancelado"
                assento_cancelado = assento

        if not assento_cancelado:
            assento_cancelado = {
                "assento": {
                    "id": "0",
                    "numero": "0",
                    "status": "cancelado",
                },
                "id_da_passagem": conteudo["id_da_passagem"],
            }

        print("Finalizando o cancelamento do assento")
        print()
        print(assento_cancelado)
        print()
        time.sleep(2)

        # retorna uma referencia do assento marcado como cancelado
        return {
            "id_do_assento": assento_cancelado["assento"]["id"],
            "status_do_assento": assento_cancelado["assento"]["status"],
            "id_da_passagem": conteudo["id_da_passagem"],
        }

    def marca_como_reservado(self, conteudo):
        # gera um id aleatorio
        id_do_assento = "".join([str(random.randint(1, 99)) for _ in range(2)])

        # gera um numero de assento aleatorio
        numero_do_assento = random.randint(1, 9)

        # monta o dicionario com as informacoes do assento
        assento = {
            "assento": {
                "id": id_do_assento,
                "numero": numero_do_assento,
                "status": "reservado",
            },
            "id_da_passagem": conteudo["id_da_passagem"],
        }

        # atualiza o body com as informacoes do assento
        self.handler.assentos.append(assento)
        return {
            "id_do_assento": assento["assento"]["id"],
            "status_do_assento": assento["assento"]["status"],
            "id_da_passagem": conteudo["id_da_passagem"],
        }


class VerificadorDeAssentoDeMentira:
    def verifica(self, conteudo):
        return False if conteudo["destino"] == "madri" else True
