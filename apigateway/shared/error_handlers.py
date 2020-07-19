from functools import wraps

from apigateway import logger


def handle_kafka_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as error:
            logger(error)

    return decorated_function

