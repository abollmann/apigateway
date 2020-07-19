import os

SECRET_KEY = os.environ.get('SECRET_KEY', '7j@+pza(6(=*)$7zsb)bu*$f$fu1kcs*-oz78chs&r(x)@fu-d')
DEBUG = os.environ.get('DEBUG', False)
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
TRAP_BAD_REQUEST_ERRORS = True

TOKEN_INTROSPECTION_URL = 'https://116.203.242.235.xip.io/auth/realms/apartments/protocol/openid-connect/token/introspect'
CLIENT_ID = 'api-gateway'
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


KAFKA_HOST = os.environ.get('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = os.environ.get('KAFKA_PORT', '9093')
KAFKA_PREFIX = os.environ.get('KAFKA_PREFIX', 'local')
