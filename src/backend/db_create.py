#!flask/bin/python
#This script will automatically setup database for you, in your new GDE
#Uncomment the badges and leadrboard according to the need (one at a time).

from migrate.versioning import api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

################## BADGES START ################
from badges.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from badges import db
################## BADGES ENDS #################
############## LEADER BOARD STARTS #############
# from leaderboard.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
# from leaderboard import db
############## LEADER BOARD ENDS ###############

import os.path
db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))