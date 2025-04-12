""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

from ..logic.research import *

import sys

import jwt

from werkzeug.security import *

from ..logic.scrap import *

from ..logic.search import *

from ..logic.pdf_logic import *

from ..logic.AI_Logic import *

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
            papers = get_papers(topic)
            papers = add_link(papers)
            
            return jsonify(papers)
        
        except Exception as E:
            return 'Error! Network Failure'    
    else:
        return 'Error! Unauthorized Access'

@logic_.route('/paper/<doi>')
def paper(doi):
    doi = decode_url(doi)
    paper = get_doi(doi)
    return render_template('paper.html', paper = paper)

@logic_.route('/analyze/<doi>', methods = ['GET','POST'])
def analyze(doi):
    auth_user = session.get("token")
    if auth_user:
        doi = decode_url(doi)
        paper = get_doi(doi)
        link = get_pdf(paper['pdf'],doi)
        content = get_content(link)
        analysis = get_analysis(content)
        pdf_link = set_pdf(analysis['pdf'],doi)
        return jsonify(analysis['html'])
    else:
        return redirect(url_for('auth/login'))