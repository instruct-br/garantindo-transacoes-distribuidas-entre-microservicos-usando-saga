FROM python:3.10-alpine AS base

ENV PYTHONUNBUFERRED 1

ENV USER_ID=65535
ENV USER_NAME=leaf

ENV GROUP_ID=65535
ENV GROUP_NAME=leaf

ENV HOME /home/leaf

RUN addgroup \
  -g ${USER_ID} ${GROUP_NAME} && \
  adduser \
  --shell /sbin/nologin \
  --disabled-password \
  --uid ${USER_ID} \
  --ingroup ${GROUP_NAME} ${USER_NAME}

USER ${USER_NAME}
WORKDIR ${HOME}

FROM base AS passagens
COPY ./reserva-de-passagem passagens/
EXPOSE 8001
CMD [ "python", "passagens/main.py" ]

FROM base AS assentos
COPY ./reserva-de-assento assentos/
EXPOSE 8002
CMD [ "python", "assentos/main.py" ]

FROM base AS pagamentos
COPY ./pagamentos pagamentos/
EXPOSE 8003
CMD [ "python", "pagamentos/main.py" ]
