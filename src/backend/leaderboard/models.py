from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, fullname):
        self.fullname = fullname

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.fullname
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
            'description': self.description,
            'type': 'leaderboard'
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
