# Sistema di Analisi del Sentimento

Questo progetto implementa una pipeline asincrona per l'analisi del sentimento delle recensioni degli utenti, utilizzando un modello di machine learning per classificare automaticamente i feedback.

## Panoramica dell'Architettura

L'applicazione segue un modello di coda di attività asincrona per garantire un'elaborazione scalabile e disaccoppiata delle recensioni degli utenti:

- **Livello API (FastAPI)**: Gestisce gli endpoint per ricevere le recensioni e scarica l'elaborazione su una coda di attività in background.
- **Livello di Messaggistica (RabbitMQ)**: Funge da message broker tra l'API e il worker in background.
- **Livello di Elaborazione (Consumer Celery)**: Ascolta la coda dei messaggi, esegue l'analisi del sentimento ML utilizzando modelli pre-addestrati e salva il risultato nel database.
- **Livello Database (PostgreSQL)**: Memorizza i dati dell'azienda, delle recensioni e dei clienti.
- **Livello di Osservabilità**: 
    - **Prometheus/Celery Exporter**: Raccoglie metriche di sistema e delle attività.
    - **Loki**: Aggrega i log per la risoluzione dei problemi.
    - **Grafana**: Fornisce la visualizzazione di metriche e log.

## Diagramma di Sistema

```mermaid
graph LR
    User[Client] -->|POST /reviews| API[FastAPI Backend]
    API -->|Enqueue Task| MQ[RabbitMQ]
    MQ -->|Consume| Consumer[Celery Consumer]
    Consumer -->|Run Inference| ML[Sentiment Model]
    Consumer -->|Save| DB[(PostgreSQL)]
    
    subgraph Observability
        Prometheus
        Loki
        Grafana
    end
    
    API -.->|Metrics| Prometheus
    Consumer -.->|Metrics| Prometheus
    Consumer -.->|Logs| Loki
    Prometheus & Loki -->|Data| Grafana
```

## Stack Tecnologico

- **API**: FastAPI
- **Coda di Attività**: Celery, RabbitMQ
- **Database**: PostgreSQL
- **Monitoraggio**: Prometheus, Loki, Grafana

## Prerequisiti

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configurazione ed Esecuzione

1. **Clonare la repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Costruire e avviare i container**:
   ```sh
   docker compose up --build
   ```
   Questo comando inizializza l'intero stack, inclusi il backend, il consumer, il message broker, il database e lo stack di osservabilità.

3. **Verificare lo stato dei container**:
   ```sh
   docker ps
   ```

4. **Arrestare i container**:
   ```sh
   docker compose down
   ```

## Monitoraggio

Il progetto include uno stack di osservabilità accessibile tramite Grafana.

- **Grafana**: Disponibile all'indirizzo `http://localhost:3000` (credenziali predefinite).
- **Dashboard**: Le dashboard preconfigurate si trovano nella directory `/dashboards`. Puoi importarle direttamente in Grafana per visualizzare lo stato di salute del sistema, la latenza delle richieste e le metriche di elaborazione dell'analisi del sentimento.

## Come Verificare

Per verificare che il sistema funzioni correttamente:
1. Assicurarsi che tutti i container siano in esecuzione tramite `docker ps`.
2. Accedere alla documentazione dell'API all'indirizzo `http://localhost:8000/docs` e inviare una recensione di prova.
3. Controllare i log nel terminale o utilizzare Loki/Grafana per verificare che l'attività sia stata elaborata dal worker Celery.
4. Visualizzare le metriche in Grafana per vedere il throughput di elaborazione delle recensioni e l'utilizzo delle risorse di sistema.
