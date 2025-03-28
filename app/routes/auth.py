""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

import sys

from werkzeug.security import *

import jwt

from ..config import *

sys.path.insert(0,'../../')

auth_ = Blueprint('auth',
            import_name='__name__',
            static_folder='./src',
            template_folder='./src/templates',
            url_prefix='auth_'
            )

class Token:
    def __init__(self):
        self.secret_key = SECRET_KEY

    def generate_token(self,name,mail,pwd):
        data = jwt.encode({'name': name,'mail':mail,'pwd':pwd},self.secret_key,algorithm='HS256')
        return data

    def verify_token(self,token):
        try:
            data = jwt.decode(token,self.secret_key,algorithms=['HS256'])
            return data['name']
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
    


@auth_.route('/signup',methods = ["GET","POST"])
def signup():
    pass