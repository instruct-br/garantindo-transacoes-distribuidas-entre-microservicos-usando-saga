from common import (
    abertura,
    escolhe_um_destino,
    pega_referencia_da_passagem,
    solicita_pagamento,
    solicita_reserva_de_passagem_para,
)


def main():
    while True:
        destino = escolhe_um_destino()
        passagem_reservada = solicita_reserva_de_passagem_para(destino)
        referencia_da_passagem = pega_referencia_da_passagem(passagem_reservada)
        solicita_pagamento(referencia_da_passagem)


if __name__ == "__main__":
    abertura()
    main()
