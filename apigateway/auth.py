from functools import wraps

from flask import request

from keycloak import KeycloakOpenID


class AuthEndpoint:

    def __init__(self, app):
        self.app = app
        self.url = self.app.config['KEYCLOAK_URL']
        self.client_id = self.app.config['CLIENT_ID']
        self.client_secret = self.app.config['CLIENT_SECRET']
        self.keycloak_openid = KeycloakOpenID(server_url=self.url,
                                              client_id=self.client_id,
                                              realm_name='apartments',
                                              client_secret_key=self.client_secret,
                                              verify=False)

    def require_token(self, roles=None):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    return 'Authorization required', 401
                if 'Bearer ' not in auth_header:
                    return 'Bearer token required', 401
                token = auth_header.replace('Bearer ', '')
                try:
                    user = self.keycloak_openid.introspect(token)
                    missing_roles = set(roles) - set(user['resource_access']['api-gateway']['roles'])
                    if missing_roles:
                        return F'Unauthorized, missing roles. {missing_roles}', 401
                except Exception:
                    return 'Unauthorized', 401
                return f(*args, **kwargs)

            return decorated_function

        return decorator
