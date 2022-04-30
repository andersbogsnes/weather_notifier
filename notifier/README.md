# Notifier

A service to alert users if weather conditions exceed a given threshold set by the user

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
and make `notifier` available as a command in the shell and importable in the Python interpreter

### Setup .env file
To be able to run the project locally, you'll need some configuration variables.
These can be set in the `.env.example` file, which should then be renamed to `.env`

You'll need the following values:

#### API_KEY
An [Open Weather Map](openweathermap.org) API key.
Click the link above, create an account and grab a key from the API key page

#### SMTP_HOST
The SMTP host you want to use to send the emails.
To create a dummy one for local development, you can use the [mailhog](https://github.com/mailhog/MailHog) project. The simplest way is to use the `mailhog/mailhog` docker image. Note the ports from the documentation

#### SUBSCRIPTION_API_URL
The URL of the Subscription API. Start one locally from the weather-notifier-api repo

## Testing
```bash
tox
```

This will run all tests as well as the linter suite.

To run just the tests, use `pytest`
