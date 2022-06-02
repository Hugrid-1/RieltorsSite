import datetime
import os

from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from sweater import app, db, manager, ALLOWED_EXTENSIONS, photos, session, dbEngine
from flask import render_template, request, flash, redirect, url_for, send_from_directory

from sweater.models import User, Realty, Sale
from sqlalchemy.orm import query, sessionmaker




def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def mainPage():
    # print(current_user.get_id())
    realtys = Realty.query.filter_by(is_for_sale=True).limit(9).all()

    return render_template("index.html", realtys=realtys)

def passwordCorrectCheck(password): # проверка пароля
    checkStatus = False
    if len(password) < 8:
        print("Длина пароля недостаточна")
        return False
    alphaCounter = 0 #счетчик букв
    for i in password:
        if i.isalpha() and alphaCounter <= 3:
            alphaCounter += 1 #увеличение счетчика
            print(i)
            print(alphaCounter)
        elif alphaCounter >= 4:
            checkStatus = True
            return checkStatus #выход из цикла при наборе нужного количества букв
    print("Символов недостаточно")

    return checkStatus
@app.route('/about')
def aboutPage():
    return render_template("about.html")


@app.route('/contacts')
def contactsPage():
    return render_template("contacts.html")

@app.route('/catalog',methods=['GET','POST'])
def catalog():
    realtys = Realty.query.filter_by(is_for_sale=True).all()
    minPrice = request.form.get('min_price')

    maxPrice = request.form.get('max_price')

    print(request.form)
    if request.method == "POST" and minPrice and maxPrice:
        minPrice = int(minPrice)

        maxPrice = int(maxPrice)
        # minPrice=minPrice + 1
        # maxPrice=maxPrice + 1
        realtys = Realty.query.filter(Realty.price<maxPrice, Realty.price>minPrice).all()

    return render_template("catalog.html",realtys=realtys)

@app.route('/buy/<id>', methods=['GET','POST'])
@login_required
def buyPage(id): #Страница квартиры при покупке
    realty = Realty.query.filter_by(id=id).first()
    if request.method == 'POST':
        if request.form['submit_button'] == 'buy':
            realty.owner_id = current_user.get_id()
            realty.is_for_sale = False
            new_sale = Sale(buyer_id=current_user.get_id(),realty_id=realty.id,date_sale=datetime.date.today())
            db.session.add(new_sale)
            db.session.commit()
        if request.form['submit_button'] == 'withdraw from sale':
            realty.owner_id = current_user.get_id()
            realty.is_for_sale = False
            db.session.commit()
        elif request.form['submit_button'] == 'sell':
            realty.is_for_sale = True
            db.session.commit()
    return render_template("realty.html",realty=realty)


@app.route('/sell', methods=["POST", "GET"])
@login_required
def addRealtyForSalePage():
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
            return redirect(url_for('addRealtyForSalePage'))
        else:
            if imageFile and allowed_file(imageFile.filename):  # проверка на наличие файла
                imageFilename = secure_filename(imageFile.filename)
                imageFile.save(os.path.join(app.config['UPLOAD_FOLDER'], imageFilename),buffer_size=16384)
                imageFile.close()
                new_realty = Realty(title=title, price=price, area=area, roomCount=roomCount, floor=floor, address=address,
                                    description=description,image=imageFilename,owner_id = current_user.get_id(),is_for_sale=True)
                db.session.add(new_realty)
                db.session.commit()
                flash('Успешно добавлено')
                return redirect(url_for('addRealtyForSalePage'))
            flash('Файл некорректен!')
            return redirect(url_for('addRealtyForSalePage'))

    return render_template("sell.html")
@app.route('/uploads/<name>')
def download_file(name):
    print(send_from_directory(app.config["UPLOAD_FOLDER"], name))
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/registration', methods=['GET', 'POST'])
def registrationPage():
    #получение данных из формы на сайте
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')

    if request.method == 'POST':
        if not (login or password or password2 or email):  # проверка на наличие всех полей
            flash('Заполните все поля!')
        elif password != password2:
            flash('Пароли не одинаковые!')
        elif not passwordCorrectCheck(password):
            flash('Пароль не соответствует требованиям, пароль должен быть не меньше 8 символов в длину  и иметь хотя бы 6 букв')
        else:
            hash_pwd = generate_password_hash(password)  # Хеширование пароля
            new_user = User(login=login, password=hash_pwd, email=email)
            print(f"Зарегистрирован {new_user.login}")
            # login_user(new_user)
            db.session.add(new_user)
            db.session.commit()

            realtys = Realty.query.filter_by(is_for_sale=True).limit(9).all()
            return render_template("index.html",realtys=realtys)
    return render_template("registration.html")

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            print(next_page)
            realtys = Realty.query.filter_by(is_for_sale=True).limit(9).all()
            return render_template("index.html", realtys=realtys)
        else:
            flash('Логин или пароль некорректен')
    return render_template("login.html")

@app.route('/account') #профиль
@login_required
def profilePage():
    user_realtys = Realty.query.filter_by(owner_id = current_user.get_id()).all() #получение данных о недвижимости пользователя
    user_buys_list = Sale.query.filter_by(buyer_id = current_user.get_id()).all() #получение данных о покупках пользователя
    return render_template("accountpage.html",user_realtys=user_realtys,user_buys_list =user_buys_list )

@app.route('/top') #топ пользователей
def topUsers():
    topUserList = dbEngine.execute('SELECT * FROM userstoplist').fetchall() #получение данных из представления userstoplist
    return render_template("top.html",topUserList=topUserList)

@manager.user_loader #загрузка пользователя
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/logout', methods=['GET', 'POST']) #дезавторизация пользователя
@login_required
def logout():
    logout_user()
    return redirect(url_for('mainPage'))

