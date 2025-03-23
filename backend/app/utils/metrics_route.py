from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest

from .metrics import (
    update_system_metrics,
)


metrics_router = APIRouter(prefix="/metrics")


@metrics_router.get("")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
