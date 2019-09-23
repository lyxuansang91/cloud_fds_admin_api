import json

from flask_jwt_extended import create_access_token
from flask_restplus import Namespace, Resource

from app.errors.exceptions import BadRequest
from app.extensions import flask_bcrypt
from app.repositories.user import user_repo

from ..utils import consumes, use_args, to_json

ns = Namespace(name="users", description="Users related operation")


@ns.route('')
class APIUserRegister(Resource):
    @use_args(**{
        'type': 'object',
        'properties': {
            'username': {'type': 'string', 'maxLength': 128},
            'password': {'type': 'string'},
            'company': {'type': 'string'},
            'createdBy': {'type': 'string'},
            'email': {
                'type': 'string',
                'format': 'email'
            },
            'address': {'type': 'string'},
            'roleType': {'type': 'string', "enum": ['Admin', 'User']},
            'contactNumber': {
                'type': 'string',
                'pattern': '^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$'
            }
        },
        'required': ['email', 'password']
    })
    def post(self, args):
        ''' register user endpoint '''
        role_type = args.get('roleType', 'User')
        if role_type not in ['Admin', 'User']:
            raise BadRequest(message='Role type must be Admin or User')
        args['createdBy'] = args.get('createdBy', 'Admin')
        args['roleType'] = role_type
        if 'username' not in args and 'email' not in args:
            raise BadRequest(code=400, message='username or email must be required')
        args['password'] = flask_bcrypt.generate_password_hash(args['password'])
        user = user_repo.insert_one(args)
        if user is None:
            raise BadRequest(code=400, message="user existed")
        print('user:', user._data)
        return {'item': to_json(user._data), 'message': 'Signup user is successful'}, 201


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
        if user.roleType == 'User':
            raise BadRequest(code=400, message='RoleType is not valid')
        if user and flask_bcrypt.check_password_hash(user.password, args['password']):
            data = user._data
            del data['password']
            del args['password']
            access_token = create_access_token(identity=args)
            data['access_token'] = access_token
            return {'item': to_json(data), 'message': 'Login successfully'}, 200
        else:
            raise BadRequest(code=400, message='Invalid username or password')
