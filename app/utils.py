import enum
import string
from datetime import datetime
from functools import wraps
from random import choice, randint

from bson.objectid import ObjectId
from flask import g, request
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError

from app.errors.exceptions import BadRequest, UnSupportedMediaType


def get_current_user():
    return getattr(g, 'user', None)


def generate_random_code(n=6):
    return ''.join([str(randint(0, 9)) for i in range(n)])


def generate_random_string(n=20):
    return ''.join([choice(string.ascii_lowercase) for i in range(n)])


def consumes(*content_types):
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.mimetype not in content_types:
                raise UnSupportedMediaType(message='Unsupported media type')
            return func(*args, **kwargs)
        return wrapper
    return decorated


def use_args(**schema):
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req_args = request.args.to_dict()
            if request.method in ('POST', 'PUT', 'PATCH', 'DELETE') \
                    and request.mimetype == 'application/json':
                req_args.update(request.get_json())
            req_args = {k: v for k, v in req_args.items(
            ) if k in schema['properties'].keys()}
            if 'required' in schema:
                for field in schema['required']:
                    if field not in req_args or not req_args[field]:
                        field_name = field
                        if field in schema['properties']:
                            if 'name' in schema['properties'][field]:
                                field_name = schema['properties'][field]['name']
                        raise BadRequest(message='{} is required'.format(field_name))
            try:
                validate(instance=req_args, schema=schema,
                         format_checker=FormatChecker())
            except ValidationError as exp:
                exp_info = list(exp.schema_path)
                error_type = ('type', 'format', 'pattern',
                              'maxLength', 'minLength')
                if set(exp_info).intersection(set(error_type)):
                    field = exp_info[1]
                    field_name = field
                    if field_name in schema['properties']:
                        if 'name' in schema['properties'][field]:
                            field_name = schema['properties'][field]['name']
                    message = '{} is not valid'.format(field_name)
                else:
                    message = exp.message  # pragma: no cover
                raise BadRequest(message=message)
            new_args = args + (req_args, )
            return func(*new_args, **kwargs)
        return wrapper
    return decorated


def get_model_value(val):
    if isinstance(val, ObjectId):
        return str(val)
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(val, enum.Enum):
        return val.value
    if isinstance(val, bytes):
        return str(val, 'utf-8')
    return val


def to_json(val):
    keys = val.keys()
    res = {
        k: get_model_value(val[k]) for k in keys
    }
    return res
