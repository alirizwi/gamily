#!flask/bin/python
#This script will automatically create database migrations for you.
#Uncomment the badges and leadrboard according to the need (one at a time).

import imp
from migrate.versioning import api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

################## BADGES START ################
# from badges import models
# from badges import db
# from badges.config import SQLALCHEMY_DATABASE_URI
# from badges.config import SQLALCHEMY_MIGRATE_REPO
################## BADGES ENDS #################
############## LEADER BOARD STARTS #############
from leaderboard import models
from leaderboard import db
from leaderboard.config import SQLALCHEMY_DATABASE_URI
from leaderboard.config import SQLALCHEMY_MIGRATE_REPO
############## LEADER BOARD ENDS ###############
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))