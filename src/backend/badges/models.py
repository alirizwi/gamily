from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, fullname):
        self.fullname = fullname

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    image_name = db.Column(db.String(12))

    def __init__(self, name, description, image_name):
        self.name = name
        self.description = description
        self.image_name = image_name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_name': self.image_name,
            'type': 'badge'
        }

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    badge_id = db.Column(db.Integer, index=True)

    def __init__(self, user, badge):
        self.user_id = user.id
        self.badge_id = badge.id
