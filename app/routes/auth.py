""" 
Author : A.I Instaraj
__retro__ : Information Systems
"""

from flask import *

import sys

from werkzeug.security import *

import jwt

from ..config import *

from ..models import *

sys.path.insert(0,'../../')

auth_ = Blueprint('auth',
            import_name='__name__',
            static_folder='./src',
            template_folder='./src/templates',
            url_prefix='/auth_'
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
    try:
        ses_name = session["name"]
        ses_mail = session["mail"]
        ses_pwd = session['pwd']
        ses_token = session['token']

        if ses_name and ses_mail and ses_pwd and ses_token:
            return redirect(url_for('index'))
        
    except Exception as E:
        if request.method == 'POST':
            form_name = request.form['user-name']
            form_mail = request.form['res-mail']
            form_res_ins = request.form["research-interest"]
            form_edu_level = request.form["academic-level"]
            form_pwd = request.form["res-pwd"]

            pwd_ = generate_password_hash(form_pwd,'scrypt')

            exist_user = user.query.filter_by(username = form_name).first()
            exist_mail = user.query.filter_by(mail=form_mail).first()

            if exist_user or exist_mail:
                print('User Exists')

                flash("Username or e-mail address already exists. Please choose another username or e-mail!.","error")

                return redirect(url_for('auth.login'))
            
            else:
                TokenHandler = Token()

                token = TokenHandler.generate_token(form_name,form_mail,pwd_)

                session['name'] = form_name
                session['mail'] = form_mail
                session['interest'] = form_res_ins
                session['level'] = form_edu_level
                session['pwd'] = pwd_
                session['token'] = token

                new_user = user(username = form_name, mail = form_mail,res_ins = form_res_ins,
                                acad_level = form_edu_level,password = pwd_, token = token)
                db.session.add(new_user)
                db.session.commit() 


                flash("Signup Sucessful!.","sucess")
                print(f'Account {form_name} Created Successfully')

                return redirect(url_for('auth.login'))
    return render_template('signup.html')


@auth_.route('/login',methods = ["GET","POST"])
def login():

    try:
        ses_name = session["name"]
        ses_mail = session["mail"]
        ses_pwd = session['pwd']
        ses_token = session['token']

        if ses_name and ses_mail and ses_pwd and ses_token:
            return redirect(url_for('index'))
        
    except Exception as E:

        if request.method == "POST":
            name_ = request.form["user-name"]
            mail_ = request.form['res-mail']
            pwd_ = request.form['res-pwd']

            User = user.query.filter_by(username = name_,mail = mail_).first()
            p = check_password_hash(User.password,pwd_)

            if User and p:
                flash('Login Successful!','sucess')

                session['name'] = User.username
                session['mail'] = User.mail
                session['interest'] = User.res_ins
                session['level'] = User.acad_level
                session['pwd'] = User.password
                session['token'] = User.token

                
                return redirect(url_for('index'))
        

            else:
                print(f'Password Incorrect{User.username}')
                flash('Invalid Username or Password', 'error')

                return redirect(url_for("auth.login"))
            
        return render_template('login.html')
    
@auth_.route('/logout')
def logout():
    
    session.pop("name")
    session.pop("mail")
    session.pop("interest")
    session.pop("level")
    session.pop("pwd")
    session.pop("token")


    return redirect(url_for('index'))

@auth_.route('/delete')
def delete_account():
    ses_name = session["name"]
    ses_mail = session["mail"]
    ses_pwd = session['pwd']
    ses_token = session['token']   
    User = user.query.filter_by(username = ses_name,mail = ses_mail,token = ses_token,password=ses_pwd).first()
    db.session.delete(User)
    db.session.commit()
    
    session.pop("name")
    session.pop("mail")
    session.pop("interest")
    session.pop("level")
    session.pop("pwd")
    session.pop("token")

    print(f"Account {ses_name} Successfully Deleted")
    
    return redirect(url_for('index'))
