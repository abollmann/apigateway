from apigateway import app, oidc, logger
from apigateway.producer import produce_command

BUILDINGS_BASE_PATH = '/api/buildings'
DEVICES_BASE_PATH = '/api/devices'
TENANTS_BASE_PATH = '/api/tenants'


@app.route(BUILDINGS_BASE_PATH, methods=['GET'])
@oidc.require_token(roles=['read'])
def get_all():
    produce_command('apartments', 'GET_ALL')
    return 'helo', 200


@app.route(F'{BUILDINGS_BASE_PATH}/<object_id>', methods=['GET'])
@oidc.require_token(roles=['read'])
def get_one(object_id):
    return 'herllo', 200


@app.route(BUILDINGS_BASE_PATH, methods=['POST'])
@oidc.require_token(roles=['read', 'write'])
def create_one():
    return 'herllo', 200


@app.errorhandler(Exception)
def handle_http_errors(error):
    logger.error(error)
    return str(error), 400
