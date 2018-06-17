from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jsonpify import jsonify

leaderboard = Flask(__name__)
leaderboard.config.from_object('leaderboard.config')
print leaderboard.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(leaderboard)
from leaderboard import models
from leaderboard.models import *
leaderboard = Blueprint('leaderboard', 'leaderboard')

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

@leaderboard.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Leader board module'

@leaderboard.route('/users', methods=["GET"])
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

@leaderboard.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = User.query.filter_by(fullname=page).first()
    scores = UserScore.query.filter_by(user_id=user.id)
    leaderboard = []
    for score in scores:
        instance = Instance.query.filter_by(id=score.instance_id).first()
        temp_ = instance.to_dict()
        temp_['score'] = score.score
        leaderboard.append(temp_)
    data = ({
        'id': user.id,
        'name': user.fullname,
        'scores': leaderboard
    })
    return jsonify({
        'success': True,
        'message': 'User exist',
        'data': data
    })

@leaderboard.route('/instance/<page>')
def show_leaderboard(page, methods=["GET"]):
    instance = Instance.query.filter_by(name=page).first()
    scores = UserScore.query.filter_by(instance_id=instance.id)
    users = []
    for score in scores:
        user = User.query.filter_by(id=score.user_id).first()
        temp_ = user.to_dict()
        temp_['score'] = score.score
        users.append(temp_)
    data = ({
        'id': instance.id,
        'name': instance.name,
        'description': instance.description,
        'scores': users
    })
    return jsonify({
        'success': True,
        'message': 'Instanct exist',
        'data': data
    })

@leaderboard.route('/create', methods=["POST"])
def create_instance():
    try:
        instance = Instance(request.form['name'], request.form['description'])
        # instance = Instance(request.args['name'], request.args['description'])
        print request.form['name'], request.form['description']
        db.session.add(instance)
        db.session.commit()
    except Exception as e:
        print e
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'New instance created successfully'
    })

@leaderboard.route('/list', methods=["GET"])
def show_all_leaderboard():
    leaderboard = Instance.query.all()
    data = []
    for l in leaderboard:
        data.append(l.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@leaderboard.route('/actions', methods=["GET"])
def show_all_leaderboard_actions():
    data = []
    data.append({'name': 'give'})
    data.append({'name': 'take'})
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })


@leaderboard.route('/give', methods=["POST","GET"])
def give_score_to_user():
    try:
        # user = find_user_force(request.form['username'])
        # instance = find_instance(request.form['instance'])
        # amount = int(request.form['amount'])
        user = find_user_force(request.args['username'])
        instance = find_instance(request.args['instance'])
        amount = int(request.args['amount'])
        existing = UserScore.query.filter_by(user_id=user.id, instance_id=Instance.id).all()
        if len(existing) > 0:
            score_data = existing[0]
            score_data.score += amount
        else:
            score_data = UserScore(user, instance, amount)
            db.session.add(score_data)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Points awarded successfully'
    })


@leaderboard.route('/take', methods=["POST"])
def take_score_from_user():
    try:
        user = find_user_force(request.form['username'])
        instance = find_instance(request.form['instance'])
        amount = int(request.form['amount'])
        existing = UserScore.query.filter_by(user_id=user.id, instance_id=Instance.id).all()
        if len(existing) > 0:
            score_data = existing[0]
            score_data.score -= amount
        else:
            score_data = UserScore(user, instance, -1*amount)
            db.session.add(score_data)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Points taken successfully'
    })
