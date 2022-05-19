import json
import random
import time
from http import HTTPStatus
from http.client import HTTPConnection
from io import BytesIO


class ManipuladorDeConteudo:
    def __init__(self, handler):
        # define o cabecalho da requisicao
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

    def monta_resposta(self, referencia_da_passagem, referencia_do_assento):
        return {**referencia_da_passagem, **referencia_do_assento}


class BancoDeDadosDeMentira:
    def __init__(self, handler):
        self.handler = handler

    def marca_como_cancelada(self, conteudo):
        ##################################################
        # Processamento pesado de mentira
        # para cancelar uma passagem
        ##################################################
        print("Iniciando cancelamento da passagem")
        print()
        print(conteudo)
        print()
        time.sleep(2)

        # pega a passagem que sera cancelada
        passagem_para_deletar = {}
        for passagem in self.handler.passagens:
            if passagem["passagem"]["id"] == conteudo["id_da_passagem"]:
                passagem["passagem"]["status"] = "cancelada"
                passagem_para_deletar = passagem

        print("Finalizando o cancelamento da passagem")
        print()
        print(passagem_para_deletar)
        print()
        time.sleep(2)

        return {
            "id_da_passagem": passagem_para_deletar["passagem"]["id"],
            "status_da_passagem": passagem_para_deletar["passagem"]["status"],
        }

    def marca_com_pendente(self, conteudo):
        ids = [str(random.randint(1, 99)) for _ in range(2)]
        id_da_passagem = "".join(ids)

        numeros = [str(random.randint(1, 9)) for _ in range(5)]
        numero_reserva = "".join(numeros)

        passagem = {
            "passagem": {
                "id": id_da_passagem,
                "numero": numero_reserva,
                "valor": "3.75",
                "status": "pendente",
            },
            "destino": conteudo["destino"],
        }

        self.handler.passagens.append(passagem)

        return {
            "id_da_passagem": passagem["passagem"]["id"],
            "status_da_passagem": passagem["passagem"]["status"],
        }

    def marca_como_reservada(self, referencia_do_assento):
        referencia_da_passagem = {}
        for passagem in self.handler.passagens:
            if passagem["passagem"]["id"] == referencia_do_assento["id_da_passagem"]:
                passagem["passagem"]["status"] = "reservada"
                referencia_da_passagem = {
                    "id_da_passagem": passagem["passagem"]["id"],
                    "status_da_passagem": passagem["passagem"]["status"],
                }
        return referencia_da_passagem


class SolicitadorDeAssentosDeMentira:
    def __init__(self, handler):
        self.handler = handler

    def solicita_o_cancelamento_do_assento_com(self, referencia_da_passagem):
        ##################################################
        # Processamento pesado de mentira
        # para solicitar o cancelamento de um assento
        ##################################################
        print("Iniciando a solicitacao de cancelamento de um assento.")
        print()
        print(referencia_da_passagem)
        print()
        time.sleep(2)

        # cria uma conexao com localhost na porta 8002
        connection = HTTPConnection("localhost", 8002)

        # seta o cabecalho para json
        headers = {"Content-Type": "application/json"}

        # define o payload que sera enviado para cancelar o assento
        data = json.dumps(referencia_da_passagem)

        # faz uma requisicao post para /assentos/cancela
        connection.request("POST", "/assentos/cancela", data, headers)

        #
        response = connection.getresponse()
        data = json.loads(response.read().decode())

        print("Finalizando a solicitacao de cancelamento de um assento.")
        print()
        print(data)
        print()
        time.sleep(2)

        return data

    def solicita_reserva_com(self, referencia_da_passagem):
        # abre uma conexao com localhost na porta 8002
        connection = HTTPConnection("localhost", 8002)
        # seta o cabecalho para json
        headers = {"Content-Type": "application/json"}

        #
        data = json.dumps(referencia_da_passagem)

        # faz uma requisicao posta para /assentos
        connection.request("POST", "/assentos", data, headers)

        # pega a resposta da requisicao
        response = connection.getresponse()

        # converte para dicionario
        data = json.loads(response.read().decode())
        return data
