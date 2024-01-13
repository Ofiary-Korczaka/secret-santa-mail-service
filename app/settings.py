import os


DEBUG = os.environ.get("MAIL_SERVICE_DEBUG", False)

RABBIT_HOST = os.environ.get("MAIL_SERVICE_RABBIT_HOST", "localhost")
RABBIT_PORT = os.environ.get("MAIL_SERVICE_RABBIT_PORT", 5672)

RABBIT_USERNAME = os.environ.get("MAIL_SERVICE_RABBIT_USERNAME", "root")
RABBIT_PASSWORD = os.environ.get("MAIL_SERVICE_RABBIT_PASSWORD", "secret")

RABBIT_MAIL_EXCHANGE_NAME = os.environ.get("MAIL_SERVICE_EXCHANGE_NAME", "mail-exchange")

RABBIT_MAIL_QUEUE_NAME = os.environ.get("MAIL_SERVICE_QUEUE_NAME", "mail-queue")

MAILTRAP_SENDER_EMAIL = os.environ.get("MAIL_SERVICE_MAILTRAP_EMAIL", "")
MAILTRAP_API_KEY = os.environ.get("MAIL_SERVICE_MAILTRAP_API_KEY", "")
