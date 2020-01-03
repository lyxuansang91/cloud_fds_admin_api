import os  # noqa
from datetime import datetime

from app.extensions import db


class Block(db.Document):
    currency = db.StringField(required=True)
    height = db.IntField(required=True)
    createdAt = db.DateTimeField(required=True, default=datetime.utcnow)
    updatedAt = db.DateTimeField()

    meta = {
        'collection': 'block',
        'indexes': ['currency', '-createdAt']
    }

    @staticmethod
    def get_current_block(currency):
        block = Block.objects(currency=currency).first()
        if block is None:
            latest_block = int(os.environ.get('ETH_LATEST_BLOCK', 0))
            block = Block(currency=currency, height=latest_block, updatedAt=datetime.utcnow())
            block.save()
        return block
