# Secret Santa Mail Service
This service fetches messages (in JSON format) from RabbitMQ queue and sends them as an email to the user using Mailtrap API.

>Note: You need to have MailTrap API configured to run this app properly.
## How to run
### Development
Currently this service runs only in production mode.
### Production
1. Set up MailTrap account properly.
2. Fill at least MAIL_SERVICE_MAILTRAP_EMAIL and MAIL_SERVICE_MAILTRAP_API_KEY env variables.
3. Start docker compose with "prod" profile.
## Environment configuration
- MAIL_SERVICE_RABBIT_HOST - Address to RabbitMQ broker. Default: localhost
- MAIL_SERVICE_RABBIT_PORT - Port to RabbitMQ broker. Default: 5672
- MAIL_SERVICE_RABBIT_USERNAME - Username for RabbitMQ broker. Default: root
- MAIL_SERVICE_RABBIT_PASSWORD - Password for RabbitMQ broker. Default: secret
- MAIL_SERVICE_EXCHANGE_NAME - Exchange name which will be set up in RabbitMQ broker during app startup. Default: mail-exchange
- MAIL_SERVICE_QUEUE_NAME - Queue name which will be set up in RabbitMQ broker during app startup. Default: mail-queue
- MAIL_SERVICE_MAILTRAP_EMAIL - An email address from which you will send various notifications to the user. You can obtain it from MailTrap website. Default: **Required to fill**
- MAIL_SERVICE_MAILTRAP_API_KEY - API key which you will get from MailTrap. Default: **Required to fill**

> If you change default exchange or queue name, then this should be reflected in Secret Santa App env variables also.
## Throubleshooting
You can pass one more env variable to do dome debugging stuff:
- MAIL_SERVICE_DEBUG=1 will allow you to display debug level logs from the application.