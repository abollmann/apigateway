from flask import request

from apigateway import app, oidc, logger
from apigateway.consumer import await_response
from apigateway.producer import produce_command

BUILDINGS_BASE_PATH = '/api/buildings'
DEVICES_BASE_PATH = '/api/devices'
TENANTS_BASE_PATH = '/api/tenants'


@app.route(BUILDINGS_BASE_PATH, methods=['GET'])
@oidc.require_token(roles=['read'])
def get_all_buildings():
    message_id = produce_command('buildings', 'GET_ALL')
    return await_response('buildings', message_id)


@app.route(F'{BUILDINGS_BASE_PATH}/<internal_id>', methods=['GET'])
@oidc.require_token(roles=['read'])
def get_one_building(internal_id):
    message_id = produce_command('buildings', 'GET_BY_ID', {'internal_id': internal_id})
    return await_response('buildings', message_id)


@app.route(BUILDINGS_BASE_PATH, methods=['POST'])
@oidc.require_token(roles=['read', 'write'])
def create_one_building():
    message_id = produce_command('buildings', 'CREATE', request.data.decode('utf-8'))
    return await_response('buildings', message_id)


@app.route(DEVICES_BASE_PATH, methods=['GET'])
@oidc.require_token(roles=['read'])
def get_al_devices():
    message_id = produce_command('devices', 'GET_ALL')
    return await_response('devices', message_id)


@app.errorhandler(Exception)
def handle_http_errors(error):
    logger.error(error)
    return 500
