import flask_restplus as frp
from flask import request
from flask_jwt_extended import jwt_required

from app.errors.exceptions import BadRequest
from app.repositories.billing_type import billing_type_repo
from app.repositories.price import price_repo

from ..decorators import authorized

ns = frp.Namespace(name="prices", description="Price related operation")


@ns.route('')
class APIPriceInfo(frp.Resource):
    @jwt_required
    @authorized()
    def get(self, current_user):
        args = request.args
        if 'typeid' not in args or 'date' not in args:
            raise BadRequest(message='typeid or date is required')
        type_id = args.get('typeid')
        billing_type = billing_type_repo.get_by_id(type_id)
        if billing_type is None:
            raise BadRequest(message='BillingType is not found')
        _date = args.get('date')
        price = price_repo.findPrice(type_id, _date)
        return {'item': {'billingType': billing_type.billingType, 'price': float(price)}}, 200
