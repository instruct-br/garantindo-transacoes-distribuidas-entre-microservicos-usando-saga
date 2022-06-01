import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from common import (
    BancoDeDadosDeMentira,
    ManipuladorDeConteudoDeMentira,
    VerificadorDeAssentoDeMentira,
)


class Handler(BaseHTTPRequestHandler):
    assentos = []

    def envia_de_volta(self, resposta):
        self.wfile.write(bytes(json.dumps(resposta), "utf-8"))

    def do_POST(self):
        if self.path == "/assentos/cancela":
            manipulador = ManipuladorDeConteudoDeMentira(self)
            referencia_da_passagem = manipulador.pega_conteudo()

            banco = BancoDeDadosDeMentira(self)
            referencia_do_assento = banco.marca_como_cancelado(referencia_da_passagem)

            self.envia_de_volta(referencia_do_assento)

        if self.path == "/assentos":
            banco = BancoDeDadosDeMentira(self)

            manipulador = ManipuladorDeConteudoDeMentira(self)
            conteudo = manipulador.pega_conteudo()

            verificador = VerificadorDeAssentoDeMentira()
            existe_assento_disponivel = verificador.verifica(conteudo)

            if existe_assento_disponivel:
                """fluxo normal
                cria um assento reservado e retorna uma referencia dele.
                """
                referencia_do_assento = banco.marca_como_reservado(conteudo)
                self.envia_de_volta(referencia_do_assento)
            else:
                """fluxo de compensacao
                cria um assento cancelado e retorna uma referencia dele.
                """
                referencia_do_assento = banco.marca_como_cancelado(conteudo)
                self.envia_de_volta(referencia_do_assento)


if __name__ == "__main__":
    with HTTPServer(("0.0.0.0", 8002), Handler) as server:
        print("Servico de assentos rodando na porta 8002")
        server.serve_forever()
