""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

import sys

from werkzeug.security import *

from ..logic.scrap import *

from ..logic.search import *

from .auth import Token

sys.path.insert(0,'../../')

logic_ = Blueprint('logic',
            import_name='__name__',
            static_folder='./src',
            template_folder='./src/templates'
            )

@logic_.route('/search')
def search():
    auth_user = session.get("token")
    return render_template('search.html', auth = auth_user)

@logic_.route('/scrap',methods=['POST','GET'])
def scrap():
    auth = session['token']
    auth = Token().verify_token(auth)

    if auth != False:

        data = request.get_json()
        topic = data['message']

        try:
            papers = search_publications(topic)
            return jsonify(papers)
        
        except Exception as E:
            print(E)
            return 'Error! Network Failure'
        
    else:
        return 'Error! Unauthorized Access'

@logic_.route('/analyze', methods = ['GET','POST'])
def analyze():
    auth_user = session.get("token")
    return render_template('analyze.html', auth = auth_user)