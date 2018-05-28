from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
from random import random
from flask_jsonpify import jsonify

avatar = Blueprint('avatar', 'avatar')

#========= The above part will be more or less the same for all GDE =======#


#========================= Routes are defined below =======================#

@avatar.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Avatar module'

@avatar.route('/random', methods=["GET"])
def send_static():
    print '128 ('+str(int(random()*42+1))+').jpg'
    return send_from_directory('avatar/images', '128 ('+str(int(random()*42+1))+').jpg')