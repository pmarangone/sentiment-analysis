# Use prefork for CPU-heavy tasks
celery:
	celery -A app.celery_app worker -P prefork --loglevel=info --queues=sentiment-analysis