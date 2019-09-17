from flask_jwt_extended import create_access_token
from flask_restplus import Namespace, Resource

from app.errors.exceptions import BadRequest
from app.extensions import flask_bcrypt
from app.repositories.user import user_repo

from ..utils import consumes, use_args

ns = Namespace(name="users", description="Users related operation")


@ns.route('')
class APIUserRegister(Resource):
    @consumes('application/json')
    @use_args(**{
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'company': {'type': 'string'},
            'email': {'type': 'string'},
            'address': {'type': 'string'},
        },
        'required': ['password']
    })
    def post(self, args):
        ''' register user endpoint '''
        if 'username' not in args and 'email' not in args:
            raise BadRequest(message='username or email must be required')
        args['password'] = flask_bcrypt.generate_password_hash(args['password'])
        item = user_repo.insert_one(args)
        return {'item': item, 'message': 'Signup user is successful'}, 201


@ns.route('/login')
class APIUserLogin(Resource):
    @consumes('application/json')
    @use_args(**{
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'required': ['username', 'password']
    })
    def post(self, args):
        username = args.get('username')
        user = user_repo.find_by_username_or_email(username)
        if user and flask_bcrypt.check_password_hash(user['password'], args['password']):
            del user['password']
            access_token = create_access_token(identity=args)
            user['access_token'] = access_token
            return {'item': user, 'message': 'Login successfully'}, 200
        else:
            raise BadRequest(code=400, message='Invalid username or password')
