from typing import Any, Dict

import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse


def general_response(body, status_code):
    return JSONResponse(
        content=jsonable_encoder(body),
        status_code=status_code,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    )


def OK():
    return PlainTextResponse(
        content="OK",
        status_code=fastapi.status.HTTP_200_OK,
        headers={
            "Access-Control-Allow-Origin": "*",
        },
    )


def success(body):
    return general_response(body, fastapi.status.HTTP_200_OK)


def created(body):
    return general_response(body, fastapi.status.HTTP_201_CREATED)


def bad_request(body: Dict[str, Any]):
    return general_response(body, fastapi.status.HTTP_400_BAD_REQUEST)


def not_allowed(body):
    return general_response(body, fastapi.status.HTTP_403_FORBIDDEN)


def not_found(body=None):
    return general_response(body, fastapi.status.HTTP_404_NOT_FOUND)


def server_error(body):
    return general_response(
        {"error": body}, fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    )
