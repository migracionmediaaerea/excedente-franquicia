#! /usr/bin/env sh
exec uvicorn \
    djangoproject.asgi:application \
    --host 0.0.0.0 \
    --port 8000