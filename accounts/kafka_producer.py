from confluent_kafka import Producer
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class KafkaProducer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KafkaProducer, cls).__new__(cls)
            cls._instance.producer = Producer({'bootstrap.servers': settings.KAFKA_BROKER_URL})
        return cls._instance

    def produce_message(self, topic, message):
        """
        Produces a message to the specified Kafka topic.
        :param topic: The topic to publish to
        :param message: A dictionary representing the message
        """
        try:
            print(f"DEBUG: Attempting to produce to {topic}: {message}", flush=True)
            self.producer.produce(
                topic,
                key=str(message.get('user_id', '')),
                value=json.dumps(message),
                callback=self.delivery_report
            )
            self.producer.flush()
        except Exception as e:
            logger.error(f"Failed to produce message to Kafka: {e}")
            print(f"DEBUG: Failed to produce: {e}", flush=True)


    def delivery_report(self, err, msg):
        """ Callback called once message is delivered or failed. """
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")
