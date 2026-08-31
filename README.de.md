# Sentiment-Analyse-System
Dieses Projekt implementiert eine asynchrone Sentiment-Analyse-Pipeline für Benutzerbewertungen und nutzt ein Machine-Learning-Modell, um Feedback automatisch zu kategorisieren.

## Architektur-Übersicht

Die Anwendung folgt einem asynchronen Task-Queue-Muster, um eine skalierbare und entkoppelte Verarbeitung von Benutzerbewertungen zu gewährleisten:

- **API-Schicht (FastAPI)**: Stellt Endpunkte bereit, um Bewertungen zu empfangen und die Verarbeitung an eine Hintergrund-Task-Queue auszulagern.
- **Messaging-Schicht (RabbitMQ)**: Fungiert als Message-Broker zwischen der API und dem Hintergrund-Worker.
- **Verarbeitungsschicht (Celery Consumer)**: Überwacht die Message-Queue, führt eine ML-Sentiment-Analyse mit vortrainierten Modellen durch und speichert das Ergebnis in der Datenbank.
- **Datenbankschicht (PostgreSQL)**: Speichert Unternehmens-, Bewertungs- und Kundendaten.
- **Observability-Schicht**:
    - **Prometheus/Celery Exporter**: Sammelt System- und Task-Metriken.
    - **Loki**: Aggregiert Logs zur Fehlerbehebung.
    - **Grafana**: Bietet Visualisierung von Metriken und Logs.

## Systemdiagramm

```mermaid
graph LR
    User[Client] -->|POST /reviews| API[FastAPI Backend]
    API -->|Task einreihen| MQ[RabbitMQ]
    MQ -->|Konsumieren| Consumer[Celery Consumer]
    Consumer -->|Inferenz ausführen| ML[Sentiment Modell]
    Consumer -->|Speichern| DB[(PostgreSQL)]
    
    subgraph Observability
        Prometheus
        Loki
        Grafana
    end
    
    API -.->|Metriken| Prometheus
    Consumer -.->|Metriken| Prometheus
    Consumer -.->|Logs| Loki
    Prometheus & Loki -->|Daten| Grafana
```

## Tech-Stack

- **API**: FastAPI
- **Task-Queue**: Celery, RabbitMQ
- **Datenbank**: PostgreSQL
- **Monitoring**: Prometheus, Loki, Grafana

## Voraussetzungen

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Einrichtung & Ausführung

1. **Repository klonen**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Container bauen und starten**:
   ```sh
   docker compose up --build
   ```
   Dieser Befehl initialisiert den gesamten Stack, einschließlich Backend, Consumer, Message-Broker, Datenbank und dem Observability-Stack.

3. **Container-Status prüfen**:
   ```sh
   docker ps
   ```

4. **Container stoppen**:
   ```sh
   docker compose down
   ```

## Monitoring

Das Projekt enthält einen Observability-Stack, der über Grafana zugänglich ist.

- **Grafana**: Verfügbar unter `http://localhost:3000` (Standard-Zugangsdaten).
- **Dashboards**: Vorkonfigurierte Dashboards befinden sich im Verzeichnis `/dashboards`. Sie können diese direkt in Grafana importieren, um Systemstatus, Anfragelatenz und Metriken zur Verarbeitung der Sentiment-Analyse zu visualisieren.

## Überprüfung

Um sicherzustellen, dass das System korrekt funktioniert:
1. Überprüfen Sie mit `docker ps`, ob alle Container laufen.
2. Rufen Sie die API-Dokumentation unter `http://localhost:8000/docs` auf und übermitteln Sie eine Testbewertung.
3. Überprüfen Sie die Logs im Terminal oder verwenden Sie Loki/Grafana, um zu verifizieren, dass die Aufgabe vom Celery-Worker verarbeitet wurde.
4. Betrachten Sie die Metriken in Grafana, um den Durchsatz der Bewertungsverarbeitung und die Systemressourcenauslastung zu sehen.
