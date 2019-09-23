import json
from datetime import datetime

from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from flask_cors import CORS


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


ma = Marshmallow()
flask_bcrypt = Bcrypt()
jwt_manager = JWTManager()
db = MongoEngine()
cors = CORS()
