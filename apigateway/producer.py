import uuid

from kafka import KafkaProducer
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX

producer = KafkaProducer(
    bootstrap_servers=[F'{KAFKA_HOST}:{KAFKA_PORT}'],
    client_id=F'{KAFKA_PREFIX}-apigateway-producer')


def produce_log(msg):
    value = bytes(msg, encoding='utf-8')
    producer.send(F'{KAFKA_PREFIX}-apigateway-logs', value=value)


def produce_command(api_name, command_type, data=None):
    value = {'data': {} if data is None else data,
             'command_type': command_type,
             'id': str(uuid.uuid4())}
    value = bytes(str(value), encoding='utf-8')
    producer.send(F'{KAFKA_PREFIX}-{api_name}-commands', value=value)
