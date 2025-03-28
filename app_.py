from flask import *

from app.models import *

from app.routes.auth import *

from app.routes.logic import *

app = Flask(__name__,
            static_folder='src/assets',
            template_folder='src/templates')

app.config.from_pyfile('app\\config.py')

db.init_app(app)

app.register_blueprint(auth_,url_prefix='/auth_')

app.register_blueprint(logic_)

@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def icon():
    return send_from_directory(directory=app.config["STATIC_FOLDER"],path="img/favicon.ico")

@app.route('/robots.txt')
def robots():
    return send_from_directory(directory=app.config["STATIC_FOLDER"],path="info/robots.txt")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5425)
