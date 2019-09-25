
from flask import Blueprint
from flask_restplus import Api
from app.api.user import ns as user_ns


bp = Blueprint('api', __name__, url_prefix='/v1/admin')

api = Api(bp, version=1.0, title='CloudFDS Admin API', description='CloudFDS Admin API', doc='/doc/')

api.add_namespace(ns=user_ns)
