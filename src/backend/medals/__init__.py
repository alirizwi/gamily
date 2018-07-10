from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jsonpify import jsonify

medal = Flask(__name__)
medal.config.from_object('medals.config')
print medal.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(medal)
from medals import models
from medals.models import *
medals = Blueprint('medals', 'medals')
import requests
import json

# from ..runserver import Player as User

# import sys
# sys.path.append("..")
# from runserver import Player as User
#========= The above part will be more or less the same for all GDE =======#

#========================= Non-route functions ============================#

def add_user(username):
    me = User(username)
    db.session.add(me)
    db.session.commit()
    return

def find_user_force(username):
    user = User.query.filter_by(fullname=username).first()
    if user is None:
        add_user(username)
        user = User.query.filter_by(fullname=username).first()
    return user

def find_badge(name):
    medal = Medal.query.filter_by(name=name).first()
    return medal

def delete_all_users(username):
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

#========================= Routes are defined below =======================#

@medals.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Medals module'

# @medals.route('/users', methods=["GET"])
# def show_all_users():
#     users = User.query.all()
#     data = []
#     for user in users:
#         data.append({
#             'id': user.id,
#             'name': user.fullname
#         })
#     return jsonify({
#         'success': True,
#         'message': '',
#         'data': data
#     })

@medals.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = User.query.filter_by(fullname=page).first()
    badge_ids = UserMedal.query.filter_by(user_id=user.id)
    medals = []
    for b in badge_ids:
        medal = Medal.query.filter_by(id=b.badge_id, type='medal').first()
        print medal
        medals.append(medal.to_dict())
    data = ({
        'id': user.id,
        'name': user.fullname,
        'medals': medals
    })
    return jsonify({
        'success': True,
        'message': 'User exist',
        'data': data
    })

@medals.route('/create', methods=["GET"])
def create_badge():
    try:
        # medal = Medal(request.form['name'], request.form['description'], request.form['image_name'])
        # print request.form['name'], request.form['description'], request.form['image_name']
        medal = Medal(request.args['name'], request.args['description'])
        print "medal id:", medal.id
        print "medal ID:", medal.getId()
        db.session.add(medal)
        db.session.commit()
        print "medal id2:", medal.id
        print "medal ID2:", medal.getId()        
        badge_details = MedalDetails(medal.getId(), request.args['image_name'])
        print request.args['name'], request.args['description'], request.args['image_name']
        db.session.add(badge_details)
        db.session.commit()
    except Exception as e:
        print e
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Medal added successfully'
    })

@medals.route('/list', methods=["GET"])
def show_all_badges():
    medals = Medal.query.all()
    data = []
    for medal in medals:
        if medal.type == 'medal':
            print "medal.id:", medal.id
            print "medal.type", medal.type
            url = "http://127.0.0.1:5000/rules/list?id="+str(medal.id)+"&type="+medal.type
            print "url:", url
            r = requests.get(url=url)
            print "res: ", r.text
            obj = json.loads(r.text)

            print "obj: ", obj
            print len(obj['data'])
            data.append({
            'id': medal.id,
            'name': medal.name,
            'description': medal.description,
            'type': medal.type,
            'rule_count': len(obj['data'])
            })
        # data.append(medal.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@medals.route('/list/id/<id>', methods=["GET"])
def show_current_badge(id):
    print "id:", id
    medal = Medal.query.filter_by(id=id).first()
    print medal.name
    return medal.name

@medals.route('/actions', methods=["GET"])
def show_all_badge_actions():
    data = []
    data.append({'name': 'award'})
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@medals.route('/award', methods=["POST"])
def create_badge_user_mapping():
    try:
        user = find_user_force(request.form['username'])
        medal = find_badge(request.form['medal'])
        existing = UserMedal.query.filter_by(user_id=user.id, badge_id=medal.id).all()
        if len(existing) > 0:
            return jsonify({
                'success': False,
                'message': 'User already has this medal'
            })
        mapping = UserMedal(user, medal)
        db.session.add(mapping)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Medal awarded successfully'
    })

@medals.route('/user_badges', methods=["GET"])
def show_all_user_badges():
    user_badges = UserMedal.query.all()
    data = []
    for user_badge in user_badges:
        data.append(user_badge.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@medals.route('/static/<page>', methods=["GET"])
def send_static(page):
    return send_from_directory('medals/static', page)