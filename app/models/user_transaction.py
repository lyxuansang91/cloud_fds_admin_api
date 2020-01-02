from datetime import datetime
from app.extensions import db


class UserTransaction(db.Document):
    userId = db.ObjectIdField()
    fromAddress = db.StringField(required=True, max_length=200)
    fromCurrency = db.StringField(required=True, max_length=20)
    toAddress = db.StringField(required=True, max_length=200)
    toCurrency = db.StringField(required=True, max_length=20)
    amount = db.DecimalField(required=True, precision=10)
    transactionType = db.StringField(required=True, default="deposit", regex=r'^(deposit|withdrawal)$')
    outputIndex = db.IntField(default=0)
    txHash = db.StringField(required=False, max_length=200)
    createdAt = db.DateTimeField(default=datetime.utcnow)
    updatedAt = db.DateTimeField()

    meta = {
        'collection': 'userTransaction',
        'indexes': [
            'userId',
            'fromAddress',
            'fromCurrency',
            'toCurrency',
            'toAddress',
            '-createdAt',
        ]
    }
