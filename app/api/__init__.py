import json

import jwt
import requests
from flask import Blueprint, current_app, g, request
from flask_restplus import Api

# from app import models as m
# from app.api.action import ns as action_ns
# from app.api.client import ns as client_ns
# from app.api.permission import ns as permission_ns
# from app.api.resource import ns as resource_ns
# from app.api.role import ns as role_ns
# from app.api.route import ns as route_ns
# from app.api.scope import ns as scope_ns
# from app.api.scope_request import ns as scope_request_ns
# from app.api.service import ns as service_ns
# from app.api.service_group import ns as service_group_ns
# from app.api.user import ns as user_ns
from app.errors.exceptions import Unauthorized

bp = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(bp, version=1.0, title='Identity Admin API', description='Idenity Admin API', doc='/doc/')


# api.add_namespace(ns=client_ns)
# api.add_namespace(ns=scope_ns)
# api.add_namespace(ns=user_ns)
# api.add_namespace(ns=scope_request_ns)
# api.add_namespace(ns=resource_ns)
# api.add_namespace(ns=service_group_ns)
# api.add_namespace(ns=service_ns)
# api.add_namespace(ns=role_ns)
# api.add_namespace(ns=action_ns)
# api.add_namespace(ns=permission_ns)
# api.add_namespace(ns=route_ns)


def _check_public_keys():
    if not hasattr(g, 'public_keys'):
        g.public_keys = None
    if g.public_keys is None:
        jwks_route = current_app.config.get('JWKS_ROUTE')
        response = requests.get(jwks_route, headers={'Content-Type': 'application/json'})
        jwks = response.json()
        public_keys = {}
        for jwk in jwks.get('keys'):
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        g.public_keys = public_keys
    return g.public_keys


def get_token():
    authorize_headers = request.headers.get('Authorization')
    if authorize_headers is None:
        return None
    headers = authorize_headers.split()
    if len(headers) > 0:
        return headers[1]
    else:
        return None


@bp.before_request
def before_request():
    if request.method == 'OPTIONS':
        return
    public_keys = _check_public_keys()
    token = get_token()
    user = None
    if token:
        try:
            kid = jwt.get_unverified_header(token).get('kid')
            aud = jwt.decode(token, verify=False, algorithms=['RSA256']).get('aud')
            pubkey = public_keys.get(kid)
            payload = jwt.decode(token, key=pubkey, algorithms=["RS256"], audience=aud)
            user_id = payload.get('sub')
            user = m.User.query.get(user_id)
        except Exception as e:
            current_app.logger.error("Error on: ", e)
            user = None
    g.user = user.id if user else None
    if user is None:
        raise Unauthorized(code=401, message="Unauthorized Error")
