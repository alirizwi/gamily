from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, nickname):
        self.nickname = nickname

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.nickname
        }


class Instance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    instance_id = db.Column(db.Integer, index=True)
    score = db.Column(db.Integer)

    def __init__(self, user, instance, score):
        self.user_id = user.id
        self.instance_id = instance.id
        self.score = score
