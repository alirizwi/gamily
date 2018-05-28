from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jsonpify import jsonify

badge = Flask(__name__)
badge.config.from_object('badges.config')
print badge.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(badge)
from badges import models
from badges.models import *
badges = Blueprint('badges', 'badges')

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
    badge = Badge.query.filter_by(name=name).first()
    return badge

def delete_all_users(username):
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

#========================= Routes are defined below =======================#

@badges.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Badges module'

@badges.route('/users', methods=["GET"])
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

@badges.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = User.query.filter_by(fullname=page).first()
    badge_ids = UserBadge.query.filter_by(user_id=user.id)
    badges = []
    for b in badge_ids:
        badge = Badge.query.filter_by(id=b.badge_id).first()
        badges.append(badge.to_dict())
    data = ({
        'id': user.id,
        'name': user.fullname,
        'badges': badges
    })
    return jsonify({
        'success': True,
        'message': 'User exist',
        'data': data
    })

@badges.route('/create', methods=["GET", "POST"])
def create_badge():
    try:
        # badge = Badge(request.form['name'], request.form['description'], request.form['image_name'])
        print request.args['name'], request.args['description'], request.args['image_name']
        badge = Badge(request.args['name'], request.args['description'], request.args['image_name'])
        db.session.add(badge)
        print badge.id
        print "AA Gya"
        db.session.commit()
        print "AA Gya"
    except Exception as e:
        print e
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Badge added successfully'
    })

@badges.route('/list', methods=["GET"])
def show_all_badges():
    badges = Badge.query.all()
    data = []
    for badge in badges:
        data.append(badge.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })


@badges.route('/award', methods=["POST"])
def create_badge_user_mapping():
    try:
        user = find_user_force(request.form['username'])
        badge = find_badge(request.form['badge'])
        existing = UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).all()
        if len(existing) > 0:
            return jsonify({
                'success': False,
                'message': 'User already has this badge'
            })
        mapping = UserBadge(user, badge)
        db.session.add(mapping)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Badge awarded successfully'
    })

@badges.route('/static/<page>', methods=["GET"])
def send_static(page):
    return send_from_directory('badges/static', page)