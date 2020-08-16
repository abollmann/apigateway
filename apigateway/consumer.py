import json

from kafka import KafkaConsumer

from config import KAFKA_HOST, KAFKA_PORT, KAFKA_PREFIX, KAFKA_TOPICS


def init_consumers():
    return {consumer: KafkaConsumer(
        F'{KAFKA_PREFIX}-{consumer}-data',
        bootstrap_servers=[F'{KAFKA_HOST}:{KAFKA_PORT}'],
        client_id=F'{KAFKA_PREFIX}-{consumer}-consumer',
        group_id=F'{KAFKA_PREFIX}-{consumer}-data')
        for consumer in KAFKA_TOPICS}


consumers = init_consumers()


def await_response(consumer, message_id):
    for message in consumers[consumer]:
        message = json.loads(message.value.decode('utf-8'))
        if message['id'] == message_id:
            return json.dumps(message['data']), message['status_code']
    return 500
