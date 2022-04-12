from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from sweater import app, db, manager
from flask import render_template, request, flash, redirect, url_for

from sweater.models import User


@app.route( '/' , methods = ['GET','POST'] )
@app.route('/home',methods = ['GET','POST'])
def mainPage( ):
    login = request.form.get('login')
    password = request.form.get('password')
    modalIsActive = False;

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            #next_page = request.args.get('next')

            return render_template("index.html",modalIsActive=modalIsActive)
        else:
            flash('Login or password is not correct')
            modalIsActive = True;


    return render_template("index.html",modalIsActive=modalIsActive)

@app.route( '/about' )
def aboutPage( ):
    return render_template("about.html")

@app.route( '/contacts' )
def contactsPage( ):
    return render_template("contacts.html")

@app.route( '/buy' )
def buyPage( ):
    return render_template("buy.html")

@app.route( '/sell' )
def sellPage( ):
    return render_template("sell.html")

@app.route( '/registration',methods = ['GET','POST'])
def registrationPage(  ):
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')

    if request.method == 'POST':
        if not (login or password or password2 or email): #проверка на наличие всех полей
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)  #Хеширование пароля
            new_user = User(login=login, password=hash_pwd,email=email)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('mainPage'))
    return render_template("registration.html")

@app.route( '/account' )
def profilePage( ):
    return render_template("accountpage.html")

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('mainPage'))