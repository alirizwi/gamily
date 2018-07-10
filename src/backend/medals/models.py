from . import db
# Documentation : http://flask-sqlalchemy.pocoo.org/2.1/
from instance.models import User, Instance

class Medal(Instance):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), db.ForeignKey(Instance.id))
    # description = db.Column(db.String(256), db.ForeignKey(Instance.description))
    # image_name = db.Column(db.String(12))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        # self.image_name = image_name
        self.type = 'medal'
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

class MedalDetails(db.Model):
    __tablename__='medal_details'
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


class UserMedal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    medal_id = db.Column(db.Integer, index=True)

    def __init__(self, user, medal):
        self.user_id = user.id
        self.medal_id = medal.id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'medal_id': self.medal_id,
        }
