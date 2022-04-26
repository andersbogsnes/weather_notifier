FROM python:3.10 as base

ENV PATH=/opt/venv/bin:$PATH \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

FROM base as installer

RUN python -m venv /opt/venv && \
    apt-get update && \
    apt-get install -y \
            libpq-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg

RUN pip install .

FROM base as final

WORKDIR app

COPY --from=installer /opt/venv /opt/venv

CMD ["uvicorn", "--host", "0.0.0.0", "--factory", "weather_notifier.app:create_app"]