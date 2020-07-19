from threading import Thread
import json

from kafka import KafkaConsumer

from apigateway import logger
from apigateway.shared.error_handlers import handle_kafka_errors
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX


# class ApartmentCommandConsumer(Thread):
#     daemon = True
#
#     def run(self):
#         topic = F'{KAFKA_PREFIX}-{KAFKA_TOPIC}'
#
#         consumer = KafkaConsumer(
#             F'{topic}-commands',
#             bootstrap_servers=[F'{KAFKA_HOST}:{KAFKA_PORT}'],
#             client_id=F'{KAFKA_PREFIX}-{KAFKA_TOPIC}-consumer',
#             group_id=F'{KAFKA_PREFIX}-{KAFKA_TOPIC}-commands')
#
#         for message in consumer:
#             handle_message(message)
#
#
# @handle_kafka_errors
# def handle_message(message):
#     message = json.loads(message.value.decode('utf-8'))
#     assert all(key in message for key in ['id', 'commandType', 'data'])
#
#     command_type = message['commandType']
#     assert any(command == command_type for command in ['CREATE', 'GET_ALL', 'GET_ONE'])
#
#     if command_type == 'CREATE':
#         data = message['data']
#         apartments.insert(data)
#         logger.warn(F'Created {data}')
