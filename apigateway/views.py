import json

import requests
from flask import request, Response
from flask_cors import cross_origin

from apigateway import app, oidc, logger
from apigateway.producer import produce_command, broadcast_command
from apigateway.shared.util import find_by_ids, find_by_id

from config import BUILDINGS_BASE_URL, TENANTS_BASE_URL, DEVICES_BASE_URL

BUILDINGS_BASE_PATH = '/api/buildings'
DEVICES_BASE_PATH = '/api/devices'
TENANTS_BASE_PATH = '/api/tenants'

BASE_URLS = [BUILDINGS_BASE_URL, DEVICES_BASE_URL, TENANTS_BASE_URL]


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
    buildings = data[BUILDINGS_BASE_URL]
    for tenant in tenants:
        tenant_devices = find_by_ids(devices, tenant['devices'])
        tenant['devices'] = tenant_devices
        tenant['total_meter_value'] = sum([d['meter_value_diff'] for d in tenant_devices])
        tenant['home'] = find_by_id(buildings, tenant['home_building'])
    return json.dumps(tenants), 200


@app.route(TENANTS_BASE_PATH, methods=['PUT'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def alter_device_distribution():
    request_data = request.data.decode('utf-8')
    if json.loads(request_data)['device_ids']:
        broadcast_command(['devices', 'tenants'], 'DISTRIBUTE_DEVICES', request_data)
    else:
        broadcast_command(['devices', 'tenants'], 'REMOVE_DEVICES', request_data)
    return Response(status=201)


@app.route(TENANTS_BASE_PATH, methods=['POST'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def create_one_tenant():
    request_data = request.data.decode('utf-8')
    response = requests.post(TENANTS_BASE_URL, request_data, verify=False)
    if response.status_code == 201:
        new_tenant = response.content.decode('utf-8')
        produce_command('buildings', 'ADD_TENANT', new_tenant)
    return response.content.decode('utf-8'), response.status_code


@app.route(F'{TENANTS_BASE_PATH}/<tenant_id>', methods=['DELETE'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def delete_tenant(tenant_id):
    response = requests.delete(F'{TENANTS_BASE_URL}/{tenant_id}', verify=False)
    if response.status_code != 204:
        return Response(status=response.status_code)
    produce_command('devices', 'REMOVE_DEVICES', {'tenant_id': tenant_id})
    return Response(status=204)


@app.route(DEVICES_BASE_PATH, methods=['PUT'])
@cross_origin()
@oidc.require_token(roles=['admin'])
def reset_meter_value():
    produce_command('devices', 'RESET_METER_VALUE', request.data.decode('utf-8'))
    return Response(status=204)


@app.errorhandler(Exception)
def handle_http_errors(error):
    logger.error(error)
    return Response(status=500)
