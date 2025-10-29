#!/bin/bash
# Usa el puerto que Azure provee en $PORT
export PORT=${PORT:-8000}
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
