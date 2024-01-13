import logging
import json
import pika
import mailtrap as mt
import settings

from message_category import MessageCategory
from mail_service_exception import MailServiceException


logging.basicConfig(format="%(asctime)s :: %(levelname)s :: %(message)s")


class MailService:
    """
    A class that represents a mail service for sending emails using RabbitMQ and Mailtrap.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

        self.amqp_connection = self.__get_amqp_connection()
        self.channel = self.amqp_connection.channel()
        self.channel.basic_qos(prefetch_count=1)

        self.__configure_amqp_channel()

    def start_consuming(self):
        """
        Start consuming messages from the RabbitMQ queue.
        """
        self.logger.info("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def stop_consuming(self):
        """
        Stop consuming messages from the RabbitMQ queue.
        """
        self.logger.info("Stopping application...")
        self.channel.stop_consuming()

    def __amqp_callback(self, channel, method, properties, body):
        """
        Callback function for processing AMQP messages.

        Args:
            channel: The AMQP channel.
            method: The AMQP method.
            properties: The AMQP properties.
            body: The message body.

        Returns:
            None
        """
        body_json = body.decode("utf-8")

        self.logger.debug("Received %s", body_json)

        body_dict = json.loads(body_json)

        try:
            recipient_email = body_dict["recipientEmail"]
            message_subject = body_dict["messageSubject"]
            message_body = body_dict["messageBody"]
            message_category = body_dict["messageCategory"]
        except json.JSONDecodeError:
            self.logger.error("JSON parsing error")
            return

        if not MessageCategory.is_valid_category(message_category):
            self.logger.error("Invalid message category")
            return

        try:
            self.__send_email(
                recipient_email,
                message_subject,
                message_body,
                message_category,
            )
        except MailServiceException as e:
            self.logger.error(e)
            return

    def __get_amqp_connection(self):
        """
        Get the RabbitMQ connection.

        Returns:
            pika.BlockingConnection: The RabbitMQ connection.
        """
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBIT_HOST,
                port=settings.RABBIT_PORT,
                credentials=pika.PlainCredentials(
                    settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD
                ),
                heartbeat=600,
                blocked_connection_timeout=300,
            )
        )

    def __configure_amqp_channel(self):
        """
        Configure the RabbitMQ channel for message exchange and queue declaration.
        """
        self.channel.exchange_declare(
            exchange=settings.RABBIT_MAIL_EXCHANGE_NAME,
            exchange_type="direct",
            durable=True,
        )
        self.channel.queue_declare(queue=settings.RABBIT_MAIL_QUEUE_NAME, durable=True)

        self.channel.basic_consume(
            queue=settings.RABBIT_MAIL_QUEUE_NAME,
            on_message_callback=self.__amqp_callback,
            auto_ack=True,
        )

    def __send_email(self, recipient, subject, body, category):
        """
        Sends an email using the Mailtrap service.

        Args:
            recipient (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body of the email.
            category (str): The category of the email.

        Raises:
            MailServiceException: If an error occurs while sending the email.

        """
        try:
            mail = mt.Mail(
                sender=mt.Address(email=settings.MAILTRAP_SENDER_EMAIL, name=subject),
                to=[mt.Address(email=recipient)],
                subject=subject,
                text=body,
                category=category,
            )

            client = mt.MailtrapClient(token=settings.MAILTRAP_API_KEY)
            client.send(mail)
        except Exception as e:
            raise MailServiceException(e) from e


if __name__ == "__main__":
    if settings.DEBUG:
        from util import log_environment_variables

        log_environment_variables()

    mail_service = MailService()

    try:
        mail_service.start_consuming()
    except KeyboardInterrupt:
        mail_service.stop_consuming()
