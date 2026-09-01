# Système d'Analyse de Sentiment

Ce projet met en œuvre un pipeline asynchrone d'analyse de sentiment pour les avis des utilisateurs, utilisant un modèle d'apprentissage automatique pour catégoriser les retours automatiquement.

## Aperçu de l'Architecture

L'application suit un modèle de file d'attente de tâches asynchrone pour assurer un traitement évolutif et découplé des avis des utilisateurs :

- **Couche API (FastAPI)** : Sert les points de terminaison pour recevoir les avis et délègue le traitement à une file d'attente de tâches en arrière-plan.
- **Couche de Messagerie (RabbitMQ)** : Agit comme le courtier de messages entre l'API et le travailleur en arrière-plan.
- **Couche de Traitement (Consommateur Celery)** : Écoute la file d'attente de messages, effectue l'analyse de sentiment ML en utilisant des modèles pré-entraînés, et persiste le résultat dans la base de données.
- **Couche de Base de Données (PostgreSQL)** : Stocke les données de l'entreprise, des avis et des clients.
- **Couche d'Observabilité** : 
    - **Prometheus/Celery Exporter** : Collecte les métriques du système et des tâches.
    - **Loki** : Agrège les journaux pour le dépannage.
    - **Grafana** : Fournit une visualisation des métriques et des journaux.

## Schéma du Système

```mermaid
graph LR
    User[Client] -->|POST /reviews| API[Back-end FastAPI]
    API -->|Mise en file d'attente| MQ[RabbitMQ]
    MQ -->|Consommation| Consumer[Consommateur Celery]
    Consumer -->|Exécution de l'inférence| ML[Modèle de Sentiment]
    Consumer -->|Sauvegarde| DB[(PostgreSQL)]
    
    subgraph Observabilité
        Prometheus
        Loki
        Grafana
    end
    
    API -.->|Métriques| Prometheus
    Consumer -.->|Métriques| Prometheus
    Consumer -.->|Journaux| Loki
    Prometheus & Loki -->|Données| Grafana
```

## Pile Technique

- **API** : FastAPI
- **File d'attente de tâches** : Celery, RabbitMQ
- **Base de données** : PostgreSQL
- **Surveillance** : Prometheus, Loki, Grafana

## Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuration & Exécution

1. **Cloner le dépôt** :
   ```sh
   git clone <url-du-dépôt>
   cd <répertoire-du-dépôt>
   ```

2. **Construire et démarrer les conteneurs** :
   ```sh
   docker compose up --build
   ```
   Cette commande initialise toute la pile, y compris le back-end, le consommateur, le courtier de messages, la base de données et la pile d'observabilité.

3. **Vérifier le statut des conteneurs** :
   ```sh
   docker ps
   ```

4. **Arrêter les conteneurs** :
   ```sh
   docker compose down
   ```

## Surveillance

Le projet inclut une pile d'observabilité accessible via Grafana.

- **Grafana** : Disponible sur `http://localhost:3000` (identifiants par défaut).
- **Tableaux de bord** : Les tableaux de bord pré-configurés se trouvent dans le répertoire `/dashboards`. Vous pouvez les importer directement dans Grafana pour visualiser la santé du système, la latence des requêtes et les métriques de traitement de l'analyse de sentiment.

## Comment vérifier

Pour vérifier que le système fonctionne correctement :
1. Assurez-vous que tous les conteneurs sont en cours d'exécution via `docker ps`.
2. Accédez à la documentation de l'API sur `http://localhost:8000/docs` et soumettez un avis de test.
3. Vérifiez les journaux dans le terminal ou utilisez Loki/Grafana pour vérifier que la tâche a été traitée par le travailleur Celery.
4. Visualisez les métriques dans Grafana pour voir le débit de traitement des avis et l'utilisation des ressources système.
