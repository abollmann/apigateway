import json

import requests
from flask import request, Response
from flask_cors import cross_origin

from apigateway import app, oidc, logger
from apigateway.consumer import await_response, get_data
from apigateway.producer import produce_command, broadcast_command
from apigateway.shared.util import find_by_ids

from config import BUILDINGS_BASE_URL, TENANTS_BASE_URL, DEVICES_BASE_URL

BUILDINGS_BASE_PATH = '/api/buildings'
DEVICES_BASE_PATH = '/api/devices'
TENANTS_BASE_PATH = '/api/tenants'

BASE_URLS = [BUILDINGS_BASE_URL, DEVICES_BASE_URL, TENANTS_BASE_URL]


# @app.route(F'{BUILDINGS_BASE_PATH}/<internal_id>', methods=['GET'])
# @oidc.require_token(roles=['read'])
# def get_one_building(internal_id):
#     message_id = produce_command('buildings', 'GET_BY_ID', {'internal_id': internal_id})
#     return await_response('buildings', message_id)


# @app.route(BUILDINGS_BASE_PATH, methods=['POST'])
# @oidc.require_token(roles=['read', 'write'])
# def create_one_building():
#     message_id = produce_command('buildings', 'CREATE', request.data.decode('utf-8'))
#     return await_response('buildings', message_id)

# @app.route(F'{TENANTS_BASE_PATH}/<email>', methods=['PUT'])
# @oidc.require_token(roles=['read', 'write'])
# def add_devices_to_tenant():
#     message_id = produce_command('tenants', 'DEVICES', request.data.decode('utf-8'))
#     return await_response('tenants', message_id)


@app.route(BUILDINGS_BASE_PATH, methods=['GET'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def get_all_buildings():
    response = requests.get(BUILDINGS_BASE_URL, verify=False)
    return response.content.decode('utf-8'), response.status_code


@app.route(DEVICES_BASE_PATH, methods=['GET'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def get_all_devices():
    response = requests.get(DEVICES_BASE_URL, verify=False)
    return response.content.decode('utf-8'), response.status_code


@app.route(TENANTS_BASE_PATH, methods=['GET'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def get_all_tenants():
    data = {url: requests.get(url, verify=False) for url in BASE_URLS}
    for key, response in data.items():
        if response.status_code != 200:
            return response.status_code
        data[key] = json.loads(response.content.decode('utf-8'))
    tenants = data[TENANTS_BASE_URL]
    devices = data[DEVICES_BASE_URL]
    for tenant in tenants:
        tenant_devices = find_by_ids(devices, tenant['devices'])
        tenant['devices'] = tenant_devices
        tenant['bill'] = sum([d['current_price'] for d in tenant_devices])
    return json.dumps(tenants), 200


@app.route(F'{DEVICES_BASE_PATH}/distribute', methods=['POST'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def alter_device_distribution():
    broadcast_command(['devices', 'tenants'], 'DISTRIBUTE_DEVICES', request.data.decode('utf-8'))
    return Response(status=201)


@app.route(TENANTS_BASE_PATH, methods=['POST'])
@cross_origin()
@oidc.require_token(roles=['read', 'write'])
def create_one_tenant():
    response = requests.post(TENANTS_BASE_URL, request.data.decode('utf-8'), verify=False)
    return response.content.decode('utf-8'), response.status_code


@app.route(F'{TENANTS_BASE_PATH}/<email>', methods=['DELETE'])
@cross_origin()
@oidc.require_token(roles=['read', 'write'])
def delete_tenant(email):
    message_id = produce_command('tenants', 'DELETE', {'email': email})
    return await_response('tenants', message_id)


@app.errorhandler(Exception)
def handle_http_errors(error):
    logger.error(error)
    return Response(status=500)
