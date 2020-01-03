
from flask import Blueprint, current_app, jsonify
from flask_restplus import Api
from werkzeug.exceptions import HTTPException

from app.api.billing_type import ns as billing_type_ns
from app.api.password import ns as password_ns
from app.api.price import ns as price_ns
from app.api.user import ns as user_ns
from app.api.withdrawal_request import ns as withdrawal_request_ns
from app.errors.exceptions import ApiException

bp = Blueprint('api', __name__, url_prefix='/v1/admin')

api = Api(bp, version=1.0, title='CloudFDS Admin API', description='CloudFDS Admin API', doc='/doc/')

api.add_namespace(ns=user_ns)
api.add_namespace(ns=password_ns)
api.add_namespace(ns=billing_type_ns)
api.add_namespace(ns=price_ns)
api.add_namespace(ns=withdrawal_request_ns)


@bp.before_app_first_request
def before_app_first_request():
    from app.repositories.billing_type import billing_type_repo
    if billing_type_repo.get_by_billing_type('Monthly') is None:
        billing_type_repo.create({'billingType': 'Monthly'})
    if billing_type_repo.get_by_billing_type('Metered') is None:
        billing_type_repo.create({'billingType': 'Metered'})
    if billing_type_repo.get_by_billing_type('Free trial') is None:
        billing_type_repo.create({'billingType': 'Free trial'})


@api.errorhandler(ApiException)
def api_error_handler(error):
    current_app.logger.error(error)
    current_app.logger.warning(
        f'HTTP_STATUS_CODE: {error.status_code} - {error.to_dict}')
    return jsonify(error.to_dict), error.status_code


@api.errorhandler(HTTPException)
def http_error_handler(error):
    current_app.logger.error(error)
    return jsonify({'error': {'code': error.code, 'message': error.description}}), error.code


@api.errorhandler(Exception)
def unexpected_error_handler(error):
    current_app.logger.error(error)
    return jsonify({'error': {'code': 500, 'message': 'Internal Server Error'}}), 500
