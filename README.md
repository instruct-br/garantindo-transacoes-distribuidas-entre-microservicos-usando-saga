# Direto ao ponto

### Passo a Passo para executar os servicos
### Observacao: Os comandos abaixo devem ser executados no terminal.

1 - acesse o pacote reserva-de-assento e digite:
```bash
python main.py
```
confira o resultado:
```bash
Servico de assentos rodando na porta 8002
```

2 - accesse o pacote reserva-de-passagem e digite:
```bash
python main.py
```
confira o resultado:
```bash
Servico de passagens rodando na porta 8001
```

3 - accesse o pacote formula e digite:
```bash
python main.py
```

confira o resultado:
```bash

    Servico ingenuo e extremamente limitado de reserva de passagem
    
Para onde voce quer ir?

```

# Vamos brincar

1 - escolha um destino

```bash

    Servico ingenuo e extremamente limitado de reserva de passagem
    
Para onde voce quer ir? Lisboa

```
2 - aguarde alguns instantes, depois confira o resultado dos logs em cada um dos terminais.

# Vamos conferir os logs de um fluxo normal

1 - Resultado do servico de formulario
```bash
    Servico ingenuo e extremamente limitado de reserva de passagem
    
Para onde voce quer ir? Lisboa

{'destino': 'Lisboa', 'passagem': {'numero': '16996', 'valor': '3.75', 'status': 'reservada'}, 'assento': {'numero': 5, 'status': 'reservado'}}

Para onde voce quer ir?
```

2 - Resultado do servico de reserva-de-passagem

```bash
127.0.0.1 - - [16/May/2022 11:48:49] "POST /passagens HTTP/1.1" 200 -
Um momento, estamos processando a sua requisicao.

{'passagem': {'numero': '16996', 'valor': '3.75', 'status': 'pendente'}}

Reserva de passagem pendente aguardando confirmacao de assento.

Requisitando reserva de assento

Requisicao realizado com sucesso.

Iniciando o fluxo de resposta Normal

Atualizando o status da passagem para reservada no banco de dados

{'destino': 'Lisboa', 'passagem': {'numero': '16996', 'valor': '3.75', 'status': 'reservada'}}

Status atualizado com sucesso.

Atualizando o status da passagem para reservada no response

{'destino': 'Lisboa', 'passagem': {'numero': '16996', 'valor': '3.75', 'status': 'reservada'}, 'assento': {'numero': 5, 'status': 'reservado'}}

Status atualizado com sucesso.

Finalizando o fluxo de resposta Normal

```

3 - Resultado do servico de reserva-de-assento
```bash
127.0.0.1 - - [16/May/2022 11:48:55] "POST /assentos HTTP/1.1" 200 -
Um momento, estamos processando a sua requisicao.

Iniciando fluxo de resposta normal

Atualizando o status do assento para reservado no banco de dados

{'destino': 'Lisboa', 'passagem': {'numero': '16996', 'valor': '3.75', 'status': 'pendente'}, 'assento': {'numero': 5, 'status': 'reservado'}}

Assento reservado com sucesso.

Finalizando fluxo de resposta normal
```

# Vamos conferir os logs de um fluxo onde acontece uma operacao de compensacao.

1 - Resultado do servico de formulario
```bash
    Servico ingenuo e extremamente limitado de reserva de passagem
    
Para onde voce quer ir? madri

{'destino': 'madri', 'passagem': {'numero': '37581', 'valor': '3.75', 'status': 'cancelada'}, 'assento': {'numero': 0, 'status': 'cancelado'}}

Para onde voce quer ir? 
```

2 - Resultado do servico de reserva-de-passagem
```bash
127.0.0.1 - - [16/May/2022 11:53:24] "POST /passagens HTTP/1.1" 200 -
Um momento, estamos processando a sua requisicao.

{'passagem': {'numero': '37581', 'valor': '3.75', 'status': 'pendente'}}

Reserva de passagem pendente aguardando confirmacao de assento.

Requisitando reserva de assento

Requisicao realizado com sucesso.

Inicializando o fluxo de resposta de compensacao

Atualizando o status da passagem para cancelada no banco de dados

{'destino': 'madri', 'passagem': {'numero': '37581', 'valor': '3.75', 'status': 'cancelada'}}

Status atualizado com sucesso.

Atualizando o status da passagem para cancelada no response

{'destino': 'madri', 'passagem': {'numero': '37581', 'valor': '3.75', 'status': 'cancelada'}, 'assento': {'numero': 0, 'status': 'cancelado'}}

Status atualizado com sucesso.

Finalizando o fluxo de resposta de compensacao
```

3 - Resultado do servico de reserva-de-assento
```bash
127.0.0.1 - - [16/May/2022 11:53:30] "POST /assentos HTTP/1.1" 200 -
Um momento, estamos processando a sua requisicao.

Iniciando fluxo de resposta de compensacao

Atualizando o status do assento para cancelado no banco de dados

{'destino': 'madri', 'passagem': {'numero': '37581', 'valor': '3.75', 'status': 'pendente'}, 'assento': {'numero': 0, 'status': 'cancelado'}}

Desculpa! nao foi possivel reservar um assento

Finalizando fluxo de resposta de compensacao
```