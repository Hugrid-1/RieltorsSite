import os

from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from sweater import app, db, manager, ALLOWED_EXTENSIONS, photos
from flask import render_template, request, flash, redirect, url_for, send_from_directory

from sweater.models import User, Realty


def passwordCorrectCheck(password):  ############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!NEED TO CREATE!!!!!!!!!!!!!!!!!
    return True

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def mainPage():
    login = request.form.get('login')
    password = request.form.get('password')
    modalIsActive = False;

    realtys = Realty.query.limit(9).all()

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # next_page = request.args.get('next')

            return render_template("index.html", modalIsActive=modalIsActive)
        else:
            flash('Login or password is not correct')
            modalIsActive = True;

    return render_template("index.html", modalIsActive=modalIsActive, realtys=realtys)


@app.route('/about')
def aboutPage():
    return render_template("about.html")


@app.route('/contacts')
def contactsPage():
    return render_template("contacts.html")

@app.route('/catalog')
def catalog():
    realtys = Realty.query.limit(9).all()
    return render_template("catalog.html",realtys=realtys)
@app.route('/buy/<id>')
@login_required
def buyPage(id):
    realty = Realty.query.filter_by(id=id).first()
    return render_template("buy.html",realty=realty)


@app.route('/sell', methods=["POST", "GET"])
@login_required
def sellPage():
    title = request.form.get("title")
    price = request.form.get("price")
    area = request.form.get("area")
    roomCount = request.form.get("roomCount")
    floor = request.form.get("floor")
    address = request.form.get("address")
    description = request.form.get("description")
    if request.method == 'POST':
        imageFile = request.files['image']
        print(request.form)


        if not (title or price or area or roomCount or floor or address or imageFile):  # проверка на наличие всех полей
            flash('Заполните все необходимые поля!')
            return redirect(url_for('sellPage'))

        else:
            if imageFile and allowed_file(imageFile.filename):  # проверка на наличие файла
                imageFilename = secure_filename(imageFile.filename)
                imageFile.save(os.path.join(app.config['UPLOAD_FOLDER'], imageFilename),buffer_size=16384)
                imageFile.close()
                new_realty = Realty(title=title, price=price, area=area, roomCount=roomCount, floor=floor, address=address,
                                    description=description,image=imageFilename)
                db.session.add(new_realty)
                db.session.commit()
                flash('Успешно добавлено')
                return redirect(url_for('download_file',name=imageFilename))
            flash('Файл некорректен!')
            return redirect(url_for('sellPage'))

    return render_template("sell.html")
@app.route('/uploads/<name>')
def download_file(name):
    print(send_from_directory(app.config["UPLOAD_FOLDER"], name))
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/registration', methods=['GET', 'POST'])
def registrationPage():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')

    if request.method == 'POST':
        if not (login or password or password2 or email):  # проверка на наличие всех полей
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        elif not passwordCorrectCheck(password):
            pass
        else:
            hash_pwd = generate_password_hash(password)  # Хеширование пароля
            new_user = User(login=login, password=hash_pwd, email=email)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('mainPage'))
    return render_template("registration.html")


@app.route('/account')
@login_required
def profilePage():
    return render_template("accountpage.html")


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('mainPage'))

