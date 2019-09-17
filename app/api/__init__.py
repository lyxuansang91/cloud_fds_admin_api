
from flask import Blueprint
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

bp = Blueprint('api', __name__, url_prefix='/v1/admin')
api = Api(bp, version=1.0, title='CloudFDS Admin API', description='CloudFDS Admin API', doc='/doc/')


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
