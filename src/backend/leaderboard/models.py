from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/
from instance.models import User, Instance


class Leaderboard(Instance):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), index=True, unique=True)
    # description = db.Column(db.String(256))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.type = 'leaderboard'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type
        }

class Levels(Instance):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), index=True, unique=True)
    # description = db.Column(db.String(256))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.type = 'levels'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type
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

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'instance_id': self.instance_id,
            'score': self.score
        }
