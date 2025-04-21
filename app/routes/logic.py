""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

from ..logic.scrap.research import *

import sys

import html

from langchain.schema import AIMessage

from werkzeug.security import *

from ..logic.scrap.scrap import *

from ..logic.scrap.search import *

from ..logic.AI.pdf_logic import *

from ..logic.AI.AI_Logic import *

from ..logic.AI.AI_Chat import *

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
        return redirect(url_for('auth.login'))
    

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
        doi = decode_url(doi)
        paper = get_doi(doi)
        #paper = {'title': 'OSCAR: Online Soft Compression And Reranking', 'authors': ['Maxime Louis', 'Thibault Formal', 'Hervé Dejean', 'Stéphane Clinchant'], 'date': '17 Mar 2025', 'url': "https://arxiv.org/abs/2504.07109", 'doi': 'arXiv:2504.07109', 'pdf': "https://arxiv.org/pdf/2504.07109", 'abstract': 'Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs) by integrating external knowledge, leading to improved accuracy and relevance. However, scaling RAG pipelines remains computationally expensive as retrieval sizes grow. To address this, we introduce OSCAR, a novel query-dependent online soft compression method that reduces computational overhead while preserving performance. Unlike traditional hard compression methods, which shorten retrieved texts, or soft compression approaches, which map documents to continuous embeddings offline, OSCAR dynamically compresses retrieved information at inference time, eliminating storage overhead and enabling higher compression rates. Additionally, we extend OSCAR to simultaneously perform reranking, further optimizing the efficiency of the RAG pipeline. Our experiments demonstrate state-of-the-art performance with a 2-5x speed-up in inference and minimal to no loss in accuracy for LLMs ranging from 1B to 24B parameters. The models are available at: this https URL.', 'field': ['Information Retrieval', 'Artificial Intelligence', 'Computation and Language']}
        return render_template('paper.html', paper = paper,auth = auth_user)
    else:
        return redirect(url_for('auth.login'))

@logic_.route('/analyze/', methods = ['GET','POST'])
def analyze():

    auth_user = request.get_json()['user']

    doi = request.get_json()['doi']

    if auth_user:
        
        paper = get_doi(doi)
        analysis = get_analysis(paper)
        try:
            set_pdf(analysis,doi)

        except Exception as E:
            return E

        return Response(analysis, mimetype='text/html')
    
    else:

        return redirect(url_for('auth.login'))
    
    
@logic_.route('/sum-download/<doi>')
def summary(doi):

    doi = decode_url(doi)

    try:
        pdf_path = f"Dynax!-{doi}.pdf"

        return send_from_directory(
            app.config['PDF_FOLDER'], pdf_path)
    
    except Exception as E:

        paper = get_doi(doi)
        Analysis = get_analysis(paper)
        set_pdf(Analysis,doi)

        pdf_path_x = f"Dynax!-{doi}.pdf"

        return send_from_directory(
            app.config['PDF_FOLDER'], pdf_path_x
        )
    

@logic_.route('/chat')
def chat():
    auth_user = session.get("token")

    if auth_user:
        return render_template('chat.html', auth = auth_user)
    else:
        return redirect(url_for('auth.login'))
    

@logic_.route('/bot', methods=['POST'])
def bot():
    auth_user = session.get("token")

    response = request.get_json()
    msg = response['msg']

    content = research(auth_user, msg)['message']

    if isinstance(content, AIMessage):
        return jsonify({"response": html.escape(content.content.replace("```html",'').replace("```",""))})
    elif isinstance(content, dict):
        return jsonify({"response": content.get("output", str(content))})
    else:
        return jsonify({"response": str(content)})