from app.extensions import db

class Seq(db.Document):
    name = db.StringField(required=True, unique=True, max_length=200)
    value = db.IntField(required=True, unique=True)
    
    meta = {
        'collection': 'sequence',
        'indexes': [
            'name'
        ]
    }

    @staticmethod
    def getNextValue(seqName):
        doc = Seq.objects(name=seqName).modify(
                                        upsert=True,
                                        new=True,
                                        inc__value=1,
                                        set__name=seqName)
        return doc.value