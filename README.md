# Weather Notifier

A service consisting of a Rest API to allow users to sign up for weather alerts and a scheduler
called `notifier` which will poll the API for which alerts it needs to check, and then
calls the OpenWeatherMap API to see if the user needs to be alerted.

## Running the project

For more detailed information about the services in the project, check the subfolder READMEs

To start all the components of the project locally, use the docker-compose file.

You'll need to get an API_KEY (see the notifier README for details if you don't have one)
Add this to the `.env.example` and rename to `.env` or set the API_KEY env variable to the API KEY

When this is done run `docker compose up` (or `docker-compose up` if you've installed docker-compose
separately)

This will start the REST API, the notifier scheduler, the Postgres database as well as a Mailhog
email server

To see the emails coming in, navigate to http://localhost:8025 - it should take 1 minute for the
first email to tick in

