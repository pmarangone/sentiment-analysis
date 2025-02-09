# Análise de Sentimento - Consumidor

## Requisitos
Antes de iniciar, certifique-se de ter instalado:
- [Docker](https://docs.docker.com/get-docker/)

## Configuração e Execução

### 1. Clonar o Repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>/consumer
```

### 2. Construir a Imagem Docker
```sh
docker build -t sentiment-analysis-consumer .
```

### 3. Executar o Contêiner
```sh
docker run --rm --name sentiment-analysis-consumer \
  -e DATABASE_URL=postgresql+psycopg://user:password@postgres:5432/database \
  -e RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672 \
  -e POOL_SIZE=3 \
  -e MAX_RETRIES=3 \
  sentiment-analysis-consumer
```

### 4. Parar o Contêiner
O contêiner será removido automaticamente ao ser parado. Para interrompê-lo manualmente:
```sh
docker stop sentiment-analysis-consumer
```
