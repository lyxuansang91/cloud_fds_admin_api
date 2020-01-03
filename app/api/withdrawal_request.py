import flask_restplus as frp
from flask_jwt_extended import jwt_required

from app.repositories.withdrawal_request import withdrawal_request_repo
from app.errors.exceptions import BadRequest

from ..decorators import authorized, use_args

ns = frp.Namespace(name="withdrawal_requests", description="WithdrawalRequest related operation")


@ns.route('/<string:withdrawal_id>/approve')
class APIWithdrawalApprove(frp.Resource):
    @jwt_required
    @authorized()
    @use_args(**{
        'type': 'object',
        'properties': {
            'code': {'type': 'string'},
        },
        'required': ['code']
    })
    def post(self, current_user, args, withdrawal_id):
        withdrawal_request = withdrawal_request_repo.get_withdrawal(withdrawal_id)
        if str(current_user.id) != str(withdrawal_request.userId):
            raise BadRequest(message='User is not valid')
        if withdrawal_request.code != args['code']:
            raise BadRequest(message='Code is not valid')
        withdrawal_request_repo.approve_request(withdrawal_request)
        return {'message': 'Request approved'}, 204

    @jwt_required
    @authorized()
    def get(self, current_user, withdrawal_id):
        pass
