from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jsonpify import jsonify

instance = Flask(__name__)
instance.config.from_object('instance.config')
print instance.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(instance)

from instance import models
from instance.models import *
instance = Blueprint('instance', 'instance')

#========= The above part will be more or less the same for all GDE =======#

#========================= Non-route functions ============================#

def add_user(username):
    me = User(username)
    db.session.add(me)
    db.session.commit()
    return

def find_user(username):
    user = User.query.filter_by(fullname=username).first()
    return user

def find_user_force(username):
    user = User.query.filter_by(fullname=username).first()
    if user is None:
        add_user(username)
        user = User.query.filter_by(fullname=username).first()
    return user

def find_instance(name):
    instance = Instance.query.filter_by(name=name).first()
    return instance

def delete_all_users(username):
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

#========================= Routes are defined below =======================#

@instance.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Instance module'

@instance.route('/users', methods=["GET"])
def show_all_users():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'name': user.fullname
        })
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

# @instance.route('/create', methods=["GET"])
# def create_instance():
#     try:
#         # instance = Instance(request.form['name'], request.form['description'], request.form['type'])
#         instance = Instance(request.args['name'], request.args['description'], request.args['description'])
#         # print request.form['name'], request.form['description'], request.form['type']
#         db.session.add(instance)
#         db.session.commit()
#     except Exception as e:
#         print e
#         return jsonify({
#             'success': False,
#             'message': 'Something went wrong :('
#         })
#     return jsonify({
#         'success': True,
#         'message': 'New instance created successfully'
#     })

@instance.route('/list', methods=["GET"])
def show_all_instances():
    instance = Instance.query.all()
    data = []
    for l in instance:
        data.append(l.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@instance.route('/list/id/<id>', methods=["GET"])
def show_current_instances(id):
    instance = Instance.query.filter_by(id=id).first()
    return instance.name

@instance.route('/list/<type>', methods=["GET"])
def show_current_type_instances(type):
    instance = Instance.query.filter_by(type=type).all()
    return instance
