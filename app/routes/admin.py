""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

from werkzeug.security import *

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

