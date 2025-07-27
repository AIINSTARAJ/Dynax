""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

from werkzeug.security import *

from flask_mail import *

import sys

from ..config import *

from ..models import *

sys.path.insert(0,'../../')

admin = Blueprint('admin',
            import_name='__name__',
            static_folder='./src',
            template_folder='./src/templates',
            url_prefix='/admin'
            )


mail = Mail()
   

@admin.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    try:
        name = session["name"]
        email = session["mail"]

    except Exception as E:
        name = data.get('name')
        email = data.get('email')
        print(E)

    message = data.get('message')

    try:
        msg = Message(subject=f'New Message from {name}',
                      recipients=['tomjayray05@gmail.com'],
                      html = render_template("msg.html", name = name, email = email, message = message)
        )
        mail.send(msg)
        return jsonify({'message': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/view')
def view():
    auth_user = session.get('token','')

    if auth_user != '':
        return redirect(url_for('auth.login'))
    else:
        users = User.query.order_by(User.auth_date).all()
        return render_template('view.html',users=users)
    
@admin.post('/delete/<int:id>')
def delete(id):
    auth_user = session.get('token','')

    if auth_user != '':
        return redirect(url_for('auth.login'))
    else:
        user = User.query.get_or_404(id)

        db.session.delete(user)
        db.session.commit()
        
        return redirect(url_for('view'))

