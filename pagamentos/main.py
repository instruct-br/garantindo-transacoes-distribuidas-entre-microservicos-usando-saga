import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from common import (
    BancoDeDadosDeMentira,
    GeradorDePagamentoDeMentira,
    ManipuladorDeConteudoDeMentira,
    SolicitadorDePassagemDeMentira,
    VerificadorDePagamentoDeMentira,
)


class Handler(BaseHTTPRequestHandler):
    pagamentos = []

    def envia_de_volta(self, resposta):
        self.wfile.write(bytes(json.dumps(resposta), "utf-8"))

    def do_POST(self):
        if self.path == "/pagamentos":
            gerador = GeradorDePagamentoDeMentira()
            banco = BancoDeDadosDeMentira(self)

            manipulador = ManipuladorDeConteudoDeMentira(self)
            conteudo = manipulador.pega_conteudo()

            verificador = VerificadorDePagamentoDeMentira()
            pagamento_esta_valido = verificador.verifica_pagamento(conteudo)

            if pagamento_esta_valido:
                """fluxo normal
                cria um pagamento pago e retorna uma referencia dele.
                """
                pagamento_valido = gerador.gera_pagamento_valido(conteudo)
                referencia_do_pagamento = banco.salva(pagamento_valido)
                self.envia_de_volta(referencia_do_pagamento)
            else:
                """fluxo de compensacao
                solicita cancelamento da passagem, cria um pagament cancelado
                e retorna uma referencia dele.
                """
                referencia_da_passagem = manipulador.pega_referencia_da_passagem(
                    conteudo
                )
                solicitador = SolicitadorDePassagemDeMentira(self)
                referencia_da_passagem = (
                    solicitador.solicita_o_cancelamento_da_passagem_com(
                        referencia_da_passagem
                    )
                )
                pagamento_invalido = gerador.gera_pagamento_invalido(conteudo)
                referencia_do_pagamento = banco.salva(pagamento_invalido)
                self.envia_de_volta(referencia_do_pagamento)


if __name__ == "__main__":
    with HTTPServer(("", 8003), Handler) as server:
        print("Servico de pagamentos rodando na porta 8003")
        server.serve_forever()
