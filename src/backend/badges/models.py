from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/
from instance.models import User, Instance

class Badge(Instance):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), db.ForeignKey(Instance.id))
    # description = db.Column(db.String(256), db.ForeignKey(Instance.description))
    # image_name = db.Column(db.String(12))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        # self.image_name = image_name
        self.type = 'badge'
        # super().__init__(self)
        
    def getId(self):
        return self.id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            # 'image_name': self.image_name,
            'type': self.type
        }

class BadgeDetails(db.Model):
    __tablename__='badge_details'
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.Integer, db.ForeignKey(Instance.id))
    image_name = db.Column(db.String(256))

    def __init__(self, instance_id, image_name):
        self.instance_id = instance_id
        self.image_name = image_name
    
    def to_dict(self):
        return {
            'id': self.id,
            'instance_id': self.instance_id,
            'image_name': self.image_name
        }


class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    badge_id = db.Column(db.Integer, index=True)

    def __init__(self, user, badge):
        self.user_id = user.id
        self.badge_id = badge.id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'badge_id': self.badge_id,
        }
