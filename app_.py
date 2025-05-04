from flask import *

from app.models import *

from app.routes.auth import *

from app.routes.logic import *

app = Flask(__name__,
            static_folder='src/assets',
            template_folder='src/templates')

app.config.from_pyfile('app/config.py')

db.init_app(app)

app.register_blueprint(auth_,url_prefix='/auth')

app.register_blueprint(logic_)

@app.route('/',methods = ['GET'])
def index():
    auth_user = session.get("token")
    return render_template('index.html',auth = auth_user)

@app.route('/about')
def about():
    auth_user = session.get("token")
    return render_template('about.html',auth = auth_user)

@app.errorhandler(404)
def PageError(error):
    auth_user = session.get("token")
    return render_template('404.html',auth = auth_user)

@app.errorhandler(500)
def ServerError(error):
    print(error)
    auth_user = session.get("token")
    return render_template('500.html',auth = auth_user)

@app.errorhandler(Exception)
def Error(e):
    print(e)
    auth_user = session.get("token")
    return render_template('500.html',auth = auth_user),500

@app.route('/favicon.ico')
def icon():
    return send_from_directory(directory=app.config["STATIC_FOLDER"],path="img/favicon.ico")

@app.route('/robots.txt')
def robots():
    return send_from_directory(directory=app.config["STATIC_FOLDER"],path="info/robots.txt")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5425))
    app.run(debug=True,host='0.0.0.0',port=port)
