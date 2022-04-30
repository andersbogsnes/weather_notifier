# Subscription API

A Web API which allows users to register a subscription to weather alert monitoring

## Development guide

### Setup a virtualenv

Use your method of choice (pyenv, virtualenv etc.) or use the following commands

```bash
python -m venv venv
```

### Activate the virtualenv

#### Windows

```bash
./venv/Scripts/activate
```

#### Linux

```bash
source ./venv/bin/activate
```

### Install project

```bash
pip install -e ".[dev]"
```

This will install the project in "editable" mode

### Setup .env file
To be able to run the project locally, you'll need some configuration variables.
These can be set in the `.env.example` file, which should then be renamed to `.env`

You'll need the following values:

#### DB_URL
A SQLAlchemy connection string to the Postgres database

## Testing
```bash
tox
```

This will run all tests as well as the linter suite.

To run just the tests, use `pytest`
