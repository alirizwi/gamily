from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jsonpify import jsonify
from instance.models import *
from instance import *

leaderboard = Flask(__name__)
leaderboard.config.from_object('leaderboard.config')
print leaderboard.config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(leaderboard)
from leaderboard import models
from leaderboard.models import *
leaderboard = Blueprint('leaderboard', 'leaderboard')
import requests
import json

#========= The above part will be more or less the same for all GDE =======#

# #========================= Non-route functions ============================#


#========================= Routes are defined below =======================#

@leaderboard.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Leader board module'

# @leaderboard.route('/users', methods=["GET"])
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

@leaderboard.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = User.query.filter_by(fullname=page).first()
    scores = UserScore.query.filter_by(user_id=user.id)
    leaderboard = []
    for score in scores:
        leaderboard = Leaderboard.query.filter_by(id=score.instance_id, type='leaderboard').first()
        temp_ = leaderboard.to_dict()
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

@leaderboard.route('/leaderboard/<page>')
def show_leaderboard(page, methods=["GET"]):
    leaderboard = Leaderboard.query.filter_by(name=page, type='leaderboard').first()
    scores = UserScore.query.filter_by(instance_id=leaderboard.id)
    users = []
    for score in scores:
        user = User.query.filter_by(id=score.user_id).first()
        temp_ = user.to_dict()
        temp_['score'] = score.score
        users.append(temp_)
    data = ({
        'id': leaderboard.id,
        'name': leaderboard.name,
        'description': leaderboard.description,
        'scores': users
    })
    return jsonify({
        'success': True,
        'message': 'Instanct exist',
        'data': data
    })

@leaderboard.route('/create', methods=["GET"])
def create_instance():
    try:
        # leaderboard = Leaderboard(request.form['name'], request.form['description'])
        leaderboard = Leaderboard(request.args['name'], request.args['description'])
        print request.args['name'], request.args['description']
        # print request.form['name'], request.form['description']
        db.session.add(leaderboard)
        db.session.commit()
    except Exception as e:
        print e
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'New leaderboard created successfully'
    })

@leaderboard.route('/list', methods=["GET"])
def show_all_leaderboard():
    leaderboard = Leaderboard.query.all()
    data = []
    for l in leaderboard:
        if l.type == 'leaderboard':
            print "l.id:", l.id
            print "l.type", l.type
            url = "http://127.0.0.1:5000/rules/list?id="+str(l.id)+"&type="+l.type
            print "url:", url
            r = requests.get(url=url)
            print "res: ", r.text
            obj = json.loads(r.text)

            print "obj: ", obj
            print len(obj['data'])
            data.append({
            'id': l.id,
            'name': l.name,
            'description': l.description,
            'type': l.type,
            'rule_count': len(obj['data'])
            })
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@leaderboard.route('/list/id/<id>', methods=["GET"])
def show_current_leaderboard(id):
    leaderboard = Leaderboard.query.filter_by(id=id, type='leaderboard').first()
    return leaderboard.name

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


@leaderboard.route('/give', methods=["POST"])
def give_score_to_user():
    try:
        user = find_user_force(request.form['username'])
        leaderboard = find_instance(request.form['leaderboard'])
        amount = int(request.form['amount'])
        existing = UserScore.query.filter_by(user_id=user.id, instance_id=Leaderboard.id).all()
        if len(existing) > 0:
            score_data = existing[0]
            score_data.score += amount
        else:
            score_data = UserScore(user, leaderboard, amount)
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
        leaderboard = find_instance(request.form['leaderboard'])
        amount = int(request.form['amount'])
        existing = UserScore.query.filter_by(user_id=user.id, instance_id=Leaderboard.id).all()
        if len(existing) > 0:
            score_data = existing[0]
            score_data.score -= amount
        else:
            score_data = UserScore(user, leaderboard, -1*amount)
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

@leaderboard.route('/user_score', methods=["GET"])
def show_all_user_score():
    user_scores = UserScore.query.all()
    data = []
    for user_score in user_scores:
        data.append(user_score.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@leaderboard.route('/get_level/<user>', methods=["GET"])
def get_level(user):
    user = User.query.filter_by(fullname=user).first()    
    user_scores = UserScore.query.filter_by(user_id=user.id).first()
    score = user_scores.score
    if(score>0 and score<=100):
        level = 1
        progress = score
    elif(score>100 and score<=200):
        level = 2
        progress = score/2
    elif(score>=300):
        level = 3
        progress = score/3
    data = {'level': level,
            'score': score,
            'progress': progress}
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })