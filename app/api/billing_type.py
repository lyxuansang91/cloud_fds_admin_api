import flask_restplus as frp
from flask_jwt_extended import jwt_required

from app.repositories.billing_type import billing_type_repo
from app.repositories.user_activity import user_activity_repo

from ..decorators import authorized
from ..utils import to_json

ns = frp.Namespace(name="billing_types", description="BillingType related operation")


@ns.route('')
class APIBillingTypeList(frp.Resource):
    @jwt_required
    @authorized()
    def get(self, current_user):
        user_activity_repo.create_activity({
            'userId': current_user.id,
            'activity': 'Get Billing Type',
            'desc': 'success'
        })
        billing_types = billing_type_repo.get_list()
        return {'items': [to_json(billing_type._data) for billing_type in billing_types], 'count': len(billing_types)}, 200
