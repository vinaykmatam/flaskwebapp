from flask.globals import request
from flask import redirect, url_for
from flask import flash
from sqlalchemy.sql.functions import user
from website import view
from flask import Blueprint,render_template
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Loged in sucessfuly!",category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Check password",category='error')
        else:
            flash("User Not Found! Please Sign Up to Login",category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Someone already used this mail,Try to signup with new Email or You have account already please login .',category='error')
        elif len(email) < 4:
           flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
           flash('first name must be greater than 2 characters.', category='error')
        elif password1 != password2:
           flash("password doesn't match.", category='error')
        elif len(password1)<7:
          flash('Password must be at least 7 characters.', category='error')
        else:   
          new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1,method='sha256')) 
          db.session.add(new_user)
          db.session.commit() 
          login_user(user, remember=True)
          flash('Accountt created!', category='success')
          return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)




