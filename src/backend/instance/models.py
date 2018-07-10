from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, fullname):
        self.fullname = fullname

    def to_dict(self):
        return {
            'id': self.id,
            'fullname': self.fullname
        }

class Instance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    type = db.Column(db.String(64))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type
        }