from flask import Flask, request, redirect
import importlib
from flask_cors import CORS
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import string
import hashlib
import random
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

# Model for normal user
class Player(db.Model):
    __tablename__ = 'player'
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.fullname
        }

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

class Rule(db.Model):
    __tablename__ = 'rule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instance_id = db.Column(db.Integer, db.ForeignKey(Instance.id))
    action_id = db.Column(db.Integer, db.ForeignKey(Action.id))
    value = db.Column(db.String(256))

# Badges registering
from badges import badges
app.register_blueprint(badges, url_prefix='/badges')

# Leaderboard registering
from leaderboard import leaderboard
app.register_blueprint(leaderboard, url_prefix='/leaderboard')

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

app.run(debug=True)