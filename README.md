# Análise de sentimento
Projeto que demonstra a utilização de modelos de aprendizagem na classificação de avaliação de usuários.


## Requisitos
Antes de iniciar, certifique-se de ter instalado:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Estrutura dos Contêineres
- **PostgreSQL**: Banco de dados relacional.
- **RabbitMQ**: Sistema de mensageria.
- **Consumer**: Processa mensagens do RabbitMQ e interage com o banco de dados.
- **Backend**: API FastAPI para análise de sentimentos.

## Configuração e Execução

### 1. Clonar o Repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Construir e Iniciar os Contêineres
Execute o seguinte comando na raiz do projeto:
```sh
docker compose up --build
```
Este comando:
- Constrói as imagens do backend e do consumidor.
- Inicia os serviços PostgreSQL, RabbitMQ, consumidor e backend.

### 3. Verificar os Contêineres em Execução
Para verificar se os contêineres estão ativos:
```sh
docker ps
```

### 4. Acessar a API de Análise de Sentimentos
A API estará disponível em:
```
http://localhost:8000
```

### 5. Parar os Contêineres
Para interromper a execução dos contêineres:
```sh
docker compose down
```
