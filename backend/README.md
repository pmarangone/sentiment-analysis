# Análise de Sentimento - API

## Requisitos
Antes de iniciar, certifique-se de ter instalado:
- [Docker](https://docs.docker.com/get-docker/)

Verifique se os serviços do PostgreSQL, RabbitMQ e Consumidor estão rodando.

## Configuração e Execução

### 1. Clonar o Repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>/backend
```

### 2. Construir a Imagem Docker
```sh
docker build -t sentiment-analysis-backend .
```

### 3. Executar o Contêiner
```sh
docker run --rm --name sentiment-analysis-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://user:password@postgres:5432/database \
  -e RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672 \
  -e POOL_SIZE=3 \
  sentiment-analysis-backend
```

### 4. Parar o Contêiner
O contêiner será removido automaticamente ao ser parado. Para interrompê-lo manualmente:
```sh
docker stop sentiment-analysis-backend
```

## Acessando a API
A API estará disponível em:
```
http://localhost:8000
```


## Documentação
FastAPI oferece Swagger no endpoint: http://127.0.0.1:8000/docs

Caso prefira utilizar Postman, o arquivo está na raiz do projeto.

## Testes


### Configure o ambiente localmente
O projeto utiliza UV como gerenciador de bibliotecas. https://docs.astral.sh/uv/getting-started/installation/

### 1. Instale as dependências
```sh
uv sync --frozen --no-cache
```

### 2. Executar testes
```sh
pytest tests/
```