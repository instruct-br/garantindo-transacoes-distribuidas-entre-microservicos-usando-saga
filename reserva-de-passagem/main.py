import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from common import (
    BancoDeDadosDeMentira,
    ManipuladorDeConteudo,
    SolicitadorDeAssentosDeMentira,
)


class Handler(BaseHTTPRequestHandler):
    """servico de reserva de passagens"""

    passagens = []

    def envia_de_volta(self, resposta):
        self.wfile.write(bytes(json.dumps(resposta), "utf-8"))

    def do_POST(self):
        if self.path == "/passagens/cancela":
            manipulador = ManipuladorDeConteudo(self)
            conteudo = manipulador.pega_conteudo()

            banco = BancoDeDadosDeMentira(self)
            referencia_da_passagem = banco.marca_como_cancelada(conteudo)

            solicitador = SolicitadorDeAssentosDeMentira(self)
            referencia_do_assento = solicitador.solicita_o_cancelamento_do_assento_com(
                referencia_da_passagem
            )

            resposta = manipulador.monta_resposta(
                referencia_da_passagem, referencia_do_assento
            )

            self.envia_de_volta(resposta)

        if self.path == "/passagens":
            manipulador = ManipuladorDeConteudo(self)
            conteudo = manipulador.pega_conteudo()
            print(conteudo)

            banco = BancoDeDadosDeMentira(self)
            referencia_da_passagem = banco.marca_com_pendente(conteudo)

            solicitador = SolicitadorDeAssentosDeMentira(self)
            referencia_do_assento = solicitador.solicita_reserva_com(
                {"destino": conteudo["destino"], **referencia_da_passagem}
            )

            if referencia_do_assento["status_do_assento"] == "reservado":
                """fluxo normal
                marca a passagem como reservada e retorna uma referencia dela.
                """
                referencia_da_passagem = banco.marca_como_reservada(
                    referencia_do_assento
                )
                self.envia_de_volta(referencia_da_passagem)
            else:
                """fluxo de compensacao
                marca a passagem como cancelada e retorna uma referencia dela.
                """
                referencia_da_passagem = banco.marca_como_cancelada(
                    referencia_do_assento
                )
                self.envia_de_volta(referencia_da_passagem)


if __name__ == "__main__":
    with HTTPServer(("0.0.0.0", 8001), Handler) as server:
        print("Servico de passagens rodando na porta 8001")
        server.serve_forever()
