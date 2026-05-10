# Análise de sentimento
Projeto que demonstra a utilização de modelos de aprendizagem na classificação de avaliação de usuários.

## Requisitos
Antes de iniciar, certifique-se de ter instalado:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Estrutura dos Contêineres
- **PostgreSQL**: Banco de dados relacional que armazena informações sobre clientes e avaliações, incluindo os resultados da análise de sentimento. Utilizado tanto pelo backend quanto pelo consumidor.
- **RabbitMQ**: Sistema de mensageria que atua como uma fila de trabalho. O backend envia tarefas de análise de sentimento para esta fila, que são então consumidas e processadas pelo serviço Consumer.
- **Consumer**: Serviço responsável por processar as mensagens da fila RabbitMQ. Ele recupera as avaliações, aplica o modelo de Machine Learning para análise de sentimento e persiste os resultados no PostgreSQL. Este serviço utiliza Celery para orquestração de tarefas assíncronas.
- **Backend**: API construída com FastAPI que serve como interface principal para o sistema. Ele recebe requisições de clientes, interage com o PostgreSQL para armazenar e recuperar dados, e envia tarefas de análise de sentimento para o RabbitMQ para processamento assíncrono.

## Arquitetura do Sistema

A arquitetura do sistema é dividida em módulos que interagem de forma assíncrona para processar e analisar avaliações de clientes.

```mermaid
graph TD
    User[Usuário] --> |Cria ou consulta avaliação| Backend[FastAPI Backend];
    Backend --> |Salva avaliação inicial| PostgreSQL[PostgreSQL Database];
    Backend --> |Envia tarefa de análise| RabbitMQ[RabbitMQ Message Broker];
    RabbitMQ --> |Consome tarefa| Consumer[Celery Consumer];
    Consumer --> |Executa análise de sentimento| MLModel[Modelo ML (Análise de Sentimento)];
    MLModel --> Consumer;
    Consumer --> |Atualiza avaliação com resultado| PostgreSQL;
    Backend --> |Consulta avaliações com sentimento| PostgreSQL;
```

**Fluxo de Dados:**
1. Um **Usuário** interage com o **Backend** (API FastAPI) para criar uma nova avaliação.
2. O **Backend** salva a avaliação inicial no **PostgreSQL** e, em seguida, envia uma tarefa de análise de sentimento para o **RabbitMQ**.
3. O **Consumer** (worker Celery) consome esta tarefa do **RabbitMQ**.
4. O **Consumer** utiliza o **Modelo ML** para realizar a análise de sentimento da avaliação.
5. Após a análise, o **Consumer** atualiza a avaliação no **PostgreSQL** com o resultado do sentimento.
6. O **Backend** pode consultar o **PostgreSQL** para exibir avaliações já classificadas com seus respectivos sentimentos.

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
Você pode acessar a documentação interativa (Swagger UI) em `http://localhost:8000/docs`.

### 5. Parar os Contêineres
Para interromper a execução dos contêineres:
```sh
docker compose down
```