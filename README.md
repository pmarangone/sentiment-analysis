# Sentiment Analysis System

This project implements an asynchronous sentiment analysis pipeline for user reviews, utilizing a machine learning model to categorize feedback automatically.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [System Diagram](#system-diagram)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Running](#setup--running)
- [Monitoring](#monitoring)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [How to Verify](#how-to-verify)

## Architecture Overview

The application follows an asynchronous task-queue pattern to ensure scalable and decoupled processing of user reviews:

- **API Layer (FastAPI)**: Serves endpoints to receive reviews and offloads processing to a background task queue.
- **Messaging Layer (RabbitMQ)**: Acts as the message broker between the API and the background worker.
- **Processing Layer (Celery Consumer)**: Listens to the message queue, performs ML sentiment analysis using pre-trained models, and persists the result to the database.
- **Database Layer (PostgreSQL)**: Stores company, review, and customer data.
- **Observability Layer**: 
    - **Prometheus/Celery Exporter**: Collects system and task metrics.
    - **Loki**: Aggregates logs for troubleshooting.
    - **Grafana**: Provides visualization of metrics and logs.

## System Diagram

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

## Tech Stack

- **API**: FastAPI
- **Task Queue**: Celery, RabbitMQ
- **Database**: PostgreSQL
- **Monitoring**: Prometheus, Loki, Grafana

## Project Structure

```text
.
├── backend/            # FastAPI API source code
├── configs/            # Application and infrastructure configurations
├── consumer/           # Celery consumer source code
├── dashboards/         # Grafana dashboard JSON files
├── docker-compose.yml  # Infrastructure definition
└── README.md           # This document
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup & Running

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and start the containers**:
   ```sh
   docker compose up --build
   ```
   This command initializes the entire stack, including the backend, consumer, message broker, database, and the observability stack.

3. **Check container status**:
   ```sh
   docker ps
   ```

4. **Stop the containers**:
   ```sh
   docker compose down
   ```

## Monitoring

The project includes an observability stack accessible via Grafana.

- **Grafana**: Available at `http://localhost:3000` (default credentials).
- **Dashboards**: Pre-configured dashboards are located in the `/dashboards` directory. Import them into Grafana to visualize system health, request latency, and sentiment analysis processing metrics.

## Configuration

Configuration files are located in the `configs/` directory. Modify these files to adjust database credentials, API settings, or infrastructure parameters.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file (if available) for more details.


## How to Verify

To verify the system is functioning correctly:
1. Ensure all containers are running via `docker ps`.
2. Access the API documentation at `http://localhost:8000/docs` and submit a test review.
3. Check the logs in the terminal or use Loki/Grafana to verify the task was processed by the Celery worker.
4. View metrics in Grafana to see the review processing throughput and system resource utilization.

Reviewer last review: 2026-09-05
