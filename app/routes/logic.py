""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

from ..logic.research import *

import sys

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

    if auth_user:
        return render_template('search.html', auth = auth_user)
    else:
        return redirect(url_for('auth/login'))

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
            print(E)
            return 'Error! Network Failure'    
    else:
        return 'Error! Unauthorized Access'

@logic_.route('/paper/<doi>')
def paper(doi):
    auth_user = session.get('token')
    if auth_user:
        '''doi = decode_url(doi)
        paper = get_doi(doi)'''
        paper = {'title': 'Learning Robotics, with Robotics, by Robotics', 'authors': 'Ilaria Gaudiello, Elisabetta Zibetti', 'date': 'April 2016', 'citations': 26, 'url': 'https://doi.org/10.1002/9781119335740', 'abstract': 'Endometrial cancer is the most common gynecological cancer in women in most of the developed world. The majority of these women with endometrial cancer will be unaffected by their disease. The challenge therefore is for surgical treatment not to be worse than the disease. Robotics has changed the way that we care for women living with endometrial cancer by making low-impact surgical treatment available to more women than was previously possible.', 'doi': '10.1002/9781119335740', 'publisher': 'Wiley', 'publication': 'Not available', 'journal_type': 'monograph','field':'Machine Learning, Artificial Intelligence','pdf':'https://arxiv.org/pdf/2450.1842'}
        return render_template('paper.html', paper = paper)
    else:
        return redirect(url_for('auth/login'))

@logic_.route('/analyze/<doi>', methods = ['GET','POST'])
def analyze(doi):

    auth_user = request.get_json()['user']

    if auth_user:

        doi = decode_url(doi)

        analysis = get_analysis(doi)
        pdf_link = set_pdf(analysis['pdf'],doi)

        return jsonify(analysis['html'])
    
    else:

        return redirect(url_for('auth/login'))
    
    
@logic_.route('/sum-download/<doi>')
def summary(doi):

    doi = decode_url(doi)

    try:
        pdf_path = f"Dynax!-{doi}.pdf"

        return send_from_directory(
            app.config['SUMMARY FOLDER'], pdf_path)
    
    except Exception as E:

        Analysis = get_analysis(doi)
        link = set_pdf(Analysis['pdf'],doi)

        pdf_path_x = f"Dynax!-{doi}.pdf"

        return send_from_directory(
            app.config['PDF_FOLDER'], pdf_path_x
        )
    
