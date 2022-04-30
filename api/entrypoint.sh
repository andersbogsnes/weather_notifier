#!/usr/bin/env bash
set -euo pipefail

alembic upgrade head &&
uvicorn --host 0.0.0.0 --factory weather_notifier.app:create_app