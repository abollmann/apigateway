from functools import wraps

from flask import request

import requests as req


class AuthEndpoint:

    def __init__(self, app):
        self.app = app
        self.user = None
        self.url = self.app.config['TOKEN_INTROSPECTION_URL']
        self.client_id = self.app.config['CLIENT_ID']
        self.client_secret = self.app.config['CLIENT_SECRET']

    def require_token(self, roles=None):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.user:
                    auth_header = request.headers.get('Authorization')
                    if not auth_header:
                        return 'Authorization required', 401
                    if 'Bearer ' not in auth_header:
                        return 'Bearer token required', 401
                    status_code, user = self.get_user(auth_header.replace('Bearer ', ''))
                    if user == {'active': False} or str(status_code).startswith('4') or 'error' in user.keys():
                        return 'Unauthorized', 401
                    self.user = user

                if roles:
                    resource_access = self.user['resource_access']
                    if self.client_id not in resource_access.keys():
                        return F'User not authorized for client {self.client_id}', 401
                    assigned_roles = resource_access[self.client_id]['roles']
                    missing_roles = set(roles) - set(assigned_roles)
                    if missing_roles:
                        return F'Roles {missing_roles} are required for this endpoint', 401
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def get_user(self, token):
        response = req.post(self.url,
                            data={'client_id': self.client_id, 'client_secret': self.client_secret, 'token': token},
                            verify=False)
        return response.status_code, response.json()
