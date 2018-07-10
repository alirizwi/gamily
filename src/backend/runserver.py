from flask import Flask, request, redirect
import importlib
from flask_cors import CORS
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import string
import hashlib
import random
import requests
from validate_email import validate_email
from flask_jsonpify import jsonify

app = Flask(__name__)
CORS(app)
app.secret_key = '~X@H!jmM]Lwf/,?KTF12Zr47jsd8u3hj\3yX'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:galaxyj5@localhost/gamily'

db = SQLAlchemy(app)

########################################
################ MODELS ################
########################################

# Model for admin
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    fullname = db.Column(db.String(120))
    validate_hash = db.Column(db.String(120))
    is_validated = db.Column(db.Integer, default=0)

    def __init__(self, email, password, fullname):
        self.fullname = fullname
        self.email = email
        self.password = self.encrypt_password(password)
        self.create_random_hash()

    def encrypt_password(self, password):
        hash = hashlib.md5()
        hash.update(password)
        return hash.hexdigest()

    def verify(self, hash):
        if self.validate_hash == hash:
            self.is_validated = True
            return True
        return False

    def login(self, password):
        if self.password == self.encrypt_password(password):
            return True
        return False

    def is_verified(self):
        return self.is_validated

    def create_random_hash(self):
        lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(60)]
        self.validate_hash = "".join(lst)

    def get_hash(self):
        return self.validate_hash

    def __repr__(self):
        return '<User %r>' % self.email

class GDE(db.Model):
    __tablename__ = 'gde'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    path = db.Column(db.String(120), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path
        }

class Action(db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    path = db.Column(db.String(20))
    meaning = db.Column(db.String(20))
    gde = db.Column(db.Integer, db.ForeignKey(User.id))
    need = db.Column(db.String(120))

class Instance(db.Model):
    __tablename__ = 'instance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gde_id = db.Column(db.Integer, db.ForeignKey(GDE.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

# class Rule(db.Model):
#     __tablename__ = 'rule'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     instance_id = db.Column(db.Integer, db.ForeignKey(Instance.id))
#     action_id = db.Column(db.Integer, db.ForeignKey(Action.id))
#     value = db.Column(db.String(256))

class Rule(db.Model):
    __tablename__ = 'rule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    action = db.Column(db.String(20))
    meaning = db.Column(db.String(256))
    value = db.Column(db.String(256))
    event = db.Column(db.String(256))
    gde_id = db.Column(db.Integer, db.ForeignKey(GDE.id))
    gde_type = db.Column(db.String(20))

    def __init__(self, name, action, meaning, value, event, gde_id, gde_type):
        self.name = name
        self.action = action
        self.meaning = meaning
        self.value = value
        self.event = event
        self.gde_id = gde_id
        self.gde_type = gde_type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'action': self.action,
            'meaning': self.meaning,
            'value': self.value,
            'event': self.event,
            'gde_id': self.gde_id,
            'gde_type': self.gde_type
        }    

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    type = db.Column(db.String(64))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        } 

class Hooks(db.Model):
    __tablename__ = 'hooks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    type = db.Column(db.String(64))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        }    

# Instance registering
from instance import instance
app.register_blueprint(instance, url_prefix='/instance')

# Badges registering
from badges import badges
app.register_blueprint(badges, url_prefix='/instance/badge')

# Badges registering
from medals import medals
app.register_blueprint(medals, url_prefix='/instance/medal')

# Leaderboard registering
from leaderboard import leaderboard
app.register_blueprint(leaderboard, url_prefix='/instance/leaderboard')

# Avatar registering
from avatar import avatar
app.register_blueprint(avatar, url_prefix='/avatar')


def send_verification_email(email, fullname, hash):
    import smtplib
    sender = 'syedmohdali.rizwi@students.iiit.ac.in'
    receivers = [email]

    message = """From: 'Syed Mohd Ali Rizwi <'syedmohdali.rizwi@students.iiit.ac.in'>
To: """ + fullname + """ <""" + email + """>
Subject: Gamily account verification

Thanks for registering your Gamily account. Please verify your email by opening the following link:
http://app.gamily.in/backend/verify/""" + email + """/""" + hash + """

If you have not registered Gamily account. Please ignore this email.

--
Gamily
Gamification for all
"""
    try:
        smtpObj = smtplib.SMTP('students.iiit.ac.in')
        smtpObj.set_debuglevel(False)
        smtpObj.login('syedmohdali.rizwi', '')
        try:
            smtpObj.sendmail(sender, receivers, message)
        finally:
            smtpObj.quit()
        return True
    except smtplib.SMTPException:
        return False

def email_not_used(email):
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return False
    return True

@app.route('/register', methods=["POST"])
def register():
    msg_e = []
    msg_s = ['Registration successful. Please verify your email ID.']
    fullname = request.form.get('fullname', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not validate_email(email):
        msg_e.append('Invalid Email ID used.')
    if not len(fullname) > 0:
        msg_e.append('Please fill Full Name.')
    if not len(password) > 0:
        msg_e.append('Please choose some password.')

    try:
        if len(msg_e) == 0 and email_not_used(email):
            new_user = User(email=email, password=password, fullname=fullname)
            if not send_verification_email(email, fullname, new_user.get_hash()):
                new_user.verify(new_user.get_hash())
                msg_s = ['Registration successful. Please login.']
            db.session.add(new_user)
            db.session.commit()
        else:
            msg_e.append('Email already registered.')
    except exc.IntegrityError:
        msg_e.append('This email is already registered.')

    if len(msg_e) > 0:
        return jsonify({
            'success': False,
            'message': msg_e
        })
    else:
        return jsonify({
            'success': True,
            'message': msg_s
        })

@app.route('/verify/<email>/<hash>', methods=["GET"])
def verify_email(email, hash):
    try:
        user = User.query.filter_by(email=email).first()
        if not user.is_verified():
            if user.verify(hash):
                session['user'] = user.id
                db.session.add(user)
                db.session.commit()
                return redirect("http://app.gamily.in/", code=302)
            else:
                return 'Wrong hash. Kindly recheck your email!'
        else:
            return 'You were already verified. :)'
    except:
        return 'User not found. Are you sure you had registered?<br><br>Please contact administrator at shivam.khandelwal@research.iiit.ac.in'

@app.route('/sign', methods=["POST"])
def sign_in():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    try:
        user = User.query.filter_by(email=email).first()
        if not user.is_verified():
                return jsonify({
                    'success': False,
                    'message': ['Please verify your email ID.']
                })
        if user.login(password):
            session['user'] = user.id
            return jsonify({
                'success': True
            })
    except:
        pass
    return jsonify({
        'success': False,
        'message': ['Wrong email/password combination.']
    })

@app.route('/logout', methods=["GET"])
def sign_out():
    session['user'] = ''
    return jsonify({
        'success': True
    })

@app.route('/check', methods=["GET"])
def is_logged_in():
    try:
        if session['user'] != '':
            user = User.query.filter_by(id=session['user']).first()
            response = jsonify({
                'success': True,
                'user': {
                    'fullname': user.fullname,
                    'email': user.email
                }})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except:
        pass
    return jsonify({
                'success': False,
                'user': {
                    'fullname': 'Shivam Khandelwal',
                    'email': 'sk@students.iiit.ac.in'
                }})

@app.route('/gde/list', methods=["GET"])
def show_all_gdes():
    gdes = GDE.query.all()
    data = []
    for gde in gdes:
        data.append(gde.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@app.route('/rules/list', methods=["GET"])
def show_all_rules():
    print request.args['id'], request.args['type']
    # rule = Rule.query.all()
    rule = Rule.query.filter_by(gde_type=request.args['type'], gde_id=request.args['id'])
    data = []
    for r in rule:
        data.append(r.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@app.route('/rules/create', methods=["POST"])
def create_rules():
    try:
        rule = Rule(request.form['name'], request.form['action'], request.form['meaning'], request.form['value'], request.form['event'],request.form['gde_id'],request.form['gde_type'])
        # instance = Instance(request.args['name'], request.args['description'])
        print request.form['name'], request.form['value'], request.form['gde_id']
        db.session.add(rule)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'New Rule created successfully'
        })
    except Exception as e:
        print e
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })

@app.route('/events/list', methods=["GET"])
def show_all_events():
    events = Events.query.all()
    data = []
    for event in events:
        data.append(event.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

def get_events_listening_to_hook(hook):
    events = Events.query.filter_by(name=hook).all()
    return events

def rule_depending_on_event(event):
    rules = Rule.query.filter_by(event=event).all()
    return rules

@app.route('/hooks', methods=["POST"])
def hooks_function():
    try:
        events = get_events_listening_to_hook(request.form['hook_name'])
        username = request.form['username']
        print "Events:", events
        if len(events) == 0:
            return jsonify({
                'success': False,
                'message': 'No event exist with that name!!'
            })            
        print  "Username:", username
        for event in events:
            print event.name
            rules = rule_depending_on_event(event.name)
            print "Rules:" ,rules
            for rule in rules:
                print rule.name, rule.gde_type, rule.action

                if rule.gde_type == 'leaderboard':
                    print "LB"
                    gde_url = 'http://localhost:5000/instance/leaderboard/list/id/'+str(rule.gde_id)
                    print "gde url", gde_url
                    r = requests.get(url=gde_url)
                    data = r.text
                    print "Res:", data

                    url = 'http://localhost:5000/instance/leaderboard/'+rule.action
                    print "url:", url
                    data = {'username': username,
                            'instance': data,
                            'amount': 10}
                    r = requests.post(url=url, data=data)
                    print "R:", r.text

                elif rule.gde_type == 'badge':
                    print "B"
                    gde_url = 'http://localhost:5000/instance/badge/list/id/'+str(rule.gde_id)
                    print "gde url", gde_url
                    r = requests.get(url=gde_url)
                    data = r.text
                    print "Res:", data

                    url = 'http://localhost:5000/instance/badges/'+rule.action
                    print "url:", url
                    data = {'username': username,
                            'badge': data}
                    r = requests.post(url=url, data=data)
                    print "R:", r.text   
        return jsonify({
            'success': True,
            'message': 'Successful'
        })             

    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })


app.run(debug=True)