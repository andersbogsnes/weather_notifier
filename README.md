# Weather Notifier

## Python Coding Test

We need to develop a small app that can be used to consume and monitor an external weather
API (e.g. https://openweathermap.org/api) and generate alerts when certain conditions are met.

### Functional Requirements:
Develop a Rest API with endpoints for weather alert subscriptions. A subscription has an email
address, a location (e.g. city) and some simple weather conditions to be alerted about, (e.g.
temperature less than 0 celsius).

Endpoints should be available to create/list/read/update and delete (cancel) subscriptions.
The app should regularly poll a public weather API for the city locations that have been
subscribed to, check the current weather information based on the conditions and if the
conditions are met log the alert (e.g. into a text file) that could be sent out to an email address
(email sending functionality not required).

### Other Requirements:
- Use a Python web framework of your choice (e.g. Django, Django REST, Flask, FastAPI
etc.)
- Design a DB schema for the above and use a relational database for persistence (e.g.
Postgres).
- You can use other dependencies needed for functionality. When you use other
dependencies we will discuss your choice and reasons why you decided to use any.
- Write tests.
- Use python type hints.
- Write instructions to run the application.
Notes:
- Keep it simple.
- Do not spend more than 2 hours.
- This task should give us a sense of your coding style and an insight into how you would
structure an app, how you write tests, how you consume external resources and how
you deal with errors.
- Submit your code in a public git repository (preferred) or in a zip file via email

## Developer Guide

To install the project alongside the dev-dependencies, run the following:

```bash
pip install -e .[dev]
```

This will install the weather_notifier Python package alongside test and dev dependencies

### Pre-commit hooks

Install the git pre-commit hooks by running

```bash
pre-commit install
```

This will create the git hooks to run lint checks before every commit

### Tests

When the dev dependencies are installed, run the testsuite with

```bash
tox
```

This will run the pre-commit linters as well as the testsuite

### Lint
