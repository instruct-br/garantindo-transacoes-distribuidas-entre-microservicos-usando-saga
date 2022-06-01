# Direto ao ponto

### Passo a Passo para executar os servicos
> Observacao: Os comandos abaixo devem ser executados no terminal.

1 - na raiz do projeto execute o comando:
```bash
docker-compose up --detach
```

2 - confira se os containers estao executando
```bash
docker-compose ps
```

3 - o resultado deve ser parecido com esse
```bash
NAME                COMMAND                  SERVICE             STATUS              PORTS
assentos            "python assentos/mai…"   assentos            running             8002/tcp
pagamentos          "python pagamentos/m…"   pagamentos          running             8003/tcp
passagens           "python passagens/ma…"   passagens           running             8001/tcp
```

4 - acesse o pacote formulario e digite:
```bash
docker image build -t formulario .
```

5 - execute o comando abaixo para subir o container do formulario:
```bash
docker container run --rm -it --network external formulario 
```

6 - acesse os logs dos containers, por exemplo o de passagens
```bash
docker container logs -f passagens
```

> se voce escolheu algun destino, os logs do servico de passagens de estar parecido com isso aqui
```bash

    Servico ingenuo e extremamente limitado de reserva de passagem
        
Para onde voce quer ir? casa

{'id_da_passagem': '127', 'status_da_passagem': 'reservada'}

Digite o valor do pagamento: 3.75

{'id_do_pagamento': '5822', 'status_do_pagamento': 'pago'}

```

