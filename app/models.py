import sys 

sys.path.insert(0,'../../')

from sqlalchemy.sql import *

from werkzeug.security import *

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(12),nullable = False)
    mail = db.Column(db.String(48),nullable = False)
    res_ins = db.Column(db.String(48),nullable = False)
    acad_level = db.Column(db.String(48),nullable = False)
    password = db.Column(db.String(128),nullable = False)
    token = db.Column(db.String(100),nullable = False)
    auth_date = db.Column(db.DateTime(timezone=True), server_default = func.now())

    def __repr__(self):
        return f'<user {self.username}>'